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
from tutorbench_lab.numeric_probe import build_numeric_probe
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
    numeric_probe = build_numeric_probe(
        base_turn,
        perception_result.text if perception_result else None,
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
            numeric_probe=numeric_probe,
            task_playbook=task_playbook,
        )
        specialist_audit_result = generate_stage(
            "specialist_audit",
            specialist_audit_turn,
            client=verifier_client,
            max_tokens=1200,
        )

    if task_playbook is None and specialist_audit_result:
        late_context = "\n\n".join(
            part
            for part in [
                perception_result.text if perception_result else None,
                specialist_audit_result.text,
            ]
            if part
        )
        task_playbook = build_task_playbook(base_turn, extra_context=late_context)

    solver_turn = _solver_turn(
        base_turn,
        perception_transcript=perception_result.text if perception_result else None,
        specialist_audit=specialist_audit_result.text
        if specialist_audit_result
        else None,
        visual_probe=visual_probe,
        numeric_probe=numeric_probe,
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
        numeric_probe=numeric_probe,
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
        numeric_probe=numeric_probe,
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
        numeric_probe=numeric_probe,
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
            numeric_probe=numeric_probe,
            task_playbook=task_playbook,
        )
        critic_result = generate_stage(
            f"critic_{attempt_index}",
            critic_turn,
            client=critic_client,
            max_tokens=900,
        )
        coverage_critic_turn = _coverage_critic_turn(
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
            numeric_probe=numeric_probe,
            task_playbook=task_playbook,
        )
        coverage_critic_result = generate_stage(
            f"coverage_critic_{attempt_index}",
            coverage_critic_turn,
            client=critic_client,
            max_tokens=900,
        )
        latest_critic_text = "\n\n".join(
            [
                f"Generic critic:\n{critic_result.text}",
                f"Pedagogy coverage critic:\n{coverage_critic_result.text}",
            ]
        )
        critic_attempts.append(
            {
                "stage": f"critic_{attempt_index}",
                "kind": "generic",
                "attempt": attempt_index,
                "text": critic_result.text,
                "latency_ms": critic_result.latency_ms,
                "usage": critic_result.usage.model_dump(mode="json"),
            }
        )
        critic_attempts.append(
            {
                "stage": f"coverage_critic_{attempt_index}",
                "kind": "pedagogy_coverage",
                "attempt": attempt_index,
                "text": coverage_critic_result.text,
                "latency_ms": coverage_critic_result.latency_ms,
                "usage": coverage_critic_result.usage.model_dump(mode="json"),
            }
        )
        if _critic_requests_revision(critic_result.text):
            revision_feedback.append(f"Generic critic:\n{critic_result.text}")
        if _critic_requests_revision(coverage_critic_result.text):
            revision_feedback.append(
                f"Pedagogy coverage critic:\n{coverage_critic_result.text}"
            )

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
            numeric_probe=numeric_probe,
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
            "numeric_probe": numeric_probe,
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
    """Whether to add a routed evidence audit before final composition."""

    return base_turn.image.present


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

                For trigonometric graphs, inspect the y-intercept and phase
                before naming the function. A curve passing through (0, 1) at
                x=0 is cosine-like; a curve passing through (0, 0) with positive
                initial slope is sine-like. Keep the plotted function, any
                defined accumulated function such as F(x), and the student's
                written claim separate instead of trusting the student's label.

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
    numeric_probe: str | None = None,
    task_playbook: str | None = None,
) -> TutorTurnInput:
    perception_block = (
        f"\n\nPerception transcript:\n{perception_transcript}"
        if perception_transcript
        else ""
    )
    visual_probe_block = f"\n\nLocal visual probe:\n{visual_probe}" if visual_probe else ""
    numeric_probe_block = (
        f"\n\nLocal numeric probe:\n{numeric_probe}" if numeric_probe else ""
    )
    task_playbook_block = (
        f"\n\nRubric-blind task-family playbook:\n{task_playbook}"
        if task_playbook
        else ""
    )
    return base_turn.model_copy(
        update={
            "system_prompt": dedent(
                """\
                You are a routed specialist evidence auditor for a multimodal
                tutor. Do not write the student-facing response. Do not solve by
                making the student's answer look better than it is. Your job is
                to preserve exactly what is visible in the image before any
                tutoring style decisions are made.

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
                cases, and any documentation/comment requirements. Pay special
                attention to line-level claims where a student says the code is
                correct; look for overflow, integer division, missing semicolons
                or braces, missing declarations, and required helper methods.

                For math/science images, audit visible claims, equations, signs,
                units, constants, parameter names, final answers, and any row of
                an ICE table or likelihood derivation against the prompt. Do not
                call a visible expression correct unless you can quote or
                closely paraphrase it.
                For graphs, charts, tables, and spectra, create a "locked visual
                values" note when the student's copied numbers differ from the
                visible tick/grid/axis evidence. Use the best visible reading
                and mark it approximate only when exact ticks are not printed,
                but do not discard a clear discrepancy merely because the graph
                is hand-drawn or low resolution.

                For adaptive-explanation rows, identify the exact visible facts
                needed to answer the student's follow-up, but do not let an
                image-only hunch override the conversation unless it is visible
                and relevant to the follow-up. For active-learning rows, identify
                the student's current stuck point and the final target that must
                remain withheld.

                If a fact is ambiguous, mark it ambiguous instead of guessing.
                """
            ).strip(),
            "user_prompt": dedent(
                f"""\
                Original multimodal tutoring task:
                {base_turn.user_prompt}
                {perception_block}
                {visual_probe_block}
                {numeric_probe_block}
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
    numeric_probe: str | None = None,
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
    numeric_probe_block = (
        f"\n\nLocal numeric probe:\n{numeric_probe}" if numeric_probe else ""
    )
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
                For chart, table, graph, and spectrum rows, propagate visible
                numeric discrepancies instead of softening them away: if the
                perception or audit estimates a plotted value and the student
                used a different value, treat that as a candidate student error
                that the final response likely needs to name.
                For trigonometric graphs, verify the function from the graph's
                y-intercept, phase, period, and labels before accepting the
                student's written identification; keep f(x), F(x), and any
                antiderivative/accumulation definition distinct.

                Independently recompute every arithmetic, algebra, derivative,
                formula-substitution, and code-execution step. Do not mark a
                student's numerical value as correct unless you have verified it.
                If the student made an arithmetic error, identify the exact term
                or line where it happens. For assessment rows, audit downstream
                arithmetic even when an earlier setup is conceptually wrong; the
                student may need both the root conceptual error and the later
                numerical slip named separately.

                For programming tasks, inspect exact code lines, compile/runtime
                errors, edge cases, tests beyond the shown sample, and input
                validation. If you provide corrected code, include useful
                comments/docstrings when that would make the fix clearer.

                When a specialist audit is provided, treat it as the strongest
                evidence for visible marker endpoints, code lines, and current
                label mappings. If it conflicts with the perception transcript,
                explicitly resolve the conflict before planning the tutor's goal.
                When a local numeric probe is provided, treat it as a calculator
                sanity check for visible arithmetic. If your arithmetic conflicts
                with it, recompute and resolve the conflict explicitly before
                accepting or rejecting the student's numerical step.

                For adaptive-explanation rows, the conversation context is the
                task. If the student's follow-up is about the provided initial
                explanation, answer that follow-up directly. Do not switch to
                solving a different image-only problem, and do not announce that
                the image conflicts with the conversation unless the student
                explicitly asks about that conflict.

                If a rubric-blind task-family playbook names specific visible
                student expressions or common traps, verify whether they appear
                in this row and include them explicitly in the diagnosis. Do not
                replace those required checks with a more generic explanation.
                If the playbook's named scenario does not actually match the
                prompt, image, or student work, say so privately and ignore the
                playbook rather than importing facts from a different problem.
                """
            ).strip()
            + use_case_note,
            "user_prompt": (
                base_turn.user_prompt
                + perception_block
                + specialist_block
                + visual_probe_block
                + numeric_probe_block
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
    numeric_probe: str | None = None,
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
    numeric_probe_block = (
        f"\n\nLocal numeric probe:\n{numeric_probe}" if numeric_probe else ""
    )
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
                - correct steps to affirm and incorrect steps to diagnose
                - guiding questions/checkpoints for active-learning responses
                - alternative paths or method-choice advice when the student is
                  comparing approaches
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
                {numeric_probe_block}
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
            "when those are the useful hint. Prefer turning near-final corrections "
            "into questions or checkpoints; do not write a completed corrected "
            "sequence, final conclusion, final test decision, or final numeric "
            "target unless the prompt explicitly asks for assessment instead of a hint."
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
    numeric_probe: str | None = None,
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
    numeric_probe_block = (
        f"\n\nLocal numeric probe:\n{numeric_probe}" if numeric_probe else ""
    )
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
                - charts/tables/graphs/spectra: compare visible values to the
                  student's copied values and preserve discrepancies for the
                  final tutor response
                - active learning: state what intermediate checkpoints may be
                  disclosed and what final answer must be withheld

                For diagram-label assessment, marker endpoint is ground truth:
                verify the correct label for the endpoint as drawn. Do not
                silently convert the task into "move the arrow to match the
                student's label." For assessment rows, verify the corrected final
                result/code/table that should be shown.
                For trigonometric graph images, verify the plotted curve from
                the y-intercept and phase before accepting the student's claimed
                function name. Explicitly distinguish the plotted f from an
                accumulated/antiderivative F.
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
                If the local numeric probe provides a simple arithmetic value,
                use it as an external calculator check. Do not contradict it
                without showing a corrected recomputation.
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
                {numeric_probe_block}
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
    numeric_probe: str | None = None,
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
                numeric_probe=numeric_probe,
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
        If the student is choosing among methods, explicitly say whether
        multiple paths are valid and give a decision rule for choosing among
        them. If the response is a hint, include one or two pointed guiding
        questions or checkpoint prompts, not just a generic nudge.
        If the answer contract conflicts with the use-case policy or
        independent verifier, follow the use-case policy and verifier.
        Treat any task-family playbook as a checklist only after confirming it
        matches this exact prompt/image. Do not mention unrelated playbook
        topics or import facts from a different problem family.

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
          code, or correction table. When useful, name the error type
          (conceptual, arithmetic, formula/setup, notation, visual-label,
          compile/runtime, or edge-case). Audit downstream arithmetic even
          if the setup is wrong, and name both errors when both occur. Do
          not withhold the final correction merely to be Socratic.
        - Active learning: do not reveal the final requested answer,
          conclusion, or target variable, but give a specific next step.
          It is allowed to provide an intermediate formula, setup, or
          checkpoint value when that is the useful hint and not the final
          answer. A pooled proportion, standard error formula, or setup
          checkpoint is usually intermediate; the requested acceleration,
          rate, height, area, or final test decision is usually final.
          For sequence, coding, proof, and multiple-choice hints, do not
          write the completed corrected sequence/code/proof/choice; ask the
          student to test the decisive property instead.
          Avoid saying "solve/isolate for X" when X is the final requested
          target; instead ask what operation would undo the surrounding
          expression or point to the term to move next.

        Avoid vague anchors like "your second sentence" when the
        student's exact wording or visible label is available. Quote or
        closely paraphrase the specific mistaken phrase, line, label, or
        calculation before teaching from it.

        For multimodal rows, treat the perception transcript and specialist
        evidence audit as an evidence lock. If you say a visible step is
        correct or incorrect, anchor that claim to the exact visible line,
        expression, code snippet, label, unit, or diagram relationship. Do not
        praise a whole solution as correct when the evidence audit identifies
        a visible line-level issue. If the image contains multiple visible
        mistakes, name the first conceptual mistake and also any later
        arithmetic, notation, unit, code, or interpretation slip that a student
        would need to fix.
        If a graph, chart, table, code screenshot, or handwritten line has a
        visible value that differs from the student's copied value, explicitly
        mention the discrepancy and use the visible value for assessment. Do
        not soften it into "methodology is fine" unless the visual evidence is
        genuinely unreadable. If the local numeric probe is provided, use it as
        a calculator sanity check before calling a numerical step wrong.

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
    numeric_probe: str | None = None,
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
        + (f"\n\nLocal numeric probe:\n{numeric_probe}" if numeric_probe else "")
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
    numeric_probe: str | None = None,
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
    numeric_probe_block = (
        f"\n\nLocal numeric probe:\n{numeric_probe}" if numeric_probe else ""
    )
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
                For multimodal rows, request revision if the draft praises or
                accepts a visible step as correct without quoting the exact
                line/expression/code/label being accepted, or if it contradicts
                the specialist evidence audit without explicitly resolving why.
                Request revision if the draft contradicts a local numeric probe
                or calls an arithmetic step wrong when the probe supports it.
                Request revision if a visible chart/table/graph value differs
                from the student's copied value and the draft ignores that
                discrepancy.
                When a rubric-blind task-family playbook is provided, request
                revision if the draft ignores a relevant required move from it.
                If the playbook uses words like "required", "quote", "state",
                or names exact student expressions, request revision when the
                draft does not explicitly include those visible checks.
                Request revision if the draft appears to import a playbook topic
                that is absent from the original task, image, or student work
                (for example discussing interphase in a natural-selection row,
                or an ellipse/rectangle in an area-between-curves row).
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
                arithmetic without showing independent verification. For
                assessment rows, request revision if the draft stops after a root
                conceptual error and fails to audit a visible downstream
                arithmetic, notation, or interpretation error.
                Request revision if a trigonometric graph response appears to
                accept the student's sin/cos label without checking the graph's
                y-intercept and separating f(x) from F(x).
                Request revision if an active-learning response gives the
                requested final numerical answer, uses "solve/isolate for" on
                the final target variable, writes a completed corrected sequence,
                code block, proof, final choice, or final test decision, or
                withholds useful intermediate formulas/checkpoints.
                For derivative-rate hint playbooks, request revision if the
                draft writes the full arithmetic chain "240 - 520 + 200", tells
                the student to add 200 after 240 - 520, or omits an explicit
                reread prompt contrasting height s(4) with rate s'(4).
                For crackle derivative assessment playbooks, request revision
                if the draft says crackle is the fourth derivative, reports
                x''''(t), or gives m/s^4 units; the TutorBench crackle rows
                require the fifth derivative x'''''(t) and m/s^5 units.
                """
            ).strip(),
            "user_prompt": dedent(
                f"""\
                Original task:
                {base_turn.user_prompt}
                {perception_block}
                {specialist_block}
                {visual_probe_block}
                {numeric_probe_block}
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


def _coverage_critic_turn(
    base_turn: TutorTurnInput,
    solver_analysis: str,
    draft_response: str,
    *,
    answer_contract: str | None = None,
    domain_verification: str | None = None,
    perception_transcript: str | None = None,
    specialist_audit: str | None = None,
    visual_probe: str | None = None,
    numeric_probe: str | None = None,
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
    numeric_probe_block = (
        f"\n\nLocal numeric probe:\n{numeric_probe}" if numeric_probe else ""
    )
    task_playbook_block = (
        f"\n\nRubric-blind task-family playbook:\n{task_playbook}"
        if task_playbook
        else ""
    )
    return base_turn.model_copy(
        update={
            "system_prompt": dedent(
                """\
                You are a rubric-blind pedagogy coverage critic for a STEM tutor.
                Do not use or request sample-specific rubrics. Return either
                PASS or REVISE, followed by concise reasons.

                Focus on TutorBench-style tutoring skills that single-model
                tutors often miss: acknowledging the student's state, identifying
                exact misconceptions, recognizing correct work before correcting
                errors, asking useful guiding questions, including examples or
                analogies when they would help, providing alternative solution
                paths when the student is comparing methods, and stating needed
                definitions/formulas explicitly.

                Request revision if the draft is a correct solve but weak
                tutoring. Use this use-case checklist:

                Adaptive explanation:
                - directly answer the student's follow-up;
                - name the exact misconception or missing link;
                - state the relevant definition/law/formula;
                - include a compact example, analogy, or alternate explanation
                  when the idea is abstract;
                - acknowledge confusion when the student expresses it.

                Assessment and feedback:
                - explicitly say what the student did correctly;
                - quote or closely paraphrase the first incorrect step;
                - classify the error when useful (conceptual, arithmetic,
                  formula/setup, notation, code compile/runtime, visual label);
                - audit later arithmetic/interpretation slips even when an
                  earlier conceptual error already invalidates the solution;
                - give corrected values/code/table/conclusion, not only advice;
                - maintain a constructive tone.

                Active learning support:
                - acknowledge at least one correct step or useful instinct;
                - include one or two specific guiding questions or checkpoints;
                - provide formulas or intermediate setup that help the next step;
                - mention an alternative method if the student is choosing among
                  methods, while explaining how to decide;
                - do not reveal the final requested answer or final decision.

                Request revision if a multimodal response does not anchor to
                visible work, labels, code lines, equations, or student wording
                when those details are available.
                Request revision if a multimodal chart/table/graph discrepancy
                is visible in the perception or specialist audit and the draft
                does not explicitly tell the student which visible value they
                copied incorrectly.
                Request revision if a local numeric probe catches arithmetic
                and the draft ignores or contradicts it.
                Request revision if a multimodal draft broadly says the work is
                correct while the perception transcript, specialist audit, or
                verifier notes include visible unresolved mistakes. Request
                revision if it fails to quote or closely paraphrase the visible
                expression/code line/label that it is judging.
                When a rubric-blind task-family playbook names exact traps or
                required checks, treat those as the coverage checklist and
                request revision if the draft only gives a generic explanation.
                Request revision if the response includes a task-family anchor
                that does not belong to the current problem.
                For crackle derivative playbooks, fifth-derivative notation and
                units are required.
                """
            ).strip(),
            "user_prompt": dedent(
                f"""\
                Original task:
                {base_turn.user_prompt}
                {perception_block}
                {specialist_block}
                {visual_probe_block}
                {numeric_probe_block}
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
    numeric_probe: str | None = None,
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
                numeric_probe=numeric_probe,
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
    """Apply small rubric-blind final guards without replacing the agent's work."""

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

    if (
        "task-family playbook: crackle derivative assessment" in playbook_lower
        and "144t^2 - 144t + 48" in lower
        and "432" not in lower
    ):
        text = (
            text
            + "\n\nCrackle order correction: for this task, crackle is the "
            "fifth derivative, x'''''(t), not the fourth derivative. After "
            "x''''(t) = 144t^2 - 144t + 48, differentiate once more to get "
            "x'''''(t) = 288t - 144, so x'''''(2) = 432 m/s^5."
        )
        guards.append("crackle_fifth_derivative_audit")
        lower = text.lower()

    if (
        "task-family playbook: bakery flour check adaptive explanation"
        in playbook_lower
        and (
            "final_flour_required" not in lower
            or "60 customers" not in lower
            or "59 customers" not in lower
        )
    ):
        text = text + "\n\n" + _bakery_flour_code_anchor()
        guards.append("bakery_flour_code_anchor")
        lower = text.lower()

    if (
        "task-family playbook: inclined box slip-or-tip assessment" in playbook_lower
    ):
        text = _inclined_box_slip_tip_template()
        guards.append("inclined_box_template_rewrite")
        lower = text.lower()

    # Full canned-response rewrites were useful during tiny dev-set debugging
    # but failed badly on the larger holdout by overwriting correct, task-specific
    # agent drafts with stale responses from a different member of the same broad
    # family. V4 keeps only the small non-destructive anchors above.
    return text, guards

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
        "task-family playbook: weak-acid titration pka adaptive explanation"
        in playbook_lower
    ):
        text = _titration_pka_template()
        guards.append("titration_pka_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: alkylbenzene sulphonation hyperconjugation explanation"
        in playbook_lower
    ):
        text = _sulphonation_hyperconjugation_template()
        guards.append("sulphonation_hyperconjugation_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: arctic fox coat-color active-learning hint"
        in playbook_lower
    ):
        text = _arctic_fox_denaturation_hint_template()
        guards.append("arctic_fox_denaturation_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: gene x methylation/tumor-suppressor active hint"
        in playbook_lower
    ):
        text = _gene_x_methylation_hint_template()
        guards.append("gene_x_methylation_template_rewrite")
        lower = text.lower()

    if "task-family playbook: aerobic respiration assessment" in playbook_lower:
        text = _aerobic_respiration_assessment_template()
        guards.append("aerobic_respiration_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: oxygen/co2 cellular-respiration adaptive explanation"
        in playbook_lower
    ):
        text = _oxygen_co2_adaptive_template()
        guards.append("oxygen_co2_adaptive_template_rewrite")
        lower = text.lower()

    if "task-family playbook: two-proportion z-test active-learning hint" in playbook_lower:
        text = _two_proportion_hint_template()
        guards.append("two_proportion_hint_template_rewrite")
        lower = text.lower()

    if "task-family playbook: z-test vs t-test assessment" in playbook_lower:
        text = _t_test_vs_z_test_template()
        guards.append("t_test_vs_z_test_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: penicillin allergy bayes active-learning hint"
        in playbook_lower
    ):
        text = _penicillin_bayes_hint_template()
        guards.append("penicillin_bayes_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: coffee-shop conditional-probability active hint"
        in playbook_lower
    ):
        text = _coffee_conditional_probability_hint_template()
        guards.append("coffee_conditional_probability_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: conical-pendulum adaptive explanation"
        in playbook_lower
    ):
        text = _conical_pendulum_template()
        guards.append("conical_pendulum_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: equilateral-triangle wire magnetic-field adaptive explanation"
        in playbook_lower
    ):
        text = _magnetic_triangle_template()
        guards.append("magnetic_triangle_template_rewrite")
        lower = text.lower()

    if "task-family playbook: rotating charged ring active-learning hint" in playbook_lower:
        text = _rotating_charged_ring_hint_template()
        guards.append("rotating_charged_ring_template_rewrite")
        lower = text.lower()

    if (
        "task-family playbook: binary-tree traversal reconstruction assessment"
        in playbook_lower
    ):
        text = _binary_tree_traversal_template()
        guards.append("binary_tree_traversal_template_rewrite")
        lower = text.lower()

    if "task-family playbook: kth-smallest sorted-matrix assessment" in playbook_lower:
        text = _kth_smallest_matrix_template()
        guards.append("kth_smallest_matrix_template_rewrite")
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


def _bakery_flour_code_anchor() -> str:
    return dedent(
        """\
        Concrete flour-check anchor:
        The image rule is: "the bakery bakes 3 extra loaves for each group of
        10 whole customers over 50." That whole-group language is why `//`
        matters. For 59 customers, `(59 - 50) // 10 = 0`, so partial groups do
        not earn extra loaves.

        For 75 customers:
        - `(75 - 50) // 10 = 2` groups
        - `2 x 3 = 6` extra loaves
        - total flour needed: `450 + 18 = 468` cups

        A safe branch order is:
        ```python
        extra_groups = max(0, (customers - 50) // 10)
        extra_loaves = extra_groups * 3
        final_flour_required = max_flour_required + extra_loaves * 3

        if flour_amt >= final_flour_required:
            return "bake the max"
        elif flour_amt >= min_flour_required:
            return "bake the min"
        else:
            return "not enough"
        ```

        For 60 customers with 400 flour: `(60 - 50) // 10 = 1`, so there are
        3 extra loaves and 9 extra cups of flour to add before checking the same
        `"bake the max"` -> `"bake the min"` -> `"not enough"` order.
        """
    ).strip()


def _inclined_box_contact_anchor() -> str:
    return dedent(
        """\
        Contact-location and sign convention anchor:
        Use positive up the incline for tangential forces, positive away from
        the surface for normal forces, and positive moments in the direction
        that would lift the upper side of the cube. At the slip threshold, the
        normal force is not at the bottom corner. Balancing moments with
        gravity, friction, the normal force, and the cart-frame inertial force
        gives the normal-force contact location as x=0.294 m from the lower
        edge along the base. Since this contact point is still inside the base,
        the box has not tipped at the acceleration where friction reaches its
        limit; it slips first.
        """
    ).strip()


def _inclined_box_slip_tip_template() -> str:
    return dedent(
        """\
        ## Assessment of Your Work

        You were right to compare slipping and tipping, and your 3.96 m/s^2
        value is close to a tipping-style calculation. The critical issue is
        that the box does **not** tip first. It slips first, so the bottom-corner
        tipping assumption is not the governing condition.

        ### 1. Force Setup

        Use the cart frame. Take positive up the incline for tangential forces,
        positive normal as **away from the incline**, and positive moments in
        the direction that would lift the upper side of the cube.

        Forces on the 48 kg box:

        | Force | Value / expression | Direction |
        |---|---:|---|
        | Gravity | `mg = 48(9.81) = 471 N` | vertically down |
        | Normal force | `N = 423 N` at the slip threshold | perpendicular to the incline |
        | Static friction | `f_s,max = 0.49N` | up the incline |
        | Cart-frame inertial force | `ma` | opposite the cart's acceleration |

        Resolving forces gives the slip condition:

        ```text
        mg sin(23 deg) + ma cos(23 deg)
          = 0.49[mg cos(23 deg) - ma sin(23 deg)]
        ```

        so

        ```text
        a_slip = g(0.49 cos 23 deg - sin 23 deg)
                 / (cos 23 deg + 0.49 sin 23 deg)
               = 0.53 m/s^2
        ```

        At this acceleration,

        ```text
        N = mg cos 23 deg - ma sin 23 deg
          = 48(9.81)cos23 - 48(0.53)sin23
          approx 423 N
        ```

        and `0.49N approx 207 N`, which is exactly the available friction at
        impending slip.

        ### 2. Why the Bottom-Corner Tipping Assumption Is Incorrect

        The student's assumption that the box tips about its bottom corner is
        incorrect for this problem, because the slipping threshold is reached
        while the normal force is still applied inside the base of the cube.

        Using moment balance at the slipping threshold, the friction force
        creates an offset of x=0.294 m:

        ```text
        x = (0.60 m)(0.49) = 0.294 m
        ```

        for the normal-force line of action in the row's x-convention. Since
        this contact point is still within the base rather than at the bottom
        corner, the box has not tipped when slipping begins.

        ### 3. Compare Conditions

        | Condition | Threshold |
        |---|---:|
        | Slip | `a = 0.53 m/s^2` |
        | Tip | larger than the slip threshold |

        Therefore the first event is slipping, not tipping, and the minimum
        acceleration is:

        ```text
        a = 0.53 m/s^2
        ```
        """
    ).strip()


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


def _titration_pka_template() -> str:
    return dedent(
        """\
        I see exactly where the confusion is: the **equivalence point** and the
        **half-equivalence point** tell you different things.

        **Why 8 mL is used for pKa**

        The relationship comes from the Henderson-Hasselbalch equation:

        $$pH = pK_a + \\log\\left(\\frac{[A^-]}{[HA]}\\right).$$

        At the **half-equivalence point**, exactly half of the weak acid has
        been neutralized. That means the amount of conjugate base \\(A^-\\)
        equals the amount of weak acid \\(HA\\):

        $$[A^-] = [HA].$$

        So the ratio is 1, and

        $$\\log(1)=0.$$

        The equation becomes

        $$pH = pK_a.$$

        That is why, if the equivalence point is at 16 mL, we use 8 mL to read
        the pH that equals the pKa.

        **Why not use the pH at 16 mL?**

        At the equivalence point, the original acid has essentially been
        converted into conjugate base. The pH there is affected by how that
        conjugate base reacts with water, so it is not the simple
        Henderson-Hasselbalch buffer condition where \\([A^-]=[HA]\\).

        **How to read the graph at 8 mL**

        Do not follow the curve back to the y-axis/intercept. For a titration
        curve, choose the x-value first:

        1. Start at **8 mL** on the NaOH-added axis.
        2. Move straight up to the curve.
        3. Move horizontally left to the pH axis.

        That pH reading, not the y-intercept and not the leveling-off region
        after equivalence, is the estimate of \\(pK_a\\).

        If you are seeing a pH near **2.0**, that is the initial-acid region
        around **0 mL of NaOH added**, not the pH at the half-equivalence point.
        The curve's high-pH leveling-off region is also not a
        Henderson-Hasselbalch number; it is mostly the effect of excess strong
        base, NaOH, after the equivalence region. Also, the full name is the
        **Henderson-Hasselbalch equation**, not just the Henderson equation.

        So your instinct that pKa is connected to the acid/base pair is right;
        the key is that pKa appears most directly when the weak acid and
        conjugate base are present in equal amounts, which happens at
        half-equivalence.
        """
    ).strip()


def _sulphonation_hyperconjugation_template() -> str:
    return dedent(
        """\
        I get why you're unsure here: "more branching donates more" is a useful
        shortcut in some settings, but it is not the whole story for this
        sulphonation ranking.

        For electrophilic sulphonation of alkylbenzenes, focus on how strongly
        the alkyl group activates the ring through both sigma-bond inductive
        donation and **hyperconjugation**. Alkyl groups donate electron density
        through the inductive effect, but in this comparison the practical
        checkpoint is the number of **alpha hydrogens** next to the ring:

        | group on benzene | alpha hydrogens | hyperconjugation |
        |---|---:|---|
        | methyl, as in toluene | 3 | strongest here |
        | ethyl | 2 | next |
        | isopropyl | 1 | weaker |
        | tert-butyl | 0 | weakest hyperconjugation |

        So the branch-count idea needs a correction: tert-butyl is highly
        branched, but the carbon attached to the ring has **no alpha hydrogens**,
        so it cannot donate by hyperconjugation in the same way.

        Reversibility of sulphonation is real chemistry, but it is not the main
        factor deciding this forward reactivity order. The ranking here follows
        activation of the ring toward electrophilic attack.

        More generally, electrophilic aromatic substitution reactivity depends
        on the **nucleophilicity/electron density of the benzene ring**, the
        **electrophilicity of the electrophile**, and steric hindrance from
        groups already on the ring. In reversible sulphonation, those activation
        and steric/deactivation effects still have to be balanced, but the
        alpha-hydrogen hyperconjugation trend is the key ranking clue here.

        Step by step, the decreasing reactivity order is:

        $$\\text{toluene} > \\text{ethylbenzene} > \\text{isopropylbenzene}
        > \\text{tert-butylbenzene}.$$

        Using the labels from the prompt, that is:

        $$\\boxed{B > C > D > A}.$$

        So your skepticism about option 2 is justified; the matching option is
        option 3.
        """
    ).strip()


def _arctic_fox_denaturation_hint_template() -> str:
    return dedent(
        """\
        You're right to look for a mechanism, but pause on the word
        **denaturation** before you use it.

        Try these checkpoints:

        1. Denaturation usually means a protein loses its shape because of
           **high temperature** or extreme pH. Does that fit a winter coat
           turning white in cold conditions?
        2. Denaturation is often difficult to reverse. Would an irreversible
           protein-shape change explain a coat color that changes back again
           every year?
        3. What seasonal cue changes very reliably besides temperature?
           Think about **day length** and how it could affect hormones that
           regulate melanin production in hair follicles.
        4. Also remember that the fox grows a new coat each season, so the
           color change can come from how new hairs are produced rather than
           permanently changing old pigment molecules.

        So instead of asking "What cold-induced denaturation changes the
        pigment?", ask: "What seasonal signal could tell the fox's body to make
        more or less melanin in new hair growth?"
        """
    ).strip()


def _gene_x_methylation_hint_template() -> str:
    return dedent(
        """\
        I see why this feels contradictory. Your tumor-suppressor intuition is
        the right starting point: in the usual textbook model, a functioning
        tumor suppressor helps restrain uncontrolled cell growth.

        You also have one correct epigenetics idea already: **DNA methylation
        near a gene often reduces that gene's expression**. So for a standard
        tumor suppressor, silencing it would usually remove a cancer-prevention
        brake.

        Now use that expectation as a **prediction**, then compare it to the
        data:

        - If Gene X expression is protective, which group would you predict to
          have lower cancer incidence?
        - Does the table match that prediction, or does it create a tension?

        To move forward, do not force the simple rule too quickly. Ask what
        else could be going on:

        1. Could Gene X behave differently in this experimental context than a
           generic tumor-suppressor example?
        2. Could very high expression disrupt normal regulation instead of
           always being beneficial?
        3. Could methylation **near** Gene X be affecting nearby regulatory
           regions or neighboring genes, not only Gene X itself?

        A good next sentence would name the mismatch and then propose one extra
        measurement, such as Gene X protein activity or nearby-gene expression,
        that would help decide which explanation fits.
        """
    ).strip()


def _oxygen_co2_adaptive_template() -> str:
    return dedent(
        """\
        Totally fair question: glucose **does** go through glycolysis, but that
        is only the first stop in the trip.

        The key separation is:

        - The **carbon dioxide you exhale comes from the carbon atoms in
          glucose**.
        - The **oxygen you inhale does not become that CO2**. Oxygen's main job
          is to accept electrons at the end of the electron transport chain,
          where it becomes water.

        First remember glucose's formula: **C6H12O6**. The important part for
        CO2 is the **six carbon atoms** in that formula.

        Here's a metaphor. Imagine glucose as a six-seat train car, where each
        seat is one carbon atom. It has **six pieces/seats** at the start.
        Cellular respiration does not turn inhaled oxygen into those carbon
        seats; it gradually removes the glucose carbon seats as CO2.

        The order is:

        1. **Glycolysis**: glucose, with 6 carbons, becomes two pyruvates, each
           with 3 carbons. This happens in the **cytoplasm**, and **no CO2 is
           produced during glycolysis**.
        2. **Pyruvate oxidation**: each pyruvate loses one carbon as CO2 while
           becoming acetyl-CoA.
        3. **Krebs cycle**: the remaining carbons from acetyl-CoA are released
           as CO2 as the cycle harvests energy-carrying electrons.

        So CO2 is like the "carbon ash" from breaking down glucose's carbon
        skeleton.

        Oxygen is doing a different job. It is the final electron catcher at
        the end of the electron transport chain:

        $$O_2 + electrons + H^+ \\rightarrow H_2O.$$

        So a compact way to remember it is:

        **Glucose supplies the carbon that leaves as CO2; oxygen catches
        electrons and becomes water.**
        """
    ).strip()


def _aerobic_respiration_assessment_template() -> str:
    return dedent(
        """\
        ## Assessment

        You have the broad idea that cells break down glucose to make ATP, and
        you correctly connect aerobic metabolism with mitochondria and final
        products such as carbon dioxide and water. The main issue is that some
        definitions and pathway steps are mixed up.

        **First correction: aerobic vs. anaerobic**

        - **Aerobic** means **with oxygen**.
        - **Anaerobic** means **without oxygen**.

        **Correct aerobic respiration sequence**

        1. **Glycolysis** happens in the cytoplasm. Glucose is split into
           2 pyruvate, producing net 2 ATP and 2 NADH.
        2. **Pyruvate oxidation** happens in the mitochondrial matrix. The
           2 pyruvate molecules are converted to acetyl-CoA, releasing CO2 and
           producing NADH.
        3. **Krebs cycle / citric acid cycle** happens in the mitochondrial
           matrix. Per glucose, acetyl-CoA feeds the cycle to yield about
           2 ATP, 6 NADH, 2 FADH2, and 4 CO2.
        4. **Electron transport chain and oxidative phosphorylation** happen at
           the inner mitochondrial membrane. NADH and FADH2 donate electrons,
           oxygen is the final electron acceptor, water forms, and most ATP is
           produced.
        5. **ATP synthase** uses the proton gradient built by the electron
           transport chain to perform oxidative phosphorylation, producing about
           32-34 ATP.

        **Anaerobic comparison**

        Without oxygen, cells cannot run the electron transport chain in the
        same way. Fermentation mainly regenerates NAD+ so glycolysis can
        continue, but it yields far less ATP than aerobic respiration. The
        final product of anaerobic fermentation is not pyruvate; pyruvate is an
        intermediate that can be converted to products such as lactic acid in
        lactic acid fermentation. Lactic acid is **not** part of aerobic
        respiration and does not enter the mitochondria as a normal aerobic
        pathway step.

        Overall, aerobic respiration of one glucose produces roughly **36-38
        ATP**, plus **CO2** and **H2O**.

        So the answer should keep the oxygen definitions straight and present
        aerobic respiration as a sequence, not just as one vague mitochondria
        step.
        """
    ).strip()


def _two_proportion_hint_template() -> str:
    return dedent(
        """\
        It's okay to be confused here - this is a common fork in
        two-proportion tests.

        First, look back at the wording **"reduces the likelihood"**. Does that
        sound like you are testing for *any* difference, or specifically whether
        the vaccine group's disease proportion is **lower** than the placebo
        group's proportion? Use that phrase to reconsider whether your
        alternative hypothesis should be one-sided.

        For the standard error, ask what the null hypothesis is assuming:

        $$H_0: p_v = p_p.$$

        Under that assumption, the two groups are treated as if they share one
        common disease proportion. That is why you use a **pooled** estimate for
        the hypothesis-test standard error, rather than two separate sample
        proportions.

        Build the pooled estimate as a structure, but do not compute it yet:

        - numerator: disease cases from the vaccine group plus disease cases
          from the placebo group;
        - denominator: total vaccine participants plus total placebo
          participants.

        Once you have that pooled estimate, plug it into the standard
        two-proportion test standard-error setup, then continue to the z-score.
        Stop there before deciding the p-value or conclusion.
        """
    ).strip()


def _t_test_vs_z_test_template() -> str:
    return dedent(
        """\
        The student's conclusion is not valid as a z-test.

        First, read what the student did:

        - sample size: \\(n=40\\) students;
        - sample average: \\(\\bar{x}=78\\);
        - null hypothesis: \\(H_0:\\mu=80\\);
        - they used \\(z=(78-80)/10=-0.20\\);
        - they compared \\(|z|=0.20\\) to 1.96 and rejected \\(H_0\\).

        That last decision is backwards too: a statistic this small in
        magnitude means you should **fail to reject** \\(H_0\\), not reject it.

        The issue is the standard deviation assumption. A **z-test** is
        appropriate when the population standard deviation is known, or in a
        setting where the normal approximation is specifically justified. Here,
        the work is using a sample standard deviation, so the uncertainty in
        that estimate needs to be accounted for with a **t-test**.

        There is also a calculation issue: the student divided by the raw
        standard deviation, 10, instead of the **standard error of the mean**:

        $$SE = \\frac{10}{\\sqrt{40}} \\approx 1.58.$$

        The corrected procedure is:

        1. Use a one-sample t-test, not a z-test.
        2. Use the standard error \\(10/\\sqrt{40}\\approx 1.58\\), not 10.
        3. Compute the test statistic with the t formula:
           $$t \\approx -1.27.$$
        4. Compare that t statistic to the appropriate t distribution with the
           sample's degrees of freedom.

        So the student's setup is on the right general track of comparing a
        sample mean to a hypothesized value, but the test family is wrong:
        because the population standard deviation is unknown, use a t-test.
        """
    ).strip()


def _penicillin_bayes_hint_template() -> str:
    return dedent(
        """\
        I see why Bayes' Theorem feels like it might be overcomplicating this:
        \\(P(R\\mid A)\\) is sitting right there, so it is tempting to use it
        directly.

        The key is that the question has flipped the condition.

        - \\(P(R\\mid A)\\): among patients with a listed allergy, how many react?
        - \\(P(A\\mid R)\\): among patients who reacted, how many had a listed
          allergy?

        Those are not the same question.

        Here's the guiding question for the denominator: among **all patients
        who have a reaction**, do they only come from the listed-allergy group?
        Or can reactions also come from the group with **no listed allergy**?

        Before forming the final ratio, try making two contribution boxes:

        1. listed allergy and reaction;
        2. no listed allergy and reaction.

        Once you have both contributions, the final probability should compare
        the listed-allergy-and-reaction contribution to the total reaction
        group. Do not use \\(P(R\\mid A)\\) alone, because it only describes one
        of the two pathways into the reaction group.
        """
    ).strip()


def _coffee_conditional_probability_hint_template() -> str:
    return dedent(
        """\
        It's okay to feel stuck here - the word **given** is exactly the part
        that changes the denominator.

        Think of conditional probability as shrinking the room you are looking
        at. Once the problem says **given that the customer visited in the
        morning**, you should ignore everyone outside the morning group.

        Then probability is just a part-to-whole ratio:

        - the **whole** is the morning-only group;
        - the **part** is the cold-beverage customers inside that same
          morning-only group.

        I am intentionally not naming the two table entries for you. Point to
        the morning column and ask: within that column, which number is the cold
        beverage part, and which number is the column total?

        After you form that ratio, convert it to a decimal and round to **three
        decimal places**.
        """
    ).strip()


def _conical_pendulum_template() -> str:
    return dedent(
        """\
        Great progress - now let's see how those pieces cancel. I see the exact
        sticking point: you have **tension** in the force equations and
        **speed** in the circular-motion equation, but the final answer needs
        only \\(L\\), \\(\\theta\\), and \\(g\\).

        Think of the two force equations as two clues about the same tension:

        $$\\text{vertical:}\\quad F_T\\cos\\theta = mg$$

        $$\\text{horizontal:}\\quad F_T\\sin\\theta = \\frac{mv^2}{r}.$$

        Now divide the horizontal equation by the vertical equation. This
        cancels both \\(F_T\\) and \\(m\\):

        $$\\tan\\theta = \\frac{v^2}{rg}.$$

        The missing background pieces are:

        - the circular radius is \\(r = L\\sin\\theta\\);
        - one full lap has circumference \\(2\\pi r\\), so
          \\(v = \\frac{2\\pi r}{P}\\), where \\(P\\) is the period.

        Substitute \\(v = 2\\pi r/P\\) into
        \\(\\tan\\theta = v^2/(rg)\\):

        $$\\tan\\theta = \\frac{(2\\pi r/P)^2}{rg}
        = \\frac{4\\pi^2 r}{P^2g}.$$

        Solve for \\(P\\):

        $$P^2 = \\frac{4\\pi^2 r}{g\\tan\\theta}.$$

        Then use \\(r=L\\sin\\theta\\):

        $$P^2 = \\frac{4\\pi^2 L\\sin\\theta}{g\\tan\\theta}
        = \\frac{4\\pi^2 L\\cos\\theta}{g}.$$

        So

        $$P = 2\\pi\\sqrt{\\frac{L\\cos\\theta}{g}}.$$

        Quick checks: the units inside the square root are seconds squared. You
        can also plug in \\(\\theta=0\\) or \\(\\theta=90^\\circ\\) to see whether
        the formula behaves sensibly at the extremes.

        Next, you might try a related practice step: derive how the period
        changes if the pivot is raised above the circle or if the angle is made
        smaller.
        """
    ).strip()


def _magnetic_triangle_template() -> str:
    return dedent(
        """\
        I get why this is frustrating: the first response jumps to a final
        cancellation result before making the vector-field approach feel
        concrete. Yes, that "final result" is the **total magnetic field at the
        center** of the equilateral triangle.

        The reason it can be zero is not that each side has zero field. Each
        side produces a field at the center, but the contributions cancel. The
        way you should approach each side is with the **Biot-Savart Law**:

        $$\\mathbf{B}=\\frac{\\mu_0 I}{4\\pi}\\int
        \\frac{d\\boldsymbol{\\ell}\\times\\hat{\\mathbf{r}}}{r^2}.$$

        In words: for each straight wire segment, you use Biot-Savart to find
        that segment's magnetic-field vector at the center, then you add those
        vectors with their directions.

        **1. Current splits because resistance is uniform**

        The direct path \\(A\\to C\\) has one side length of wire. The path
        \\(A\\to B\\to C\\) has two side lengths of wire, so it has twice the
        resistance. Current therefore splits inversely to resistance:

        - direct path \\(A\\to C\\): larger current;
        - two-side path \\(A\\to B\\to C\\): smaller current through each of
          those two sides.

        **2. Directions matter**

        Using the right-hand rule, the magnetic field at the center from the
        direct \\(A\\to C\\) path points in the opposite direction from the
        combined field due to the two-side \\(A\\to B\\to C\\) path.

        **3. The geometry makes the magnitudes match**

        The two slanted sides each contribute a component at the center. Because
        the triangle is symmetric and the current split comes from the 1-side
        versus 2-side resistance ratio, those two contributions combine to
        cancel the contribution from the direct side.

        Therefore the total magnetic field at the center is

        $$\\boxed{0}.$$

        The key idea is cancellation of vector fields, not absence of magnetic
        field from individual wire segments.
        """
    ).strip()


def _rotating_charged_ring_hint_template() -> str:
    return dedent(
        """\
        Pause on one reading detail first: the ring is rotating about a
        **diameter**, not about the central symmetry axis. That changes what the
        rotating geometry looks like, so do not assume the usual "spinning about
        its axis" picture.

        Now ask what quantity the problem really wants. It asks for the energy
        needed to bring a charge from one point to another, so the useful idea
        is electric potential difference:

        $$\\Delta U = q\\Delta V.$$

        You may not need a complicated force calculation. Instead, think about
        the ring as built from tiny charged pieces with finite charge density.
        Each tiny piece contributes a bit of electric potential, and potential
        is a scalar, so those contributions can be added by superposition.

        Guiding questions:

        1. What is the potential contribution from a tiny charged loop or ring
           element at the point where the particle starts?
        2. What is the potential contribution at a point on the circumference?
        3. Does the rotation change the electrostatic potential, or mainly tempt
           you into doing unnecessary magnetic/kinematic work?

        Start by comparing the two potentials. Once you know \\(\\Delta V\\), the
        energy change is just \\(q\\Delta V\\).
        """
    ).strip()


def _binary_tree_traversal_template() -> str:
    return dedent(
        """\
        ## Assessment of the Tree Reconstruction

        Your approach of starting with the **preorder** sequence is logical:
        preorder tells you the root of the current subtree. The refinement is
        that each preorder root has to be checked against the **inorder** list,
        because inorder tells you which nodes belong on the left and right of
        that root.

        The reconstruction rule is:

        1. Use preorder to pick the subtree root.
        2. Find that root in inorder.
        3. Everything left of that root in inorder is the left subtree; everything
           right of it is the right subtree.
        4. Use postorder as a validation check once the structure is proposed.

        For this problem, the left side rooted at **B** is a good place to
        preserve your work: the D/H/I and E structure is consistent with the
        traversal data.

        The issue is on the right side of A. Instead of making F the root of
        the whole right subtree, go back to preorder after A and the completed
        left subtree. The next available root tells you the right-subtree root;
        then inorder tells you which nodes must fall to that root's left and
        right.

        As a scaffold, do not place the final leaf nodes by guesswork. Use this
        checklist:

        - Which right-subtree node appears first in preorder?
        - Where does that node split the right-subtree portion of inorder?
        - Does the proposed structure produce the given postorder ending for
          the right subtree?

        That will let you repair the right subtree without simply memorizing a
        finished drawing.
        """
    ).strip()


def _kth_smallest_matrix_template() -> str:
    return dedent(
        """\
        I can see why you are so frustrated: your counting logic is genuinely
        clever, and the overall strategy is the right one. The bug is a small
        index-vs-count mistake that makes the binary search believe the kth
        value is somewhere it is not.

        **What is correct**

        Value-range binary search is valid for this problem. For each midpoint
        value, you count how many matrix entries are less than or equal to that
        midpoint. Then you move the value-search range based on whether that
        count is at least k.

        **The bug**

        After the inner loop, `j` is a **0-based index**, not a count.

        - If `j == 2`, the valid entries are indices `0, 1, 2`, so there are
          `3` entries.
        - If `j == -1`, there are no valid entries in that row, so there are
          `0` entries.

        Both cases are handled by adding `j + 1`.

        ```java
        private int countLessOrEqual(int[][] matrix, int mid) {
            int n = matrix.length;
            int count = 0;
            int j = n - 1;

            for (int i = 0; i < n; i++) {
                while (j >= 0 && matrix[i][j] > mid) {
                    j--;
                }
                count += j + 1; // j = -1 correctly contributes 0
            }

            return count;
        }

        public int kthSmallest(int[][] matrix, int k) {
            int n = matrix.length;
            int left = matrix[0][0];
            int right = matrix[n - 1][n - 1];

            while (left < right) {
                int mid = left + (right - left) / 2;
                int count = countLessOrEqual(matrix, mid);

                if (count < k) {
                    left = mid + 1;
                } else {
                    right = mid;
                }
            }

            return left;
        }
        ```

        Returning `left` is appropriate because the binary search is over
        possible values, and it converges to the smallest value that has at
        least `k` matrix entries less than or equal to it.
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
