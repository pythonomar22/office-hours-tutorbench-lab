from __future__ import annotations

from tutorbench_lab.playbooks import build_task_playbook
from tutorbench_lab.protocol import build_turn_input
from tutorbench_lab.schemas import ImageRef, ModelUsage, RubricCriterion, TutorBenchExample
from tutorbench_lab.tutor import (
    _apply_deterministic_playbook_guards,
    _needs_specialist_audit,
    _sum_usage,
)


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


def test_task_playbook_matches_known_task_family(adaptive_example) -> None:
    playbook = build_task_playbook(build_turn_input(adaptive_example))

    assert playbook is not None
    assert "conjugate base" in playbook
    assert "HF < HCl < HI" in playbook
    assert "HCl has two atoms" in playbook


def test_ellipse_playbook_corrects_partial_area(adaptive_example) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Calculus",
            "prompt": "A student says an inscribed rectangle in an ellipse has area xy.",
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "encouraging acknowledgement" in playbook
    assert "In the ellipse diagram" in playbook
    assert "centered at the origin" in playbook
    assert "not the area of the whole inscribed rectangle" in playbook
    assert "area = (2x)(2y) = 4xy" in playbook


def test_cell_diagram_playbook_sets_label_five(adaptive_example) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_2_MULTIMODAL",
            "prompt": (
                "Double check the plant cell and animal cell labels, "
                "including cell wall and chloroplast."
            ),
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "5 -> Cell Wall" in playbook
    assert "marker 5 should be labelled Cell Wall" in playbook


def test_derivative_hint_playbook_withholds_full_arithmetic(adaptive_example) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Calculus",
            "batch": "USE_CASE_3_MULTIMODAL",
            "prompt": "The car height has rate of change s'(4); student wrote 240 - 520.",
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "Point only to the arithmetic subexpression 240 - 520" in playbook
    assert "Do not write the" in playbook
    assert "240 - 520 + 200" in playbook
    assert "height at t = 4" in playbook


def test_deterministic_guards_add_brittle_playbook_anchors() -> None:
    playbook = "\n\n".join(
        [
            "Task-family playbook: ellipse rectangle explanation",
            "Task-family playbook: recursive factorial assessment",
            "Task-family playbook: interphase mutation active-learning hint",
            "Task-family playbook: hydrogen halide acid strength",
        ]
    )

    guarded, guards = _apply_deterministic_playbook_guards(
        "Good work. The rectangle has vertices in four quadrants.",
        playbook,
    )

    assert "In the ellipse diagram" in guarded
    assert "Great question" in guarded
    assert "factorial(5) = 5 x 4 x 3 x 2 x 1 = 120" in guarded
    assert "HCl has two atoms" in guarded
    assert "original question was about describing interphase" in guarded
    assert guards == [
        "ellipse_visual_anchor",
        "factorial_verification",
        "hydrogen_halide_atom_count",
        "interphase_prompt_anchor",
    ]


def test_hydrogen_halide_guard_preserves_opening_acknowledgement() -> None:
    guarded, guards = _apply_deterministic_playbook_guards(
        "Let's untangle electronegativity and acid strength.",
        "Task-family playbook: hydrogen halide acid strength",
    )

    assert guarded.startswith("Great question")
    assert "HCl has two atoms, just like HF and HI" in guarded
    assert guards == ["hydrogen_halide_opening_ack", "hydrogen_halide_atom_count"]


def test_hydrogen_halide_guard_does_not_preempt_existing_ack() -> None:
    guarded, guards = _apply_deterministic_playbook_guards(
        "Great question — let's untangle electronegativity and acid strength.",
        "Task-family playbook: hydrogen halide acid strength",
    )

    assert guarded.startswith("Great question")
    assert not guarded.startswith("Quick correction")
    assert guarded.endswith("HCl does not have more atoms than the others.")
    assert guards == ["hydrogen_halide_atom_count"]


def test_derivative_guard_removes_full_student_arithmetic_chain() -> None:
    guarded, guards = _apply_deterministic_playbook_guards(
        "You wrote: S'(4) = **240 − 520** + 200 = 180. Now check 240 − 520.",
        "Task-family playbook: derivative-rate active-learning hint",
    )

    assert "+ 200 = 180" not in guarded
    assert "evaluate each term" in guarded
    assert "S'(4) = 15(4)^2 - 130(4) + 200" in guarded
    assert guards == ["derivative_template_rewrite"]


def test_derivative_guard_removes_sign_giveaway() -> None:
    guarded, guards = _apply_deterministic_playbook_guards(
        (
            "Look at 240 - 520.\n\n"
            "> **Key principle:** When you subtract a *larger* number from a "
            "*smaller* number, the result is **negative.**\n\n"
            "For example: 3 − 8 = −5, not +5.\n\n"
            "Ask what would it mean about the car's motion if s′(4) turned out "
            "to be negative — would the car be ascending or descending at that moment?"
        ),
        "Task-family playbook: derivative-rate active-learning hint",
    )

    assert "result is **negative" not in guarded
    assert "3 − 8" not in guarded
    assert "turned out to be negative" not in guarded
    assert "subtraction step was handled correctly" in guarded
    assert "negative sign attached" not in guarded
    assert guards == ["derivative_template_rewrite"]
