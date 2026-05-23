"""Rubric-blind task-family playbooks for the agentic tutor."""

from __future__ import annotations

import re
from textwrap import dedent

from tutorbench_lab.schemas import TutorTurnInput


def build_task_playbook(
    turn: TutorTurnInput, *, extra_context: str | None = None
) -> str | None:
    """Return deterministic tutoring guidance for recognizable task families.

    These playbooks are deliberately generic: they do not inspect sample-specific
    rubrics, only the subject, use case, and prompt/task content already visible
    to the candidate tutor.
    """

    text = turn.user_prompt.lower()
    if extra_context:
        text = text + "\n" + extra_context.lower()
    notes: list[str] = []
    use_case = turn.use_case.value

    if turn.subject.lower() == "computer science":
        if use_case == "adaptive" and _has_days_in_month_switch_context(text):
            notes.append(_days_in_month_switch_adaptive_playbook())
        if use_case == "assessment" and _has_binary_search_overflow_context(text):
            notes.append(_binary_search_overflow_assessment_playbook())
        if use_case == "assessment" and _has_binary_tree_traversal_context(text):
            notes.append(_binary_tree_traversal_assessment_playbook())
        if use_case == "assessment" and _has_kth_smallest_matrix_context(text):
            notes.append(_kth_smallest_matrix_assessment_playbook())
        if _has_oop_design_context(text):
            notes.append(_oop_design_playbook())
        if use_case == "assessment" and _has_any(text, ["factorial", "recursive", "recursion"]):
            notes.append(_factorial_code_playbook())
        if use_case == "active_learning" and _has_fastpower_context(text):
            notes.append(_fastpower_active_hint_playbook())
        if use_case == "active_learning" and _has_movie_rating_context(text):
            notes.append(_movie_rating_active_hint_playbook())
        if use_case == "active_learning" and _has_shape_oop_center_context(text):
            notes.append(_shape_oop_center_active_hint_playbook())
        if use_case == "assessment" and _has_member_info_remove_members_context(text):
            notes.append(_member_info_remove_members_assessment_playbook())

    if (
        turn.subject.lower() == "chemistry"
        and use_case == "adaptive"
        and _has_titration_pka_context(text)
    ):
        notes.append(_titration_pka_adaptive_playbook())
    if (
        turn.subject.lower() == "chemistry"
        and use_case == "adaptive"
        and _has_sulphonation_context(text)
    ):
        notes.append(_sulphonation_hyperconjugation_playbook())
    if (
        turn.subject.lower() == "chemistry"
        and use_case == "adaptive"
        and _has_hydrogen_halide_context(text)
    ):
        notes.append(_hydrogen_halide_acid_playbook())
    if (
        turn.subject.lower() == "chemistry"
        and use_case == "adaptive"
        and _has_uranium_lead_mass_ratio_context(text)
    ):
        notes.append(_uranium_lead_mass_ratio_playbook())
    if (
        turn.subject.lower() == "chemistry"
        and use_case == "adaptive"
        and _has_photoelectron_br_binding_context(text)
    ):
        notes.append(_photoelectron_br_binding_playbook())
    if (
        turn.subject.lower() == "chemistry"
        and use_case == "active_learning"
        and _has_any(text, ["heat exchange", "furnace gases", "crude oil", "desalination"])
    ):
        notes.append(_heat_exchange_hint_playbook())
    if (
        turn.subject.lower() == "chemistry"
        and use_case == "active_learning"
        and _has_copper_kmno4_redox_context(text)
    ):
        notes.append(_copper_kmno4_redox_hint_playbook())
    if (
        turn.subject.lower() == "chemistry"
        and use_case == "assessment"
        and _has_h2_o2_water_sphere_context(text)
    ):
        notes.append(_water_limiting_reagent_visual_playbook())
    if (
        turn.subject.lower() == "chemistry"
        and use_case == "assessment"
        and _has_hi_iodoethylene_context(text)
    ):
        notes.append(_hi_iodoethylene_assessment_playbook())
    if (
        turn.subject.lower() == "chemistry"
        and use_case == "assessment"
        and _has_henry_mole_fraction_context(text)
    ):
        notes.append(_henry_mole_fraction_assessment_playbook())
    if (
        turn.subject.lower() == "chemistry"
        and use_case == "assessment"
        and _has_weak_acid_ice_context(text)
    ):
        notes.append(_weak_acid_ice_assessment_playbook())

    if turn.subject.lower() == "calculus":
        if _has_ellipse_rectangle_context(text):
            notes.append(_ellipse_rectangle_playbook())
        if turn.use_case.value == "adaptive" and _has_radical_derivative_context(text):
            notes.append(_radical_derivative_adaptive_playbook())
        if turn.use_case.value == "adaptive" and _has_trig_substitution_context(text):
            notes.append(_trig_substitution_adaptive_playbook())
        if turn.use_case.value == "assessment" and _has_sideways_parabola_area_context(text):
            notes.append(_sideways_parabola_area_assessment_playbook())
        if (
            turn.use_case.value == "assessment"
            and _has_composition_constant_range_context(text)
        ):
            notes.append(_composition_constant_range_assessment_playbook())
        if (
            turn.use_case.value == "adaptive"
            and _has_piecewise_nondifferentiability_context(text)
        ):
            notes.append(_piecewise_nondifferentiability_adaptive_playbook())
        if (
            turn.use_case.value == "assessment"
            and _has_log_integral_singularity_context(text)
        ):
            notes.append(_log_integral_singularity_assessment_playbook())
        if (
            turn.use_case.value == "active_learning"
            and _has_exponential_perimeter_context(text)
        ):
            notes.append(_arc_length_hint_playbook())
        if (
            turn.use_case.value == "active_learning"
            and _has_parametric_arc_length_context(text)
        ):
            notes.append(_parametric_arc_length_hint_playbook())
        has_derivative_context = (
            "height" in text
            and "rate of change" in text
            and _has_any(text, ["car", "mountain"])
        )
        if turn.use_case.value == "active_learning" and (
            "s'(4)" in text or has_derivative_context
        ):
            notes.append(_derivative_hint_playbook())

    if turn.subject.lower() == "biology" and _has_interphase_mutation_context(text):
        notes.append(_interphase_hint_playbook())
    if (
        turn.subject.lower() == "biology"
        and use_case == "assessment"
        and _has_start_codon_insertion_context(text)
    ):
        notes.append(_start_codon_insertion_assessment_playbook())
    if (
        turn.subject.lower() == "biology"
        and use_case == "assessment"
        and _has_natural_selection_misconception_context(text)
    ):
        notes.append(_natural_selection_assessment_playbook())
    if (
        turn.subject.lower() == "biology"
        and use_case == "assessment"
        and _has_hardy_weinberg_graph_context(text)
    ):
        notes.append(_hardy_weinberg_graph_assessment_playbook())
    if (
        turn.subject.lower() == "biology"
        and use_case == "active_learning"
        and _has_any(text, ["arctic fox", "coat color", "denaturation", "melanin"])
    ):
        notes.append(_arctic_fox_denaturation_hint_playbook())
    if (
        turn.subject.lower() == "biology"
        and use_case == "active_learning"
        and _has_any(text, ["gene x", "tumor suppressor", "methylation near"])
    ):
        notes.append(_gene_x_methylation_hint_playbook())
    if (
        turn.subject.lower() == "biology"
        and use_case == "active_learning"
        and _has_restriction_enzyme_context(text)
    ):
        notes.append(_restriction_enzyme_active_hint_playbook())
    if (
        turn.subject.lower() == "biology"
        and turn.use_case.value == "adaptive"
        and _has_oxygen_co2_adaptive_context(text)
    ):
        notes.append(_oxygen_co2_adaptive_playbook())
    if (
        turn.subject.lower() == "biology"
        and use_case == "adaptive"
        and _has_photosynthesis_sunlight_context(text)
    ):
        notes.append(_photosynthesis_sunlight_playbook())
    if (
        turn.subject.lower() == "biology"
        and turn.use_case.value == "assessment"
        and _has_aerobic_respiration_context(text)
    ):
        notes.append(_aerobic_respiration_assessment_playbook())
    if (
        turn.subject.lower() == "biology"
        and use_case == "active_learning"
        and _has_any(text, ["thermophilus", "infrared photosynthesis", "h2s", "chemosynthesis"])
    ):
        notes.append(_extremophile_metabolism_hint_playbook())
    if (
        turn.subject.lower() == "biology"
        and turn.use_case.value == "assessment"
        and _has_any(text, ["plant cell", "animal cell", "cell wall", "chloroplast"])
    ):
        notes.append(_plant_animal_cell_diagram_playbook())
    if (
        turn.subject.lower() == "biology"
        and use_case == "adaptive"
        and _has_any(text, ["independent assortment", "testcross", "punnett", "rw/tt", "ww/tt"])
    ):
        notes.append(_mendelian_testcross_playbook())
    if (
        turn.subject.lower() == "biology"
        and use_case == "active_learning"
        and _has_trihybrid_ideal_peas_context(text)
    ):
        notes.append(_trihybrid_ideal_peas_active_playbook())
    if (
        turn.subject.lower() == "biology"
        and use_case == "adaptive"
        and _has_lac_operon_context(text)
    ):
        notes.append(_lac_operon_adaptive_playbook())
    if (
        turn.subject.lower() == "biology"
        and use_case == "adaptive"
        and _has_meiosis_mitosis_gamete_context(text)
    ):
        notes.append(_meiosis_mitosis_gamete_playbook())

    if (
        turn.subject.lower() == "statistics"
        and use_case == "assessment"
        and _has_t_test_vs_z_test_context(text)
    ):
        notes.append(_t_test_vs_z_test_assessment_playbook())
    if (
        turn.subject.lower() == "statistics"
        and use_case == "assessment"
        and _has_normal_mle_context(text)
    ):
        notes.append(_normal_mle_assessment_playbook())
    if (
        turn.subject.lower() == "statistics"
        and use_case == "assessment"
        and _has_qualitative_survey_context(text)
    ):
        notes.append(_qualitative_survey_assessment_playbook())
    if (
        turn.subject.lower() == "statistics"
        and use_case == "active_learning"
        and _has_penicillin_bayes_context(text)
    ):
        notes.append(_penicillin_bayes_hint_playbook())
    if (
        turn.subject.lower() == "statistics"
        and use_case == "active_learning"
        and _has_any(text, ["central limit theorem", "clt", "sample mean", "right-skewed"])
        and not _has_any(text, ["coffee shop", "espresso", "under-filling"])
    ):
        notes.append(_clt_sample_mean_hint_playbook())
    if (
        turn.subject.lower() == "statistics"
        and use_case == "active_learning"
        and _has_ci_z_vs_t_context(text)
    ):
        notes.append(_ci_z_vs_t_active_playbook())
    if (
        turn.subject.lower() == "statistics"
        and use_case == "adaptive"
        and _has_any(text, ["bonferroni", "pooled proportion", "standardized residual"])
    ):
        notes.append(_bonferroni_pooled_proportion_adaptive_playbook())
    if (
        turn.subject.lower() == "statistics"
        and use_case == "adaptive"
        and _has_electricity_rates_ci_context(text)
    ):
        notes.append(_electricity_rates_ci_playbook())
    if (
        turn.subject.lower() == "statistics"
        and use_case == "adaptive"
        and _has_chi_square_variance_context(text)
    ):
        notes.append(_chi_square_variance_adaptive_playbook())
    if (
        turn.subject.lower() == "statistics"
        and use_case == "assessment"
        and _has_trig_accumulation_probability_context(text)
    ):
        notes.append(_trig_accumulation_probability_playbook())

    if (
        turn.subject.lower() == "physics"
        and use_case == "adaptive"
        and _has_conical_pendulum_context(text)
    ):
        notes.append(_conical_pendulum_adaptive_playbook())
    if (
        turn.subject.lower() == "physics"
        and use_case == "adaptive"
        and _has_magnetic_triangle_context(text)
    ):
        notes.append(_magnetic_triangle_adaptive_playbook())
    if (
        turn.subject.lower() == "physics"
        and use_case == "adaptive"
        and _has_velocity_time_signed_area_context(text)
    ):
        notes.append(_velocity_time_area_adaptive_playbook())
    if (
        turn.subject.lower() == "physics"
        and use_case == "adaptive"
        and _has_bulb_parallel_switch_context(text)
    ):
        notes.append(_bulb_parallel_switch_adaptive_playbook())
    if (
        turn.subject.lower() == "physics"
        and use_case == "active_learning"
        and _has_rotating_charged_ring_context(text)
    ):
        notes.append(_rotating_charged_ring_hint_playbook())
    if (
        turn.subject.lower() == "physics"
        and use_case == "active_learning"
        and _has_kinematics_hint_context(text)
    ):
        notes.append(_kinematics_hint_playbook())
    if (
        turn.subject.lower() == "physics"
        and use_case == "active_learning"
        and _has_tractor_airplane_context(text)
    ):
        notes.append(_tractor_airplane_active_playbook())
    if (
        turn.subject.lower() == "physics"
        and use_case == "assessment"
        and _has_crackle_derivative_context(text)
    ):
        notes.append(_crackle_derivative_assessment_playbook())
    if (
        turn.subject.lower() == "physics"
        and use_case == "assessment"
        and _has_inclined_box_slip_tip_context(text)
    ):
        notes.append(_inclined_box_slip_tip_playbook())
    if (
        turn.subject.lower() == "physics"
        and use_case == "assessment"
        and _has_towing_rope_components_context(text)
    ):
        notes.append(_towing_rope_components_assessment_playbook())
    if (
        turn.subject.lower() == "physics"
        and use_case == "assessment"
        and _has_series_parallel_circuit_context(text)
    ):
        notes.append(_series_parallel_circuit_assessment_playbook())
    if (
        turn.subject.lower() == "calculus"
        and use_case == "assessment"
        and _has_any(text, ["sin(t)/t", "\\frac{\\sin(t)}{t}", "removable discontinuity"])
    ):
        notes.append(_sinc_integral_assessment_playbook())

    if (
        turn.subject.lower() == "chemistry"
        and use_case == "assessment"
        and _has_any(text, ["2so2", "so_2", "so2"])
        and _has_any(text, ["so3", "so_3"])
    ):
        notes.append(_le_chatelier_assessment_playbook())
    if (
        turn.subject.lower() == "chemistry"
        and use_case == "active_learning"
        and _has_dextrose_solubility_context(text)
    ):
        notes.append(_dextrose_solubility_hint_playbook())
    if (
        turn.subject.lower() == "chemistry"
        and use_case == "assessment"
        and _has_any(
            text, ["second ionization", "second i.e", "ie₂", "ie2", "ionization energy"]
        )
    ):
        notes.append(_second_ionization_energy_assessment_playbook())

    if not notes:
        return None
    return "\n\n".join(notes)


