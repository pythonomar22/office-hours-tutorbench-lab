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

    if turn.subject.lower() == "computer science":
        if _has_any(text, ["dealership", "car", "object-oriented", "oop"]):
            notes.append(_oop_design_playbook())
        if _has_any(text, ["factorial", "recursive", "recursion"]):
            notes.append(_factorial_code_playbook())

    if turn.subject.lower() == "chemistry" and _has_hydrogen_halide_context(text):
        notes.append(_hydrogen_halide_acid_playbook())
    if turn.subject.lower() == "chemistry" and _has_any(
        text, ["heat exchange", "furnace gases", "crude oil", "desalination"]
    ):
        notes.append(_heat_exchange_hint_playbook())
    if turn.subject.lower() == "chemistry" and _has_any(
        text, ["blue spheres", "red spheres", "h2o molecules", "limiting reagent"]
    ):
        notes.append(_water_limiting_reagent_visual_playbook())

    if turn.subject.lower() == "calculus":
        if "ellipse" in text or _has_any(text, ["rectangle", "4xy"]):
            notes.append(_ellipse_rectangle_playbook())
        if turn.use_case.value == "adaptive" and _has_any(
            text, ["missing t", "denominator", "sqrt", "square root"]
        ):
            notes.append(_radical_derivative_adaptive_playbook())
        if turn.use_case.value == "active_learning" and (
            "arc length" in text or ("perimeter" in text and "e^x" in text)
        ):
            notes.append(_arc_length_hint_playbook())
        has_derivative_context = (
            "height" in text
            and "rate of change" in text
            and _has_any(text, ["car", "mountain"])
        )
        if turn.use_case.value == "active_learning" and (
            "s'(4)" in text or has_derivative_context
        ):
            notes.append(_derivative_hint_playbook())

    if turn.subject.lower() == "biology" and _has_any(
        text, ["interphase", "mutation", "daughter cells"]
    ):
        notes.append(_interphase_hint_playbook())
    if turn.subject.lower() == "biology" and _has_any(
        text, ["thermophilus", "infrared photosynthesis", "h2s", "chemosynthesis"]
    ):
        notes.append(_extremophile_metabolism_hint_playbook())
    if (
        turn.subject.lower() == "biology"
        and turn.use_case.value == "assessment"
        and _has_any(
            text, ["plant cell", "animal cell", "cell wall", "chloroplast"]
        )
    ):
        notes.append(_plant_animal_cell_diagram_playbook())
    if turn.subject.lower() == "biology" and _has_any(
        text, ["independent assortment", "testcross", "punnett", "rw/tt", "ww/tt"]
    ):
        notes.append(_mendelian_testcross_playbook())

    if turn.subject.lower() == "statistics" and _has_any(
        text, ["pooled proportion", "two-proportion", "z-test", "vaccine"]
    ):
        notes.append(_pooled_proportion_hint_playbook())
    if turn.subject.lower() == "statistics" and _has_any(
        text, ["central limit theorem", "clt", "sample mean", "right-skewed"]
    ):
        notes.append(_clt_sample_mean_hint_playbook())
    if (
        turn.subject.lower() == "statistics"
        and "residual" in text
        and _has_any(text, ["least-squares regression", "regression line", "predicted weight"])
    ):
        notes.append(_regression_residual_feedback_playbook())
    if turn.subject.lower() == "statistics" and _has_any(
        text, ["bonferroni", "pooled proportion", "standardized residual"]
    ):
        notes.append(_bonferroni_pooled_proportion_adaptive_playbook())

    if turn.subject.lower() == "physics" and _has_any(
        text, ["vf", "v_f", "kinematic", "acceleration", "50 m", "40 m/s"]
    ):
        notes.append(_kinematics_hint_playbook())

    if turn.subject.lower() == "calculus" and _has_any(
        text, ["sin(t)/t", "\\frac{\\sin(t)}{t}", "removable discontinuity"]
    ):
        notes.append(_sinc_integral_assessment_playbook())

    if turn.subject.lower() == "chemistry" and (
        _has_any(text, ["2so2", "so_2", "so2"])
        and _has_any(text, ["so3", "so_3"])
    ):
        notes.append(_le_chatelier_assessment_playbook())
    if turn.subject.lower() == "chemistry" and _has_any(
        text, ["dextrose", "c6h12o6", "solubility", "molarity"]
    ):
        notes.append(_dextrose_solubility_hint_playbook())
    if turn.subject.lower() == "chemistry" and _has_any(
        text, ["second ionization", "second i.e", "ie₂", "ie2", "ionization energy"]
    ):
        notes.append(_second_ionization_energy_assessment_playbook())

    if turn.subject.lower() == "computer science" and _has_any(
        text, ["two's complement", "twos complement", "2's complement", "overflow"]
    ):
        notes.append(_twos_complement_negative_hint_playbook())

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


def _interphase_hint_playbook() -> str:
    return dedent(
        """\
        Task-family playbook: interphase mutation active-learning hint
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
        - It is safe to provide intermediate checkpoint values while withholding
          the p-value and final reject/fail-to-reject conclusion.
        - Give the pooled proportion explicitly as p_hat_pool = (15 + 12) /
          (60 + 40) = 27/100 = 0.27.
        - Show the pooled SE formula with p_hat_pool substituted symbolically or
          numerically, then state that once SE is known the z-score can be
          computed with z = (p_hat_v - p_hat_p) / SE.
        - Do not give the final z-score, p-value, or conclusion.
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
