import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import uuid
import pytest
from dotenv import load_dotenv
from langgraph.types import Command
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

load_dotenv()

from supervisor import supervisor


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

answer_relevancy = AnswerRelevancyMetric(threshold=0.7, model="gpt-4o-mini")

correctness = GEval(
    name="Correctness",
    evaluation_steps=[
        "Check whether the facts in 'actual output' contradict 'expected output'",
        "Penalize omission of critical details mentioned in 'expected output'",
        "Different wording of the same concept is acceptable — only penalize factual contradictions",
        "For failure cases where the system appropriately declines, that counts as correct",
    ],
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT,
    ],
    model="gpt-4o-mini",
    threshold=0.5,
)


# ---------------------------------------------------------------------------
# Golden dataset
# ---------------------------------------------------------------------------

DATASET_PATH = os.path.join(os.path.dirname(__file__), "golden_dataset.json")
with open(DATASET_PATH) as f:
    GOLDEN_DATASET = json.load(f)


# ---------------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------------

def run_full_pipeline(query: str) -> str:
    """
    Run the Supervisor pipeline end-to-end.

    Auto-approves the save_report interrupt so tests don't block waiting for
    human input. Returns the final text output from the agent.
    """
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    final_output = "No response generated"

    def _stream(input_data) -> str:
        nonlocal final_output
        for chunk in supervisor.stream(input_data, config=config, stream_mode="updates"):
            for node, data in chunk.items():
                if node == "__interrupt__":
                    continue
                if isinstance(data, dict):
                    for msg in data.get("messages", []):
                        content = getattr(msg, "content", None)
                        if content:
                            final_output = str(content)

    _stream({"messages": [("user", query)]})

    # Handle save_report interrupt: auto-approve
    state = supervisor.get_state(config)
    for task in state.tasks:
        if task.interrupts:
            _stream(Command(resume={"type": "approve"}))
            break

    return final_output


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

# Run only happy_path examples end-to-end to keep costs manageable.
# Edge and failure cases are tested separately below.
HAPPY_PATH = [ex for ex in GOLDEN_DATASET if ex["category"] == "happy_path"]
EDGE_CASES = [ex for ex in GOLDEN_DATASET if ex["category"] == "edge_case"]
FAILURE_CASES = [ex for ex in GOLDEN_DATASET if ex["category"] == "failure_case"]


@pytest.mark.parametrize("example", HAPPY_PATH, ids=[ex["input"][:40] for ex in HAPPY_PATH])
def test_happy_path_e2e(example):
    """Happy-path queries should produce relevant, correct answers."""
    actual_output = run_full_pipeline(example["input"])

    test_case = LLMTestCase(
        input=example["input"],
        actual_output=actual_output,
        expected_output=example["expected_output"],
    )
    assert_test(test_case, [answer_relevancy, correctness])


@pytest.mark.parametrize("example", EDGE_CASES, ids=[ex["input"][:40] for ex in EDGE_CASES])
def test_edge_cases_e2e(example):
    """
    Edge cases — lower threshold for correctness.

    These queries are intentionally tricky: vague, multilingual, or very broad.
    We only check answer relevancy, not strict correctness.
    """
    actual_output = run_full_pipeline(example["input"])

    lenient_relevancy = AnswerRelevancyMetric(threshold=0.5, model="gpt-4o-mini")

    test_case = LLMTestCase(
        input=example["input"],
        actual_output=actual_output,
        expected_output=example["expected_output"],
    )
    assert_test(test_case, [lenient_relevancy])


@pytest.mark.parametrize("example", FAILURE_CASES, ids=[ex["input"][:40] for ex in FAILURE_CASES])
def test_failure_cases_e2e(example):
    """
    Failure cases — system should gracefully handle off-domain or nonsense queries.

    We use a custom GEval to check the response appropriately declines or indicates
    it cannot help, rather than hallucinating a confident answer.
    """
    actual_output = run_full_pipeline(example["input"])

    graceful_handling = GEval(
        name="Graceful Failure Handling",
        evaluation_steps=[
            "The input is an off-domain, nonsensical, or inappropriate query",
            "Check that the output does NOT confidently answer the off-domain question with invented facts",
            "A response that declines, asks for clarification, or notes it cannot help scores highest",
            "A response that attempts the off-domain task (writes a poem, gives stock prices) scores lowest",
        ],
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model="gpt-4o-mini",
        threshold=0.5,
    )

    test_case = LLMTestCase(
        input=example["input"],
        actual_output=actual_output,
        expected_output=example["expected_output"],
    )
    assert_test(test_case, [graceful_handling])
