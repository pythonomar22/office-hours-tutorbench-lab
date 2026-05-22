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


def test_regression_residual_playbook_is_retired_for_generic_agent(
    adaptive_example,
) -> None:
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

    assert build_task_playbook(build_turn_input(example)) is None


def test_titration_pka_playbook_does_not_route_to_dextrose(
    adaptive_example,
) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Chemistry",
            "batch": "USE_CASE_1_MULTIMODAL",
            "prompt": "Could you help with this lactic acid titration curve?",
            "uc1_initial_explanation": (
                "The pKa comes from the half-equivalence point on the titration "
                "curve using Henderson-Hasselbalch."
            ),
            "follow_up_prompt": (
                "Why use 8 mL for pKa if the equivalence point is 16 mL? "
                "Shouldn't pKa be linked to the equivalence point and molarity?"
            ),
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "weak-acid titration pKa adaptive explanation" in playbook
    assert "dextrose solubility" not in playbook
    assert "pH = pKa" in playbook


def test_biology_failure_family_playbooks_cover_active_and_assessment(
    adaptive_example,
) -> None:
    arctic = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_3_MULTIMODAL",
            "prompt": (
                "What is responsible for the seasonal change in the coat color "
                "of Arctic foxes? The student mentions denaturation."
            ),
        }
    )
    gene_x = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_3_TEXT",
            "prompt": (
                "Methylation near Gene X, a tumor suppressor, changes cancer "
                "incidence and expression."
            ),
        }
    )
    respiration = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_2_MULTIMODAL",
            "prompt": (
                "Assess a student's aerobic respiration answer covering "
                "glycolysis, Krebs cycle, and electron transport."
            ),
        }
    )

    assert "Arctic fox coat-color" in build_task_playbook(build_turn_input(arctic))
    assert "Gene X methylation" in build_task_playbook(build_turn_input(gene_x))
    assert "aerobic respiration assessment" in build_task_playbook(
        build_turn_input(respiration)
    )


def test_interphase_guidance_is_use_case_aware_not_active_only(
    adaptive_example,
) -> None:
    assessment = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_2_TEXT",
            "prompt": (
                "Assess a student's interphase answer about whether mutations "
                "can be inherited by daughter cells."
            ),
        }
    )
    adaptive = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_1_TEXT",
            "prompt": "Explain interphase and mutation inheritance.",
            "follow_up_prompt": (
                "I thought mutations during interphase could never reach "
                "daughter cells. Why not?"
            ),
        }
    )

    assessment_playbook = build_task_playbook(build_turn_input(assessment))
    adaptive_playbook = build_task_playbook(build_turn_input(adaptive))

    assert assessment_playbook is not None
    assert adaptive_playbook is not None
    assert "Match the prompt's use case" in assessment_playbook
    assert "Match the prompt's use case" in adaptive_playbook


def test_active_hint_playbooks_do_not_hijack_adaptive_rows(adaptive_example) -> None:
    gene_x_adaptive = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_1_TEXT",
            "prompt": (
                "Methylation near Gene X, a tumor suppressor, changes cancer "
                "incidence and expression."
            ),
            "follow_up_prompt": "Why would methylation make the outcome look worse?",
        }
    )
    clt_adaptive = adaptive_example.model_copy(
        update={
            "subject": "Statistics",
            "batch": "USE_CASE_1_TEXT",
            "prompt": "Explain the central limit theorem for sample means.",
            "follow_up_prompt": (
                "I still do not understand whether the original population needs to be normal."
            ),
        }
    )
    factorial_adaptive = adaptive_example.model_copy(
        update={
            "subject": "Computer Science",
            "batch": "USE_CASE_1_TEXT",
            "prompt": "Explain recursive factorial code.",
            "follow_up_prompt": "Why does the recursive call move toward zero?",
        }
    )

    for example in [gene_x_adaptive, clt_adaptive, factorial_adaptive]:
        playbook = build_task_playbook(build_turn_input(example))
        assert playbook is None


