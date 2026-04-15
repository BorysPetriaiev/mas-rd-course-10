import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

load_dotenv()

from agents.research import researcher_agent


# ---------------------------------------------------------------------------
# Metric definition
# ---------------------------------------------------------------------------

groundedness = GEval(
    name="Groundedness",
    evaluation_steps=[
        "Extract every factual claim from 'actual output'",
        "For each claim, check if it can be directly supported by the text in 'retrieval context'",
        "Claims not traceable to the retrieval context count as ungrounded, even if they are generally true",
        "Score = (number of grounded claims) / (total claims). Higher is better.",
    ],
    evaluation_params=[
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.RETRIEVAL_CONTEXT,
    ],
    model="gpt-4o-mini",
    threshold=0.6,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

RAG_PLAN = """Research Plan:
Goal: Understand the main components and architecture of Retrieval-Augmented Generation systems.
Search Queries:
  - RAG system components and architecture
  - vector store retrieval for RAG
  - RAG vs fine-tuning comparison
Sources to Check: knowledge_base, web
Output Format: Structured markdown report with sections for each component."""

LANGCHAIN_PLAN = """Research Plan:
Goal: Explain how LangChain simplifies building LLM-powered applications.
Search Queries:
  - LangChain framework overview
  - LangChain chains and agents
  - LangChain document loaders and text splitters
Sources to Check: knowledge_base, web
Output Format: Summary with key features and code examples."""


def invoke_researcher(plan: str):
    """
    Run the researcher agent and return (final_output, retrieval_context).

    retrieval_context is collected from all knowledge_search ToolMessage results
    so DeepEval can evaluate groundedness against what was actually retrieved.
    """
    result = researcher_agent.invoke({"messages": [("user", plan)]})
    messages = result["messages"]

    # Collect retrieval context from knowledge_search tool results
    retrieval_context = []
    for msg in messages:
        if isinstance(msg, ToolMessage) and msg.name == "knowledge_search":
            content = str(msg.content)
            if content and content != "Nothing found in the local knowledge base.":
                retrieval_context.append(content)

    # Also collect web_search results for context
    for msg in messages:
        if isinstance(msg, ToolMessage) and msg.name == "web_search":
            content = str(msg.content)
            if content:
                retrieval_context.append(content[:1000])  # limit web snippets

    final_output = messages[-1].content
    return final_output, retrieval_context


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_research_grounded_rag():
    """Researcher output about RAG should be grounded in retrieved documents."""
    actual_output, retrieval_context = invoke_researcher(RAG_PLAN)

    if not retrieval_context:
        # If nothing was retrieved, skip groundedness test
        pytest.skip("No retrieval context available — knowledge index may not be built")

    test_case = LLMTestCase(
        input=RAG_PLAN,
        actual_output=actual_output,
        retrieval_context=retrieval_context,
    )
    assert_test(test_case, [groundedness])


def test_research_grounded_langchain():
    """Researcher output about LangChain should be grounded in retrieved documents."""
    actual_output, retrieval_context = invoke_researcher(LANGCHAIN_PLAN)

    if not retrieval_context:
        pytest.skip("No retrieval context available — knowledge index may not be built")

    test_case = LLMTestCase(
        input=LANGCHAIN_PLAN,
        actual_output=actual_output,
        retrieval_context=retrieval_context,
    )
    assert_test(test_case, [groundedness])
