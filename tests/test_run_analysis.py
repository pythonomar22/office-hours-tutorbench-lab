from __future__ import annotations

from tutorbench_lab.judge import compute_arrw
from tutorbench_lab.protocol import build_turn_input
from tutorbench_lab.run_analysis import analysis_markdown, build_run_analysis
from tutorbench_lab.schemas import (
    CriterionRating,
    JudgedRunRecord,
    JudgeResult,
    Strategy,
    TutorResponse,
)
from tutorbench_lab.tutor import record_for_response


def test_run_analysis_summarizes_failures_and_negative_criteria(
    adaptive_example,
    active_learning_example,
) -> None:
    adaptive = _judged(
        adaptive_example,
        [
            CriterionRating(criterion_index=0, passed=True),
            CriterionRating(criterion_index=1, passed=False),
        ],
    )
    active = _judged(
        active_learning_example,
        [
            CriterionRating(criterion_index=0, passed=False),
            CriterionRating(criterion_index=1, passed=True),
        ],
    )

    analysis = build_run_analysis([adaptive, active], top_n=1, bootstrap_samples=0)

    assert analysis["summary"]["row_count"] == 2
    assert analysis["summary"]["negative_weight_review_count"] == 1
    assert analysis["weakest_rows"][0]["task_id"] == active_learning_example.task_id
    truthfulness = {
        row["name"]: row for row in analysis["rubric_dimensions"]
    }["truthfulness"]
    assert truthfulness["pass_rate"] == 0
    assert any(
        row["triggered_negative_criteria"] == 1
        for row in analysis["rubric_dimensions"]
    )
    markdown = analysis_markdown(analysis)
    assert "Weakest Rows" in markdown
    assert "Throughput Headroom" in markdown


def _judged(example, ratings: list[CriterionRating]) -> JudgedRunRecord:
    turn = build_turn_input(example)
    response = TutorResponse(
        task_id=example.task_id,
        text="The final answer is visible in this synthetic response.",
        model="test-model",
        strategy=Strategy.AGENTIC,
        prompt_version="test",
        latency_ms=10,
        usage={"input_tokens": 5, "output_tokens": 7},
    )
    run = record_for_response(
        example=example,
        turn=turn,
        response=response,
        run_id="analysis-test",
    )
    judge = JudgeResult(
        task_id=example.task_id,
        judge_model="test-judge",
        ratings=ratings,
        latency_ms=20,
        usage={"input_tokens": 11, "output_tokens": 13},
    )
    arrw_raw, arrw, manual_review = compute_arrw(run, judge)
    return JudgedRunRecord(
        run=run,
        judge=judge,
        arrw_raw=arrw_raw,
        arrw=arrw,
        manual_weight_review=manual_review,
    )