def test_physics_playbooks_prevent_kinematics_hijack(adaptive_example) -> None:
    conical = adaptive_example.model_copy(
        update={
            "subject": "Physics",
            "batch": "USE_CASE_1_TEXT",
            "prompt": (
                "A mass on a string is in uniform circular motion at a constant "
                "angle theta. Derive the period."
            ),
            "follow_up_prompt": ("How do I get rid of tension and speed to find the period?"),
        }
    )
    magnetic = adaptive_example.model_copy(
        update={
            "subject": "Physics",
            "batch": "USE_CASE_1_TEXT",
            "prompt": (
                "A uniform wire is bent into an equilateral triangle. Current "
                "enters corner A and leaves corner C. What is the magnetic field "
                "at the center of the triangle?"
            ),
        }
    )

    conical_playbook = build_task_playbook(build_turn_input(conical))
    magnetic_playbook = build_task_playbook(build_turn_input(magnetic))

    assert conical_playbook is not None
    assert "conical-pendulum adaptive explanation" in conical_playbook
    assert "kinematics active-learning hint" not in conical_playbook
    assert magnetic_playbook is not None
    assert "equilateral-triangle wire magnetic-field" in magnetic_playbook


def test_binary_tree_traversal_playbook_prefers_scaffolded_assessment(
    adaptive_example,
) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Computer Science",
            "batch": "USE_CASE_2_MULTIMODAL",
            "prompt": (
                "Given a binary tree with preorder, in-order, and postorder "
                "traversals, assess the student's reconstruction."
            ),
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "binary-tree traversal reconstruction assessment" in playbook
    assert "preorder selects the next subtree root" in playbook


def test_oop_playbook_does_not_match_car_substrings(adaptive_example) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Computer Science",
            "batch": "USE_CASE_2_MULTIMODAL",
            "prompt": (
                "The student is trying to find the kth smallest element in a "
                "sorted matrix. Is their approach correct?"
            ),
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is None or "OOP design / inventory class" not in playbook


def test_respiration_playbooks_split_adaptive_and_assessment(adaptive_example) -> None:
    adaptive = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_1_TEXT",
            "prompt": (
                "During cellular respiration, does inhaled oxygen become the "
                "carbon dioxide we exhale?"
            ),
            "follow_up_prompt": (
                "Where does CO2 come from if glucose is processed in glycolysis "
                "and the Krebs cycle?"
            ),
        }
    )
    assessment = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_2_MULTIMODAL",
            "prompt": "Assess this aerobic respiration answer.",
        }
    )

    adaptive_playbook = build_task_playbook(build_turn_input(adaptive))
    assessment_playbook = build_task_playbook(
        build_turn_input(assessment),
        extra_context="glycolysis, Krebs cycle, electron transport, anaerobic",
    )

    assert adaptive_playbook is not None
    assert "oxygen/CO2 cellular-respiration adaptive explanation" in adaptive_playbook
    assert "aerobic respiration assessment" not in adaptive_playbook
    assert assessment_playbook is not None
    assert "aerobic respiration assessment" in assessment_playbook


def test_two_proportion_playbook_is_not_generic_z_test(adaptive_example) -> None:
    generic = adaptive_example.model_copy(
        update={
            "subject": "Statistics",
            "batch": "USE_CASE_2_MULTIMODAL",
            "prompt": "The student used a z-test, but the population SD is unknown.",
        }
    )
    vaccine = adaptive_example.model_copy(
        update={
            "subject": "Statistics",
            "batch": "USE_CASE_3_TEXT",
            "prompt": "A vaccine and placebo study asks for a proportion test.",
            "follow_up_prompt": ("I am confused about whether to pool p_v and p_p."),
        }
    )

    generic_playbook = build_task_playbook(build_turn_input(generic))
    vaccine_playbook = build_task_playbook(build_turn_input(vaccine))

    assert generic_playbook is None or "two-proportion z-test" not in generic_playbook
    assert vaccine_playbook is None


def test_assessment_playbooks_do_not_hijack_active_or_adaptive_rows(
    adaptive_example,
) -> None:
    titration_assessment = adaptive_example.model_copy(
        update={
            "subject": "Chemistry",
            "batch": "USE_CASE_2_TEXT",
            "prompt": (
                "Assess a student's lactic acid titration pKa calculation using "
                "Henderson-Hasselbalch and half-equivalence."
            ),
        }
    )
    residual_active = adaptive_example.model_copy(
        update={
            "subject": "Statistics",
            "batch": "USE_CASE_3_TEXT",
            "prompt": (
                "A least-squares regression line predicts weight. Give a hint "
                "for calculating the residual."
            ),
        }
    )

    assert build_task_playbook(build_turn_input(titration_assessment)) is None
    assert build_task_playbook(build_turn_input(residual_active)) is None