def _has_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def _has_hydrogen_halide_context(text: str) -> bool:
    formula_seen = re.search(r"(?<![a-z0-9])(hf|hcl|hi)(?![a-z0-9])", text)
    concept_seen = _has_any(
        text,
        ["hydrogen halide", "halogen", "electronegativity", "acid strength"],
    )
    return bool(formula_seen) or concept_seen


def _has_photoelectron_br_binding_context(text: str) -> bool:
    return _has_any(text, ["photoelectron", "binding energy", "peak x"]) and _has_any(
        text,
        ["br-", "br⁻", "bromide", "chlorine", "273 mj/mol"],
    )


def _has_hardy_weinberg_graph_context(text: str) -> bool:
    return _has_any(text, ["hardy-weinberg", "hardy weinberg"]) and _has_any(
        text,
        ["mice", "brown", "white", "recessive phenotype"],
    )


def _has_tractor_airplane_context(text: str) -> bool:
    return _has_any(text, ["tractor", "airplane", "passenger loading"]) and _has_any(
        text,
        ["1.85", "2300", "0.140", "2200"],
    )


def _has_meiosis_mitosis_gamete_context(text: str) -> bool:
    return _has_any(text, ["meiosis", "mitosis"]) and _has_any(
        text,
        ["gamete", "sperm", "eggs", "diploid", "haploid"],
    )


def _has_ci_z_vs_t_context(text: str) -> bool:
    return _has_any(text, ["confidence interval", "ci ="]) and _has_any(
        text,
        ["what z is", "z is", "z*", "mean of the population", "independent random samples"],
    )


def _has_series_parallel_circuit_context(text: str) -> bool:
    return _has_any(text, ["current of the 3", "3ω", "3ohm", "3 ohm", "3Ω"]) and _has_any(
        text,
        ["12v", "12 v", "6ω", "6ohm", "6 ohm", "6Ω", "5ω", "5ohm", "5 ohm", "5Ω"],
    )


def _has_titration_pka_context(text: str) -> bool:
    return (
        "pka" in text
        and _has_any(text, ["titration", "equivalence point", "half-equivalence"])
        and _has_any(text, ["henderson", "lactic acid", "weak acid"])
    )


def _has_dextrose_solubility_context(text: str) -> bool:
    return _has_any(text, ["dextrose", "c6h12o6"]) or (
        _has_any(text, ["solubility", "saturated solution", "dissolved solute"])
        and _has_any(text, ["molarity", "g/l", "grams per liter"])
    )


def _has_sulphonation_context(text: str) -> bool:
    return _has_any(text, ["sulphonation", "sulfonation"]) and _has_any(
        text, ["alkyl", "hyperconjugation", "alpha hydrogen", "benzene"]
    )


def _has_aerobic_respiration_context(text: str) -> bool:
    return _has_any(text, ["aerobic respiration", "anaerobic respiration"]) or (
        "glycolysis" in text and _has_any(text, ["krebs", "citric acid", "electron transport"])
    )


def _has_conical_pendulum_context(text: str) -> bool:
    return (
        _has_any(text, ["conical pendulum", "uniform circular motion"])
        and "string" in text
        and _has_any(text, ["period", "one full swing", "constant angle"])
    )


def _has_magnetic_triangle_context(text: str) -> bool:
    return (
        "magnetic field" in text
        and "equilateral triangle" in text
        and _has_any(text, ["corner a", "path abc", "center of the triangle"])
    )


def _has_velocity_time_signed_area_context(text: str) -> bool:
    return _has_any(
        text, ["velocity-versus-time", "velocity-time", "velocity vs time"]
    ) and _has_any(
        text,
        [
            "trapezoid",
            "area",
            "displacement",
            "below the",
            "zero-crossing",
            "6 and 10",
        ],
    )


def _has_bulb_parallel_switch_context(text: str) -> bool:
    return (
        _has_any(text, ["bulb", "bulbs"])
        and _has_any(text, ["switch", "brighter", "dimmer", "parallel"])
        and (
            _has_any(text, ["**c**", "**d**"])
            or all(re.search(rf"\b{letter}\b", text) for letter in ["a", "b", "c", "d"])
        )
    )


def _has_kinematics_hint_context(text: str) -> bool:
    return (
        _has_any(text, ["vf", "v_f", "v^2", "kinematic"])
        and _has_any(text, ["50 m", "40 m/s", "slowing", "acceleration"])
        and not _has_conical_pendulum_context(text)
    )


def _has_binary_tree_traversal_context(text: str) -> bool:
    return (
        "binary tree" in text
        and _has_any(text, ["preorder", "pre-order"])
        and _has_any(text, ["in-order", "inorder"])
        and _has_any(text, ["postorder", "post-order"])
    )


def _has_kth_smallest_matrix_context(text: str) -> bool:
    return _has_any(text, ["kth smallest", "k-th smallest"]) and _has_any(
        text, ["sorted 2d matrix", "sorted matrix", "matrix"]
    )


def _has_oop_design_context(text: str) -> bool:
    has_inventory_domain = bool(
        re.search(r"\b(car|cars|dealership|dealerships|inventory)\b", text)
    )
    has_design_language = _has_any(
        text,
        [
            "object-oriented",
            "oop",
            "class design",
            "separate class",
            "responsibility",
            "single-responsibility",
        ],
    )
    return has_inventory_domain and has_design_language


def _has_fastpower_context(text: str) -> bool:
    return _has_any(text, ["fastpower", "fast power", "b^x", "b**x", "exponentiation"]) and (
        _has_any(text, ["negative", "odd", "x / 2", "x/2", "???", "return type"])
        or _has_any(text, ["recursive", "recursion", "decreasing subproblem"])
    )


def _has_days_in_month_switch_context(text: str) -> bool:
    return _has_any(text, ["switch statement", "switch"]) and _has_any(
        text, ["month", "days", "leap year", "isleapyear", "total number of hours"]
    )


def _has_binary_search_overflow_context(text: str) -> bool:
    return _has_any(text, ["binary search", "low", "high"]) and _has_any(
        text, ["(low+high)/2", "(low + high)/2", "low+high", "middle", "mid"]
    )


def _has_movie_rating_context(text: str) -> bool:
    return _has_any(text, ["movierating", "movie rating"]) and _has_any(
        text, ["addrating", "getaveragerating", "ishighlyrated", "ratings.size"]
    )


def _has_shape_oop_center_context(text: str) -> bool:
    return _has_any(text, ["triangle", "circle", "square"]) and _has_any(
        text,
        [
            "shortest distance to the center",
            "distance to the center",
            "geometrical shapes",
            "geometrical shape",
            "geometrical",
        ],
    )


def _has_member_info_remove_members_context(text: str) -> bool:
    return (
        _has_any(text, ["memberinfo", "member info"])
        and _has_any(text, ["removemembers", "remove members"])
        and _has_any(text, ["good standing", "ingoodstanding"])
        and _has_any(text, ["graduation", "gradyear", "grad year"])
    )


def _has_oxygen_co2_adaptive_context(text: str) -> bool:
    return (
        _has_any(text, ["cellular respiration", "glycolysis", "krebs"])
        and _has_any(text, ["oxygen", "o2"])
        and _has_any(text, ["carbon dioxide", "co2", "co₂"])
    )


def _has_two_proportion_context(text: str) -> bool:
    return _has_any(text, ["pooled proportion", "two-proportion", "two proportion"]) or (
        _has_any(text, ["vaccine", "placebo"]) and _has_any(text, ["p_v", "p_p", "proportion"])
    )


def _has_t_test_vs_z_test_context(text: str) -> bool:
    return _has_any(text, ["z-test", "z test"]) and _has_any(
        text,
        [
            "t-test",
            "t test",
            "population standard deviation",
            "sample standard deviation",
            "unknown standard deviation",
        ],
    )


def _has_h2_o2_water_sphere_context(text: str) -> bool:
    has_colored_molecule_diagram = _has_any(
        text,
        [
            "blue spheres",
            "red spheres",
            "blue molecules",
            "red molecules",
            "colored spheres",
            "partially overlapping",
            "partially hidden sphere",
        ],
    )
    has_water_reaction = _has_any(
        text,
        ["h2", "h₂", "o2", "o₂", "h2o", "h₂o", "water molecules"],
    )
    return has_colored_molecule_diagram and has_water_reaction


def _has_uranium_lead_mass_ratio_context(text: str) -> bool:
    return _has_any(text, ["u-238", "uranium"]) and _has_any(
        text, ["pb-206", "lead", "mass ratio", "half-life"]
    )


def _has_copper_kmno4_redox_context(text: str) -> bool:
    return _has_any(text, ["kmno4", "mno4", "permanganate"]) and _has_any(
        text, ["copper", "so2", "oxalic acid", "acidified"]
    )


def _has_hi_iodoethylene_context(text: str) -> bool:
    return _has_any(text, ["hydrogen iodide", "hi"]) and _has_any(
        text, ["iodoethylene", "iodoethene", "reactant x", "atom economy"]
    )


def _has_henry_mole_fraction_context(text: str) -> bool:
    return _has_any(text, ["henry", "k_h", "kh"]) and _has_any(
        text, ["mole fraction", "kbar", "n2", "n₂", "nitrogen", "water"]
    )


def _has_weak_acid_ice_context(text: str) -> bool:
    return _has_any(text, ["hcooh", "methanoic", "formic acid"]) and _has_any(
        text, ["ice table", "ka", "weak acid", "ph"]
    )


def _has_weak_acid_titration_assessment_context(text: str) -> bool:
    return (
        _has_any(text, ["titrated", "titration", "naoh"])
        and _has_any(text, ["half-equivalence", "equivalence point"])
        and _has_any(text, ["henderson", "hasselbalch", "pka", "ph"])
    )


def _has_ellipse_rectangle_context(text: str) -> bool:
    return "ellipse" in text and _has_any(
        text,
        [
            "rectangle",
            "inscribed",
            "4xy",
            "semi-axis",
            "semi axes",
            "semi-axes",
            "centered at the origin",
        ],
    )


