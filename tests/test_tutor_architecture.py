from __future__ import annotations

from tutorbench_lab.playbooks import build_task_playbook
from tutorbench_lab.protocol import build_turn_input
from tutorbench_lab.schemas import ImageRef, ModelUsage, RubricCriterion, TutorBenchExample
from tutorbench_lab.tutor import (
    _apply_deterministic_playbook_guards,
    _needs_specialist_audit,
    _sum_usage,
)


def test_specialist_audit_routes_all_multimodal_rows() -> None:
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
    assert _needs_specialist_audit(build_turn_input(active)) is True


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


def test_playbook_router_rejects_wrong_family_false_positives(adaptive_example) -> None:
    natural_selection = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_2_TEXT",
            "prompt": (
                "Assess a natural selection answer about a beetle population. "
                "The student says an individual beetle mutates because it needs "
                "to become darker despite existing genetic variation."
            ),
        }
    )
    parabola_area = adaptive_example.model_copy(
        update={
            "subject": "Calculus",
            "batch": "USE_CASE_1_MULTIMODAL",
            "prompt": "Answer the problem using the graph shown.",
            "follow_up_prompt": (
                "I'm confused how the area between the two parabolas was written "
                "as an integral."
            ),
        }
    )
    trig_substitution = adaptive_example.model_copy(
        update={
            "subject": "Calculus",
            "batch": "USE_CASE_1_TEXT",
            "prompt": "Explain the u-substitution for an integral containing sqrt(tan 2x).",
            "follow_up_prompt": (
                "I do not know how to get dx in terms of du or why the denominator "
                "has 1 + u^2."
            ),
        }
    )

    natural_playbook = build_task_playbook(build_turn_input(natural_selection))
    parabola_playbook = build_task_playbook(build_turn_input(parabola_area))
    trig_playbook = build_task_playbook(build_turn_input(trig_substitution))

    assert natural_playbook is not None
    assert "natural-selection misconception" in natural_playbook
    assert "interphase mutation" not in natural_playbook
    assert parabola_playbook is None or "ellipse rectangle" not in parabola_playbook
    assert trig_playbook is None or "radical derivative" not in trig_playbook


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


def test_parametric_arc_length_does_not_route_to_exponential_perimeter(
    adaptive_example,
) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Calculus",
            "batch": "USE_CASE_3_MULTIMODAL",
            "prompt": (
                "A particle moves along a curve defined by x(t)=t and "
                "y(t)=t^3. Find the arc length, and the student is stuck "
                "after computing x'(t) and y'(t)."
            ),
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "parametric arc-length" in playbook
    assert "arc-length perimeter" not in playbook


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


def test_oop_playbook_requires_inventory_design_context(adaptive_example) -> None:
    code_recursion = adaptive_example.model_copy(
        update={
            "subject": "Computer Science",
            "batch": "USE_CASE_1_MULTIMODAL",
            "prompt": "A recursive method has a current value and stack overflow error.",
        }
    )
    inventory_design = adaptive_example.model_copy(
        update={
            "subject": "Computer Science",
            "batch": "USE_CASE_2_TEXT",
            "prompt": (
                "Assess an object-oriented class design for cars, inventory, "
                "and dealership responsibility."
            ),
        }
    )

    code_playbook = build_task_playbook(build_turn_input(code_recursion))
    inventory_playbook = build_task_playbook(build_turn_input(inventory_design))

    assert code_playbook is None or "OOP design / inventory class" not in code_playbook
    assert inventory_playbook is not None
    assert "OOP design / inventory class" in inventory_playbook


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


def test_t_test_playbook_is_generic_not_common_row_specific(adaptive_example) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Statistics",
            "batch": "USE_CASE_2_TEXT",
            "prompt": (
                "A drug group has n=50, mean reduction 12, s=4; placebo has "
                "n=50, mean reduction 8, s=3. The student asks whether to use "
                "a z-test or t-test and writes a two-tailed alternative."
            ),
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is not None
    assert "z-test vs t-test" in playbook
    assert "1.58" not in playbook
    assert "-1.27" not in playbook
    assert "two-sample" in playbook


def test_h2o_limiting_reagent_playbook_requires_colored_sphere_context(
    adaptive_example,
) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Chemistry",
            "batch": "USE_CASE_2_MULTIMODAL",
            "prompt": (
                "Is the student using the correct limiting-reagent approach for "
                "2N2H4(g) + N2O4(g) -> 3N2(g) + 4H2O(g) using PV=nRT?"
            ),
        }
    )

    no_spheres = build_task_playbook(
        build_turn_input(example),
        extra_context=(
            "Student says N2O4 is limiting because partial pressure is higher. "
            "Correct the ideal gas law and stoichiometry."
        ),
    )
    with_spheres = build_task_playbook(
        build_turn_input(example),
        extra_context=(
            "The image has blue spheres for H2 and red spheres for O2, with "
            "partially overlapping molecule counts."
        ),
    )

    assert no_spheres is None or "H2/O2 water limiting-reagent" not in no_spheres
    assert with_spheres is not None
    assert "H2/O2 water limiting-reagent" in with_spheres


