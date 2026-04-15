import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

load_dotenv()

from agents.critic import critic_agent


# ---------------------------------------------------------------------------
# Metric definition
# ---------------------------------------------------------------------------

critique_quality = GEval(
    name="Critique Quality",
    evaluation_steps=[
        "Check that the critique identifies specific issues, not just vague complaints like 'needs improvement'",
        "Check that revision_requests are actionable — a researcher must be able to act on them directly",
        "If verdict is APPROVE, the gaps list should be empty or contain only minor items",
        "If verdict is REVISE, there must be at least one clear revision_request",
        "Check that strengths are specific and refer to actual qualities found in the findings",
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model="gpt-4o-mini",
    threshold=0.7,
)


# ---------------------------------------------------------------------------
# Sample findings
# ---------------------------------------------------------------------------

GOOD_FINDINGS = """
## Research Findings: RAG Systems

### From local knowledge base:
The knowledge base contains comprehensive coverage of RAG architectures (2024 publications).
Key findings:
- **Retriever**: FAISS vector store with cosine similarity, enhanced by BM25 for keyword matching
- **Reranker**: Cross-encoder (BAAI/bge-reranker-base) improves top-k precision by ~15%
- **Chunking**: Sentence-window strategy (window=3) outperforms fixed-size chunks for long docs
- **Embedding model**: text-embedding-3-small achieves 89% recall@5 on domain queries

### From web search (2025 sources):
- Source: "RAG Survey 2024" — https://arxiv.org/abs/2312.10997
  Modular RAG architectures now outperform naive RAG on 7 of 8 standard benchmarks.
- Source: "Improving RAG with LangChain" — https://blog.langchain.dev/rag-improvements
  Hybrid retrieval (dense + sparse) consistently improves recall across domains.

### Synthesis:
RAG systems combine a retriever (vector + BM25 hybrid), a reranker, and an LLM reader.
The hybrid approach is the current best practice as of early 2025.

### Sources:
- Local: retrieval-augmented-generation.pdf (ingested 2024)
- Web: arxiv.org/abs/2312.10997, blog.langchain.dev
"""

POOR_FINDINGS = """
## Research Findings: RAG

RAG is a method that combines retrieval and generation. It is useful for many tasks.
LLMs are powerful tools that can answer questions. RAG makes them better because they
have access to external data. There are many different types of RAG systems.
Some are better than others. Companies use RAG for their products.

No specific sources cited. No publication dates. No quantitative comparisons.
"""


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def invoke_critic(findings: str) -> str:
    """Run the critic agent and return a formatted string of the critique."""
    result = critic_agent.invoke({"messages": [("user", findings)]})
    critique = result.get("structured_response")
    if critique:
        strengths = "\n".join(f"  + {s}" for s in critique.strengths) or "  (none)"
        gaps = "\n".join(f"  - {g}" for g in critique.gaps) or "  (none)"
        revisions = "\n".join(f"  * {r}" for r in critique.revision_requests) or "  (none)"
        return (
            f"Verdict: {critique.verdict}\n"
            f"Is Fresh: {critique.is_fresh}\n"
            f"Is Complete: {critique.is_complete}\n"
            f"Is Well Structured: {critique.is_well_structured}\n"
            f"Strengths:\n{strengths}\n"
            f"Gaps:\n{gaps}\n"
            f"Revision Requests:\n{revisions}"
        )
    return result["messages"][-1].content


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_critique_approve_good_findings():
    """Critic should APPROVE high-quality, well-cited, structured findings."""
    actual_output = invoke_critic(GOOD_FINDINGS)

    test_case = LLMTestCase(
        input=GOOD_FINDINGS,
        actual_output=actual_output,
    )
    assert_test(test_case, [critique_quality])


def test_critique_revise_poor_findings():
    """Critic should REVISE vague findings with no sources and no specifics."""
    actual_output = invoke_critic(POOR_FINDINGS)

    test_case = LLMTestCase(
        input=POOR_FINDINGS,
        actual_output=actual_output,
    )

    # Custom metric: checks that REVISE verdict comes with actionable requests
    revise_quality = GEval(
        name="Revise Verdict Quality",
        evaluation_steps=[
            "The findings provided are clearly vague, lack sources, and contain no specific data",
            "Check that the verdict is REVISE (APPROVE on clearly poor findings should score 0)",
            "Check that revision_requests list at least 2 actionable items (e.g. 'add source URLs', 'add quantitative comparisons')",
            "Check that the critique does not blindly approve content that has obvious gaps",
        ],
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model="gpt-4o-mini",
        threshold=0.7,
    )

    assert_test(test_case, [revise_quality])