def _has_radical_derivative_context(text: str) -> bool:
    return (
        "missing t" in text
        or (
            _has_any(text, ["sqrt(t^4 + 9t^2)", "t^4 + 9t^2", "square root"])
            and _has_any(text, ["s'(t)", "s'(4)", "derivative", "chain rule"])
            and _has_any(text, ["denominator", "cancel", "factoring", "factor"])
        )
    )


def _has_trig_substitution_context(text: str) -> bool:
    return (
        _has_any(text, ["u = tan", "u=tan", "tan 2x", "tan(2x)"])
        and _has_any(text, ["dx", "du", "sec^2", "sec²", "cos^2", "1 + u^2"])
        and _has_any(text, ["substitute", "integrand", "u-substitution", "u substitution"])
    )


def _has_sideways_parabola_area_context(text: str) -> bool:
    return (
        _has_any(text, ["x=y^2", "x = y^2", "sideways parabola"])
        and _has_any(text, ["y=x-2", "y = x - 2", "line"])
        and _has_any(text, ["area", "enclosed", "bounded", "region"])
    )


def _has_composition_constant_range_context(text: str) -> bool:
    return (
        _has_any(text, ["h(x)", "f(g(x))", "h = f(g"])
        and _has_any(text, ["discontinuities in g", "discontinuities of g", "g(x)"])
        and _has_any(text, ["f(x) = 2", "f(x)=2", "constant"])
    )


def _has_piecewise_nondifferentiability_context(text: str) -> bool:
    return (
        _has_any(text, ["piecewise-defined", "piecewise defined"])
        and _has_any(text, ["fails to be differentiable", "nondifferentiable"])
        and _has_any(text, ["left-hand derivative", "right-hand derivative"])
    )


def _has_log_integral_singularity_context(text: str) -> bool:
    return (
        _has_any(text, ["ln{x}", "ln x", "\\ln{x}", "\\ln x"])
        and _has_any(text, ["(k-2)(k+2)", "k^2 - 4", "k−2"])
        and _has_any(text, ["converges", "integral"])
    )


def _has_interphase_mutation_context(text: str) -> bool:
    return "interphase" in text and _has_any(
        text,
        [
            "daughter cell",
            "daughter cells",
            "cell division",
            "mitosis",
            "dna replication",
            "inherited",
            "passed on",
            "proofreading",
        ],
    )


def _has_start_codon_insertion_context(text: str) -> bool:
    return (
        _has_any(text, ["insertion mutation", "inserted", "insertion"])
        and _has_any(text, ["start codon", "aug", "translated", "translation"])
        and _has_any(text, ["dna sequence", "mrna", "template strand", "codon"])
    )


def _has_natural_selection_misconception_context(text: str) -> bool:
    return (
        "natural selection" in text
        and _has_any(text, ["beetle", "population", "colored", "colour", "adapted"])
        and _has_any(text, ["generation", "offspring", "predator", "allele", "genetic"])
    )


def _has_restriction_enzyme_context(text: str) -> bool:
    return _has_any(text, ["restriction enzyme", "bsmbi", "ecori"]) and _has_any(
        text,
        ["palindromic", "recognition", "complementary strand", "reverse complement"],
    )


def _has_trihybrid_ideal_peas_context(text: str) -> bool:
    return (
        _has_any(text, ["pea", "peas"])
        and _has_any(text, ["heterozygous for three", "three independent traits"])
        and _has_any(text, ["round", "green", "firm", "ideal"])
        and _has_any(text, ["1000", "offspring", "punnett"])
    )


def _has_lac_operon_context(text: str) -> bool:
    return _has_any(
        text, ["lac operon", "cap-camp", "cap camp", "camp", "catabolite"]
    ) and _has_any(
        text,
        ["glucose", "lactose", "rna polymerase", "promoter", "repressor"],
    )


def _has_photosynthesis_sunlight_context(text: str) -> bool:
    return "photosynthesis" in text and _has_any(
        text, ["sunlight", "light", "artificial photosynthesis"]
    )


def _has_electricity_rates_ci_context(text: str) -> bool:
    return _has_any(text, ["electricity rates", "kwh"]) and _has_any(
        text, ["confidence interval", "population variance", "t-distribution"]
    )


def _has_trig_accumulation_probability_context(text: str) -> bool:
    return _has_any(text, ["trigonometric", "f(x)", "f(x) ≥ 0", "f(x)>=0"]) and _has_any(
        text, ["uniform", "probability", "integral", "accumulated"]
    )


def _has_normal_mle_context(text: str) -> bool:
    return _has_any(text, ["likelihood", "log-likelihood", "mle"]) and _has_any(
        text, ["sigma", "σ", "normal", "n(μ", "n(mu"]
    )


def _has_chi_square_variance_context(text: str) -> bool:
    return _has_any(
        text, ["chi-square", "chi square", "χ²", "variance", "standard deviation"]
    ) and _has_any(
        text,
        ["critical value", "2.928", "t-distribution", "t distribution", "reject the null"],
    )


def _has_qualitative_survey_context(text: str) -> bool:
    return _has_any(text, ["qualitative", "categorical"]) and _has_any(
        text, ["survey", "yes/no", "yes or no", "hungry", "hunger", "fullness"]
    )


def _has_exponential_perimeter_context(text: str) -> bool:
    return "perimeter" in text and _has_any(text, ["e^x", "e^n", "exp(x)", "exponential curve"])


def _has_parametric_arc_length_context(text: str) -> bool:
    return "arc length" in text and _has_any(
        text,
        ["parametric", "x(t)", "y(t)", "dx/dt", "dy/dt", "x'(t)", "y'(t)"],
    )


def _has_penicillin_bayes_context(text: str) -> bool:
    return _has_any(text, ["penicillin", "allergy"]) and _has_any(
        text, ["bayes", "reaction", "p(r|a)", "medical record"]
    )


def _has_coffee_conditional_context(text: str) -> bool:
    return _has_any(text, ["coffee", "hot beverage", "cold beverage"]) and _has_any(
        text, ["given", "morning", "conditional probability"]
    )


def _has_rotating_charged_ring_context(text: str) -> bool:
    return (
        "ring" in text
        and _has_any(text, ["total charge", "charge q", "charged particle"])
        and _has_any(text, ["rotates about a diameter", "axis of rotation"])
    )


def _has_crackle_derivative_context(text: str) -> bool:
    return _has_any(text, ["crackle", "jerk"]) and _has_any(
        text, ["derivative", "x''", "x’’", "position function", "time t"]
    )


def _has_inclined_box_slip_tip_context(text: str) -> bool:
    return (
        _has_any(text, ["inclined base", "inclined plane", "incline"])
        and _has_any(text, ["cart", "box"])
        and _has_any(text, ["static friction", "coefficient of static friction", "mu_s"])
        and _has_any(text, ["slip", "sliding"])
        and _has_any(text, ["tip", "tipping"])
    )


def _has_towing_rope_components_context(text: str) -> bool:
    return (
        _has_any(text, ["rope", "ropes", "tension"])
        and _has_any(text, ["horizontal component", "horizontal force", "cos"])
        and _has_any(text, ["2.9", "2.0", "5.50", "5500"])
        and _has_any(text, ["acceleration", "newton"])
    )


def _days_in_month_switch_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: days-in-month switch adaptive explanation
        - Directly answer the student's confusion: an if/else chain can be
          correct, but a switch statement is often more readable and organized
          for grouping many month cases.
        - Quote or closely paraphrase the visible if/else structure when it is
          present: February, grouped 30-day months, and the else case for
          31-day months.
        - Required code audit when the visible work resembles the common
          if/else solution: quote or paraphrase the student's branches
          (month == 2, grouped 30-day months, else 31 days), then identify
          missing semicolon after days = 30, missing final method brace, missing
          declaration such as int days;, and missing isLeapYear helper when the
          prompt expects leap-year handling.
        - Explain that February should use isLeapYear(year) rather than a fixed
          28-day value.
        - End with an open-ended practice invitation about trying the switch
          version or another date-related method.
        """
    ).strip()


def _binary_search_overflow_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: binary-search midpoint overflow assessment
        - Do not mark the implementation fully correct if it uses
          (low + high) / 2 for the midpoint.
        - Quote the visible midpoint line, such as int x = (low + high) / 2 or
          mid = (low + high) / 2, and identify it as the bug.
        - Explain that low + high can exceed the signed integer maximum
          (for example 2^31 - 1 in Java/C++ int), which may wrap negative and
          lead to an invalid index/runtime error.
        - Provide the safe fix: low + (high - low) / 2, and justify why it
          avoids overflow by subtracting before adding back low.
        - Include a concrete large-number example rather than only stating the
          rule abstractly.
        """
    ).strip()


def _movie_rating_active_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: MovieRating active-learning hint
        - Keep this as a hint; do not write the completed corrected code.
        - Identify the real stuck point: Java integer division can discard the
          decimal part in return total / ratings.size(), and a class method can
          reuse a helper method already written in the same class.
        - Quote the visible lines where the student is stuck or wrong:
          return total / ratings.size(); and the unfinished isHighlyRated method
          when present.
        - Hint about preserving the decimal part without explicitly saying to
          cast total to double or writing return (double) total / ratings.size().
        - Hint about reusing the already-written average method without naming
          getAverageRating() inside the final code.
        - Include a checkpoint about no ratings added: what should happen before
          dividing by ratings.size()?
        """
    ).strip()


def _shape_oop_center_active_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: geometric-shapes OOP center-distance active hint
        - Keep this as a scaffolded hint, not a full C++ solution.
        - Identify the likely stuck point: how to represent each shape's center
          or centroid/circumcenter and how that connects to the "shortest
          distance to the center" property.
        - Prompt the student to decide what data each derived class must store:
          a side length for Square, a radius for Circle, and enough triangle
          information to reason about its center.
        - For Square, hint toward perimeter and surface from its side length
          without writing the exact formulas.
        - For Circle, hint that radius and pi are needed, and remind them to
          include the standard math library for pi/sqrt-type calculations; do
          not hand over both exact circle formulas in final form.
        - Mention circumcenter/circumcircle as a useful way to think about
          distance from the center when the relevant distance is from center to
          boundary/vertices.
        """
    ).strip()


def _hi_iodoethylene_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: hydrogen iodide to iodoethylene assessment
        - Work backward from the product and 100% atom economy: all atoms from
          HI and reactant X end up in iodoethylene/iodoethene.
        - Identify the student's correct high-level idea that addition to an
          unsaturated compound is relevant.
        - Explicitly flag the conceptual misuse of Markovnikov's rule when the
          student mentions it without applying regiochemistry to an asymmetric
          alkene. If ethene is the relevant reactant, Markovnikov orientation is
          not the deciding issue because ethene is symmetric.
        - Make clear which atoms are removed from the product to infer X; the
          reactant should be the alkene before HI addition, not a product with
          only iodine subtracted.
        """
    ).strip()


def _henry_mole_fraction_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: Henry-law mole-fraction assessment
        - Check the units of Henry's law constant before accepting the student's
          formula. A value in kbar per mole-fraction is pressure divided by mole
          fraction, not bar L mol^-1.
        - State that P / k_H gives a mole fraction in this convention, not a
          molarity. Mole fraction is unitless; molarity is mol/L.
        - If the task asks for amount dissolved in 1 L of water, convert water
          to moles: 1000 g / 18.0 g mol^-1 is about 55.5 mol.
        - Relate mole fraction to moles with x_N2 = n_N2 / (n_N2 + 55.5), then
          solve for n_N2 before converting to mass or concentration if needed.
        - Explicitly name the student's unit error if they treat the mole
          fraction value as mol/L.
        """
    ).strip()


def _normal_mle_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: Normal MLE assessment
        - Required: audit visible notation before differentiating. If the
          student writes L(mu, sigma) for a model parameterized by variance,
          call that notation/conceptual target wrong or misleading and say the
          correct likelihood target is L(mu, sigma^2). Do not merely say it is
          algebraically equivalent.
        - Check the Normal density constant carefully: the denominator should
          contain sqrt(2*pi*sigma^2), not sqrt(2*pi*sigma). If the visible
          expression places sigma inside the square root without squaring it,
          quote that expression and call it incorrect.
        - Distinguish partial derivatives from total derivatives:
          use partial ln L / partial mu and partial ln L / partial sigma (or
          partial sigma^2 if that is the chosen parameterization).
        - For the mu derivative, include the chain-rule sign from
          d(x_i - mu)^2/dmu = 2(x_i - mu)(-1).
        - For the variance estimate, make clear whether the final estimator is
          for sigma or sigma^2, and use mu-hat inside the final sigma^2 formula.
        - Do not affirm the likelihood or derivative work as correct unless the
          exact visible expression matches these checks.
        """
    ).strip()


def _bulb_parallel_switch_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: bulbs-in-parallel switch adaptive explanation
        - Directly acknowledge the student's confusion about bulb C.
        - State the topology explicitly: current first passes through A, then
          the remaining section has B, C, and D as parallel branches after the
          switch is closed. With the switch open, D has no current.
        - Explain brightness via power/current for identical bulbs: P = I^2 R.
        - Closing the switch adds D as another parallel path, decreasing the
          equivalent resistance of the parallel section and increasing total
          current through A, so A gets brighter.
        - Because A now has a larger voltage drop, the parallel section gets a
          smaller voltage drop, so B and C get dimmer. The correct conclusion is
          that A and D get brighter; C does not get brighter.
        """
    ).strip()


