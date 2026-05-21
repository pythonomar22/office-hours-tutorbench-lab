"""Candidate tutor strategies."""

from __future__ import annotations

from textwrap import dedent
from uuid import uuid4

from tutorbench_lab.constants import (
    AGENT_PROMPT_VERSION,
    DATASET_REVISION,
    DEFAULT_CRITIC_MODEL,
    DEFAULT_SOLVER_MODEL,
)
from tutorbench_lab.protocol import build_turn_input
from tutorbench_lab.providers import make_client, response_from_result
from tutorbench_lab.schemas import (
    RunRecord,
    Strategy,
    TutorBenchExample,
    TutorResponse,
    TutorTurnInput,
    UseCase,
)


def dry_run_response(example: TutorBenchExample) -> TutorResponse:
    """Deterministic no-API response for smoke tests and plumbing checks."""

    if example.use_case == UseCase.ACTIVE_LEARNING:
        text = (
            "You are on the right track. Look closely at the next step and ask "
            "what relationship or definition should connect the quantities."
        )
    elif example.use_case == UseCase.ASSESSMENT:
        text = (
            "The work needs a careful check. Identify the step that uses the main "
            "formula, verify each substitution, and then correct the first mismatch."
        )
    else:
        text = (
            "Your confusion makes sense. The key is to separate the general idea "
            "from this problem's specific condition, then revisit the step that "
            "caused the mismatch."
        )
    return TutorResponse(
        task_id=example.task_id,
        text=text,
        model="dry-run",
        strategy=Strategy.DRY_RUN,
        prompt_version="dry-run-v1",
        latency_ms=0,
        trace={"note": "No API call was made."},
    )


def run_baseline(
    example: TutorBenchExample,
    *,
    model: str,
    max_tokens: int = 1200,
) -> tuple[TutorTurnInput, TutorResponse]:
    """Run a single-model baseline against the paper-style prompt."""

    turn = build_turn_input(example)
    client = make_client(model)
    result = client.generate(turn, max_tokens=max_tokens)
    response = response_from_result(
        task_id=example.task_id,
        model=model,
        strategy=Strategy.BASELINE,
        prompt_version=turn.prompt_version,
        result=result,
    )
    return turn, response


def run_agentic(
    example: TutorBenchExample,
    *,
    composer_model: str,
    solver_model: str = DEFAULT_SOLVER_MODEL,
    critic_model: str = DEFAULT_CRITIC_MODEL,
    max_tokens: int = 1600,
) -> tuple[TutorTurnInput, TutorResponse]:
    """Run the v1 rubric-blind agentic tutor pipeline.

    The pipeline intentionally never sees sample-specific rubrics. It uses
    generic TutorBench-derived tutoring skills, then asks a rubric-blind critic
    whether the draft is complete, calibrated, and safe.
    """

    base_turn = build_turn_input(example, prompt_version=AGENT_PROMPT_VERSION)
    solver_client = make_client(solver_model)
    composer_client = make_client(composer_model)
    critic_client = make_client(critic_model)

    perception_result = None
    if base_turn.image.present:
        perception_turn = _perception_turn(base_turn)
        perception_result = solver_client.generate(perception_turn, max_tokens=900)

    solver_turn = _solver_turn(
        base_turn,
        perception_transcript=perception_result.text if perception_result else None,
    )
    solver_result = solver_client.generate(solver_turn, max_tokens=max_tokens)

    composer_turn = _composer_turn(
        base_turn,
        solver_result.text,
        perception_transcript=perception_result.text if perception_result else None,
    )
    composer_result = composer_client.generate(composer_turn, max_tokens=max_tokens)

    critic_turn = _critic_turn(
        base_turn,
        solver_result.text,
        composer_result.text,
        perception_transcript=perception_result.text if perception_result else None,
    )
    critic_result = critic_client.generate(critic_turn, max_tokens=900)

    final_text = composer_result.text
    if _critic_requests_revision(critic_result.text):
        revision_turn = _revision_turn(
            base_turn,
            solver_result.text,
            composer_result.text,
            critic_result.text,
            perception_transcript=perception_result.text if perception_result else None,
        )
        revision_result = composer_client.generate(revision_turn, max_tokens=max_tokens)
        final_text = revision_result.text
        revision_trace = {
            "text": revision_result.text,
            "latency_ms": revision_result.latency_ms,
            "usage": revision_result.usage.model_dump(mode="json"),
        }
    else:
        revision_trace = None

    total_latency = sum(
        item
        for item in [
            solver_result.latency_ms,
            composer_result.latency_ms,
            critic_result.latency_ms,
            perception_result.latency_ms if perception_result else 0,
            revision_trace["latency_ms"] if revision_trace else 0,
        ]
        if item is not None
    )

    response = TutorResponse(
        task_id=example.task_id,
        text=final_text.strip(),
        model=composer_model,
        strategy=Strategy.AGENTIC,
        prompt_version=base_turn.prompt_version,
        latency_ms=total_latency,
        usage=composer_result.usage,
        trace={
            "solver_model": solver_model,
            "critic_model": critic_model,
            "perception_transcript": perception_result.text if perception_result else None,
            "solver_analysis": solver_result.text,
            "draft": composer_result.text,
            "critic": critic_result.text,
            "revision": revision_trace,
        },
    )
    return base_turn, response


