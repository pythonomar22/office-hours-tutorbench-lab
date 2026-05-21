from __future__ import annotations

from tutorbench_lab.protocol import build_turn_input
from tutorbench_lab.schemas import ImageRef, ModelUsage, RubricCriterion, TutorBenchExample
from tutorbench_lab.tutor import _needs_specialist_audit, _sum_usage


def test_specialist_audit_routes_only_multimodal_assessment() -> None:
    assessment = TutorBenchExample(
        task_id="diagram",
        batch="USE_CASE_2_MULTIMODAL",
        subject="Biology",
        prompt="Check this labelled cell diagram.",
        image=ImageRef(url="https://example.com/cell.png"),
        rubrics=[RubricCriterion(criteria="The response must assess labels.")],
    )
    active = TutorBenchExample(
        task_id="hint",
        batch="USE_CASE_3_MULTIMODAL",
        subject="Physics",
        prompt="Give a hint for this kinematics setup.",
        image=ImageRef(url="https://example.com/work.png"),
        rubrics=[RubricCriterion(criteria="The response must not reveal the answer.")],
    )

    assert _needs_specialist_audit(build_turn_input(assessment)) is True
    assert _needs_specialist_audit(build_turn_input(active)) is False


def test_sum_usage_tracks_all_agent_stages() -> None:
    usage = _sum_usage(
        [
            ModelUsage(input_tokens=10, output_tokens=5),
            ModelUsage(input_tokens=7, output_tokens=3, total_tokens=10),
        ]
    )

    assert usage.input_tokens == 17
    assert usage.output_tokens == 8
    assert usage.total_tokens == 25