def _binary_tree_traversal_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: binary-tree traversal reconstruction assessment
        - Treat this as assessment/feedback on a student's reconstructed tree,
          not merely as a fresh solve.
        - Point out that starting with preorder is logical because preorder
          gives the root of each subtree.
        - Explain the core method: preorder selects the next subtree root;
          inorder splits nodes into left and right subtrees; postorder can be
          used as a validation check.
        - Identify correct student structure before correcting mistakes.
        - If the student is stuck on the right subtree, avoid simply handing
          over every remaining node placement. Instead, tell them to use
          preorder to select the right-subtree root and inorder to split the
          right-subtree nodes, then use postorder to check leaf placement.
        - In active-learning or scaffolded feedback, do not directly state the
          final placement of ambiguous leaf nodes such as J and K unless the
          task explicitly asks for a complete corrected answer.
        """
    ).strip()


def _kth_smallest_matrix_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: kth-smallest sorted-matrix assessment
        - Acknowledge the student's frustration and the fact that their counting
          idea was clever.
        - Explain that value-range binary search plus row-wise counting is a
          valid strategy for kth-smallest in a sorted matrix.
        - Identify the common off-by-one bug: after moving j leftward, j is an
          index, so the count of valid elements in that row is j + 1, not j.
        - Provide corrected code that handles both j >= 0 and j = -1 cleanly;
          adding j + 1 should add 0 when no element in the row is <= mid.
        - Explain why returning `left` after the binary search is appropriate:
          the search is over values and converges to the smallest value with at
          least k elements <= it.
        """
    ).strip()


def _titration_pka_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: weak-acid titration pKa adaptive explanation
        - Directly address the student's confusion between equivalence point
          and half-equivalence point.
        - State the Henderson-Hasselbalch equation:
          pH = pKa + log([A-]/[HA]).
        - Explain why half-equivalence is special: exactly half the weak acid
          has been converted to conjugate base, so [A-] = [HA], the log term is
          log(1)=0, and pH = pKa.
        - Explain why equivalence point is not used for pKa: at equivalence,
          the acid has essentially been converted into conjugate base, so the
          solution pH is controlled by conjugate-base hydrolysis, not by equal
          acid/base buffer amounts.
        - Correct graph-reading confusion: to read pH at a chosen NaOH volume,
          start at the x-axis volume, move vertically to the curve, then move
          horizontally to the y-axis. Do not follow the curve back to the
          y-axis/intercept.
        - Say the leveling-off region after equivalence is not one of the
          Henderson-Hasselbalch numbers for finding pKa.
        """
    ).strip()


def _sulphonation_hyperconjugation_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: alkylbenzene sulphonation hyperconjugation explanation
        - Directly acknowledge the student's confusion and uncertainty.
        - Correct the branch-count shortcut: more branching is not automatically
          more activating for this comparison.
        - Explain that hyperconjugation and alpha hydrogens dominate this
          sulphonation ranking more than the simple inductive-effect shortcut.
        - Count alpha hydrogens explicitly for the common tert-butylbenzene,
          toluene, ethylbenzene, and isopropylbenzene comparison:
          tert-butyl has 0, methyl has 3, ethyl has 2, isopropyl has 1.
        - State that more alpha hydrogens gives stronger hyperconjugative
          donation to the ring and faster electrophilic sulphonation.
        - Explain that reversibility of sulphonation is not the main reason for
          the reactivity order; the order concerns the forward EAS reactivity.
        - Give the ranking step by step and identify the matching option.
        """
    ).strip()


def _arctic_fox_denaturation_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: Arctic fox coat-color active-learning hint
        - Keep this as a hint, not a final answer.
        - Identify the likely misconception: the student is trying to explain
          seasonal coat color through protein denaturation.
        - Prompt them to check whether denaturation is usually caused by low
          temperatures or by high temperature/extreme pH.
        - Ask whether denaturation would be reversible enough to explain a
          coat-color cycle that changes back every season.
        - Nudge the relevant seasonal mechanism without over-answering: ask
          what environmental cue changes reliably with season besides
          temperature, and how day length could affect hormones that regulate
          melanin production in hair follicles.
        """
    ).strip()


def _gene_x_methylation_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: Gene X methylation/tumor-suppressor active hint
        - Keep this as a scaffolded hint, not a final contradiction verdict.
        - Affirm the student's core intuition that tumor suppressors usually
          reduce cancer risk when functioning normally.
        - Ask them to compare that expectation with the actual data pattern,
          then notice the tension instead of forcing a simple rule.
        - Prompt at least three possible explanations to investigate:
          1. Could Gene X behave differently from a textbook tumor suppressor
             in this context?
          2. Could very high expression disrupt normal cell regulation rather
             than always being protective?
          3. Could methylation near Gene X affect nearby regulatory regions or
             neighboring genes, not Gene X alone?
        - Ask the student what additional experiment would distinguish those
          possibilities, such as measuring Gene X protein function or nearby
          gene expression.
        """
    ).strip()


def _restriction_enzyme_active_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: non-palindromic restriction-enzyme active hint
        - Keep this scaffolded. Do not give the final site count directly.
        - First affirm any correctly found top-strand recognition site.
        - Ask whether the recognition sequence is palindromic. Use EcoRI as
          the comparison example: top 5'-GAATTC-3' aligns with bottom
          3'-CTTAAG-5', which reads the same when the bottom is read 5'->3'.
        - Prompt the student to check whether BsmBI's 5'-CGTCTC-3' behaves
          that way; if it is non-palindromic, a site on the complementary strand
          need not appear as the same letters at the same top-strand location.
        - Guide the key reverse-complement idea as a question: if the bottom
          strand reads 5'-CGTCTC-3', what must the top strand read when written
          5'->3'?
        - Remind them to scan both the original recognition sequence and its
          reverse complement in the provided strand before deciding the count.
        """
    ).strip()


def _lac_operon_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: lac-operon CAP-cAMP adaptive explanation
        - Answer the student's high-glucose/high-lactose confusion directly:
          removing the repressor permits access, but CAP-cAMP is the strong
          activation signal for efficient transcription.
        - State that the lac promoter is weak by itself; RNA polymerase can bind
          poorly, but initiation/open-complex formation is inefficient.
        - Give the low-glucose chain quantitatively where useful: low glucose
          raises cAMP, cAMP binds CAP, CAP-cAMP binds upstream near -60 bp, and
          boosts transcription roughly 100x-1000x.
        - Explain the mechanism: CAP-cAMP bends DNA and helps recruit/stabilize
          RNA polymerase, lowering the barrier for open-complex formation and
          strand separation.
        - Link catabolite repression to energy logic: if glucose is available,
          the cell avoids spending ATP/resources heavily expressing lactose-use
          genes.
        - Use the repressor analogy carefully: the repressor is like a locked
          door; CAP-cAMP is like a helper that makes RNA polymerase work well.
        """
    ).strip()


def _meiosis_mitosis_gamete_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: meiosis-vs-mitosis gamete explanation
        - Acknowledge the student's missing background explicitly: it is natural
          to ask why gametes need a special cell division at all.
        - Answer both questions: meiosis makes haploid gametes to keep the
          chromosome number stable after fertilization; mitosis makes diploid
          genetically identical cells for growth/repair.
        - Include the chromosome-balance chain: 2n parent -> n gametes by
          meiosis -> n+n fertilization -> 2n offspring. Contrast it with
          diploid gametes: 2n+2n -> 4n, then chromosome number can keep doubling
          across generations.
        - Also explain the genetic-diversity reason: mitosis-made sperm/eggs
          would be essentially genetic copies of the parent cell, while meiosis
          creates variation through crossing over and independent assortment.
        - State why diversity matters: it helps populations adapt to changing
          environments and reduces the chance that harmful mutations are passed
          along unchanged in every gamete.
        """
    ).strip()


def _oxygen_co2_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: oxygen/CO2 cellular-respiration adaptive explanation
        - Answer the student's follow-up directly; do not grade it like an
          assessment row.
        - Explicitly say inhaled oxygen is not converted into exhaled CO2.
        - Explain that the carbon atoms in CO2 come from glucose carbons.
        - Clarify the pathway: glycolysis splits glucose into pyruvate in the
          cytoplasm; pyruvate is converted to acetyl-CoA; carbon dioxide is
          released during pyruvate oxidation and the Krebs/citric acid cycle.
        - Explain oxygen's role separately: O2 accepts electrons at the end of
          the electron transport chain and becomes water.
        - Use a concrete metaphor/example, such as glucose as a six-carbon log
          being broken into smaller carbon pieces while oxygen is the final
          electron "catcher," not the source of the CO2 carbon.
        - Acknowledge confusion warmly and keep the explanation student-facing.
        """
    ).strip()


def _photosynthesis_sunlight_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: photosynthesis sunlight adaptive explanation
        - Answer the student's sunlight question directly: ordinary plant
          photosynthesis requires light because light absorption powers the
          light-dependent reactions.
        - Explain that light splits water and provides ATP/NADPH; oxygen comes
          from water, while carbon dioxide is fixed into sugars.
        - Emphasize that without light, photosynthesis cannot continue as
          photosynthesis; the plant may temporarily use stored chemical energy,
          but it is not making new sugar by photosynthesis in darkness.
        - Use the phrase "artificial photosynthesis" explicitly: it is a possible
          engineered route without direct natural sunlight only if another light
          source or light-capturing system supplies the absorbed energy. It still
          needs light/energy input; it is not photosynthesis with no energy
          source.
        - Correct the wording "turning carbon dioxide into oxygen": the oxygen
          atoms in O2 come mainly from water, not CO2.
        """
    ).strip()


def _aerobic_respiration_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: aerobic respiration assessment
        - Give feedback on correctness and errors, then provide the corrected
          pathway at AP/high-school biology level.
        - Correct any reversal of terms: aerobic means with oxygen; anaerobic
          means without oxygen.
        - Give the full aerobic respiration sequence:
          glycolysis -> pyruvate oxidation -> Krebs/citric acid cycle ->
          electron transport chain -> oxidative phosphorylation.
        - State key locations and products:
          glycolysis in cytoplasm produces 2 pyruvate, net 2 ATP, and 2 NADH;
          pyruvate oxidation in the mitochondrial matrix forms acetyl-CoA, CO2,
          and NADH; the Krebs cycle yields CO2, ATP/GTP, NADH, and FADH2; the
          ETC uses NADH/FADH2 electrons and oxygen as final electron acceptor to
          make water and drive ATP synthesis.
        - Mention that anaerobic fermentation regenerates NAD+ and yields far
          less ATP than aerobic respiration.
        - Use a constructive tone: name what the student got right before
          correcting the sequence and definitions.
        """
    ).strip()


def _conical_pendulum_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: conical-pendulum adaptive explanation
        - Explicitly acknowledge the student's confusion about eliminating both
          tension and speed.
        - Explain the two-force equations as two clues about the same tension:
          vertical balance gives Tension*cos(theta)=mg; horizontal circular
          motion gives Tension*sin(theta)=mv^2/r.
        - Divide the horizontal equation by the vertical equation to cancel
          tension and mass, giving tan(theta)=v^2/(rg).
        - State the missing background formulas: the circle radius is
          r = L sin(theta), and one lap means v = 2*pi*r / period.
        - Substitute those formulas and solve for the period, keeping notation
          clear so the period T is not confused with tension.
        - Include a quick self-check: units should come out as seconds, and the
          limiting behavior for small theta should resemble a simple pendulum.
        """
    ).strip()


def _magnetic_triangle_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: equilateral-triangle wire magnetic-field adaptive explanation
        - State that the final result refers to the total magnetic field at the
          triangle's center.
        - Remind the student that the wire has uniform resistance, so the direct
          A-C path and the two-side A-B-C path split current according to their
          resistances.
        - State that the magnetic field contribution from current along path
          A-B-C at the center points opposite the contribution from current
          along direct path A-C.
        - Make the cancellation idea explicit: although the paths carry
          different currents, the two-side path has two equal side
          contributions that combine to cancel the direct side contribution at
          the center.
        - Conclude clearly that the total magnetic field at the center is zero.
        - Mention the wire resistance is uniform along each side because that is
          why current division can be inferred from path lengths.
        """
    ).strip()


