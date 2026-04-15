import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

load_dotenv()

from agents.planner import planner_agent


# ---------------------------------------------------------------------------
# Metric definition
# ---------------------------------------------------------------------------

plan_quality = GEval(
    name="Plan Quality",
    evaluation_steps=[
        "Check that the plan contains at least 2 specific search queries (not vague like 'search for info')",
        "Check that sources_to_check mentions both 'knowledge_base' and 'web' or at least one of them",
        "Check that the output_format clearly describes what the final report should look like",
        "Check that the goal accurately reflects the user's original request",
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model="gpt-4o-mini",
    threshold=0.7,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def invoke_planner(query: str) -> str:
    """Run the planner agent and return a formatted string of the plan."""
    result = planner_agent.invoke({"messages": [("user", query)]})
    plan = result.get("structured_response")
    if plan:
        queries = "\n".join(f"  - {q}" for q in plan.search_queries)
        sources = ", ".join(plan.sources_to_check)
        return (
            f"Goal: {plan.goal}\n"
            f"Search Queries:\n{queries}\n"
            f"Sources to Check: {sources}\n"
            f"Output Format: {plan.output_format}"
        )
    # Fallback: return last message content
    return result["messages"][-1].content


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_plan_quality_rag_comparison():
    """Planner should create a high-quality plan for a RAG comparison query."""
    input_query = "Compare naive RAG vs sentence-window retrieval"
    actual_output = invoke_planner(input_query)

    test_case = LLMTestCase(
        input=input_query,
        actual_output=actual_output,
    )
    assert_test(test_case, [plan_quality])


def test_plan_quality_rag_components():
    """Planner should decompose a components query into specific sub-queries."""
    input_query = "What are the main components of a RAG system?"
    actual_output = invoke_planner(input_query)

    test_case = LLMTestCase(
        input=input_query,
        actual_output=actual_output,
    )
    assert_test(test_case, [plan_quality])


def test_plan_has_both_sources():
    """Planner should typically include both knowledge_base and web as sources."""
    input_query = "How does LangChain help build LLM applications?"
    actual_output = invoke_planner(input_query)

    # Custom GEval for source coverage
    source_coverage = GEval(
        name="Source Coverage",
        evaluation_steps=[
            "Check whether the plan mentions searching both a local knowledge base and the web",
            "A plan that only uses web search without checking a local knowledge base scores lower",
            "A plan that lists both sources clearly scores highest",
        ],
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model="gpt-4o-mini",
        threshold=0.6,
    )

    test_case = LLMTestCase(
        input=input_query,
        actual_output=actual_output,
    )
    assert_test(test_case, [source_coverage])
