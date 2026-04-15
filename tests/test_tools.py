import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
import pytest
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from deepeval import assert_test
from deepeval.metrics import ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall

load_dotenv()

from agents.planner import planner_agent
from agents.research import researcher_agent
from supervisor import supervisor


# ---------------------------------------------------------------------------
# Helper: extract tool calls from LangGraph message list
# ---------------------------------------------------------------------------

def extract_tool_calls(messages: list) -> list[ToolCall]:
    """Pull ToolCall objects from a list of LangChain messages."""
    tool_calls = []
    for msg in messages:
        if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
            for tc in msg.tool_calls:
                tool_calls.append(
                    ToolCall(
                        name=tc["name"],
                        input_parameters=tc.get("args", {}),
                    )
                )
    return tool_calls


# ---------------------------------------------------------------------------
# Test 1: Planner must use search tools
# ---------------------------------------------------------------------------

def test_planner_tools():
    """Planner must call web_search or knowledge_search when given a research topic."""
    input_query = "What is RAG and how does it work?"
    result = planner_agent.invoke({"messages": [("user", input_query)]})
    messages = result["messages"]

    tool_calls = extract_tool_calls(messages)
    actual_output = messages[-1].content

    test_case = LLMTestCase(
        input=input_query,
        actual_output=actual_output,
        tools_called=tool_calls,
        expected_tools=[
            ToolCall(name="knowledge_search"),
            ToolCall(name="web_search"),
        ],
    )
    metric = ToolCorrectnessMetric(threshold=0.5, model="gpt-4o-mini")
    assert_test(test_case, [metric])


# ---------------------------------------------------------------------------
# Test 2: Researcher must use research tools
# ---------------------------------------------------------------------------

def test_researcher_tools():
    """Researcher must call knowledge_search, web_search, or read_url for a given plan."""
    plan_input = (
        "Research Plan:\n"
        "Goal: Understand retrieval strategies in RAG systems.\n"
        "Search Queries:\n"
        "  - RAG retrieval strategies overview\n"
        "  - dense retrieval vs BM25 comparison\n"
        "Sources to Check: knowledge_base, web\n"
        "Output Format: Structured markdown with comparison table."
    )
    result = researcher_agent.invoke({"messages": [("user", plan_input)]})
    messages = result["messages"]

    tool_calls = extract_tool_calls(messages)
    actual_output = messages[-1].content

    test_case = LLMTestCase(
        input=plan_input,
        actual_output=actual_output,
        tools_called=tool_calls,
        expected_tools=[
            ToolCall(name="knowledge_search"),
            ToolCall(name="web_search"),
            ToolCall(name="read_url"),
        ],
    )
    metric = ToolCorrectnessMetric(threshold=0.5, model="gpt-4o-mini")
    assert_test(test_case, [metric])


# ---------------------------------------------------------------------------
# Test 3: Supervisor must call 'plan' first
# ---------------------------------------------------------------------------

def test_supervisor_calls_plan_first():
    """Supervisor must call the 'plan' tool as its first action for any research request."""
    input_query = "What are the differences between LangChain and LangGraph?"
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    collected_messages = []

    # Stream supervisor one step at a time; stop after the first AI tool call
    # so we don't run the expensive full pipeline.
    gen = supervisor.stream(
        {"messages": [("user", input_query)]},
        config=config,
        stream_mode="updates",
    )
    try:
        for chunk in gen:
            for node, data in chunk.items():
                if node == "__interrupt__":
                    break
                if isinstance(data, dict):
                    msgs = data.get("messages", [])
                    collected_messages.extend(msgs)
                    # Stop as soon as we see the supervisor's first tool call
                    if any(
                        isinstance(m, AIMessage) and getattr(m, "tool_calls", None)
                        for m in msgs
                    ):
                        raise StopIteration
    except StopIteration:
        pass
    finally:
        gen.close()

    tool_calls = extract_tool_calls(collected_messages)
    actual_output = (
        collected_messages[-1].content if collected_messages else "no output"
    )

    test_case = LLMTestCase(
        input=input_query,
        actual_output=actual_output,
        tools_called=tool_calls,
        expected_tools=[ToolCall(name="plan")],
    )
    metric = ToolCorrectnessMetric(threshold=0.5, model="gpt-4o-mini")
    assert_test(test_case, [metric])