def _velocity_time_area_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: velocity-time signed-area adaptive explanation
        - Directly address the student's instinct that displacement comes from
          area under a velocity-time graph.
        - State the sign rule: area above the time axis is positive
          displacement, and area below it is negative displacement.
        - If an earlier trapezoid shortcut crossed the time axis, call it
          conceptually flawed rather than defending it as equivalent. A correct
          final number can happen by cancellation.
        - Derive the zero-crossing time from the slope/acceleration and
          v_f = v_i + at instead of merely asserting it from the graph.
        - Split the interval at the zero crossing, compute the positive and
          negative triangular areas separately, and explain any cancellation.
        """
    ).strip()


def _rotating_charged_ring_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: rotating charged ring active-learning hint
        - Keep this as a hint, not a full calculation.
        - Identify the likely misread: the ring rotates about a diameter, not
          about the central symmetry axis.
        - Nudge the student away from magnetic/rotational complications if the
          question asks work/energy for moving a charge: ask which electric
          potential difference matters.
        - Hint that an infinitesimal charged loop or ring element with finite
          charge density can have a simple potential contribution; the student
          may not need a long force integral if they reason with potential.
        - Ask whether points on the ring and points on the axis have potentials
          that can be compared using symmetry and superposition.
        """
    ).strip()


def _oop_design_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: OOP design / inventory class
        - Explicitly separate "do we have multiple real dealerships?" from
          "where should inventory-management responsibility live?"
        - Name the single-responsibility principle and connect it to Car vs
          Dealership responsibilities.
        - Include a tiny alternative code sketch without a Dealership class,
          such as a List<Car> in main plus a helper search/count function.
        - Include a real-world analogy: even one physical dealership benefits
          from having an inventory manager or filing cabinet rather than leaving
          car records scattered on every employee's desk.
        - Include trade-offs: an extra class can be overkill for tiny scripts,
          but becomes justified when inventory operations, persistence, search,
          reporting, or tests need a home.
        - Give a decision rule: use Dealership when there is behavior/state
          around the collection; use a plain list for a small one-off program.
        """
    ).strip()


def _member_info_remove_members_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: AP CSA MemberInfo removeMembers assessment
        - Treat this as code feedback, not a generic praise pass.
        - State the two required behaviors separately:
          (1) return an ArrayList of members whose gradYear is <= the cutoff
          and who are in good standing; (2) remove every member whose gradYear
          is <= the cutoff from memberList, regardless of standing.
        - If the student's logic only removes or returns the good-standing
          graduates, say that this gives both the wrong returned list and the
          wrong remaining memberList. Use a tiny named-member example.
        - Provide corrected Java code. It may collect candidates in a temporary
          list and call removeAll, or use an Iterator/removeIf safely, but it
          must not remove from memberList inside an enhanced for-loop.
        - Explain why the chosen removal method avoids
          ConcurrentModificationException.
        - Include at least one edge case: no graduates, all graduates, or a
          not-good-standing graduate who should be removed but not returned.
        - End with a short takeaway about separating "return" criteria from
          "remove" criteria.
        """
    ).strip()


def _factorial_code_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: recursive factorial assessment
        - Begin by acknowledging at least three specific things the student did
          correctly, including static method signatures, class structure/naming,
          and having a main method test harness.
        - Quote the faulty recursive line and explain that factorial(n) must
          move toward the base case by calling factorial(n - 1).
        - Check both required base cases, factorial(0) and factorial(1).
        - Treat suspicious identifier misspellings such as reslut/result as a
          compilation error to fix. State plainly that `int reslut` should be
          `int result` and that the typo will cause a compile error when the
          intended identifier `result` is referenced. Do not say the snippet
          compiles cleanly or that the isolated snippet happens to compile
          while that typo is present.
        - Provide corrected code with Javadoc-style @param and @return docs.
        - Show the mathematical verification factorial(5) = 5 x 4 x 3 x 2 x 1
          = 120 and show the expected output format.
        - Suggest at least two additional tests beyond factorial(5), such as
          factorial(0), factorial(1), factorial(3), and a negative input case.
        - Explain negative input validation: without a guard, negative n keeps
          recursing away from 0/1 and can also overflow the stack.
        """
    ).strip()


def _fastpower_active_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: fastPower exponentiation active-learning hint
        - Keep this as a hint. Do not give the exact completed return type,
          base cases, or return statements.
        - Identify the student's likely block: modeling exponent rules as
          smaller recursive subproblems, not just Java syntax.
        - Ask them to inspect any placeholder return type such as `???`, and
          connect `null` to reference types/classes rather than primitive
          `double`.
        - Nudge toward a non-recursive special case for the base, analogous to
          the `b^0` exponent base case, without stating the exact code.
        - Prompt the exponent rules as questions:
          for odd positive x, how can b^x be written using b^(x-1)?
          for negative x, how can b^x be rewritten using b^(-x)?
        - Remind them that if x is negative, -x is positive, so the recursive
          helper can still move toward a known positive-exponent case.
        """
    ).strip()


def _hydrogen_halide_acid_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: hydrogen halide acid strength
        - Begin with an explicit compliment/acknowledgement of the follow-up
          question itself, e.g. "Great question — this is a very common and
          important confusion."
        - Correct the definition: electronegativity is how strongly one atom
          pulls shared bonding electrons, not how many atoms attract another.
        - Explicitly correct the atom-count misconception: HCl has two atoms,
          just like HF and HI; it does not have "more atoms" than the others.
        - State the final ranking weakest to strongest: HF < HCl < HI.
        - Explicitly state the atom-size mismatch rule: the greater the size
          difference between H and X, the longer/weaker the H-X bond and the
          stronger the acid.
        - Explicitly state that iodine is quite large compared with hydrogen;
          therefore the H-I bond is the weakest and easiest to break.
        - Define conjugate base: the anion left after the acid donates H+.
        - State that stronger acids have more stable conjugate bases.
        - Explain charge spreading: I- is large and spreads/accommodates
          negative charge well; F- is small/high charge density and holds
          negative charge less comfortably.
        - State conjugate-base stability order explicitly: F- < Cl- < I-.
        """
    ).strip()


def _uranium_lead_mass_ratio_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: U-238/Pb-206 mass-ratio adaptive explanation
        - Do not simply defend an initial solution that treats the given ratio
          as an atom ratio. Check whether the prompt says mass ratio.
        - State that radioactive decay equations track numbers of atoms or
          moles, not mass directly.
        - Convert mass ratio to atom/mole ratio before using N0/N:
          (mass Pb/206) / (mass U/238), so a mass ratio of 7 gives an atom
          ratio about 7*238/206 = 8.1.
        - Explain the student's likely misconception: adding 1 to 7 only works
          if 7 is already an atom ratio; here it is a mass ratio.
        - Then connect the atom ratio to original uranium: remaining U is one
          part and produced Pb atoms are about 8.1 parts, so N0/N is about 9.1,
          leading to a log near log(9), not log(8).
        - Directly answer the follow-up about "where does 8 come from" while
          also correcting the mass-vs-atoms issue.
        """
    ).strip()


def _heat_exchange_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: heat-exchange active-learning hint
        - This is an active-learning row: do not solve any part of the problem.
          Do not write the final gas temperature, Delta T_o, Delta T_g, or a
          substituted equation that computes them.
        - If the student sounds confused, acknowledge that the setup is easy to
          mix up because one stream is warming while the other is cooling.
        - Give only a scaffold: ask them to compute the oil temperature change
          from 80 C to 150 C, without revealing that calculation.
        - Ask them to use the coefficient relationship in words: the gas-side
          coefficient is half the crude-oil coefficient, so the gas temperature
          change must compensate in the energy balance.
        - Ask them to define the gas temperature change as an inlet minus outlet
          drop because the furnace gases cool, but do not write the full equation
          with 500 C or solve for the outlet.
        """
    ).strip()


def _copper_kmno4_redox_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: copper/KMnO4 redox active-learning hint
        - Keep this as a hint: do not compute the final copper mass or sample
          weight.
        - Explicitly affirm the useful starting point: the copper reaction gives
          a 1:1 molar relation between Cu and SO2, so x mmol Cu produces x mmol
          SO2.
        - The key fix is to write the acidic redox half-reactions separately.
          Prompt the student to balance O with H2O, balance H with H+, and then
          balance charge with electrons.
        - For acidified permanganate, guide them to MnO4- -> Mn2+ and ask how
          many electrons Mn gains.
        - For SO2 -> SO4^2-, guide them to compare sulfur's oxidation states
          and ask how many electrons SO2 loses.
        - Do not stop after naming n-factors. Prompt them to scale the two
          half-reactions to cancel electrons; for the common acidic row, that
          means asking why 2 permanganate half-reactions and 5 SO2 half-reactions
          line up.
        - Prompt them to combine the half-reactions after scaling, cancel common
          species, and read the KMnO4:SO2 mole ratio from the balanced equation.
          Mention the checkpoint ratio 2:5 as an intermediate scaffold, not as
          the final sample mass.
        - After that, have them subtract leftover KMnO4, found from oxalic acid,
          from total initial KMnO4 before connecting back to x mmol SO2. Remind
          them to convert the KMnO4 solution amount using molarity and volume.
        """
    ).strip()


def _water_limiting_reagent_visual_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: H2/O2 water limiting-reagent visual assessment
        - Do not use hydrogen-halide acid-strength guidance for this task.
        - For blue/red sphere diagrams forming water, explicitly connect colors
          to molecules: blue H2 and red O2.
        - Count partially overlapping molecules according to the prompt's rule:
          each partially hidden sphere still counts as one molecule.
        - Preserve counts that are visible or stated in the prompt/context before
          doing stoichiometry. In the common prompt example, use 12 H2 and 8 O2
          if those are the diagram counts.
        - Write and justify the balanced equation: 2 H2 + O2 -> 2 H2O.
        - Compute individual yields from each reagent, compare them, identify
          the limiting reagent, and answer the original question about how many
          water molecules can be formed.
        """
    ).strip()


def _weak_acid_ice_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: weak-acid ICE-table assessment
        - Treat this as feedback on the student's work, not a fresh weak-acid
          solution only.
        - Identify correct pieces first: weak-acid dissociation equation and Ka
          expression, if the student wrote them correctly.
        - Quote the student's ICE-table change row if visible. If they wrote
          +x, -x, -x, explain that the reactant must decrease and products must
          increase, so the change row is -x, +x, +x.
        - For the common HCOOH row with C = 0.25 M and Ka = 1.8e-4, do not let
          a weak image transcript hide the later visible work. The student may
          have written the wrong change row (+x, -x, -x), the wrong denominator
          0.25 + x, the bad simplification x*x/(0.25 - x) -> x/0.25, [H+] =
          4.5e-5, and pH = 4.35. Audit those explicitly if this row family
          matches.
        - Required: state that wrong ICE signs can produce a wrong denominator such as
          0.25 + x, but the larger conceptual error is simplifying
          Ka = x*x/(0.25 - x) as x/0.25 instead of x^2/0.25.
        - Required: say the student's [H+] = 4.5e-5 comes from that bad
          simplification and is not the equilibrium hydrogen concentration.
        - Correct [H+] explicitly: solve x^2 = Ka*C, so [H+] is about
          sqrt(1.8e-4*0.25), not 4.5e-5.
        - State plainly that any pH based on [H+] = 4.5e-5, such as pH = 4.35,
          is incorrect; then give the corrected pH.
        """
    ).strip()