def record_for_response(
    *,
    example: TutorBenchExample,
    turn: TutorTurnInput,
    response: TutorResponse,
    run_id: str | None = None,
) -> RunRecord:
    return RunRecord(
        run_id=run_id or str(uuid4()),
        dataset_revision=DATASET_REVISION,
        example=example,
        turn_input=turn,
        response=response,
    )


def _perception_turn(base_turn: TutorTurnInput) -> TutorTurnInput:
    return base_turn.model_copy(
        update={
            "system_prompt": dedent(
                """\
                You are the visual perception module for an AI tutor. Your only
                job is to transcribe and describe the image accurately. Do not
                solve the problem yet and do not infer beyond the visible image.

                Capture: printed problem text, diagrams, axes, labels, numbered
                labels, answer choices, handwritten student work, code lines,
                units, signs, and any written student claim. If something is
                ambiguous, say it is ambiguous instead of guessing.

                For numbered diagrams, do not trust the student's label list by
                itself. Inspect where each arrow or number points in the image.
                Return a table with: number, student's written label if visible,
                actual structure indicated by the arrow/marker, and whether
                they match. For code images, quote exact line numbers and exact
                code text when visible.
                """
            ).strip(),
            "user_prompt": (
                base_turn.user_prompt
                + "\n\nReturn a concise but complete visual transcript."
            ),
        }
    )


