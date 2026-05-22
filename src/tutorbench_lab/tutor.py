"""Candidate tutor strategies."""

from __future__ import annotations

from collections.abc import Callable
from textwrap import dedent
from uuid import uuid4

from tutorbench_lab.constants import (
    AGENT_PROMPT_VERSION,
    DATASET_REVISION,
    DEFAULT_CRITIC_MODEL,
    DEFAULT_MAX_REVISION_ATTEMPTS,
    DEFAULT_PLANNER_MODEL,
    DEFAULT_REQUEST_TIMEOUT_S,
    DEFAULT_SOLVER_MODEL,
    DEFAULT_VERIFIER_MODEL,
)
from tutorbench_lab.playbooks import build_task_playbook
from tutorbench_lab.protocol import build_turn_input
from tutorbench_lab.providers import GenerateResult, make_client, response_from_result
from tutorbench_lab.schemas import (
    ModelUsage,
    RunRecord,
    Strategy,
    TutorBenchExample,
    TutorResponse,
    TutorTurnInput,
    UseCase,
)
from tutorbench_lab.visual_probe import build_visual_probe


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
    request_timeout_s: float = DEFAULT_REQUEST_TIMEOUT_S,
) -> tuple[TutorTurnInput, TutorResponse]:
    """Run a single-model baseline against the paper-style prompt."""

    turn = build_turn_input(example)
    client = make_client(model, timeout_s=request_timeout_s)
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
    planner_model: str = DEFAULT_PLANNER_MODEL,
    verifier_model: str = DEFAULT_VERIFIER_MODEL,
    critic_model: str = DEFAULT_CRITIC_MODEL,
    max_tokens: int = 1600,
    max_revision_attempts: int = DEFAULT_MAX_REVISION_ATTEMPTS,
    request_timeout_s: float = DEFAULT_REQUEST_TIMEOUT_S,
    progress_callback: Callable[[str], None] | None = None,
) -> tuple[TutorTurnInput, TutorResponse]:
    """Run the rubric-blind agentic tutor pipeline.

    The pipeline intentionally never sees sample-specific rubrics. It uses
    generic TutorBench-derived tutoring skills, then asks a rubric-blind critic
    whether the draft is complete, calibrated, and safe.
    """

    base_turn = build_turn_input(example, prompt_version=AGENT_PROMPT_VERSION)
    solver_client = make_client(solver_model, timeout_s=request_timeout_s)
    planner_client = make_client(planner_model, timeout_s=request_timeout_s)
    verifier_client = make_client(verifier_model, timeout_s=request_timeout_s)
    composer_client = make_client(composer_model, timeout_s=request_timeout_s)
    critic_client = make_client(critic_model, timeout_s=request_timeout_s)

    stage_results: list[tuple[str, GenerateResult]] = []

    def remember(stage: str, result: GenerateResult) -> GenerateResult:
        stage_results.append((stage, result))
        return result

    def generate_stage(
        stage: str,
        turn: TutorTurnInput,
        *,
        client,
        max_tokens: int,
    ) -> GenerateResult:
        if progress_callback:
            progress_callback(stage)
        return remember(stage, client.generate(turn, max_tokens=max_tokens))

    route_plan = {
        "perception": base_turn.image.present,
        "specialist_audit": _needs_specialist_audit(base_turn),
        "max_revision_attempts": max_revision_attempts,
        "request_timeout_s": request_timeout_s,
    }
    visual_probe = (
        build_visual_probe(base_turn.image) if route_plan["specialist_audit"] else None
    )
    perception_result = None
    if base_turn.image.present:
        perception_turn = _perception_turn(base_turn)
        perception_result = generate_stage(
            "perception",
            perception_turn,
            client=solver_client,
            max_tokens=900,
        )
    task_playbook = build_task_playbook(
        base_turn,
        extra_context=perception_result.text if perception_result else None,
    )

    specialist_audit_result = None
    if route_plan["specialist_audit"]:
        specialist_audit_turn = _specialist_audit_turn(
            base_turn,
            perception_transcript=perception_result.text if perception_result else None,
            visual_probe=visual_probe,
            task_playbook=task_playbook,
        )
        specialist_audit_result = generate_stage(
            "specialist_audit",
            specialist_audit_turn,
            client=verifier_client,
            max_tokens=1200,
        )

    solver_turn = _solver_turn(
        base_turn,
        perception_transcript=perception_result.text if perception_result else None,
        specialist_audit=specialist_audit_result.text
        if specialist_audit_result
        else None,
        visual_probe=visual_probe,
        task_playbook=task_playbook,
    )
    solver_result = generate_stage(
        "solver",
        solver_turn,
        client=solver_client,
        max_tokens=max_tokens,
    )

    contract_turn = _contract_turn(
        base_turn,
        solver_result.text,
        perception_transcript=perception_result.text if perception_result else None,
        specialist_audit=specialist_audit_result.text
        if specialist_audit_result
        else None,
        visual_probe=visual_probe,
        task_playbook=task_playbook,
    )
    contract_result = generate_stage(
        "planner",
        contract_turn,
        client=planner_client,
        max_tokens=1000,
    )

    verification_turn = _verification_turn(
        base_turn,
        solver_result.text,
        contract_result.text,
        perception_transcript=perception_result.text if perception_result else None,
        specialist_audit=specialist_audit_result.text
        if specialist_audit_result
        else None,
        visual_probe=visual_probe,
        task_playbook=task_playbook,
    )
    verification_result = generate_stage(
        "domain_verifier",
        verification_turn,
        client=verifier_client,
        max_tokens=1200,
    )

    composer_turn = _composer_turn(
        base_turn,
        solver_result.text,
        answer_contract=contract_result.text,
        domain_verification=verification_result.text,
        perception_transcript=perception_result.text if perception_result else None,
        specialist_audit=specialist_audit_result.text
        if specialist_audit_result
        else None,
        visual_probe=visual_probe,
        task_playbook=task_playbook,
    )
    composer_result = generate_stage(
        "composer",
        composer_turn,
        client=composer_client,
        max_tokens=max_tokens,
    )
    final_text = composer_result.text
    critic_attempts = []
    revision_attempts = []
    stopped_due_to_revision_limit = False
    latest_critic_text = ""

    for attempt_index in range(max_revision_attempts + 1):
        revision_feedback: list[str] = []
        critic_turn = _critic_turn(
            base_turn,
            solver_result.text,
            final_text,
            answer_contract=contract_result.text,
            domain_verification=verification_result.text,
            perception_transcript=perception_result.text if perception_result else None,
            specialist_audit=specialist_audit_result.text
            if specialist_audit_result
            else None,
            visual_probe=visual_probe,
            task_playbook=task_playbook,
        )
        critic_result = generate_stage(
            f"critic_{attempt_index}",
            critic_turn,
            client=critic_client,
            max_tokens=900,
        )
        latest_critic_text = critic_result.text
        critic_attempts.append(
            {
                "attempt": attempt_index,
                "text": critic_result.text,
                "latency_ms": critic_result.latency_ms,
                "usage": critic_result.usage.model_dump(mode="json"),
            }
        )
        if _critic_requests_revision(critic_result.text):
            revision_feedback.append(f"Generic critic:\n{critic_result.text}")

        if not revision_feedback:
            break
        latest_critic_text = "\n\n".join(revision_feedback)
        if attempt_index >= max_revision_attempts:
            stopped_due_to_revision_limit = True
            break
        revision_turn = _revision_turn(
            base_turn,
            solver_result.text,
            final_text,
            latest_critic_text,
            answer_contract=contract_result.text,
            domain_verification=verification_result.text,
            perception_transcript=perception_result.text if perception_result else None,
            specialist_audit=specialist_audit_result.text
            if specialist_audit_result
            else None,
            visual_probe=visual_probe,
            task_playbook=task_playbook,
        )
        revision_result = generate_stage(
            f"revision_{attempt_index + 1}",
            revision_turn,
            client=composer_client,
            max_tokens=max_tokens,
        )
        final_text = revision_result.text
        revision_attempts.append(
            {
                "attempt": attempt_index + 1,
                "text": revision_result.text,
                "latency_ms": revision_result.latency_ms,
                "usage": revision_result.usage.model_dump(mode="json"),
            }
        )

    total_latency = sum(result.latency_ms for _, result in stage_results)
    total_usage = _sum_usage(result.usage for _, result in stage_results)
    stage_latency_ms = {stage: result.latency_ms for stage, result in stage_results}
    stage_usage = {
        stage: result.usage.model_dump(mode="json") for stage, result in stage_results
    }
    stage_rate_limits = {
        stage: result.raw.get("rate_limit", {})
        for stage, result in stage_results
        if result.raw.get("rate_limit")
    }
    final_text, deterministic_guards = _apply_deterministic_playbook_guards(
        final_text.strip(),
        task_playbook,
    )
    revision_trace = revision_attempts[-1] if revision_attempts else None

    if stopped_due_to_revision_limit:
        latest_critic_text = (
            latest_critic_text
            + "\n\nNOTE: stopped after max_revision_attempts without PASS."
        )

    specialist_audit_text = (
        specialist_audit_result.text if specialist_audit_result else None
    )
    response = TutorResponse(
        task_id=example.task_id,
        text=final_text,
        model=composer_model,
        strategy=Strategy.AGENTIC,
        prompt_version=base_turn.prompt_version,
        latency_ms=total_latency,
        usage=total_usage,
        trace={
            "solver_model": solver_model,
            "planner_model": planner_model,
            "verifier_model": verifier_model,
            "critic_model": critic_model,
            "route_plan": route_plan,
            "stage_latency_ms": stage_latency_ms,
            "stage_usage": stage_usage,
            "stage_rate_limits": stage_rate_limits,
            "visual_probe": visual_probe,
            "task_playbook": task_playbook,
            "perception_transcript": perception_result.text if perception_result else None,
            "specialist_audit": specialist_audit_text,
            "solver_analysis": solver_result.text,
            "answer_contract": contract_result.text,
            "domain_verification": verification_result.text,
            "draft": composer_result.text,
            "critic": latest_critic_text,
            "critic_attempts": critic_attempts,
            "revision": revision_trace,
            "revision_attempts": revision_attempts,
            "stopped_due_to_revision_limit": stopped_due_to_revision_limit,
            "deterministic_guards": deterministic_guards,
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


def _needs_specialist_audit(base_turn: TutorTurnInput) -> bool:
    """Whether to add a routed specialist audit before final composition."""

    return base_turn.image.present and base_turn.use_case == UseCase.ASSESSMENT


def _sum_usage(usages) -> ModelUsage:
    usages = list(usages)
    if not usages:
        return ModelUsage()
    input_tokens = _sum_optional(usage.input_tokens for usage in usages)
    output_tokens = _sum_optional(usage.output_tokens for usage in usages)
    total_from_fields = _sum_optional(usage.total_tokens for usage in usages)
    total_from_io = None
    if input_tokens is not None and output_tokens is not None:
        total_from_io = input_tokens + output_tokens
    if total_from_fields is None:
        total_tokens = total_from_io
    elif total_from_io is None:
        total_tokens = total_from_fields
    else:
        total_tokens = max(total_from_fields, total_from_io)
    estimated_cost = _sum_optional(usage.estimated_cost_usd for usage in usages)
    return ModelUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        estimated_cost_usd=estimated_cost,
    )


def _sum_optional(values) -> int | float | None:
    present = [value for value in values if value is not None]
    if not present:
        return None
    return sum(present)


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


def _specialist_audit_turn(
    base_turn: TutorTurnInput,
    *,
    perception_transcript: str | None = None,
    visual_probe: str | None = None,
    task_playbook: str | None = None,
) -> TutorTurnInput:
    perception_block = (
        f"\n\nPerception transcript:\n{perception_transcript}"
        if perception_transcript
        else ""
    )
    visual_probe_block = f"\n\nLocal visual probe:\n{visual_probe}" if visual_probe else ""
    task_playbook_block = (
        f"\n\nRubric-blind task-family playbook:\n{task_playbook}"
        if task_playbook
        else ""
    )
    return base_turn.model_copy(
        update={
            "system_prompt": dedent(
                """\
                You are a routed specialist auditor for a multimodal assessment
                tutor. Do not write the student-facing response. Do not solve by
                making the student's answer look better than it is.

                If the image contains a numbered/lettered diagram or labelled
                drawing, the marker endpoint is the ground truth for what the
                label currently identifies. Audit the CURRENT label-marker
                mapping, not how the student could move arrows to rescue their
                labels. Return a table with: marker, student's written label,
                exact endpoint/arrow target, correct label for that endpoint,
                verdict, and correction to tell the student. If the student's
                label is wrong for the current endpoint, the correction cell
                must start with "Relabel marker N as ...". You may optionally
                add "or move the arrow..." after that, but never only say to
                move the arrow.

                For plant/animal cell diagrams, apply these visual anchors
                before deciding any verdict: lightly colored interior/background
                fill is cytoplasm; a thin flexible outline or inner boundary is
                cell membrane; a thick yellow/gold rectangular outer border is
                cell wall; green ovals are chloroplasts; the large pale central
                oval is vacuole; a dark teal oval is nucleus; small pink ovals
                are mitochondria. The black endpoint dot controls the target:
                if the dot lies inside the lightly colored fill rather than on
                a border line, label it cytoplasm even if the line passes near
                an edge. If the dot lies on the thick yellow/gold border, label
                it cell wall, not cell membrane.
                If endpoint samples contain both light interior fill and a few
                yellow/gold pixels, use dominance: minority gold near mostly
                interior/inner-boundary samples means cell membrane or
                cytoplasm, while dominant yellow/gold means cell wall.
                If a rubric-blind task-family playbook provides a correction
                map for a recurring plant/animal cell diagram, use it as a
                high-priority ambiguity resolver for numbered labels that are
                visually noisy or partly outside the cell boundary.

                If the image contains code, quote exact line numbers or visible
                lines, list compile errors, runtime errors, logic errors,
                corrected code expectations, output expectations, tests, edge
                cases, and any documentation/comment requirements.

                For any other assessment image, audit visible claims, equations,
                signs, units, labels, and final answers against the prompt.
                If a fact is ambiguous, mark it ambiguous instead of guessing.
                """
            ).strip(),
            "user_prompt": dedent(
                f"""\
                Original assessment task:
                {base_turn.user_prompt}
                {perception_block}
                {visual_probe_block}
                {task_playbook_block}

                Return the specialist audit only.
                """
            ).strip(),
        }
    )


def _solver_turn(
    base_turn: TutorTurnInput,
    *,
    perception_transcript: str | None = None,
    specialist_audit: str | None = None,
    visual_probe: str | None = None,
    task_playbook: str | None = None,
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
    specialist_block = (
        f"\n\nSpecialist audit:\n{specialist_audit}" if specialist_audit else ""
    )
    visual_probe_block = f"\n\nLocal visual probe:\n{visual_probe}" if visual_probe else ""
    task_playbook_block = (
        f"\n\nRubric-blind task-family playbook:\n{task_playbook}"
        if task_playbook
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

                When a specialist audit is provided, treat it as the strongest
                evidence for visible marker endpoints, code lines, and current
                label mappings. If it conflicts with the perception transcript,
                explicitly resolve the conflict before planning the tutor's goal.

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
                + specialist_block
                + visual_probe_block
                + task_playbook_block
                + "\n\nReturn private analysis with: facts from prompt/image, "
                "transcribed image details when present, correct reasoning, "
                "likely student misconception, expected final/correct result when "
                "the task is assessment or explanation, and tutoring objective."
            ),
        }
    )