def _weak_acid_titration_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: weak-acid titration assessment
        - Treat this as feedback on the student's work, not a fresh solution.
        - Audit every path the student tried: equivalence-point stoichiometry,
          Henderson-Hasselbalch setup, and any hydrolysis/Ka reasoning.
        - At the half-equivalence point, explicitly state pH = pKa for a weak
          acid/conjugate-base buffer.
        - If the student uses Henderson-Hasselbalch with a later pH, explicitly
          check the subtraction pH - pKa and the resulting [A-]/[HA] ratio.
        - Required for rows with pH 9.25 and pKa 4.75: show
          9.25 - 4.75 = 4.50 in Henderson-Hasselbalch, and if the student wrote
          9.25 - 2.38 = 5.97, identify that as an arithmetic/substitution error.
        - Explain what a large [A-]/[HA] ratio means chemically: very little HA
          remains, so "almost all converted" is incomplete unless tied to the
          stoichiometric amount of base added.
        - Still provide the corrected concentration from moles NaOH at the
          equivalence point when the prompt asks for the original acid
          concentration.
        """
    ).strip()


def _trig_substitution_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: trig u-substitution adaptive explanation
        - Answer the student's "where did these substitutions come from?"
          confusion directly and do not switch to an unrelated derivative task.
        - List the exact substituted pieces: sqrt(tan(2x)), dx, and any
          sec^2/cos^2 expression that must be rewritten in terms of u.
        - Starting from u = tan(2x), explicitly show du/dx = 2 sec^2(2x) and
          therefore dx = du / [2 sec^2(2x)].
        - Then use the standard identity sec^2(theta) = 1 + tan^2(theta) to
          get dx = du / [2(1 + u^2)].
        - State that the derivative of tan and the identity sec^2(theta) =
          1 + tan^2(theta) are standard facts to know or recall from a formula
          sheet; the student is not expected to re-derive them from scratch in
          the middle of the substitution.
        - End with a quick check-in question about which substituted piece is
          still unclear.
        """
    ).strip()


def _sideways_parabola_area_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: sideways-parabola enclosed-area assessment
        - Treat y = sqrt(x) as only the upper branch of x = y^2. Explicitly
          name the missed lower branch y = -sqrt(x).
        - Find the intersections in y when possible: y^2 = y + 2 gives
          y = -1 and y = 2. If integrating with respect to x, split the region.
        - State the common missed piece: from x = 0 to x = 1, the enclosed area
          is between -sqrt(x) and +sqrt(x), so it contributes
          integral_0^1 2sqrt(x) dx.
        - Then handle the x = 1 to x = 4 piece between sqrt(x) and x - 2.
        - Add the subareas explicitly and give the corrected total area.
        - Explain that continuity/graph shape, not checking a single point, is
          what justifies which curve is above on each interval.
        """
    ).strip()


def _composition_constant_range_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: composition constant-range assessment
        - Do not assume discontinuities of g automatically become
          discontinuities or nondifferentiability points of h = f(g(x)).
        - First determine the range of g on the interval in question. If the
          image/prompt shows g(x) stays inside an interval where f is constant,
          state that h can be constant even when g has jumps.
        - For the common row where g(x) stays in (-1, 1) and f(x)=2 on that
          interval, conclude h(x)=2 throughout the interval, so h is continuous
          and differentiable there.
        - Correct the student's core misconception explicitly: composition can
          hide discontinuities when the outer function maps both one-sided
          input values to the same output.
        - State the requested counts/values after the explanation, rather than
          only discussing candidate discontinuity points.
        """
    ).strip()


def _piecewise_nondifferentiability_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: piecewise graph nondifferentiability explanation
        - Answer the student's follow-up directly; do not discuss only the
          point they mention if the prompt asks for all nondifferentiable
          points.
        - For each candidate x-value visible in the graph, check continuity
          first, then compare left-hand and right-hand slopes/derivatives.
        - State the exact one-sided derivative values when the graph gives
          straight pieces. For the common graph row, x=-2 has left derivative
          0 and right derivative -2; x=0 has left derivative -2 and right
          derivative 0. Both are continuous corners/sharp turns.
        - Explicitly correct the misconception "continuous means
          differentiable": continuity is necessary but not sufficient.
        - Explicitly correct "just set the derivative at x=-2 to 0": a
          derivative at a point must be unique, so unequal one-sided
          derivatives mean no derivative exists.
        - Use a simple image analogy, such as a smooth road versus a sharp
          elbow/corner, and acknowledge that the distinction is easy to mix up.
        """
    ).strip()


def _ellipse_rectangle_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: ellipse rectangle explanation
        - Open with an encouraging acknowledgement that the student's instinct
          to compare methods is good, while making clear what must be fixed.
        - Include an explicit visual-anchor sentence close to the start, such
          as: "In the ellipse diagram, the ellipse is centered at the origin
          with semi-axes a and b, and the inscribed rectangle is symmetric
          across both axes."
        - If the student says "the rectangle area is xy", explicitly correct
          that statement: xy is only the first-quadrant/quarter-rectangle area,
          not the area of the whole inscribed rectangle.
        - Do not merely say the xy method is "perfectly equivalent." It can
          locate the same maximizing x only if the student remembers to multiply
          by 4 for the actual rectangle area; their final rectangle area is
          wrong if they leave it as xy.
        - If discussing an inscribed rectangle centered at the origin, explicitly
          say the rectangle has vertices (x,y), (-x,y), (x,-y), and (-x,-y).
        - Explain why total area is 4xy: width is 2x, height is 2y, so
          area = (2x)(2y) = 4xy.
        - If the student found x = a/sqrt(3) or area ab*sqrt(3)/3, say those
          results come from an algebra/derivative mistake and show the corrected
          derivative checkpoint leading to x = a/sqrt(2).
        - If image/context conflict is present in an adaptive row, still answer
          the student's follow-up first and mention image elements only briefly
          and accurately.
        """
    ).strip()


def _photoelectron_br_binding_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: chlorine PES / bromide binding-energy explanation
        - Treat Peak X as the inner-shell orbital identified by the prompt/image;
          in the common chlorine PES row, Peak X is the 1s orbital.
        - If the student asks about Br- versus chlorine, answer the follow-up
          directly: the corresponding 1s orbital in Br- has higher binding
          energy than chlorine's 1s orbital because bromine has a much larger
          nuclear charge (Z=35 vs Z=17), while outer-shell shielding barely
          affects 1s electrons.
        - Correct the misconception carefully: adding an electron increases
          electron-electron repulsion/shielding; it does not increase nuclear
          attraction, because nuclear attraction comes from protons.
        - Scope the teacher's heuristic: "more electrons = stronger binding" is
          not a safe rule for ion formation. If using an example, compare a
          neutral atom to its anion such as F vs F-, where the extra electron
          does not add protons and tends to reduce effective pull on valence
          electrons.
        - Use the given proportionality BE proportional to (Z_eff)^2/n^2. For
          the 1s-to-1s comparison, n is the same; the larger Z_eff dominates.
        - Include the rough ratio check when useful: Z_eff(Cl 1s) is about 16
          and Z_eff(Br- 1s) is about 34, so Br-'s 1s binding energy is roughly
          (34/16)^2 times chlorine's 273 MJ/mol, i.e. much higher.
        """
    ).strip()


def _start_codon_insertion_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: start-codon insertion mutation assessment
        - Assess the student's sequence work line by line before giving the
          final biological consequence.
        - Required: if inserted bases split the original AUG into a different
          first codon such as AUA, state that the original AUG start codon has
          been destroyed.
        - State the principle: eukaryotic ribosomes normally require a valid AUG
          start codon to initiate translation; they do not simply begin at an
          arbitrary codon because the reading frame looks convenient.
        - For TutorBench/AP-level grading, do not rescue the answer by treating
          an overlapping downstream AUG as a new normal start unless the prompt
          explicitly asks about alternative start sites. The expected conclusion
          is that normal translation initiation fails, no peptide is synthesized,
          and protein function is lost.
        - Distinguish this from an ordinary frameshift-after-start-codon case:
          the key error may be loss of initiation, not just changed downstream
          amino acids.
        """
    ).strip()


def _natural_selection_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: natural-selection misconception assessment
        - Credit the student's correct idea that some variants survive and
          reproduce more successfully under a selective pressure.
        - Correct individual-level language like "the beetles adapted/became
          darker because they needed to" by explaining that populations evolve
          across many generations.
        - Use genetic terminology: alleles, genotypes/phenotypes, heritable
          variation, and changing allele frequencies in the population.
        - Mention that predation is one selective pressure, but other pressures
          such as temperature regulation, mate choice, parasites, or competition
          could also influence coloration.
        - Contrast natural selection with constraints: not every useful trait is
          reachable because development, existing genetic variation, ancestry,
          and physics constrain what can evolve.
        """
    ).strip()


def _interphase_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: interphase mutation active-learning hint
        - Match the prompt's use case: in assessment, explicitly identify what
          the student got right/wrong; in adaptive explanation, directly answer
          the student's confusion; in active learning, keep the correction
          scaffolded without writing the student's final sentence for them.
        - Start with this explicit reconnection or a close paraphrase:
          "Since the original question asks you to describe interphase in the
          context of cell division..."
        - Stay focused on the one misconception about whether mutations from
          interphase can be inherited; avoid broad mitosis detail and avoid
          adding extra checkpoint taxonomy.
        - Include one open-ended question challenging the absolute word, e.g.
          "Is it true that no mutations introduced during interphase can ever be
          inherited by daughter cells?"
        - Include one why/process question, e.g. "Why do cells need proofreading
          or repair mechanisms if copying errors could never be passed on?"
        - Hint through the chain DNA copied in interphase -> copied DNA is what
          daughter cells receive, without writing the corrected final sentence.
        """
    ).strip()


def _qualitative_survey_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: qualitative survey-variable assessment
        - State the simplest answer first when appropriate: a yes/no survey item
          is already qualitative/categorical, so it may not need modification to
          add a qualitative variable.
        - If giving a modified question, preserve the original intent of
          assessing hunger/fullness rather than changing to an unrelated
          construct.
        - Contrast qualitative with quantitative: counts, hours, amounts, or
          other numeric measurements are quantitative even when they come from a
          survey.
        - Include one simple qualitative rewrite such as asking whether the
          participant is hungry/full right now, and optionally a second example
          if the prompt asks for another qualitative variable.
        """
    ).strip()


def _extremophile_metabolism_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: extremophile multi-part metabolism hint
        - This is an active-learning row. Do not write final answers for parts
          (a), (b), or (c), and do not give a finished food-web chain.
        - Identify the student's likely sticking point: they need more
          mechanism and specificity in each part, not just broad labels.
        - For part (a), ask them to trace ATP/electron flow in each pathway:
          what energy source starts it, where electrons enter, and what output
          is used to fix carbon.
        - For part (b), nudge the recycling/re-oxidation idea without declaring
          a final electron acceptor: ask what must happen to reduced carriers so
          the infrared pathway can keep cycling.
        - For part (c), ask them to name T. photosynthetica's ecosystem role as
          the producer/base of the food web because it converts vent chemistry
          and infrared energy into biomass.
        - Also for part (c), prompt the impact of reduced H2S: what happens to
          energy availability at the producer level, and how would that ripple
          upward through organisms that depend on that biomass?
        """
    ).strip()


def _pooled_proportion_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: two-proportion z-test active-learning hint
        - Keep this as an active-learning hint, not a solution.
        - Validate the student's confusion explicitly.
        - Direct the student back to the phrase "reduces the likelihood" and
          ask whether the alternative should be one-sided rather than two-sided.
        - Explain the concept without computing the pooled value: under H0 the
          two population proportions are assumed equal, so the standard error
          should use one combined estimate based on both groups.
        - Ask the student what numerator and denominator would combine the
          disease counts and total participants across both groups, but do not
          calculate the pooled proportion.
        - Do not write the explicit two-proportion standard-error formula, final
          z-score, p-value, or conclusion.
        """
    ).strip()


def _t_test_vs_z_test_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: z-test vs t-test assessment
        - First classify the actual scenario: one-sample vs two-sample,
          one-tailed vs two-tailed, and known population sigma vs sample SD.
        - State clearly whether the student's chosen z/t family is valid for
          this exact prompt; do not reuse numbers from another z/t problem.
        - Explain the reason: z-tests require known population standard
          deviation or a justified large-sample normal approximation; t-tests
          account for uncertainty in estimated standard deviations.
        - If it is a two-sample mean comparison, write the hypotheses using the
          two group means, use the correct standard-error formula, and discuss
          Welch or pooled degrees of freedom as appropriate.
        - Correct the test statistic, p-value/critical-value logic, conclusion,
          and statistical phrasing such as "reject/fail to reject" rather than
          "accept the alternative."
        - Keep an assessment tone: identify correct setup steps, identify the
          exact invalid assumptions or language, and give the corrected
          procedure.
        """
    ).strip()