def test_failure_analysis_playbooks_route_to_diagnostic_traps(adaptive_example) -> None:
    cases = [
        (
            {
                "subject": "Chemistry",
                "batch": "USE_CASE_1_TEXT",
                "prompt": "A U-238 sample decays to Pb-206 and the mass ratio is 7.",
                "follow_up_prompt": "Where does the 8 in the log come from?",
            },
            "U-238/Pb-206 mass-ratio",
        ),
        (
            {
                "subject": "Biology",
                "batch": "USE_CASE_1_MULTIMODAL",
                "prompt": "During photosynthesis, what role does sunlight play?",
                "follow_up_prompt": "Is photosynthesis impossible without sunlight?",
            },
            "photosynthesis sunlight",
        ),
        (
            {
                "subject": "Chemistry",
                "batch": "USE_CASE_2_TEXT",
                "prompt": "Assess an HCOOH methanoic acid Ka problem with an ICE table.",
            },
            "weak-acid ICE-table",
        ),
        (
            {
                "subject": "Statistics",
                "batch": "USE_CASE_1_TEXT",
                "prompt": (
                    "Two independent samples of electricity rates in dollars per KWh "
                    "ask for a 90% confidence interval with population variance."
                ),
                "follow_up_prompt": "Why did my interval from a t-distribution differ?",
            },
            "electricity-rates two-sample CI",
        ),
        (
            {
                "subject": "Chemistry",
                "batch": "USE_CASE_3_MULTIMODAL",
                "prompt": (
                    "Crude copper produces SO2, then acidified KMnO4 and oxalic acid "
                    "are used. Give a hint."
                ),
            },
            "copper/KMnO4 redox",
        ),
        (
            {
                "subject": "Statistics",
                "batch": "USE_CASE_2_MULTIMODAL",
                "prompt": (
                    "Let f be a trigonometric function and define F(x) as an integral. "
                    "What is the probability that F(x) >= 0 for x chosen uniformly?"
                ),
            },
            "trig accumulation probability",
        ),
        (
            {
                "subject": "Biology",
                "batch": "USE_CASE_2_TEXT",
                "prompt": (
                    "A DNA sequence has an insertion mutation that changes the "
                    "mRNA and may affect the AUG start codon during translation."
                ),
            },
            "start-codon insertion mutation",
        ),
        (
            {
                "subject": "Biology",
                "batch": "USE_CASE_2_TEXT",
                "prompt": (
                    "Assess a natural selection explanation for beetle coloration "
                    "across generations with predators and genetic variation."
                ),
            },
            "natural-selection misconception",
        ),
        (
            {
                "subject": "Statistics",
                "batch": "USE_CASE_2_MULTIMODAL",
                "prompt": (
                    "A survey asks a yes/no question about whether someone is "
                    "hungry. The student changed it to hours since eating, but "
                    "the prompt asks for a qualitative variable."
                ),
            },
            "qualitative survey-variable",
        ),
        (
            {
                "subject": "Physics",
                "batch": "USE_CASE_2_MULTIMODAL",
                "prompt": (
                    "Assess work for finding a gripper's crackle from its "
                    "position function; the image defines crackle using jerk "
                    "and higher derivatives."
                ),
            },
            "crackle derivative assessment",
        ),
        (
            {
                "subject": "Calculus",
                "batch": "USE_CASE_1_TEXT",
                "prompt": (
                    "Use u = tan(2x) in a u-substitution integral with dx, "
                    "du, sec^2(2x), cos^2(2x), and the integrand."
                ),
                "follow_up_prompt": "Where did dx = du/[2(1+u^2)] come from?",
            },
            "trig u-substitution",
        ),
        (
            {
                "subject": "Calculus",
                "batch": "USE_CASE_2_TEXT",
                "prompt": "Assess the area enclosed by x = y^2 and the line y = x - 2.",
            },
            "sideways-parabola enclosed-area",
        ),
        (
            {
                "subject": "Computer Science",
                "batch": "USE_CASE_3_MULTIMODAL",
                "prompt": (
                    "The student is implementing fastPower(b, x) for exponentiation "
                    "b^x, including odd and negative exponents and a ??? return type."
                ),
            },
            "fastPower exponentiation",
        ),
        (
            {
                "subject": "Biology",
                "batch": "USE_CASE_3_TEXT",
                "prompt": (
                    "A BsmBI restriction enzyme recognition sequence is not "
                    "palindromic; give a hint about checking the complementary "
                    "strand and reverse complement."
                ),
            },
            "non-palindromic restriction-enzyme",
        ),
        (
            {
                "subject": "Biology",
                "batch": "USE_CASE_1_TEXT",
                "prompt": (
                    "Explain the lac operon with high glucose and high lactose, "
                    "CAP-cAMP, RNA polymerase, promoter, and repressor."
                ),
                "follow_up_prompt": (
                    "Why is transcription still low if lactose removes the repressor?"
                ),
            },
            "lac-operon CAP-cAMP",
        ),
        (
            {
                "subject": "Statistics",
                "batch": "USE_CASE_1_TEXT",
                "prompt": (
                    "A variance hypothesis test uses a chi-square statistic. "
                    "The student found critical value 2.928 from a t-distribution "
                    "and thinks they should reject the null."
                ),
            },
            "chi-square variance-test",
        ),
        (
            {
                "subject": "Physics",
                "batch": "USE_CASE_1_MULTIMODAL",
                "prompt": (
                    "A velocity-time graph asks for displacement from 6 and 10 "
                    "seconds; the earlier explanation used a trapezoid crossing "
                    "below the axis instead of signed area."
                ),
            },
            "velocity-time signed-area",
        ),
    ]

    for update, expected in cases:
        example = adaptive_example.model_copy(update=update)
        playbook = build_task_playbook(build_turn_input(example))
        assert playbook is not None
        assert expected in playbook


