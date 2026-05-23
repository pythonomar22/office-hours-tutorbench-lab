from __future__ import annotations

from tutorbench_lab.blend import BlendPolicy, blend_run_records
from tutorbench_lab.protocol import build_turn_input
from tutorbench_lab.schemas import Strategy, TutorResponse
from tutorbench_lab.tutor import record_for_response


def test_conservative_blend_uses_auxiliary_for_allowlisted_playbook(
    adaptive_example,
) -> None:
    primary = _record(adaptive_example, run_id="v6", text="primary")
    auxiliary = _record(
        adaptive_example,
        run_id="v9",
        text="auxiliary",
        task_playbook=(
            "Task-family playbook: mean-CI z-vs-t active-learning hint\n"
            "private route notes"
        ),
    )

    blended = blend_run_records(
        [primary],
        [auxiliary],
        run_id="blend",
        policy=BlendPolicy.CONSERVATIVE_V10,
    )

    assert blended[0].response.text == "auxiliary"
    assert blended[0].response.prompt_version == "blend-conservative-v10"
    assert blended[0].response.trace["blend_selected_source"] == "auxiliary"
    assert (
        blended[0].response.trace["blend_auxiliary_playbook"]
        == "mean-CI z-vs-t active-learning hint"
    )


def test_conservative_blend_uses_primary_for_unmatched_text_slice(
    adaptive_example,
) -> None:
    example = adaptive_example.model_copy(
        update={"batch": "USE_CASE_1_TEXT", "subject": "Physics"}
    )
    primary = _record(example, run_id="v6", text="primary")
    auxiliary = _record(example, run_id="v9", text="auxiliary")

    blended = blend_run_records(
        [primary],
        [auxiliary],
        run_id="blend",
        policy=BlendPolicy.CONSERVATIVE_V10,
    )

    assert blended[0].response.text == "primary"
    assert blended[0].response.trace["blend_selected_source"] == "primary"


def test_conservative_blend_uses_auxiliary_for_positive_slice(
    adaptive_example,
) -> None:
    example = adaptive_example.model_copy(
        update={"batch": "USE_CASE_3_MULTIMODAL", "subject": "Biology"}
    )
    primary = _record(example, run_id="v6", text="primary")
    auxiliary = _record(example, run_id="v9", text="auxiliary")

    blended = blend_run_records(
        [primary],
        [auxiliary],
        run_id="blend",
        policy=BlendPolicy.CONSERVATIVE_V10,
    )

    assert blended[0].response.text == "auxiliary"
    assert blended[0].response.trace["blend_selected_source"] == "auxiliary"


def _record(example, *, run_id: str, text: str, task_playbook: str = ""):
    turn = build_turn_input(example, prompt_version="test")
    response = TutorResponse(
        task_id=example.task_id,
        text=text,
        model="test-model",
        strategy=Strategy.AGENTIC,
        prompt_version=run_id,
        trace={"task_playbook": task_playbook},
    )
    return record_for_response(
        example=example,
        turn=turn,
        response=response,
        run_id=run_id,
    )