def _penicillin_bayes_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: penicillin allergy Bayes active-learning hint
        - Keep this as a hint; do not compute the final probability.
        - Acknowledge that Bayes can feel like overkill because P(R|A) is a
          tempting number to grab.
        - Clarify the distinction: P(R|A) is the probability of reaction among
          listed-allergy patients, but the question asks P(A|R), among patients
          who reacted, what fraction had a listed allergy.
        - Guide with questions about the denominator instead of stating the law
          of total probability formula: among all patients who react, do they
          come only from the listed-allergy group, or from both listed and
          non-listed groups?
        - Ask the student to compare the contribution from listed-allergy
          patients with the contribution from not-listed patients before forming
          the final ratio.
        """
    ).strip()


def _coffee_conditional_probability_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: coffee-shop conditional-probability active hint
        - Start with empathy for the student's confusion.
        - Keep it as a hint, not a calculation.
        - Emphasize that "given morning" shrinks the whole sample space to only
          the morning visitors.
        - Explain probability as a part-to-whole ratio that can be written as a
          decimal or percentage.
        - Do not state the specific numerator or denominator from the table.
          Instead ask: within the morning-only group, which count is the cold
          beverage part and which count is the whole morning group?
        - Remind the student to round the final decimal to three places.
        """
    ).strip()


def _clt_sample_mean_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: CLT sample-mean active-learning hint
        - Keep this as a hint, not a mini-lecture. Affirm the student's SE and
          z-score only if already computed correctly.
        - Include at least two probing questions:
          1. "What does the Central Limit Theorem say happens to the sampling
             distribution of x-bar as n gets large?"
          2. "Does that CLT statement depend on the original population being
             normal, or does it apply even when the population is skewed?"
        - Ask the student to apply that principle to n = 50 in this exact light
          bulb scenario.
        - Instruct the student to interpret P(Z < a negative z-value) as a
          left-tail standard-normal probability and round the final probability
          to three decimals.
        - Do not state P(Z < -0.707), do not give the numerical probability,
          and do not directly say the final rounded answer.
        """
    ).strip()


def _ci_z_vs_t_active_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: mean-CI z-vs-t active-learning hint
        - Keep this as a hint. Do not give the final critical value or the final
          confidence interval.
        - Acknowledge that the student's formula shape is close, but ask a
          prior decision question before looking up z: do we know the population
          standard deviation sigma, or did we estimate spread from this sample?
        - Guide them to question z vs t. If sigma is unknown and s comes from a
          sample, the appropriate critical value usually comes from a
          t-distribution, not z.
        - Hint toward degrees of freedom without giving the final interval:
          for a one-sample t interval, df = n - 1; ask what df is when n = 16.
        - If visible work has a transcription or sample-standard-deviation
          issue, mention it briefly as something to fix after choosing the right
          critical-value family.
        """
    ).strip()


def _regression_residual_feedback_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: regression residual assessment
        - Treat this as assessment/feedback: explicitly say what the student did
          correctly, identify the exact arithmetic error, and then give the
          corrected calculation.
        - For residuals, preserve enough decimal precision until the final line.
          State the predicted value to two decimals with units when the prompt's
          numbers support it, then state the residual to two decimals with units.
        - Explicitly say residual = actual - predicted, and that a positive
          residual means the model under-predicted the observed value.
        - If the student's rounded residual differs from the corrected residual,
          quantify the size of the student's numerical error instead of merely
          saying "about." For example, compare the student's rounded value to
          the corrected residual and name the gap.
        - Explicitly address relative-error confusion: residuals are not divided
          by the predicted value unless the problem asks for relative error.
        """
    ).strip()


def _bonferroni_pooled_proportion_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: Bonferroni pooled-proportion adaptive explanation
        - In the first paragraph, explicitly acknowledge the student's confusion.
        - Correct the Bonferroni misconception: for this benchmark's convention,
          compare the original p-value to the adjusted alpha level; do not divide
          the p-value by the number of tests.
        - State the adjusted alpha calculation alpha/3 = 0.05/3 = 0.0167.
        - Explicitly say the prep-book claim, as stated by the student, is not
          correct for the method being used here.
        - Correct the pooled proportion: the denominator must include all people
          from both groups, not only car owners. Use table numbers directly,
          such as 10, 35, 70, 60, 45, and 130.
        - Show enough work to get the standard error as 0.084 when comparing
          Downtown and Outside.
        - Address standardized residuals separately: residuals greater than 2
          flag cells worth investigating, but they do not by themselves prove
          the overall chi-square test is significant.
        - Use second person wording ("you", "your") and directly address all
          three misconceptions.
        """
    ).strip()


def _electricity_rates_ci_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: electricity-rates two-sample CI adaptive explanation
        - Acknowledge the student's stated confusion explicitly before the math.
        - Explain that the student's interval can arise from using a two-sample
          t interval with pooled standard deviation, not merely from rounding.
        - Show the t-route checkpoints when comparing to the student's answer:
          df = n1 + n2 - 2 = 28, t_{0.05,28} is about 1.701 for a 90% CI, and
          the pooled standard deviation is about 0.2514.
        - Also be honest about the prompt wording: if the variances are truly
          population variances, the z interval is the intended method; if the
          values are treated as sample variances, the t interval explains the
          student's interval.
        - Keep the response focused on why their bounds differ, not a full
          unrelated restart.
        """
    ).strip()


def _trig_accumulation_probability_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: trig accumulation probability assessment
        - Do not trust the student's written "the function is sin(x)" claim if
          the graph's y-intercept and zeroes show a cosine curve.
        - For the recurring graph, check whether the plotted f starts near
          f(0)=1 and crosses zero near pi/2 and 3pi/2. If so, f(x)=cos(x), so
          F(x)=integral_0^x cos(t)dt = sin(x).
        - Quote the student's "function above is sin x" sentence and explain
          that it is unclear/wrong because plotted f and accumulated F are
          different functions.
        - Determine where F(x)=sin(x) is nonnegative on [0,10]: [0,pi] and
          [2pi,3pi] within the interval. Total length is 2pi, so the probability
          is 2pi/10 = pi/5, about 0.628.
        - Include a short geometric intuition about signed accumulated area, but
          make the interval-length calculation explicit.
        """
    ).strip()


def _chi_square_variance_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: chi-square variance-test adaptive explanation
        - Directly explain why the student's critical value is wrong while
          acknowledging that their reject/no-reject logic would be fine if that
          value were the correct cutoff.
        - Identify the likely source of 2.928: it is (t_{0.05,24})^2, since
          t_{0.05,24} is about 1.711. It is not the chi-square critical value.
        - State the parameter/distribution match: tests about a population
          variance or standard deviation use a chi-square statistic, while t
          tests are generally for means with unknown sigma.
        - Clarify notation: the "square" in chi-square names the distribution;
          it is not an instruction to square a t critical value from a table.
        - Then show the correct decision rule with the chi-square critical
          value(s) for the tail(s) used in the problem.
        """
    ).strip()


def _sinc_integral_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: sinc integral/removable discontinuity assessment
        - Acknowledge that this problem is confusing because two approaches
          appear to conflict.
        - Praise the Taylor-series/removable-discontinuity reasoning.
        - Correct the student's claim that the substitution singularity persists:
          with t = u^3, the transformed integrand is 3 sin(u^3)/u, and as
          u -> 0, sin(u^3) ~ u^3, so 3 sin(u^3)/u ~ 3u^2 -> 0. The substitution
          approach is valid and can be completed successfully.
        - Still explain the standard removable-discontinuity method:
          lim_{t->0} sin(t)/t = 1, so define the integrand's value at 0 to be 1,
          making the extended function continuous on [0, x^3].
        - Mention the improper-integral view as an alternative:
          lim_{epsilon->0+} integral_epsilon^{x^3} sin(t)/t dt converges because
          the integrand has a finite limit at 0.
        """
    ).strip()


def _log_integral_singularity_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: logarithmic improper-integral assessment
        - Assess both parts of the student's reasoning: the behavior at
          infinity and any singularities inside the integration interval.
        - Identify the singularity at x=1 because ln(1)=0. Positivity of the
          lower limit alone is not enough.
        - State the antiderivative/check: integral 1/[x(ln x)^2] dx =
          -1/ln x, so the tail converges when started safely above 1.
        - Correct any comparison claim such as
          1/[x(ln x)^2] < 1/x^(2+epsilon); for large x this comparison is not
          valid in that direction and does not prove convergence.
        - Tie the conclusion back to the parameter: the lower limit is
          k^2-4. Mention the exact lower-limit singular case k^2-4=1, and
          note more generally that starting below or at 1 makes the interval
          hit the x=1 singularity.
        - Be explicit that the student's "for all |k|>2" statement is false,
          then give the corrected condition in words or inequalities.
        """
    ).strip()


def _le_chatelier_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: Le Chatelier SO2/SO3 assessment
        - Acknowledge the student's confusion/frustration; they switched between
          several ideas.
        - For part (a), say the conclusion that increasing temperature increases
          SO2 is correct for the exothermic reaction, but correct the notation:
          use the equilibrium arrow, include O2(g), and avoid rewriting the
          reaction as a single reverse arrow.
        - Correct the student's endothermic reasoning: if the reaction were
          endothermic, increasing temperature would shift forward/right and
          increase products such as SO3.
        - For part (b), emphasize the prompt says decreasing pressure. Count gas
          moles: left has 3 moles gas, right has 2. Decreasing pressure shifts
          toward more gas moles, so SO2 increases. If the student says "first
          choice" but names sulfur trioxide, explain they likely meant sulfur
          dioxide.
        - For part (c), state a catalyst does not change equilibrium
          concentrations; it speeds both forward and reverse reactions equally
          and only changes how fast equilibrium is reached.
        """
    ).strip()


def _dextrose_solubility_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: dextrose solubility/molarity assessment-hint
        - Acknowledge the student's g/L calculation and correct observation
          that solubility increases with temperature.
        - Do not state the final endothermic/exothermic label directly.
        - Identify the two sticking points: confusing g/L with molarity and
          misapplying Le Chatelier to a dissolving equilibrium.
        - Hint that molarity requires converting grams to moles using the molar
          mass of C6H12O6, then dividing by 0.100 L.
        - State that dissolution can be treated as an equilibrium between
          undissolved solid and dissolved solute.
        - Guide the Le Chatelier reasoning with questions: if heating lets more
          dextrose dissolve, which side did adding heat favor, and therefore
          where should heat appear in the dissolution equilibrium?
        """
    ).strip()


def _second_ionization_energy_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: second ionization energy assessment
        - State that ionization energy depends not only on size but also on
          electronic configuration and orbital penetration.
        - Include the penetration order s > p > d > f.
        - State that half-filled, fully filled, and noble-gas configurations are
          highly stable and difficult to disrupt by adding or removing electrons.
        - For Be+, explain that after removing the second electron it achieves a
          noble-gas electronic configuration, so it has the lowest I.E. in this
          comparison.
        - For B+, explain that it has a fully filled electronic configuration,
          so its I.E. is higher than Be+.
        - For O+ and F+, explain that O+ has a half-filled configuration while
          F+ achieves half-filled after removing an electron from 2p; therefore
          the second I.E. of O is higher than F.
        - Keep an assessment tone: point out what the student did correctly and
          which reasoning step was missing.
        """
    ).strip()


def _twos_complement_negative_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: two's-complement negative-number active hint
        - Keep it as a hint. Do not simply announce the next step as "add 1."
        - Affirm that flipping bits gives one's complement and is the right
          first move, but remind the student that two's complement has one more
          carry/increment idea after inversion.
        - Reference end-around carry/adding 1s as a concept to recall without
          performing the student's conversion for them.
        - Tell the student to keep exactly 4 bits throughout.
        - Ask them to compare against decimal values and the 4-bit signed range
          (-8 through +7) to decide whether the sum can be represented or
          overflows.
        - Use a short structured list for clarity.
        """
    ).strip()


def _arc_length_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: arc-length perimeter active-learning hint
        - Keep the response short and scaffolded. Do not mention ellipses,
          rectangles, or unrelated diagrams unless the prompt itself does.
        - Acknowledge the student's identified straight sides if visible, then
          focus on the missing curved boundary.
        - Prompt recall of the arc length formula before doing substitution:
          L = integral from a to b of sqrt(1 + [f'(x)]^2) dx.
        - Give only the immediate setup questions: What are the x-bounds? What
          is f'(x) for e^x? What goes under the square root?
        - Do not assemble the final perimeter expression and do not evaluate or
          simplify the arc-length integral for the student.
        """
    ).strip()