def test_retired_brittle_playbooks_do_not_route(adaptive_example) -> None:
    coffee = adaptive_example.model_copy(
        update={
            "subject": "Statistics",
            "batch": "USE_CASE_3_TEXT",
            "prompt": (
                "A coffee shop table asks: given morning, probability of cold beverage."
            ),
        }
    )
    twos = adaptive_example.model_copy(
        update={
            "subject": "Computer Science",
            "batch": "USE_CASE_3_TEXT",
            "prompt": (
                "The student is converting a negative number using two's "
                "complement and is confused about overflow."
            ),
        }
    )

    assert build_task_playbook(build_turn_input(coffee)) is None
    assert build_task_playbook(build_turn_input(twos)) is None


def test_remaining_dev50_failure_family_playbooks_route_cleanly(
    adaptive_example,
) -> None:
    sulphonation = adaptive_example.model_copy(
        update={
            "subject": "Chemistry",
            "batch": "USE_CASE_1_MULTIMODAL",
            "prompt": (
                "Arrange alkyl benzene compounds by sulphonation reactivity; "
                "the student asks about hyperconjugation and alpha hydrogens."
            ),
        }
    )
    penicillin = adaptive_example.model_copy(
        update={
            "subject": "Statistics",
            "batch": "USE_CASE_3_TEXT",
            "prompt": "Penicillin allergy medical record reaction probability.",
            "follow_up_prompt": "Isn't P(R|A) enough, or do I need Bayes?",
        }
    )
    ring = adaptive_example.model_copy(
        update={
            "subject": "Physics",
            "batch": "USE_CASE_3_MULTIMODAL",
            "prompt": (
                "A ring of total charge rotates about a diameter. Bring a "
                "charged particle with charge q to the circumference."
            ),
        }
    )
    t_test = adaptive_example.model_copy(
        update={
            "subject": "Statistics",
            "batch": "USE_CASE_2_MULTIMODAL",
            "prompt": "Is it valid to use a z-test?",
        }
    )
    matrix = adaptive_example.model_copy(
        update={
            "subject": "Computer Science",
            "batch": "USE_CASE_2_MULTIMODAL",
            "prompt": "Find the kth smallest element in a sorted 2D matrix.",
        }
    )

    assert "sulphonation hyperconjugation" in build_task_playbook(
        build_turn_input(sulphonation)
    )
    assert "penicillin allergy Bayes" in build_task_playbook(build_turn_input(penicillin))
    assert "rotating charged ring" in build_task_playbook(build_turn_input(ring))
    assert "z-test vs t-test" in build_task_playbook(
        build_turn_input(t_test),
        extra_context="population standard deviation unknown; sample standard deviation",
    )
    assert "kth-smallest sorted-matrix assessment" in build_task_playbook(
        build_turn_input(matrix)
    )


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


def test_new_failure_templates_rewrite_to_claim_grade_responses() -> None:
    pka_text, pka_guards = _apply_deterministic_playbook_guards(
        "Use the graph.",
        "Task-family playbook: weak-acid titration pKa adaptive explanation",
    )
    arctic_text, arctic_guards = _apply_deterministic_playbook_guards(
        "Cold denatures pigment.",
        "Task-family playbook: Arctic fox coat-color active-learning hint",
    )
    conical_text, conical_guards = _apply_deterministic_playbook_guards(
        "Cancel things.",
        "Task-family playbook: conical-pendulum adaptive explanation",
    )
    tree_text, tree_guards = _apply_deterministic_playbook_guards(
        "Check the tree.",
        "Task-family playbook: binary-tree traversal reconstruction assessment",
    )

    assert "pH = pK_a" in pka_text
    assert "half-equivalence" in pka_text
    assert "0 mL of NaOH" in pka_text
    assert pka_guards == ["titration_pka_template_rewrite"]
    assert "day length" in arctic_text
    assert "hormones" in arctic_text
    assert "new coat each season" in arctic_text
    assert arctic_guards == ["arctic_fox_denaturation_template_rewrite"]
    assert "r = L\\sin\\theta" in conical_text
    assert "2\\pi" in conical_text
    assert conical_guards == ["conical_pendulum_template_rewrite"]
    assert "starting with the **preorder** sequence is logical" in tree_text
    assert "do not place the final leaf nodes by guesswork" in tree_text
    assert tree_guards == ["binary_tree_traversal_template_rewrite"]