def _solver_turn(
    base_turn: TutorTurnInput, *, perception_transcript: str | None = None
) -> TutorTurnInput:
    use_case_note = ""
    if base_turn.use_case == UseCase.ADAPTIVE:
        use_case_note = (
            "\n\nFor adaptive-explanation rows, treat the given initial explanation "
            "and follow-up as the conversation context to answer. Do not pivot to "
            "a different problem or declare the prior explanation wrong unless the "
            "student's follow-up explicitly asks for that."
        )
    perception_block = (
        f"\n\nPerception transcript from the image:\n{perception_transcript}"
        if perception_transcript
        else ""
    )
    return base_turn.model_copy(
        update={
            "system_prompt": dedent(
                """\
                You are the private analysis module for an AI tutor. Diagnose the
                problem, the student's current state, likely misconceptions, and
                the mathematically/scientifically correct resolution. Be precise.
                This analysis is private and will not be shown to the student.
                Do not use or request sample-specific evaluation rubrics.

                For image rows, first transcribe every relevant visible label,
                equation, answer choice, diagram feature, and piece of student
                work before solving. If there is an apparent conflict between
                text and image, resolve it from the image evidence rather than
                guessing. Be especially careful with numbered labels, signs,
                units, code lines, and handwritten claims.

                Independently recompute every arithmetic, algebra, derivative,
                formula-substitution, and code-execution step. Do not mark a
                student's numerical value as correct unless you have verified it.
                If the student made an arithmetic error, identify the exact term
                or line where it happens.

                For programming tasks, inspect exact code lines, compile/runtime
                errors, edge cases, tests beyond the shown sample, and input
                validation. If you provide corrected code, include useful
                comments/docstrings when that would make the fix clearer.

                For adaptive-explanation rows, the conversation context is the
                task. If the student's follow-up is about the provided initial
                explanation, answer that follow-up directly. Do not switch to
                solving a different image-only problem, and do not announce that
                the image conflicts with the conversation unless the student
                explicitly asks about that conflict.
                """
            ).strip()
            + use_case_note,
            "user_prompt": (
                base_turn.user_prompt
                + perception_block
                + "\n\nReturn private analysis with: facts from prompt/image, "
                "transcribed image details when present, correct reasoning, "
                "likely student misconception, expected final/correct result when "
                "the task is assessment or explanation, and tutoring objective."
            ),
        }
    )


def _composer_turn(
    base_turn: TutorTurnInput,
    solver_analysis: str,
    *,
    perception_transcript: str | None = None,
) -> TutorTurnInput:
    mode = {
        UseCase.ADAPTIVE: "Answer the follow-up directly and repair the exact misconception.",
        UseCase.ASSESSMENT: (
            "Assess the work, name correct steps, name errors, "
            "and give actionable correction."
        ),
        UseCase.ACTIVE_LEARNING: (
            "Give a hint or guiding question without revealing the final answer."
        ),
    }[base_turn.use_case]
    return base_turn.model_copy(
        update={
            "system_prompt": dedent(
                f"""\
                You are an excellent STEM tutor. Use the private diagnosis to
                write the student-facing response. {mode}

                Optimize for: correctness, identifying the core difficulty,
                student-level calibration, emotional acknowledgement when the
                student is confused, concrete examples or analogies when helpful,
                clear structure, and concise relevance. Do not mention rubrics,
                benchmarks, or private analysis.

                Be explicit about general principles instead of only implying
                them: name relevant laws, definitions, theorems, design
                principles, or formulas; then connect them to the student's
                work. When there is an important trade-off, state it plainly.
                For OOP class-design questions, explicitly mention the
                single-responsibility principle when relevant. For acid/base
                questions, explicitly define conjugate base and state how bond
                strength and conjugate-base stability affect acid strength.

                Important: TutorBench evaluates the final response, not a future
                back-and-forth. Be complete in this one response while still
                respecting the use case. Anchor feedback to the student's own
                wording or visible work. Include formulas, numerical values,
                code snippets, definitions, trade-offs, examples, or analogies
                when they are needed to make the teaching point concrete.

                Use-case policy:
                - Adaptive explanation: directly answer the follow-up, name the
                  misconception, and give a compact example or analogy if it
                  would help. Do not discard the initial explanation context.
                  If an image seems to conflict with the provided conversation,
                  answer the student's follow-up in the provided conversation
                  rather than pivoting to a different task. Do not tell the
                  student you are changing problems unless they asked about the
                  mismatch.
                - Assessment: state what is correct, what is wrong, why it is
                  wrong, and the corrected result or next calculation.
                - Active learning: do not reveal the final answer, but give a
                  specific next step. It is allowed to provide an intermediate
                  formula, setup, or checkpoint value when that is the useful
                  hint and not the final answer. A pooled proportion, standard
                  error formula, or setup checkpoint is usually intermediate;
                  the requested acceleration, rate, height, area, or final test
                  decision is usually final. Avoid fully substituting all
                  numbers or saying "solve/isolate for X" when that would be
                  the direct next step to the final answer.

                Avoid vague anchors like "your second sentence" when the
                student's exact wording or visible label is available. Quote or
                closely paraphrase the specific mistaken phrase, line, label, or
                calculation before teaching from it.

                For code feedback, quote the exact faulty line, mention its line
                number when visible, provide corrected code, suggest at least two
                additional test cases, and discuss edge cases such as invalid or
                negative inputs when relevant. Include Javadoc/docstring-style
                parameter and return documentation when giving corrected code.
                Treat misspelled identifiers as compile-risk issues and tell the
                student to fix them, even if the current snippet appears
                internally consistent. For diagram-label feedback, give an
                explicit correction table: label number, student's label,
                correct label, and short reason.
                """
            ).strip(),
            "user_prompt": base_turn.user_prompt
            + (
                f"\n\nPerception transcript from the image:\n{perception_transcript}"
                if perception_transcript
                else ""
            )
            + "\n\nPrivate diagnosis:\n"
            + solver_analysis
            + "\n\nNow write the student-facing tutor response.",
        }
    )


