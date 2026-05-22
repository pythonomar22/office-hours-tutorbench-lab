from __future__ import annotations

import json

from tutorbench_lab.judge import compute_arrw
from tutorbench_lab.protocol import build_turn_input
from tutorbench_lab.redaction import build_redacted_trace
from tutorbench_lab.schemas import (
    CriterionRating,
    JudgedRunRecord,
    JudgeResult,
    Strategy,
    TutorResponse,
)
from tutorbench_lab.tutor import record_for_response


def test_redacted_trace_removes_dataset_prompt_and_rubric_text(
    adaptive_example,
) -> None:
    judged = _judged(adaptive_example)

    redacted = build_redacted_trace(judged)
    payload = json.dumps(redacted)

    assert redacted["task"]["task_id"] == adaptive_example.task_id
    assert redacted["response_text"] == "Synthetic tutor output."
    assert "ratings" in redacted
    assert "Rank HF" not in payload
    assert "fluorine is most electronegative" not in payload
    assert "bond strength dominates" not in payload
    assert "rubrics" not in payload
    assert "turn_input" not in payload
    assert "raw_judge_output" not in payload
    assert "Private scratchpad" not in payload
    assert "private judge text" not in payload
    assert '"example"' not in payload
    assert '"user_prompt"' not in payload
    assert '"system_prompt"' not in payload


def test_redacted_trace_can_omit_response_text_and_rating_rows(
    adaptive_example,
) -> None:
    judged = _judged(adaptive_example)

    redacted = build_redacted_trace(
        judged,
        include_response_text=False,
        include_ratings=False,
    )

    assert "response_text" not in redacted
    assert "ratings" not in redacted
    assert redacted["failure_summary"]["failed_positive_count"] == 1
    assert redacted["trace_summary"]["task_playbook"] == "synthetic route"


def _judged(example) -> JudgedRunRecord:
    turn = build_turn_input(example)
    response = TutorResponse(
        task_id=example.task_id,
        text="Synthetic tutor output.",
        model="test-model",
        strategy=Strategy.AGENTIC,
        prompt_version="test",
        latency_ms=10,
        usage={"input_tokens": 5, "output_tokens": 7},
        trace={
            "solver_model": "solver",
            "planner_model": "planner",
            "verifier_model": "verifier",
            "critic_model": "critic",
            "task_playbook": "Task-family playbook: synthetic route\nprivate notes",
            "stage_latency_ms": {"solver": 1},
            "stage_usage": {"solver": {"input_tokens": 1, "output_tokens": 2}},
            "solver_analysis": "Private scratchpad should not be exported.",
        },
    )
    run = record_for_response(
        example=example,
        turn=turn,
        response=response,
        run_id="redaction-test",
    )
    judge = JudgeResult(
        task_id=example.task_id,
        judge_model="test-judge",
        ratings=[
            CriterionRating(criterion_index=0, passed=True, rationale="private"),
            CriterionRating(criterion_index=1, passed=False, rationale="private"),
        ],
        raw_judge_output="private judge text",
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