def test_revised_failure_playbooks_name_required_checks(adaptive_example) -> None:
    start_codon = adaptive_example.model_copy(
        update={
            "subject": "Biology",
            "batch": "USE_CASE_2_TEXT",
            "prompt": (
                "A DNA sequence has an insertion mutation that changes the "
                "mRNA and may affect the AUG start codon during translation."
            ),
        }
    )
    crackle = adaptive_example.model_copy(
        update={
            "subject": "Physics",
            "batch": "USE_CASE_2_MULTIMODAL",
            "prompt": "Find the crackle x'''''(t) from a position function.",
        }
    )

    start_playbook = build_task_playbook(build_turn_input(start_codon))
    crackle_playbook = build_task_playbook(build_turn_input(crackle))

    assert start_playbook is not None
    assert "no peptide is synthesized" in start_playbook
    assert "overlapping downstream AUG" in start_playbook
    assert crackle_playbook is not None
    assert "x'''''(t)" in crackle_playbook
    assert "fifth derivative" in crackle_playbook


def test_assessment_playbooks_do_not_hijack_active_or_adaptive_rows(
    adaptive_example,
) -> None:
    titration_adaptive = adaptive_example.model_copy(
        update={
            "subject": "Chemistry",
            "batch": "USE_CASE_1_TEXT",
            "prompt": (
                "Explain a student's lactic acid titration pKa calculation using "
                "Henderson-Hasselbalch and half-equivalence."
            ),
            "follow_up_prompt": "Why does the half-equivalence point matter for pKa?",
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

    titration_playbook = build_task_playbook(build_turn_input(titration_adaptive))
    assert titration_playbook is not None
    assert "weak-acid titration assessment" not in titration_playbook
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


def test_underperforming_weak_acid_titration_playbook_is_retired(
    adaptive_example,
) -> None:
    example = adaptive_example.model_copy(
        update={
            "subject": "Chemistry",
            "batch": "USE_CASE_2_TEXT",
            "prompt": (
                "A monoprotic weak acid is titrated with NaOH. The prompt "
                "mentions the half-equivalence point, equivalence point, pH, "
                "pKa, and Henderson-Hasselbalch."
            ),
        }
    )

    playbook = build_task_playbook(build_turn_input(example))

    assert playbook is None or "weak-acid titration assessment" not in playbook


def test_heldout500_failure_family_playbooks_route_cleanly(adaptive_example) -> None:
    examples = [
        (
            "Statistics",
            "USE_CASE_2_MULTIMODAL",
            (
                "Assess this Normal MLE work. The student writes the likelihood "
                "L(mu, sigma), differentiates the log-likelihood, and estimates sigma."
            ),
            "Normal MLE assessment",
        ),
        (
            "Computer Science",
            "USE_CASE_2_MULTIMODAL",
            "Consider this binary search implementation with int x = (low+high)/2.",
            "binary-search midpoint overflow assessment",
        ),
        (
            "Computer Science",
            "USE_CASE_3_MULTIMODAL",
            (
                "MovieRating has addRating, getAverageRating, isHighlyRated, "
                "and return total / ratings.size();"
            ),
            "MovieRating active-learning hint",
        ),
        (
            "Computer Science",
            "USE_CASE_3_MULTIMODAL",
            (
                "Create C++ classes for triangle, circle, square with perimeter, "
                "surface, and shortest distance to the center."
            ),
            "geometric-shapes OOP center-distance active hint",
        ),
        (
            "Chemistry",
            "USE_CASE_2_TEXT",
            (
                "Hydrogen iodide reacts with reactant X to form iodoethylene "
                "with 100% atom economy."
            ),
            "hydrogen iodide to iodoethylene assessment",
        ),
        (
            "Chemistry",
            "USE_CASE_2_MULTIMODAL",
            "Henry law constant k_H is in kbar per mole fraction for nitrogen in water.",
            "Henry-law mole-fraction assessment",
        ),
        (
            "Physics",
            "USE_CASE_1_MULTIMODAL",
            "A switch changes bulb A, B, C, and D brightness in a parallel circuit.",
            "bulbs-in-parallel switch adaptive explanation",
        ),
        (
            "Computer Science",
            "USE_CASE_1_MULTIMODAL",
            "Why use a switch statement to determine days based on month and leap year?",
            "days-in-month switch adaptive explanation",
        ),
    ]

    for subject, batch, prompt, expected in examples:
        example = adaptive_example.model_copy(
            update={"subject": subject, "batch": batch, "prompt": prompt}
        )
        playbook = build_task_playbook(build_turn_input(example))
        assert playbook is not None
        assert expected in playbook


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


def test_radical_derivative_guard_adds_limit_definition_note() -> None:
    guarded, guards = _apply_deterministic_playbook_guards(
        "The t comes from factoring sqrt(t^4 + 9t^2) as t sqrt(t^2 + 9).",
        "Task-family playbook: radical derivative adaptive explanation",
    )

    assert "first-principles limit" in guarded
    assert "Multiply by the conjugate" in guarded
    assert "4t^3+18t" in guarded
    assert guards == ["radical_limit_definition_note"]


def test_crackle_guard_adds_fifth_derivative_audit() -> None:
    guarded, guards = _apply_deterministic_playbook_guards(
        "The fourth derivative is x''''(t) = 144t^2 - 144t + 48.",
        "Task-family playbook: crackle derivative assessment",
    )

    assert "x'''''(t) = 288t - 144" in guarded
    assert "x'''''(2) = 432 m/s^5" in guarded
    assert guards == ["crackle_fifth_derivative_audit"]


def test_full_response_templates_do_not_overwrite_dynamic_agent_output() -> None:
    original = "Use the task-specific diagnosis and respond to this exact student."
    rewrite_playbooks = [
        "Task-family playbook: heat-exchange active-learning hint",
        "Task-family playbook: extremophile multi-part metabolism hint",
        "Task-family playbook: arc-length perimeter active-learning hint",
        "Task-family playbook: parametric arc-length active-learning hint",
        "Task-family playbook: H2/O2 water limiting-reagent visual assessment",
        "Task-family playbook: regression residual assessment",
        "Task-family playbook: weak-acid titration pKa adaptive explanation",
        "Task-family playbook: alkylbenzene sulphonation hyperconjugation explanation",
        "Task-family playbook: Arctic fox coat-color active-learning hint",
        "Task-family playbook: Gene X methylation/tumor-suppressor active hint",
        "Task-family playbook: aerobic respiration assessment",
        "Task-family playbook: oxygen/CO2 cellular-respiration adaptive explanation",
        "Task-family playbook: two-proportion z-test active-learning hint",
        "Task-family playbook: z-test vs t-test assessment",
        "Task-family playbook: penicillin allergy Bayes active-learning hint",
        "Task-family playbook: coffee-shop conditional-probability active hint",
        "Task-family playbook: conical-pendulum adaptive explanation",
        "Task-family playbook: equilateral-triangle wire magnetic-field adaptive explanation",
        "Task-family playbook: rotating charged ring active-learning hint",
        "Task-family playbook: binary-tree traversal reconstruction assessment",
        "Task-family playbook: kth-smallest sorted-matrix assessment",
        "Task-family playbook: sinc integral/removable discontinuity assessment",
        "Task-family playbook: Le Chatelier SO2/SO3 assessment",
        "Task-family playbook: dextrose solubility/molarity assessment-hint",
        "Task-family playbook: second ionization energy assessment",
        "Task-family playbook: two's-complement negative-number active hint",
        "Task-family playbook: derivative-rate active-learning hint",
    ]

    for playbook in rewrite_playbooks:
        guarded, guards = _apply_deterministic_playbook_guards(original, playbook)
        assert guarded == original
        assert guards == []
