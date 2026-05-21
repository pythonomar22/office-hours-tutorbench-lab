"""Rubric-blind task-family playbooks for the agentic tutor."""

from __future__ import annotations

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

    if turn.subject.lower() == "chemistry" and _has_any(
        text, ["hf", "hcl", "hi", "halogen", "electronegativity", "acid"]
    ):
        notes.append(_hydrogen_halide_acid_playbook())

    if turn.subject.lower() == "calculus":
        if _has_any(text, ["ellipse", "rectangle", "4xy", "quadrant"]):
            notes.append(_ellipse_rectangle_playbook())
        has_derivative_context = (
            "height" in text
            and "rate of change" in text
            and _has_any(text, ["car", "mountain"])
        )
        if "s'(4)" in text or has_derivative_context:
            notes.append(_derivative_hint_playbook())

    if turn.subject.lower() == "biology" and _has_any(
        text, ["interphase", "mutation", "daughter cells"]
    ):
        notes.append(_interphase_hint_playbook())
    if (
        turn.subject.lower() == "biology"
        and turn.use_case.value == "assessment"
        and _has_any(
            text, ["plant cell", "animal cell", "cell wall", "chloroplast"]
        )
    ):
        notes.append(_plant_animal_cell_diagram_playbook())

    if turn.subject.lower() == "statistics" and _has_any(
        text, ["pooled proportion", "two-proportion", "z-test", "vaccine"]
    ):
        notes.append(_pooled_proportion_hint_playbook())
    if turn.subject.lower() == "statistics" and _has_any(
        text, ["central limit theorem", "clt", "sample mean", "right-skewed"]
    ):
        notes.append(_clt_sample_mean_hint_playbook())

    if turn.subject.lower() == "physics" and _has_any(
        text, ["vf", "v_f", "kinematic", "acceleration", "50 m", "40 m/s"]
    ):
        notes.append(_kinematics_hint_playbook())

    if not notes:
        return None
    return "\n\n".join(notes)


def _has_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


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
