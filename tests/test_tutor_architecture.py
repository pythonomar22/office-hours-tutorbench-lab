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


def test_derivative_hint_playbook_does_not_hijack_adaptive_calculus(
    adaptive_example,
) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Calculus",
            "batch": "USE_CASE_1_TEXT",
            "prompt": (
                "Two rescue robots have separation s(t) = sqrt(t^4 + 9t^2). "
                "Explain where the t in the denominator went when simplifying s'(t)."
            ),
            "follow_up_prompt": (
                "I understand you're supposed to take the derivative, but where "
                "did the t in the denominator go?"
            ),
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "derivative-rate active-learning hint" not in playbook
    assert "radical derivative adaptive explanation" in playbook
    assert "ds/du" in playbook
    assert "first-principles limit definition" in playbook


def test_quadrant_alone_does_not_trigger_ellipse_playbook(adaptive_example) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Calculus",
            "batch": "USE_CASE_3_MULTIMODAL",
            "prompt": (
                "A region in the first quadrant is bounded by y = e^x and x = n. "
                "Find its perimeter in terms of n."
            ),
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "arc-length perimeter" in playbook
    assert "ellipse rectangle" not in playbook


def test_regression_residual_playbook_requires_precision(adaptive_example) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Statistics",
            "batch": "USE_CASE_2_TEXT",
            "prompt": (
                "A least-squares regression line predicts weight. "
                "Calculate the residual and assess the student's work."
            ),
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "predicted value to two decimals" in playbook
    assert "quantify the size of the student's numerical error" in playbook


def test_mendelian_testcross_playbook_separates_two_laws(adaptive_example) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_1_TEXT",
            "prompt": (
                "A RW/Tt plant is testcrossed with WW/tt. Explain "
                "independent assortment and the Punnett square."
            ),
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "Law of Segregation" in playbook
    assert "Law of Independent Assortment" in playbook
    assert "WW/tt parent makes only W/t" in playbook


def test_hydrogen_halide_playbook_does_not_match_hi_substrings(
    adaptive_example,
) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Chemistry",
            "batch": "USE_CASE_3_MULTIMODAL",
            "prompt": (
                "A heat exchange process cools furnace gases while heating "
                "crude oil. Determine the outlet temperature."
            ),
            "uc1_initial_explanation": "",
            "follow_up_prompt": "",
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "hydrogen halide acid strength" not in playbook
    assert "heat-exchange active-learning hint" in playbook


def test_extremophile_metabolism_playbook_covers_multiple_parts(
    adaptive_example,
) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_3_MULTIMODAL",
            "prompt": (
                "Thermophilus photosynthetica uses H2S chemosynthesis and "
                "infrared photosynthesis. Give hints for parts (a), (b), and (c)."
            ),
            "uc1_initial_explanation": "",
            "follow_up_prompt": "",
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "extremophile multi-part metabolism hint" in playbook
    assert "part (a)" in playbook
    assert "part (c)" in playbook


def test_clt_sample_mean_playbook_requires_probing_questions(adaptive_example) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Statistics",
            "batch": "USE_CASE_3_TEXT",
            "prompt": (
                "A right-skewed population has a sample mean problem. The student "
                "used CLT and has z = -0.707."
            ),
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "What does the Central Limit Theorem say" in playbook
    assert "population being" in playbook
    assert "normal" in playbook
    assert "round the final probability" in playbook
    assert "to three decimals" in playbook
    assert "Do not state P(Z < -0.707)" in playbook


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


def test_radical_derivative_guard_adds_limit_definition_note() -> None:
    guarded, guards = _apply_deterministic_playbook_guards(
        "The t comes from factoring sqrt(t^4 + 9t^2) as t sqrt(t^2 + 9).",
        "Task-family playbook: radical derivative adaptive explanation",
    )

    assert "first-principles limit" in guarded
    assert "Multiply by the conjugate" in guarded
    assert "4t^3+18t" in guarded
    assert guards == ["radical_limit_definition_note"]


def test_active_learning_templates_rewrite_brittle_playbooks() -> None:
    heat_text, heat_guards = _apply_deterministic_playbook_guards(
        "Solve by substituting values.",
        "Task-family playbook: heat-exchange active-learning hint",
    )
    arc_text, arc_guards = _apply_deterministic_playbook_guards(
        "Use arc length and finish the perimeter.",
        "Task-family playbook: arc-length perimeter active-learning hint",
    )

    assert "that change?" in heat_text
    assert "70 C" not in heat_text
    assert heat_guards == ["heat_exchange_template_rewrite"]
    assert "f'(x) = e^x" in arc_text
    assert "Do not simplify or evaluate the integral yet" in arc_text
    assert arc_guards == ["arc_length_template_rewrite"]


def test_extremophile_template_prompts_parts_without_final_chain() -> None:
    guarded, guards = _apply_deterministic_playbook_guards(
        "Think about oxygen.",
        "Task-family playbook: extremophile multi-part metabolism hint",
    )

    assert "Part (a)" in guarded
    assert "Part (b)" in guarded
    assert "Part (c)" in guarded
    assert "producer/base of the food web" in guarded
    assert "finished food-web chain" not in guarded
    assert guards == ["extremophile_metabolism_template_rewrite"]


def test_water_limiting_reagent_template_uses_prompt_counts() -> None:
    guarded, guards = _apply_deterministic_playbook_guards(
        "I count 10 blue and 7 red.",
        "Task-family playbook: H2/O2 water limiting-reagent visual assessment",
    )

    assert "H2 (blue) | 12" in guarded
    assert "O2 (red) | 8" in guarded
    assert "12 water molecules" in guarded
    assert guards == ["water_limiting_reagent_template_rewrite"]


def test_regression_residual_template_preserves_student_numbers() -> None:
    guarded, guards = _apply_deterministic_playbook_guards(
        "The residual is about 8 kg.",
        "Task-family playbook: regression residual assessment",
    )

    assert "545.0" in guarded
    assert "194.7 kg" in guarded
    assert "about **10 kg**" in guarded
    assert "196.17" in guarded
    assert "8.13" in guarded
    assert "1.87 kg too high" in guarded
    assert guards == ["regression_residual_template_rewrite"]