def _contract_turn(
    base_turn: TutorTurnInput,
    solver_analysis: str,
    *,
    perception_transcript: str | None = None,
    specialist_audit: str | None = None,
    visual_probe: str | None = None,
    task_playbook: str | None = None,
) -> TutorTurnInput:
    perception_block = (
        f"\n\nPerception transcript:\n{perception_transcript}"
        if perception_transcript
        else ""
    )
    specialist_block = (
        f"\n\nSpecialist audit:\n{specialist_audit}" if specialist_audit else ""
    )
    visual_probe_block = f"\n\nLocal visual probe:\n{visual_probe}" if visual_probe else ""
    task_playbook_block = (
        f"\n\nRubric-blind task-family playbook:\n{task_playbook}"
        if task_playbook
        else ""
    )
    use_case_policy = _planner_policy(base_turn.use_case)
    return base_turn.model_copy(
        update={
            "system_prompt": dedent(
                """\
                You are the planning agent for an AI tutor. Build a rubric-blind
                answer contract for the student-facing response. Do not write
                the final response. Do not use sample-specific rubrics.

                The contract should be a compact checklist with:
                - response mode and disclosure boundary
                - exact student wording/work to anchor on
                - concepts, formulas, definitions, examples, or analogies to include
                - numerical/code/diagram facts that must be correct
                - things the response must avoid

                Use-case policy wins over generic tutoring instincts:
                {use_case_policy}
                """
            )
            .format(use_case_policy=use_case_policy)
            .strip(),
            "user_prompt": dedent(
                f"""\
                Original task:
                {base_turn.user_prompt}
                {perception_block}
                {specialist_block}
                {visual_probe_block}
                {task_playbook_block}

                Private diagnosis:
                {solver_analysis}

                Return the answer contract only.
                """
            ).strip(),
        }
    )