def _critic_turn(
    base_turn: TutorTurnInput,
    solver_analysis: str,
    draft_response: str,
    *,
    perception_transcript: str | None = None,
) -> TutorTurnInput:
    perception_block = (
        f"\n\nPerception transcript:\n{perception_transcript}"
        if perception_transcript
        else ""
    )
    return base_turn.model_copy(
        update={
            "system_prompt": dedent(
                """\
                You are a rubric-blind QA critic for a STEM tutor. Check the
                draft for factual errors, missing acknowledgement of confusion,
                failure to identify the misconception, bad calibration,
                unnecessary verbosity, and spoiler risk for hinting tasks.
                Return either PASS or REVISE, followed by concise reasons.
                Do not use or request sample-specific rubrics.

                Be strict about one-shot completeness. Request revision if the
                draft omits a needed formula, corrected answer, concrete example,
                trade-off, direct quote/paraphrase of the student's mistaken
                wording, or visible image detail. Request revision if a
                multimodal draft appears to misread the image.

                Request revision if an adaptive response pivots away from the
                conversation instead of answering the student's follow-up. Request
                revision if a code assessment omits line numbers, corrected code,
                extra tests, or edge cases. Request revision if a diagram
                assessment does not include a numbered correction table. Request
                revision if a calculus/physics/statistics answer affirms a
                student's arithmetic without showing independent verification.
                Request revision if an active-learning response gives the
                requested final numerical answer, uses "solve for" on the target
                variable, or withholds useful intermediate formulas/checkpoints.
                """
            ).strip(),
            "user_prompt": dedent(
                f"""\
                Original task:
                {base_turn.user_prompt}
                {perception_block}

                Private diagnosis:
                {solver_analysis}

                Draft response:
                {draft_response}
                """
            ).strip(),
        }
    )


def _revision_turn(
    base_turn: TutorTurnInput,
    solver_analysis: str,
    draft_response: str,
    critic_feedback: str,
    *,
    perception_transcript: str | None = None,
) -> TutorTurnInput:
    perception_block = (
        f"\n\nPerception transcript:\n{perception_transcript}"
        if perception_transcript
        else ""
    )
    return base_turn.model_copy(
        update={
            "system_prompt": base_turn.system_prompt
            + "\n\nRevise the draft using the QA feedback. Keep the response student-facing.",
            "user_prompt": dedent(
                f"""\
                Original task:
                {base_turn.user_prompt}
                {perception_block}

                Private diagnosis:
                {solver_analysis}

                Draft:
                {draft_response}

                QA feedback:
                {critic_feedback}

                Write the revised final tutor response only.
                """
            ).strip(),
        }
    )


def _critic_requests_revision(text: str) -> bool:
    return text.strip().upper().startswith("REVISE")