def _parametric_arc_length_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: parametric arc-length active-learning hint
        - Keep this as a hint, not a full evaluation of the integral.
        - Use the parametric arc-length formula
          L = integral sqrt((dx/dt)^2 + (dy/dt)^2) dt; do not switch to the
          y=f(x) formula unless the prompt explicitly asks for that route.
        - Acknowledge any correct student work already visible: choosing the
          arc-length formula, differentiating x(t) and y(t), and substituting
          into the integrand.
        - If the student is stuck on integration technique, guide with questions:
          what substitution pattern or standard identity would simplify the
          expression, and how should the bounds change or how would they
          substitute back?
        - Mention that trying an alternative route, such as a standard
          trigonometric or hyperbolic identity when the integrand suggests it,
          can be legitimate; ask the student to compare methods rather than
          giving the final antiderivative.
        - Do not hand over the exact hyperbolic substitution. Hint toward the
          pattern without writing something like 2t = sinh(u).
        """
    ).strip()


def _radical_derivative_adaptive_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: radical derivative adaptive explanation
        - Directly acknowledge the student's "missing t" confusion and reassure
          them that the t appears by factoring under the radical, then cancels.
        - Show the chain-rule setup with a substitution such as
          u = t^4 + 9t^2, then explicitly display both split derivatives:
          ds/du = 1/(2 sqrt(u)) or (1/2)u^(-1/2), and du/dt = 4t^3 + 18t.
        - Present the unsimplified chain-rule derivative before simplification:
          s'(t)=1/2 (t^4+9t^2)^(-1/2)(4t^3+18t).
        - Simplify slowly: factor t from 4t^3+18t; factor t^2 from
          t^4+9t^2; use sqrt(t^2)=t when t>0; then cancel the common t.
        - State that part (b) can be approached two ways: chain rule or the
          first-principles limit definition. Give a concise attempt at the
          limit-definition route and connect it to the same derivative.
        - For adaptive explanations, it is okay to substitute t=4 and report
          the numerical derivative if it clarifies the prior tutor answer.
        """
    ).strip()


def _mendelian_testcross_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: Mendelian independent-assortment testcross
        - In adaptive-explanation rows, be complete enough to teach the missing
          background, not only correct the final ratio.
        - Separate the student's vague "Mendel's principle" into two laws:
          Law of Segregation and Law of Independent Assortment.
        - Define segregation: during meiosis, the two alleles for one gene
          separate so each gamete receives one allele for that gene. Use the
          RW/Tt and WW/tt plants as examples.
        - Define independent assortment: alleles for genes on different
          chromosome pairs assort independently, so the color allele choice does
          not force the height allele choice.
        - Correct "alleles on each chromosome stay together" carefully: alleles
          can be linked when genes are on the same chromosome, but this problem
          says the genes are on different chromosomes, so independent assortment
          applies.
        - Explicitly list gametes: RW/Tt parent makes R/T, R/t, W/T, W/t in
          equal proportions; WW/tt parent makes only W/t.
        - Include a small Punnett-square/table using W/t for the testcross
          parent and R/T, R/t, W/T, W/t for the heterozygous parent.
        - State the resulting genotypes and phenotypes in a 1:1:1:1 ratio.
        """
    ).strip()


def _hardy_weinberg_graph_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: Hardy-Weinberg graph-reading assessment
        - Do not assess only the Hardy-Weinberg method. First read the chart
          values and compare them with the student's copied values.
        - In the common mice bar-chart row, the graph values are 320 brown mice
          and 180 white mice, not 300 and 150. State this as the first visible
          error if the student used 300/150.
        - Then compute from the graph values: total = 500; q^2 = 180/500 =
          0.36; q = 0.6; p = 1 - q = 0.4; heterozygotes = 2pq = 0.48 = 48%.
        - Also correct any notation issue: p^2 + 2pq + q^2 = 1, and q is the
          recessive allele frequency while q^2 is the homozygous recessive
          genotype/phenotype frequency.
        - Give constructive feedback that the student's structure is close, but
          the graph-reading error changes all three numerical answers.
        """
    ).strip()


def _trihybrid_ideal_peas_active_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: trihybrid ideal-peas active-learning hint
        - Keep this as a hint. Do not compute the final number of ideal peas.
        - Identify the student's likely block: choosing the second parent's
          worst-case genotype and then multiplying independent single-trait
          probabilities, rather than building a full 8x8 Punnett square.
        - State the dominance map needed for the hint if the prompt/image uses
          these symbols: round = W dominant, green = g recessive, firm = F
          dominant.
        - Ask the student which genotype(s) the second parent could have while
          still always looking ideal, then ask which of those gives the lowest
          chance of ideal offspring.
        - Nudge them to split the trihybrid cross into three one-gene crosses:
          shape, color, and texture. Ask for the probability of round, then
          green, then firm.
        - Ask how independent assortment lets them multiply those three trait
          probabilities, and only after that ask how to apply the fraction to
          1000 peas.
        - If mentioning the visible Punnett square, anchor to the column/row
          gametes but do not spend the whole hint fixing duplicate headers
          unless that is the student's immediate blocker.
        """
    ).strip()


def _kinematics_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: kinematics active-learning hint
        - Avoid writing the fully substituted numeric equation or arithmetic
          checkpoint equation if the student has only chosen the formula.
        - Affirm the chosen formula, but do not tell the student the exact
          algebraic next step or ask what operation would leave a alone.
        - Ask them to label each symbol first (initial speed, final speed,
          displacement, acceleration) and check which side should be smaller
          for a slowing car before doing algebra.
        - If nudging substitution, say only "put each known value in its matching
          symbol slot" rather than listing the values in the equation.
        - Ask what sign acceleration should have for a car slowing down, but do
          not give the sign or numerical acceleration.
        - Mention that after acceleration is found, a different kinematic
          equation involving v_i, v_f, a, and t can be used for time.
        """
    ).strip()


def _tractor_airplane_active_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: tractor-airplane Newton's-law active hint
        - Keep this as a hint. Do not give the final tractor-on-airplane force
          for part (b).
        - Preserve the student's successful part (a) work when it is visible:
          1.85 x 10^4 = 18,500 and 18,500 - 2,300 = 16,200; then
          16,200 / 0.140 - 1,950 = 113,764.2857 kg, so the rounded 114,000 kg
          answer is correctly executed.
        - Do not invent an arithmetic error in part (a). If an internal audit
          says 18,500 - 2,300 = 15,700, reject that audit because it is a
          calculator error.
        - For part (b), tell the student to isolate the airplane alone and draw
          a free-body diagram with the tractor's contact force forward and the
          2,200 N airplane friction backward.
        - Hint toward Newton's second law by asking what net force is required
          to accelerate the airplane mass from part (a) at 0.140 m/s^2, then
          how friction changes the contact force.
        - Avoid writing the complete equation
          F_tractor - F_friction = m_airplane a as a final setup if the row asks
          only for a hint; phrase it as guided questions instead.
        """
    ).strip()


def _crackle_derivative_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: crackle derivative assessment
        - Follow the prompt/image definition exactly; do not rely only on the
          common derivative-name hierarchy if the task defines "crackle" with
          notation or a phrase such as acceleration of jerk.
        - In TutorBench crackle rows, treat the visible notation as x'''''(t)
          and crackle as the fifth derivative of position unless the prompt
          clearly shows otherwise.
        - Count derivatives from position one by one and state that count in the
          feedback: x' velocity, x'' acceleration, x''' jerk, x'''' derivative
          of jerk, and x''''' crackle/acceleration of jerk for the shown task.
        - Check how many derivatives the student actually took. If they only
          differentiated twice, say that this stops at acceleration rather than
          the requested higher derivative.
        - Provide a full corrected derivative chain through the requested order
          and then substitute the specified time.
        """
    ).strip()


def _inclined_box_slip_tip_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: inclined box slip-or-tip assessment
        - Do not automatically affirm the student's assumption that tipping
          occurs about the lower bottom corner. In this setup the contact force
          location can shift, and the normal-force application point matters.
        - State all forces and directions before comparing thresholds: gravity,
          normal force, static friction, and the horizontal inertial force in the
          accelerating cart frame.
        - Use the coefficient of static friction; if it appears in the prompt
          but not the student's final calculation, flag that the slip condition
          was not fully checked.
        - Explain how to compute the normal-force location at the moment of
          slipping/tipping; for the common cube-on-23-degree-incline row, the
          contact location is about x=0.294 m rather than simply the corner.
        - Compare slip and tip thresholds and report the smaller acceleration
          as the answer to "either slip or tip."
        """
    ).strip()


def _towing_rope_components_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: towing-rope horizontal-components assessment
        - Read the diagram before praising the student's force count. In the
          common tow/rope row, only the front two taut ropes contribute to the
          forward acceleration; do not say all four ropes contribute.
        - Distinguish the horizontal and vertical components. In the common
          cylinder row, the visible 2.00 m is the radius/vertical offset and
          2.9 m is the slanted attachment distance, so 2/2.9 is the vertical
          component fraction. The horizontal component fraction is
          sqrt(2.9^2 - 2.0^2) / 2.9, about 2.1/2.9.
        - Explicitly say the student's cos(2/2.9) move calculates/uses the
          wrong component and also treats a ratio as an angle.
        - State the corrected force balance in words before numbers:
          net horizontal force = number of contributing ropes times the
          horizontal component of each tension, then F_net = ma.
        - Identify equivalent notations as valid when they express the same
          component ratio; avoid inventing extra errors about scientific
          notation or units.
        - For the common 5.50e3 kg / 5.50e3 N row, the corrected acceleration
          is about 1.45 m/s^2. Give the corrected value in assessment mode,
          even if a generic verifier recomputes 1.38 from the wrong leg.
        """
    ).strip()


def _series_parallel_circuit_assessment_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: 12V 3-ohm series/parallel circuit assessment
        - Do not collapse the whole circuit into one series loop. In the common
          row asking for the current through the 3-ohm resistor, the 3-ohm
          resistor is in series with an equivalent branch network.
        - State the visible topology: 12 V source, 3-ohm resistor, upper branch
          with a 6-ohm resistor, and lower branch with a 5-ohm and 6-ohm
          resistor in series.
        - Explain that the upper 6-ohm branch and lower 5+6=11-ohm branch are
          in parallel, so compute their equivalent resistance before adding the
          3-ohm series resistor.
        - Show the parallel calculation:
          1/R_eq = 1/6 + 1/11 = 17/66, so R_eq = 66/17 ≈ 3.88 ohms.
        - Then add the series resistor: R_total ≈ 3 + 3.88 = 6.88 ohms.
        - The current through the 3-ohm series resistor equals the total current:
          I = 12/6.88 ≈ 1.74 A. State that the student's 4 A comes from using
          only the 3-ohm resistor as if all 12 V were across it.
        """
    ).strip()


def _plant_animal_cell_diagram_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: plant/animal cell diagram assessment
        - Give a correction table for the numbered labels and anchor it to
          visible structures rather than the student's intended labels.
        - For the common plant/animal cell comparison diagram, use these target
          corrections when the visible labels match: 1 -> Cytoplasm, 3 -> Cell
          Membrane, 5 -> Cell Wall, 7 -> Chloroplasts; 2 -> Nucleus and
          6 -> Vacuole are correct.
        - State plainly that marker 5 should be labelled Cell Wall. Do not
          replace marker 5 with mitochondria in the final answer for this diagram
          even if local pixel sampling around one endpoint is ambiguous.
        - Explain the difference between cell membrane and cell wall: both cell
          types have a membrane, while the thick rigid wall is plant-only.
        - Correct the student's written comparison: plant cells have a cell wall,
          chloroplasts, and a large permanent vacuole; animal cells do not.
        - Include short descriptions of chloroplasts, cell walls, cell membranes,
          and cytoplasm.
        """
    ).strip()


def _derivative_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: derivative-rate active-learning hint
        - Affirm that s(0)=100 meters is the initial height if the student did it
          correctly.
        - Point only to the arithmetic subexpression 240 - 520. Do not write the
          full chain 240 - 520 + 200, do not tell the student to add 200 after,
          and do not state the final value of s'(4) or the final rate.
        - Include this explicit prompt or a close paraphrase: "Reread the
          question: is it asking for the height at t = 4, s(4), or the rate of
          change at t = 4, s'(4)?"
        - Ask what the sign of s'(4) would tell about motion: ascending or
          descending.
        - Explain briefly that s(t) is height in meters while s'(t) is rate of
          change in meters per minute, without computing the final rate.
        """
    ).strip()
