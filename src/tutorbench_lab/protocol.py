"""Prompt protocol for the three TutorBench use cases."""

from __future__ import annotations

from textwrap import dedent

from tutorbench_lab.constants import PROMPT_VERSION
from tutorbench_lab.schemas import TutorBenchExample, TutorTurnInput, UseCase

PAPER_SYSTEM_PROMPTS: dict[UseCase, str] = {
    UseCase.ADAPTIVE: dedent(
        """\
        You are an AI tutor. The student has already seen an initial explanation
        and is now asking a follow-up question. Explain the specific point of
        confusion directly, accurately, and at the student's level. Be warm,
        concise, and complete enough that the student can move forward.
        """
    ).strip(),
    UseCase.ASSESSMENT: dedent(
        """\
        You are an AI tutor assessing a student's work. Identify what the
        student did correctly, identify any mistakes or misconceptions, classify
        the nature of the errors when useful, and give actionable feedback that
        helps the student repair their reasoning.
        """
    ).strip(),
    UseCase.ACTIVE_LEARNING: dedent(
        """\
        You are an AI tutor helping a student who got stuck part way through a
        problem. Offer a helpful hint or guiding question toward the next step
        without giving away the full answer.
        """
    ).strip(),
}


def build_turn_input(
    example: TutorBenchExample, *, prompt_version: str = PROMPT_VERSION
) -> TutorTurnInput:
    """Assemble a provider-neutral prompt for one TutorBench example."""

    if example.use_case == UseCase.ADAPTIVE:
        user_prompt = _adaptive_prompt(example)
    elif example.use_case == UseCase.ASSESSMENT:
        user_prompt = _assessment_prompt(example)
    else:
        user_prompt = _active_learning_prompt(example)

    if example.image.present:
        user_prompt = (
            "The example includes an image of the problem or student work. "
            "Use the image as primary evidence where relevant.\n\n"
            f"{user_prompt}"
        )

    return TutorTurnInput(
        task_id=example.task_id,
        use_case=example.use_case,
        modality=example.modality,
        subject=example.subject,
        system_prompt=PAPER_SYSTEM_PROMPTS[example.use_case],
        user_prompt=user_prompt,
        image=example.image,
        prompt_version=prompt_version,
    )


def _adaptive_prompt(example: TutorBenchExample) -> str:
    return dedent(
        f"""\
        Subject: {example.subject}

        Initial student question or task:
        {example.prompt}

        Initial tutor explanation the student has already seen:
        {example.uc1_initial_explanation}

        Student follow-up:
        {example.follow_up_prompt}

        Write the next tutor response. Address the student's exact confusion
        without restarting the entire solution unless doing so is necessary.
        """
    ).strip()


def _assessment_prompt(example: TutorBenchExample) -> str:
    student_work = example.follow_up_prompt.strip()
    if not student_work:
        student_work = "The student's work is shown in the image."

    return dedent(
        f"""\
        Subject: {example.subject}

        Problem or instruction:
        {example.prompt}

        Student work or proposed answer:
        {student_work}

        Assess the student's work. State what is correct, what is incorrect,
        and what the student should do next.
        """
    ).strip()


def _active_learning_prompt(example: TutorBenchExample) -> str:
    partial_work = example.follow_up_prompt.strip()
    if not partial_work:
        partial_work = "The student's partial work is shown in the image."

    return dedent(
        f"""\
        Subject: {example.subject}

        Problem:
        {example.prompt}

        Student's current partial work:
        {partial_work}

        Give a targeted hint or guiding question for the next step. Preserve
        student agency and avoid revealing the final answer.
        """
    ).strip()
