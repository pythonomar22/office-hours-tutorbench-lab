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

    solver_turn = _solver_turn(base_turn)
    solver_result = solver_client.generate(solver_turn, max_tokens=max_tokens)

    composer_turn = _composer_turn(base_turn, solver_result.text)
    composer_result = composer_client.generate(composer_turn, max_tokens=max_tokens)

    critic_turn = _critic_turn(base_turn, solver_result.text, composer_result.text)
    critic_result = critic_client.generate(critic_turn, max_tokens=900)

    final_text = composer_result.text
    if _critic_requests_revision(critic_result.text):
        revision_turn = _revision_turn(
            base_turn,
            solver_result.text,
            composer_result.text,
            critic_result.text,
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


def _solver_turn(base_turn: TutorTurnInput) -> TutorTurnInput:
    return base_turn.model_copy(
        update={
            "system_prompt": dedent(
                """\
                You are the private analysis module for an AI tutor. Diagnose the
                problem, the student's current state, likely misconceptions, and
                the mathematically/scientifically correct resolution. Be precise.
                This analysis is private and will not be shown to the student.
                Do not use or request sample-specific evaluation rubrics.
                """
            ).strip(),
            "user_prompt": (
                base_turn.user_prompt
                + "\n\nReturn private analysis with: facts from prompt/image, "
                "correct reasoning, likely student misconception, and tutoring objective."
            ),
        }
    )


def _composer_turn(base_turn: TutorTurnInput, solver_analysis: str) -> TutorTurnInput:
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
                """
            ).strip(),
            "user_prompt": base_turn.user_prompt
            + "\n\nPrivate diagnosis:\n"
            + solver_analysis
            + "\n\nNow write the student-facing tutor response.",
        }
    )


def _critic_turn(
    base_turn: TutorTurnInput, solver_analysis: str, draft_response: str
) -> TutorTurnInput:
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
                """
            ).strip(),
            "user_prompt": dedent(
                f"""\
                Original task:
                {base_turn.user_prompt}

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
) -> TutorTurnInput:
    return base_turn.model_copy(
        update={
            "system_prompt": base_turn.system_prompt
            + "\n\nRevise the draft using the QA feedback. Keep the response student-facing.",
            "user_prompt": dedent(
                f"""\
                Original task:
                {base_turn.user_prompt}

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