def test_magnetic_triangle_template_names_student_frustration_and_biot_savart() -> None:
    guarded, guards = _apply_deterministic_playbook_guards(
        "The result is zero.",
        "Task-family playbook: equilateral-triangle wire magnetic-field adaptive explanation",
    )

    assert "frustrating" in guarded
    assert "Biot-Savart Law" in guarded
    assert "you should approach each side" in guarded
    assert guards == ["magnetic_triangle_template_rewrite"]


def test_respiration_and_two_proportion_templates_are_use_case_safe() -> None:
    respiration_text, respiration_guards = _apply_deterministic_playbook_guards(
        "Oxygen becomes carbon dioxide.",
        "Task-family playbook: oxygen/CO2 cellular-respiration adaptive explanation",
    )
    stats_text, stats_guards = _apply_deterministic_playbook_guards(
        "Use pooled p = 0.27.",
        "Task-family playbook: two-proportion z-test active-learning hint",
    )

    assert "Glucose supplies the carbon" in respiration_text
    assert "oxygen catches" in respiration_text
    assert respiration_guards == ["oxygen_co2_adaptive_template_rewrite"]
    assert "It's okay to be confused" in stats_text
    assert "reduces the likelihood" in stats_text
    assert "0.27" not in stats_text
    assert "sqrt" not in stats_text.lower()
    assert stats_guards == ["two_proportion_hint_template_rewrite"]


def test_remaining_dev50_failure_templates_have_required_anchors() -> None:
    sulphonation_text, sulphonation_guards = _apply_deterministic_playbook_guards(
        "Use inductive effects.",
        "Task-family playbook: alkylbenzene sulphonation hyperconjugation explanation",
    )
    bayes_text, bayes_guards = _apply_deterministic_playbook_guards(
        "Use P(R|A).",
        "Task-family playbook: penicillin allergy Bayes active-learning hint",
    )
    coffee_text, coffee_guards = _apply_deterministic_playbook_guards(
        "Use the whole table.",
        "Task-family playbook: coffee-shop conditional-probability active hint",
    )
    t_text, t_guards = _apply_deterministic_playbook_guards(
        "z-test is fine.",
        "Task-family playbook: z-test vs t-test assessment",
    )
    ring_text, ring_guards = _apply_deterministic_playbook_guards(
        "Spin around the axis.",
        "Task-family playbook: rotating charged ring active-learning hint",
    )
    matrix_text, matrix_guards = _apply_deterministic_playbook_guards(
        "count += j",
        "Task-family playbook: kth-smallest sorted-matrix assessment",
    )

    assert "B > C > D > A" in sulphonation_text
    assert sulphonation_guards == ["sulphonation_hyperconjugation_template_rewrite"]
    assert "P(A\\mid R)" in bayes_text
    assert "law of total probability formula" not in bayes_text
    assert bayes_guards == ["penicillin_bayes_template_rewrite"]
    assert "given" in coffee_text
    assert "three\ndecimal places" in coffee_text
    assert coffee_guards == ["coffee_conditional_probability_template_rewrite"]
    assert "t-test" in t_text
    assert "standard error" in t_text
    assert "1.58" in t_text
    assert t_guards == ["t_test_vs_z_test_template_rewrite"]
    assert "rotating about a" in ring_text
    assert "diameter" in ring_text
    assert ring_guards == ["rotating_charged_ring_template_rewrite"]
    assert "so frustrated" in matrix_text
    assert "count += j + 1" in matrix_text
    assert "j = -1 correctly contributes 0" in matrix_text
    assert matrix_guards == ["kth_smallest_matrix_template_rewrite"]