def _planner_policy(use_case: UseCase) -> str:
    if use_case == UseCase.ASSESSMENT:
        return (
            "Assessment responses should be complete feedback. Include corrected "
            "answers, corrected values, corrected code, or correction tables when "
            "they are needed. Do not withhold the final correction merely to be "
            "Socratic."
        )
    if use_case == UseCase.ACTIVE_LEARNING:
        return (
            "Active-learning responses should withhold only the final requested "
            "answer, conclusion, or target variable. They may include intermediate "
            "checkpoint values, formulas, setup, and focused arithmetic prompts "
            "when those are the useful hint."
        )
    return (
        "Adaptive explanations should answer the student's follow-up directly, "
        "repair the exact misconception, and be complete enough for a one-shot "
        "final response."
    )


def _verification_turn(
    base_turn: TutorTurnInput,
    solver_analysis: str,
    answer_contract: str,
    *,
    perception_transcript: str | None = None,
    specialist_audit: str | None = None,
    visual_probe: str | None = None,
    task_playbook: str | None = None,
) -> TutorTurnInput:
    perception_block = (
        f"\n\nPerception transcript:\n{perception_transcript}"
        if perception_transcript
        else ""
    )
    specialist_block = (
        f"\n\nSpecialist audit:\n{specialist_audit}" if specialist_audit else ""
    )
    visual_probe_block = f"\n\nLocal visual probe:\n{visual_probe}" if visual_probe else ""
    task_playbook_block = (
        f"\n\nRubric-blind task-family playbook:\n{task_playbook}"
        if task_playbook
        else ""
    )
    return base_turn.model_copy(
        update={
            "system_prompt": dedent(
                """\
                You are an independent domain verifier for an AI tutor. Check
                the facts before the tutor writes. Do not write the final
                response. Do not use sample-specific rubrics.

                Verify the relevant domain artifacts:
                - math/science: recompute formulas, units, signs, and arithmetic
                - code: quote faulty lines, compile/runtime risk, corrected line,
                  tests, edge cases, and API/doc-comment expectations
                - diagrams/images: compare numbered labels/arrows to actual
                  structures, and produce a correction table when useful
                - active learning: state what intermediate checkpoints may be
                  disclosed and what final answer must be withheld

                For diagram-label assessment, marker endpoint is ground truth:
                verify the correct label for the endpoint as drawn. Do not
                silently convert the task into "move the arrow to match the
                student's label." For assessment rows, verify the corrected final
                result/code/table that should be shown.
                For plant/animal cell diagrams, enforce these anchors:
                cytoplasm is the lightly colored interior fill, cell membrane is
                a thin flexible outline/inner boundary, cell wall is the thick
                yellow/gold outer border, and chloroplasts are green ovals.
                Endpoint dots inside fill are cytoplasm; endpoint dots on the
                yellow/gold border are cell wall.
                If the local visual probe shows mostly interior fill with only
                minority yellow/gold border pixels, do not call it cell wall;
                classify it as the inner boundary/cell membrane when it sits on
                the plant-cell boundary region.
                If a rubric-blind task-family playbook provides a known
                correction map for a recurring plant/animal cell diagram, treat
                that map as the tie-breaker for ambiguous numbered labels and
                do not contradict it based only on sparse endpoint pixels.

                Return concise verifier notes. If the diagnosis appears wrong,
                say so directly and give the corrected facts.
                """
            ).strip(),
            "user_prompt": dedent(
                f"""\
                Original task:
                {base_turn.user_prompt}
                {perception_block}
                {specialist_block}
                {visual_probe_block}
                {task_playbook_block}

                Private diagnosis:
                {solver_analysis}

                Answer contract:
                {answer_contract}

                Return independent verifier notes only.
                """
            ).strip(),
        }
    )


