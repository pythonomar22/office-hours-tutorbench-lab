from __future__ import annotations

import pytest

from tutorbench_lab.judge import (
    JudgeRatingsMismatch,
    compute_arrw,
    judge_run_record,
    parse_judge_json,
    parse_judge_json_for_indices,
)
from tutorbench_lab.protocol import build_turn_input
from tutorbench_lab.schemas import CriterionRating, JudgeResult, Strategy, TutorResponse
from tutorbench_lab.tutor import record_for_response


def test_arrw_uses_critical_weights_and_clamps_negative(active_learning_example):
    turn = build_turn_input(active_learning_example)
    response = TutorResponse(
        task_id=active_learning_example.task_id,
        text="The final answer is 2.74.",
        model="test",
        strategy=Strategy.DRY_RUN,
        prompt_version="test",
    )
    run = record_for_response(
        example=active_learning_example,
        turn=turn,
        response=response,
        run_id="run",
    )
    judge = JudgeResult(
        task_id=active_learning_example.task_id,
        judge_model="test",
        ratings=[
            CriterionRating(criterion_index=0, passed=False),
            CriterionRating(criterion_index=1, passed=True),
        ],
    )

    raw, clamped, manual_review = compute_arrw(run, judge)

    assert raw == -5.0
    assert clamped == 0.0
    assert manual_review is True


def test_heuristic_judge_produces_judged_record(adaptive_example):
    turn = build_turn_input(adaptive_example)
    response = TutorResponse(
        task_id=adaptive_example.task_id,
        text="I get why that is confusing: for hydrogen halides, bond strength dominates.",
        model="test",
        strategy=Strategy.DRY_RUN,
        prompt_version="test",
    )
    run = record_for_response(
        example=adaptive_example,
        turn=turn,
        response=response,
        run_id="run",
    )

    judged = judge_run_record(run, judge_model="heuristic")

    assert judged.run.example.task_id == adaptive_example.task_id
    assert len(judged.judge.ratings) == len(adaptive_example.rubrics)
    assert 0.0 <= judged.arrw <= 1.0


def test_judge_parser_reports_missing_indices_for_repair():
    raw = '{"ratings":[{"criterion_index":0,"passed":true,"confidence":0.9}]}'

    with pytest.raises(JudgeRatingsMismatch) as exc_info:
        parse_judge_json(raw, expected_count=2)

    assert exc_info.value.missing == [1]
    assert exc_info.value.extra == []
    assert [rating.criterion_index for rating in exc_info.value.ratings] == [0]


def test_judge_parser_accepts_targeted_repair_indices():
    raw = '{"ratings":[{"criterion_index":14,"passed":false,"confidence":0.8}]}'

    ratings = parse_judge_json_for_indices(raw, expected_indices={14})

    assert len(ratings) == 1
    assert ratings[0].criterion_index == 14
    assert ratings[0].passed is False
