"""Candidate tutor strategies."""

from __future__ import annotations

from textwrap import dedent
from uuid import uuid4

from tutorbench_lab.constants import (
    AGENT_PROMPT_VERSION,
    DATASET_REVISION,
    DEFAULT_CRITIC_MODEL,
    DEFAULT_MAX_REVISION_ATTEMPTS,
    DEFAULT_PLANNER_MODEL,
    DEFAULT_SOLVER_MODEL,
    DEFAULT_VERIFIER_MODEL,
)
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
    planner_model: str = DEFAULT_PLANNER_MODEL,
    verifier_model: str = DEFAULT_VERIFIER_MODEL,
    critic_model: str = DEFAULT_CRITIC_MODEL,
    max_tokens: int = 1600,
    max_revision_attempts: int = DEFAULT_MAX_REVISION_ATTEMPTS,
) -> tuple[TutorTurnInput, TutorResponse]:
    """Run the rubric-blind agentic tutor pipeline.

    The pipeline intentionally never sees sample-specific rubrics. It uses
    generic TutorBench-derived tutoring skills, then asks a rubric-blind critic
    whether the draft is complete, calibrated, and safe.
    """

    base_turn = build_turn_input(example, prompt_version=AGENT_PROMPT_VERSION)
    solver_client = make_client(solver_model)
    planner_client = make_client(planner_model)
    verifier_client = make_client(verifier_model)
    composer_client = make_client(composer_model)
    critic_client = make_client(critic_model)

    stage_results: list[tuple[str, GenerateResult]] = []

    def remember(stage: str, result: GenerateResult) -> GenerateResult:
        stage_results.append((stage, result))
        return result

    route_plan = {
        "perception": base_turn.image.present,
        "specialist_audit": _needs_specialist_audit(base_turn),
        "max_revision_attempts": max_revision_attempts,
    }
    visual_probe = (
        build_visual_probe(base_turn.image) if route_plan["specialist_audit"] else None
    )

    perception_result = None
    if base_turn.image.present:
        perception_turn = _perception_turn(base_turn)
        perception_result = remember(
            "perception",
            solver_client.generate(perception_turn, max_tokens=900),
        )

    specialist_audit_result = None
    if route_plan["specialist_audit"]:
        specialist_audit_turn = _specialist_audit_turn(
            base_turn,
            perception_transcript=perception_result.text if perception_result else None,
            visual_probe=visual_probe,
        )
        specialist_audit_result = remember(
            "specialist_audit",
            verifier_client.generate(specialist_audit_turn, max_tokens=1200),
        )

    solver_turn = _solver_turn(
        base_turn,
        perception_transcript=perception_result.text if perception_result else None,
        specialist_audit=specialist_audit_result.text
        if specialist_audit_result
        else None,
        visual_probe=visual_probe,
    )
    solver_result = remember(
        "solver",
        solver_client.generate(solver_turn, max_tokens=max_tokens),
    )

    contract_turn = _contract_turn(
        base_turn,
        solver_result.text,
        perception_transcript=perception_result.text if perception_result else None,
        specialist_audit=specialist_audit_result.text
        if specialist_audit_result
        else None,
        visual_probe=visual_probe,
    )
    contract_result = remember(
        "planner",
        planner_client.generate(contract_turn, max_tokens=1000),
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
    )
    verification_result = remember(
        "domain_verifier",
        verifier_client.generate(verification_turn, max_tokens=1200),
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
    )
    composer_result = remember(
        "composer",
        composer_client.generate(composer_turn, max_tokens=max_tokens),
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
        )
        critic_result = remember(
            f"critic_{attempt_index}",
            critic_client.generate(critic_turn, max_tokens=900),
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
        )
        revision_result = remember(
            f"revision_{attempt_index + 1}",
            composer_client.generate(revision_turn, max_tokens=max_tokens),
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
        text=final_text.strip(),
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
            "visual_probe": visual_probe,
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
) -> TutorTurnInput:
    perception_block = (
        f"\n\nPerception transcript:\n{perception_transcript}"
        if perception_transcript
        else ""
    )
    visual_probe_block = f"\n\nLocal visual probe:\n{visual_probe}" if visual_probe else ""
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
        Treat misspelled identifiers as compile-risk issues and tell the
        student to fix them, even if the current snippet appears internally
        consistent.

        For diagram-label assessment, correct the label-marker mapping as
        drawn. The marker endpoint is the ground truth. If marker 1 points
        to cytoplasm, say marker 1 should be labeled cytoplasm; do not only
        tell the student to move the marker to match their written label.
        For plant/animal cell diagrams, remember: lightly colored interior
        fill is cytoplasm, thin outline/inner boundary is cell membrane,
        thick yellow/gold outer border is cell wall, green ovals are
        chloroplasts, large pale central oval is vacuole, dark teal oval is
        nucleus, and small pink ovals are mitochondria.
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

                The answer contract is advisory. If it is too withholding for an
                assessment row, request revision. Assessment feedback should show
                corrected values, corrected code, or correction tables when those
                are the point of the task.

                Request revision if an adaptive response pivots away from the
                conversation instead of answering the student's follow-up. Request
                revision if a code assessment omits line numbers, corrected code,
                expected output, extra tests, or edge cases. Request revision if
                a diagram assessment does not include a numbered correction
                table for the marker endpoints as drawn, or if it only tells the
                student to move arrows to preserve wrong labels. Request revision
                if a calculus/physics/statistics answer affirms a student's
                arithmetic without showing independent verification.
                Request revision if an active-learning response gives the
                requested final numerical answer, uses "solve/isolate for" on
                the final target variable, or withholds useful intermediate
                formulas/checkpoints.
                """
            ).strip(),
            "user_prompt": dedent(
                f"""\
                Original task:
                {base_turn.user_prompt}
                {perception_block}
                {specialist_block}
                {visual_probe_block}

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