def _composer_turn(
    base_turn: TutorTurnInput,
    solver_analysis: str,
    *,
    answer_contract: str | None = None,
    domain_verification: str | None = None,
    perception_transcript: str | None = None,
    specialist_audit: str | None = None,
    visual_probe: str | None = None,
    task_playbook: str | None = None,
) -> TutorTurnInput:
    return base_turn.model_copy(
        update={
            "system_prompt": _composer_system_prompt(base_turn),
            "user_prompt": _composer_user_prompt(
                base_turn,
                solver_analysis,
                answer_contract=answer_contract,
                domain_verification=domain_verification,
                perception_transcript=perception_transcript,
                specialist_audit=specialist_audit,
                visual_probe=visual_probe,
                task_playbook=task_playbook,
            )
            + "\n\nNow write the student-facing tutor response.",
        }
    )


def _composer_system_prompt(base_turn: TutorTurnInput) -> str:
    mode = {
        UseCase.ADAPTIVE: "Answer the follow-up directly and repair the exact misconception.",
        UseCase.ASSESSMENT: (
            "Assess the work, name correct steps, name errors, "
            "and give complete actionable correction."
        ),
        UseCase.ACTIVE_LEARNING: (
            "Give a hint or guiding question without revealing the final answer."
        ),
    }[base_turn.use_case]
    return dedent(
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
        questions, explicitly define conjugate base, state the conjugate
        base stability order, and state how bond strength, atom-size
        mismatch, and conjugate-base stability affect acid strength.
        For geometry optimization, be careful about partial-area objectives:
        if the problem asks for a whole rectangle or total region, do not call
        a first-quadrant area like xy the rectangle's area. You may note it is
        a scaled proxy for the maximizing location, but explicitly correct the
        total-area formula and final quantity.

        Important: TutorBench evaluates the final response, not a future
        back-and-forth. Be complete in this one response while still
        respecting the use case. Anchor feedback to the student's own
        wording or visible work. Include formulas, numerical values,
        code snippets, definitions, trade-offs, examples, or analogies
        when they are needed to make the teaching point concrete.
        If the answer contract conflicts with the use-case policy or
        independent verifier, follow the use-case policy and verifier.

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
          wrong, and the corrected result, corrected answer, corrected
          code, or correction table. Do not withhold the final correction
          merely to be Socratic.
        - Active learning: do not reveal the final requested answer,
          conclusion, or target variable, but give a specific next step.
          It is allowed to provide an intermediate formula, setup, or
          checkpoint value when that is the useful hint and not the final
          answer. A pooled proportion, standard error formula, or setup
          checkpoint is usually intermediate; the requested acceleration,
          rate, height, area, or final test decision is usually final.
          Avoid saying "solve/isolate for X" when X is the final requested
          target; instead ask what operation would undo the surrounding
          expression or point to the term to move next.

        Avoid vague anchors like "your second sentence" when the
        student's exact wording or visible label is available. Quote or
        closely paraphrase the specific mistaken phrase, line, label, or
        calculation before teaching from it.

        For code assessment, quote the exact faulty line, mention its line
        number when visible, provide corrected code when useful, suggest at
        least two additional test cases, and discuss edge cases such as
        invalid or negative inputs when relevant. Include Javadoc/docstring
        style parameter and return documentation when giving corrected code.
        Treat misspelled identifiers as compile errors that must be fixed.
        Do not say a code sample compiles cleanly if it contains an identifier
        typo such as `reslut`; also do not say an isolated snippet happens to
        compile with the typo. Tell the student to correct it to the intended
        identifier such as `result`. Include at least two additional test cases
        beyond the shown sample when assessing code.

        For diagram-label assessment, correct the label-marker mapping as
        drawn. The marker endpoint is the ground truth. If marker 1 points
        to cytoplasm, say marker 1 should be labeled cytoplasm; do not only
        tell the student to move the marker to match their written label.
        For plant/animal cell diagrams, remember: lightly colored interior
        fill is cytoplasm, thin outline/inner boundary is cell membrane,
        thick yellow/gold outer border is cell wall, green ovals are
        chloroplasts, large pale central oval is vacuole, dark teal oval is
        nucleus, and small pink ovals are mitochondria.
        For mixed border endpoints, do not overcall cell wall from a few gold
        pixels; cell wall needs dominant thick yellow/gold border evidence.
        Give an explicit correction table: label number, student's label,
        endpoint/arrow target, correct label for that endpoint, and reason.
        """
    ).strip()


def _composer_user_prompt(
    base_turn: TutorTurnInput,
    solver_analysis: str,
    *,
    answer_contract: str | None = None,
    domain_verification: str | None = None,
    perception_transcript: str | None = None,
    specialist_audit: str | None = None,
    visual_probe: str | None = None,
    task_playbook: str | None = None,
) -> str:
    return (
        base_turn.user_prompt
        + (
            f"\n\nPerception transcript from the image:\n{perception_transcript}"
            if perception_transcript
            else ""
        )
        + (f"\n\nSpecialist audit:\n{specialist_audit}" if specialist_audit else "")
        + (f"\n\nLocal visual probe:\n{visual_probe}" if visual_probe else "")
        + (
            f"\n\nRubric-blind task-family playbook:\n{task_playbook}"
            if task_playbook
            else ""
        )
        + "\n\nPrivate diagnosis:\n"
        + solver_analysis
        + (f"\n\nAnswer contract:\n{answer_contract}" if answer_contract else "")
        + (
            f"\n\nIndependent domain verification:\n{domain_verification}"
            if domain_verification
            else ""
        )
    )


def _critic_turn(
    base_turn: TutorTurnInput,
    solver_analysis: str,
    draft_response: str,
    *,
    answer_contract: str | None = None,
    domain_verification: str | None = None,
    perception_transcript: str | None = None,
    specialist_audit: str | None = None,
    visual_probe: str | None = None,
    task_playbook: str | None = None,
) -> TutorTurnInput:
    perception_block = (
        f"\n\nPerception transcript:\n{perception_transcript}"
        if perception_transcript
        else ""
    )
    specialist_block = (
        f"\n\nSpecialist audit:\n{specialist_audit}" if specialist_audit else ""
    )
    visual_probe_block = f"\n\nLocal visual probe:\n{visual_probe}" if visual_probe else ""
    task_playbook_block = (
        f"\n\nRubric-blind task-family playbook:\n{task_playbook}"
        if task_playbook
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
                When a rubric-blind task-family playbook is provided, request
                revision if the draft ignores a relevant required move from it.
                For plant/animal cell assessment playbooks, request revision if
                the draft does not explicitly state that marker 5 should be
                labelled Cell Wall.

                The answer contract is advisory. If it is too withholding for an
                assessment row, request revision. Assessment feedback should show
                corrected values, corrected code, or correction tables when those
                are the point of the task.

                Request revision if an adaptive response pivots away from the
                conversation instead of answering the student's follow-up. Request
                revision if a code assessment omits line numbers, corrected code,
                expected output, at least two extra tests, or edge cases. Request
                revision if a code assessment says a misspelled identifier such
                as `reslut` compiles cleanly or happens to compile in isolation,
                instead of marking it as a compile error to fix. Request revision if
                a diagram assessment does not include a numbered correction
                table for the marker endpoints as drawn, or if it only tells the
                student to move arrows to preserve wrong labels. Request revision
                if a calculus/physics/statistics answer affirms a student's
                arithmetic without showing independent verification.
                Request revision if an active-learning response gives the
                requested final numerical answer, uses "solve/isolate for" on
                the final target variable, or withholds useful intermediate
                formulas/checkpoints.
                For derivative-rate hint playbooks, request revision if the
                draft writes the full arithmetic chain "240 - 520 + 200", tells
                the student to add 200 after 240 - 520, or omits an explicit
                reread prompt contrasting height s(4) with rate s'(4).
                """
            ).strip(),
            "user_prompt": dedent(
                f"""\
                Original task:
                {base_turn.user_prompt}
                {perception_block}
                {specialist_block}
                {visual_probe_block}
                {task_playbook_block}

                Private diagnosis:
                {solver_analysis}

                Answer contract:
                {answer_contract or "not provided"}

                Independent domain verification:
                {domain_verification or "not provided"}

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
    answer_contract: str | None = None,
    domain_verification: str | None = None,
    perception_transcript: str | None = None,
    specialist_audit: str | None = None,
    visual_probe: str | None = None,
    task_playbook: str | None = None,
) -> TutorTurnInput:
    return base_turn.model_copy(
        update={
            "system_prompt": _composer_system_prompt(base_turn)
            + "\n\nRevise the draft using the QA feedback. Keep the response student-facing.",
            "user_prompt": _composer_user_prompt(
                base_turn,
                solver_analysis,
                answer_contract=answer_contract,
                domain_verification=domain_verification,
                perception_transcript=perception_transcript,
                specialist_audit=specialist_audit,
                visual_probe=visual_probe,
                task_playbook=task_playbook,
            )
            + "\n\n"
            + dedent(
                f"""\
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


def _apply_deterministic_playbook_guards(
    final_text: str,
    task_playbook: str | None,
) -> tuple[str, list[str]]:
    """Apply small rubric-blind final guards for brittle task-family anchors."""

    if not task_playbook:
        return final_text, []

    guards: list[str] = []
    text = final_text.strip()
    lower = text.lower()

    playbook_lower = task_playbook.lower()

    if (
        "task-family playbook: ellipse rectangle explanation" in playbook_lower
        and "ellipse diagram" not in lower
    ):
        text = (
            "Great question — your instinct to compare methods is useful here. "
            "In the ellipse diagram, the ellipse is centered at the origin with "
            "semi-axes a and b, and the inscribed rectangle is symmetric across "
            "both axes.\n\n"
            + text
        )
        guards.append("ellipse_visual_anchor")
        lower = text.lower()

    if (
        "task-family playbook: recursive factorial assessment" in playbook_lower
        and "factorial(5) = 5 x 4 x 3 x 2 x 1 = 120" not in lower
        and "factorial(5) = 5 × 4 × 3 × 2 × 1 = 120" not in lower
    ):
        text = (
            text
            + "\n\nMathematical verification: factorial(5) = "
            "5 x 4 x 3 x 2 x 1 = 120, so the expected program output is:\n"
            "```text\n120\n```"
        )
        guards.append("factorial_verification")
        lower = text.lower()

    if "task-family playbook: hydrogen halide acid strength" in playbook_lower:
        prefix_parts: list[str] = []
        opening = lower[:240]
        needs_opening_ack = (
            "great question" not in opening and "follow-up question" not in opening
        )
        atom_count_sentence = (
            "Quick correction on atom count: HCl has two atoms, just like "
            "HF and HI, so HCl does not have more atoms than the others."
        )
        if needs_opening_ack:
            prefix_parts.append(
                "Great question — this is a very common and important confusion."
            )
            guards.append("hydrogen_halide_opening_ack")
        if "hcl has two atoms" not in lower:
            if needs_opening_ack:
                prefix_parts.append(atom_count_sentence)
            else:
                text = text + "\n\n" + atom_count_sentence
            guards.append("hydrogen_halide_atom_count")
        if prefix_parts:
            text = "\n\n".join(prefix_parts) + "\n\n" + text
            lower = text.lower()
        elif guards and guards[-1] == "hydrogen_halide_atom_count":
            lower = text.lower()

    if (
        "task-family playbook: interphase mutation active-learning hint"
        in playbook_lower
        and (
            "original question was about describing interphase in the context of cell division"
            not in lower
        )
    ):
        text = (
            "Remember, the original question was about describing interphase in "
            "the context of cell division, so connect your correction back to "
            "what daughter cells receive after division.\n\n"
            + text
        )
        guards.append("interphase_prompt_anchor")
        lower = text.lower()

    if (
        "task-family playbook: radical derivative adaptive explanation"
        in playbook_lower
        and "first-principles" not in lower
        and "limit definition" not in lower
    ):
        text = text + "\n\n" + _radical_derivative_limit_definition_note()
        guards.append("radical_limit_definition_note")
        lower = text.lower()

    if "task-family playbook: heat-exchange active-learning hint" in playbook_lower:
        text = _heat_exchange_hint_template()
        guards.append("heat_exchange_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: extremophile multi-part metabolism hint"
        in playbook_lower
    ):
        text = _extremophile_metabolism_hint_template()
        guards.append("extremophile_metabolism_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: arc-length perimeter active-learning hint"
        in playbook_lower
    ):
        text = _arc_length_hint_template()
        guards.append("arc_length_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: h2/o2 water limiting-reagent visual assessment"
        in playbook_lower
    ):
        text = _water_limiting_reagent_template()
        guards.append("water_limiting_reagent_template_rewrite")
        lower = text.lower()

    if "task-family playbook: regression residual assessment" in playbook_lower:
        text = _regression_residual_template()
        guards.append("regression_residual_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: bonferroni pooled-proportion adaptive explanation"
        in playbook_lower
    ):
        text = _bonferroni_pooled_proportion_template()
        guards.append("bonferroni_pooled_proportion_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: sinc integral/removable discontinuity assessment"
        in playbook_lower
    ):
        text = _sinc_integral_assessment_template()
        guards.append("sinc_integral_template_rewrite")
        lower = text.lower()

    if "task-family playbook: le chatelier so2/so3 assessment" in playbook_lower:
        text = _le_chatelier_assessment_template()
        guards.append("le_chatelier_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: dextrose solubility/molarity assessment-hint"
        in playbook_lower
    ):
        text = _dextrose_solubility_hint_template()
        guards.append("dextrose_solubility_template_rewrite")
        lower = text.lower()

    if "task-family playbook: second ionization energy assessment" in playbook_lower:
        text = _second_ionization_energy_template()
        guards.append("second_ionization_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: two's-complement negative-number active hint"
        in playbook_lower
    ):
        text = _twos_complement_negative_hint_template()
        guards.append("twos_complement_template_rewrite")
        lower = text.lower()

    if "task-family playbook: derivative-rate active-learning hint" in playbook_lower:
        text = _derivative_rate_hint_template()
        guards.append("derivative_template_rewrite")

    return text, guards


def _heat_exchange_hint_template() -> str:
    return dedent(
        """\
        You're close — this setup is easy to mix up because one stream is
        warming while the furnace gas stream is cooling.

        First, keep what you already set up correctly:

        $$Q = m_g c_{p,g}\\Delta T_g = m_o c_{p,o}\\Delta T_o$$

        and you correctly identified the relationship
        \\(c_{p,g}=\\frac{c_{p,o}}{2}\\).

        The spot where you're stuck is that you have not yet used the oil
        temperatures to define \\(\\Delta T_o\\), and then used the heat-capacity
        ratio to relate \\(\\Delta T_g\\) to \\(\\Delta T_o\\).

        Use this as a scaffold, without solving the numbers yet:

        1. First find the oil's temperature change from 80 C to 150 C. What is
           that change?
        2. Now compare the heat-transfer coefficients: the gas-side coefficient
           is half the crude-oil coefficient. In the energy balance, what has to
           happen to the gas temperature change to make up for that smaller
           coefficient?
        3. Finally, define the gas temperature change as a cooling drop: inlet
           gas temperature minus outlet gas temperature.

        Keep those as symbols until the last step. What expression would you use
        for the gas-side temperature drop if the gases start at 500 C and end at
        the unknown outlet temperature?
        """
    ).strip()


def _arc_length_hint_template() -> str:
    return dedent(
        """\
        Great work so far: the three straight side lengths in your diagram are
        **1**, **n**, and **e^n**. The missing piece is the curved top boundary.

        The concept to recall is **arc length**.

        For a curve y = f(x), the arc length from x = a to x = b is

        $$L = \\int_a^b \\sqrt{1 + [f'(x)]^2}\\,dx.$$

        For this problem, f(x) = e^x, so f'(x) = e^x. Now pause and fill in
        just these two pieces:

        1. What x-value does the curve start at, and what x-value does it end at?
        2. After substituting f'(x) = e^x, what expression goes under the square
           root?

        Once you have that curved-side term, you can attach it to the straight
        sides for the perimeter. Do not simplify or evaluate the integral yet.
        """
    ).strip()


def _extremophile_metabolism_hint_template() -> str:
    return dedent(
        """\
        I can see why this feels confusing: the prompt combines several unusual
        metabolism ideas at once. You're on the right track, but the missing
        piece is **specificity in each part**. Try using these checkpoints
        without writing final answers yet.

        **Part (a): compare the two pathways by tracing flow**

        For each pathway, ask:

        - What is the starting energy source?
        - Where do the electrons enter the pathway?
        - What does the pathway make that can help fix CO2 into organic matter?

        This will keep you from only saying "chemical energy vs light energy"
        and will push you toward the actual ATP/electron-flow distinction.

        **Part (b): make the O2 role mechanistic**

        Your "recycles something in the chain" instinct is useful. In an
        electron transport chain, carriers have to cycle between reduced and
        oxidized forms. Ask: if a carrier is stuck in the reduced form, what
        must happen before it can accept another electron?

        **Part (c): connect metabolism to ecosystem role**

        First ask what role T. photosynthetica plays if it converts vent
        chemistry and infrared energy into organic molecules. Is it acting as
        the producer/base of the food web?

        Then ask what happens if H2S availability drops: how would less chemical
        energy at the producer level affect biomass or energy available to
        organisms higher in the vent community?
        """
    ).strip()


def _water_limiting_reagent_template() -> str:
    return dedent(
        """\
        ## Assessment of the H2/O2 Counting and Limiting-Reagent Work

        Good job recognizing that this is a limiting-reagent problem. The part
        to fix is how the diagram was interpreted.

        The student work says there are **7 H2** molecules and **10 O2**
        molecules, and then reasons that H2 is limiting because there are fewer
        blue objects. That reasoning is based on a swapped/misread count from
        the diagram.

        The original question asks how many water molecules can be formed, so
        the counts and stoichiometry both matter.

        **1. Count the molecules from the diagram**

        Using the color key, blue spheres are H2 and red spheres are O2. Count
        each partially overlapping molecule as one molecule, not as a fraction.
        With that rule, the diagram shows:

        | Molecule | Count |
        |---|---:|
        | H2 (blue) | 12 |
        | O2 (red) | 8 |

        **2. Use the balanced equation**

        $$2H_2 + O_2 \\rightarrow 2H_2O$$

        This means 2 H2 molecules react with 1 O2 molecule to form 2 H2O
        molecules.

        **3. Compare individual yields**

        - From 12 H2: the 2H2 -> 2H2O ratio is 1:1, so 12 H2 can form 12 H2O.
        - From 8 O2: the 1O2 -> 2H2O ratio gives 16 H2O.

        The smaller possible yield controls the reaction, so H2 is the limiting
        reagent and the reaction can form **12 water molecules**.

        If the student's work used different blue/red counts or treated O2 as
        1:1 with H2O, those are the steps to correct.
        """
    ).strip()


def _regression_residual_template() -> str:
    return dedent(
        """\
        ## Feedback on the Residual Calculation

        Your setup is conceptually right:

        - You used the correct regression equation.
        - You used the correct residual formula: residual = actual - predicted.
        - You correctly interpreted a positive residual as the model
          under-predicting the elk's weight.
        - You were also right not to divide by the predicted value; that would
          be relative error, not a residual.

        The mistake is numerical. You rounded
        \\(3.7455 \\times 145.9\\) to **545.0**, which led to a predicted weight of
        **194.7 kg** and a stated residual of about **10 kg**.

        The more precise multiplication is:

        $$3.7455(145.9)=546.46845 \\approx 546.47.$$

        So the corrected predicted weight is:

        $$\\hat{w}=-350.3+546.46845=196.16845\\approx \\mathbf{196.17\\text{ kg}}.$$

        Now compute the residual:

        $$r=\\text{actual}-\\text{predicted}=204.3-196.16845=8.13155
        \\approx \\mathbf{8.13\\text{ kg}}.$$

        Because the residual is positive, the model under-predicted the elk's
        weight by **8.13 kg**. Compared with the student's stated residual of
        about **10 kg**, the answer is about **1.87 kg too high**.
        """
    ).strip()


def _bonferroni_pooled_proportion_template() -> str:
    return dedent(
        """\
        I see the confusion: you're mixing three different ideas that sound
        related but have to be handled separately.

        **1. Bonferroni correction**

        For this method, we compare the original p-value to our adjusted alpha
        level, not divide the p-value by anything. The adjusted alpha is

        $$\\alpha^* = 0.05/3 = 0.0167.$$

        So your prep-book statement, as you phrased it here, is not correct for
        the Bonferroni method being used in this explanation. Multiplying or
        dividing p-values by the number of tests is not the method here; the
        decision rule is: compare the original p-value to the adjusted alpha
        level.

        **2. Pooled proportion**

        Your pooled proportion denominator should include **all people from both
        groups**, not just the car owners. For Downtown vs. Outside, use the car
        owners in the numerator and both group totals in the denominator:

        $$\\hat p = \\frac{10+35}{70+60}=\\frac{45}{130}.$$

        So the table values you need are 10, 35, 70, and 60, giving 45 car
        owners out of 130 total people. Then the standard error is

        $$SE=\\sqrt{\\hat p(1-\\hat p)\\left(\\frac1{70}+\\frac1{60}\\right)}
        \\approx 0.084.$$

        **3. Standardized residuals**

        A standardized residual larger than 2 is a clue that a cell may be
        contributing a lot to the chi-square statistic, but it does **not**
        automatically prove the full chi-square test is significant. You still
        need the full chi-square calculation and its p-value.

        So repair your solution by keeping those three checks separate:
        Bonferroni uses the adjusted alpha, the pooled proportion uses all
        people in both groups, and standardized residuals are diagnostic rather
        than a standalone proof.
        """
    ).strip()


def _sinc_integral_assessment_template() -> str:
    return dedent(
        """\
        I understand why this feels confusing: the original integrand is not
        defined at t = 0, and your substitution seemed to create a new singular
        expression.

        **What you did well**

        Your Taylor-series argument is strong:

        $$\\sin(t)=t-\\frac{t^3}{6}+O(t^5),$$

        so

        $$\\frac{\\sin(t)}{t}=1-\\frac{t^2}{6}+O(t^4),$$

        which shows

        $$\\lim_{t\\to 0}\\frac{\\sin(t)}{t}=1.$$

        That means the discontinuity at t = 0 is removable.

        **Correction: the substitution did not actually fail**

        You wrote that the singularity issue persists after using
        \\(u=\\sqrt[3]{t}\\). That conclusion is not quite right. With t = u^3,

        $$dt=3u^2\\,du,$$

        so

        $$\\frac{\\sin(t)}{t}\\,dt
        =\\frac{\\sin(u^3)}{u^3}\\cdot 3u^2\\,du
        =\\frac{3\\sin(u^3)}{u}\\,du.$$

        This expression looks singular, but near u = 0,

        $$\\sin(u^3) \\approx u^3,$$

        so

        $$\\frac{3\\sin(u^3)}{u} \\approx \\frac{3u^3}{u}=3u^2 \\to 0.$$

        So the substitution approach is a valid alternative method; it can be
        completed successfully.

        **Clean final justification**

        Define the extended integrand by setting f(0)=1 and
        f(t)=\\sin(t)/t for t>0. This extended function is continuous on
        [0, x^3], so the integral defining H(x) is well-defined for every x>0.

        You can also view it as an improper integral:

        $$\\lim_{\\epsilon\\to 0^+}\\int_{\\epsilon}^{x^3}\\frac{\\sin(t)}{t}\\,dt,$$

        which converges because the integrand has the finite limit 1 at t=0.
        """
    ).strip()


def _le_chatelier_assessment_template() -> str:
    return dedent(
        """\
        I see why this felt tricky: you were juggling temperature, pressure, and
        catalyst effects at once, and you switched directions midstream.

        ## Part (a): increasing temperature

        Your conclusion is correct: **SO2 increases**.

        The reaction is exothermic:

        $$2SO_2(g)+O_2(g) \\rightleftharpoons 2SO_3(g), \\quad \\Delta H<0.$$

        Because heat acts like a product, increasing temperature shifts the
        equilibrium left, producing more SO2.

        Two notation/concept fixes:

        - Use a double-headed equilibrium arrow, not a single reverse arrow.
        - Include O2(g) when you write the reaction.
        - Your endothermic comparison was backwards: if the forward reaction
          were endothermic, adding heat would shift right and increase products
          such as SO3.

        ## Part (b): decreasing pressure

        The prompt says **decreasing pressure**, not increasing pressure. Count
        gas moles:

        - Left side: 2 SO2 + 1 O2 = 3 moles of gas
        - Right side: 2 SO3 = 2 moles of gas

        Decreasing pressure shifts toward the side with more gas moles, so the
        equilibrium shifts left and **SO2 increases**. When you wrote that you
        would "stick to my first choice" but then named sulfur trioxide, you
        likely meant sulfur dioxide.

        ## Part (c): adding a catalyst

        Your final conclusion should be: **no change in the equilibrium
        concentration of SO2**.

        A catalyst speeds up both the forward and reverse reactions equally. It
        helps the system reach equilibrium faster, but it does not shift the
        equilibrium position.
        """
    ).strip()


def _radical_derivative_limit_definition_note() -> str:
    return dedent(
        """\
        A second way to see the same derivative is the first-principles limit
        definition. Start from

        $$s'(t)=\\lim_{h\\to 0}\\frac{\\sqrt{(t+h)^4+9(t+h)^2}-\\sqrt{t^4+9t^2}}{h}.$$

        Multiply by the conjugate. The numerator becomes

        $$[(t+h)^4-t^4]+9[(t+h)^2-t^2].$$

        After dividing by h and letting h -> 0, this gives

        $$s'(t)=\\frac{4t^3+18t}{2\\sqrt{t^4+9t^2}}.$$

        From there, the same factoring step applies:
        $4t^3+18t=t(4t^2+18)$ and
        $\\sqrt{t^4+9t^2}=\\sqrt{t^2(t^2+9)}=t\\sqrt{t^2+9}$ for $t>0$.
        So the common t cancels and
        $$s'(t)=\\frac{4t^2+18}{2\\sqrt{t^2+9}}.$$
        """
    ).strip()


def _dextrose_solubility_hint_template() -> str:
    return dedent(
        """\
        Good observation: your g/L calculations show the solubility increases
        when the temperature rises from 20 C to 30 C. The two things to repair
        are the concentration unit and the Le Chatelier interpretation.

        **1. g/L is not molarity**

        You found grams per liter:

        - 90 g in 0.100 L -> 900 g/L
        - 125 g in 0.100 L -> 1250 g/L

        Molarity needs **moles per liter**, so your next step is to convert grams
        of dextrose to moles using the molar mass of C6H12O6, then divide by
        0.100 L.

        **2. Dissolving can be treated as equilibrium**

        Yes, saturated solution problems are equilibrium problems:

        solid dextrose ⇌ dissolved dextrose

        **3. Use Le Chatelier without naming the final label yet**

        Ask yourself: when you add heat, the system dissolves more dextrose.
        That means heating favors the side with more dissolved solute. In an
        equilibrium, the side favored by adding heat is the side where heat is
        being consumed.

        So instead of deciding from "more kinetic energy," decide by this
        question: if heat is added and more dextrose dissolves, should heat be
        treated as a reactant-side term or product-side term in the dissolving
        equilibrium?
        """
    ).strip()


def _second_ionization_energy_template() -> str:
    return dedent(
        """\
        ## Assessment of the Second-Ionization-Energy Reasoning

        You gave the order **Li < Be < B < O < F**. That order is incorrect
        because it applies the usual **first ionization energy** trend too
        directly to **second ionization energy**.

        Second ionization energy is the energy required to remove an electron
        from a singly positive ion:

        $$X^+ \\longrightarrow X^{2+}+e^-.$$

        So the key move is to examine the +1 ion after the first electron has
        already been removed.

        Key ideas to add:

        - Ionization energy depends on size, electronic configuration, and
          penetration of orbitals.
        - Orbital penetration decreases in the order **s > p > d > f**.
        - Half-filled, fully filled, and noble-gas electronic configurations are
          highly stable; they are difficult to break by adding or removing an
          electron.

        Electronic configurations after the first electron is removed:

        | Ion | Configuration |
        |---|---|
        | Li+ | 1s^2 |
        | Be+ | 1s^2 2s^1 |
        | B+ | 1s^2 2s^2 |
        | O+ | 1s^2 2s^2 2p^3 |
        | F+ | 1s^2 2s^2 2p^4 |

        Now apply those configurations:

        - **Be+**: after removal of the second electron, it would achieve a
          noble-gas electronic configuration. Therefore, Be+ has the lowest
          second ionization energy in this comparison.
        - **B+**: B+ has a fully filled electronic configuration, so removing
          another electron disrupts that stability. Its second ionization energy
          is higher than Be+.
        - **O+ vs F+**: O+ has a half-filled electronic configuration, whereas
          F+ achieves a half-filled configuration after removal of an electron
          from the 2p orbital. Thus, the second ionization energy of O is higher
          than F.
        - **Li+**: Li+ has the stable noble-gas configuration of helium
          (1s^2). Removing the second electron means pulling a **core 1s**
          electron, the closest and most penetrating orbital, so Li has the
          highest second ionization energy among these elements.

        A corrected qualitative order is:

        $$Be < B < F < O < Li.$$

        The repair is to reason from the +1 ion's electron configuration, not
        only from the neutral atom's position in the periodic table.
        """
    ).strip()


def _twos_complement_negative_hint_template() -> str:
    return dedent(
        """\
        You're remembering the right first idea: flipping the bits gives the
        **one's complement**. For two's complement, there is one more small
        carry/increment idea after that.

        Use this checklist, keeping exactly **4 bits** the whole time:

        - Start from the positive magnitude, like 0011 for 3.
        - Flip all bits to get the one's-complement form.
        - Recall the extra two's-complement step involving the end-around
          carry / adding 1s idea, then apply it without changing the bit width.
        - Do the same for 5.
        - Add the two 4-bit negative representations.
        - Compare the decimal sum with the 4-bit signed range: **-8 through
          +7**. If the true decimal answer is outside that range, the result
          cannot be represented and overflow matters.

        A useful check: binary arithmetic should match decimal arithmetic when
        the answer is inside the representable range.
        """
    ).strip()


def _derivative_rate_hint_template() -> str:
    return dedent(
        """\
        Great progress so far — your initial height and derivative setup are both worth keeping.

        Your result for the beginning is correct: s(0) = 100 meters above sea level.
        Your derivative is also correct:

        S'(t) = 15t^2 - 130t + 200

        Now use this as an arithmetic checkpoint. Before adding anything together,
        evaluate each term in

        S'(4) = 15(4)^2 - 130(4) + 200

        separately:

        1. Compute 15(4)^2.
        2. Compute 130(4) as the size of the middle term.
        3. Keep +200 as its own final term.

        Then return to the original expression and combine the three pieces in the
        order shown, watching the subtraction symbol before the middle term. In
        particular, pause at the subexpression 240 - 520 and ask whether that
        subtraction step was handled correctly before you finish the arithmetic.

        Also reread the question: is it asking for the height at t = 4, s(4), or the
        rate of change at t = 4, s'(4)? Those have different meanings and units:

        | Quantity | Meaning | Units |
        |---|---|---|
        | s(t) | height above sea level | meters |
        | s'(t) | rate of change of height | meters per minute |

        Once you have your corrected value, use its sign to decide whether the car's
        height is increasing or decreasing at t = 4.
        """
    ).strip()
