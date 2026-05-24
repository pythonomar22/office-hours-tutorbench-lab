"""Rubric-blind LLM selector for candidate tutor responses."""

from __future__ import annotations

import json
import re
import time
from datetime import UTC, datetime
from textwrap import dedent
from typing import Any, Literal

from pydantic import BaseModel, Field

from tutorbench_lab.providers import make_client
from tutorbench_lab.schemas import ModelUsage, RunRecord, Strategy, TutorTurnInput

_JSON_BLOCK_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)

SelectedSource = Literal["primary", "auxiliary"]


class SelectorDecision(BaseModel):
    """Structured response from the rubric-blind selector."""

    selected_source: SelectedSource
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str = ""


def select_run_record(
    primary: RunRecord,
    auxiliary: RunRecord,
    *,
    run_id: str,
    selector_model: str,
    max_tokens: int = 700,
    request_timeout_s: float | None = None,
    max_parse_attempts: int = 1,
) -> RunRecord:
    """Select one of two candidate responses without using rubrics or ratings."""

    if primary.example.task_id != auxiliary.example.task_id:
        raise ValueError(
            f"task ID mismatch: {primary.example.task_id} != "
            f"{auxiliary.example.task_id}"
        )

    client = make_client(selector_model, timeout_s=request_timeout_s)
    turn = build_selector_turn(primary, auxiliary)
    errors: list[str] = []
    total_latency_ms = 0
    last_text = ""
    last_usage = ModelUsage()
    for attempt in range(max_parse_attempts + 1):
        start = time.monotonic()
        result = client.generate(turn, max_tokens=max_tokens)
        total_latency_ms += int((time.monotonic() - start) * 1000)
        last_text = result.text
        last_usage = result.usage
        try:
            decision = parse_selector_decision(result.text)
        except ValueError as exc:
            errors.append(f"attempt {attempt + 1}: {exc}")
            continue
        return _selected_record(
            primary,
            auxiliary,
            decision=decision,
            run_id=run_id,
            selector_model=selector_model,
            selector_latency_ms=total_latency_ms,
            selector_usage=last_usage,
            raw_selector_output=result.text,
        )

    fallback = SelectorDecision(
        selected_source="primary",
        confidence=0.0,
        reason="selector JSON parse failed; conservatively selected primary",
    )
    return _selected_record(
        primary,
        auxiliary,
        decision=fallback,
        run_id=run_id,
        selector_model=selector_model,
        selector_latency_ms=total_latency_ms,
        selector_usage=last_usage,
        raw_selector_output=last_text,
        selector_errors=errors,
    )


def build_selector_turn(primary: RunRecord, auxiliary: RunRecord) -> TutorTurnInput:
    """Build the selector prompt from task context and two candidate responses."""

    example = primary.example
    user_prompt = dedent(
        f"""\
        TutorBench task context:
        - use_case: {example.use_case.value}
        - subject: {example.subject}
        - modality: {example.modality.value}

        Original task:
        {primary.turn_input.user_prompt}

        Candidate PRIMARY:
        {primary.response.text}

        Candidate AUXILIARY:
        {auxiliary.response.text}

        Choose the better final tutor response for this task. Use only the task
        context, the image if present, and general tutoring-quality principles.
        Do not infer or use sample-specific rubrics.

        Return strict JSON only:
        {{
          "selected_source": "primary",
          "confidence": 0.83,
          "reason": "one concise sentence"
        }}
        """
    ).strip()

    return TutorTurnInput(
        task_id=example.task_id,
        use_case=example.use_case,
        modality=example.modality,
        subject=example.subject,
        system_prompt=dedent(
            """\
            You are a rubric-blind selector for AI tutor responses.

            Your job is to choose which of two candidate tutor responses is more
            likely to satisfy a human tutoring benchmark. You never see or use
            sample-specific rubrics. Prefer the response that is more correct,
            more directly responsive to the student's actual confusion/work,
            better calibrated to the use case, and better grounded in the image
            when one is present.

            Use-case priorities:
            - adaptive explanation: answer the follow-up directly, explain the
              student's misconception, stay focused on their confusion, and do
              not redo the whole original problem unnecessarily.
            - assessment: identify correct and incorrect student steps, name
              error types, and provide corrected reasoning or calculations.
            - active learning: give enough scaffolding for the next step while
              avoiding the final requested answer.

            Penalize responses that contradict visible work, ignore the image,
            over-answer active-learning tasks, under-answer assessment tasks, or
            give generic encouragement without the needed content.
            Return strict JSON only.
            """
        ).strip(),
        user_prompt=user_prompt,
        image=example.image,
        prompt_version="selector-v1",
    )


def parse_selector_decision(raw: str) -> SelectorDecision:
    payload = _load_json(raw)
    if not isinstance(payload, dict):
        raise ValueError("selector output must be a JSON object")
    try:
        return SelectorDecision.model_validate(payload)
    except Exception as exc:
        raise ValueError(f"invalid selector decision: {exc}") from exc


def _selected_record(
    primary: RunRecord,
    auxiliary: RunRecord,
    *,
    decision: SelectorDecision,
    run_id: str,
    selector_model: str,
    selector_latency_ms: int,
    selector_usage: ModelUsage,
    raw_selector_output: str,
    selector_errors: list[str] | None = None,
) -> RunRecord:
    selected = primary if decision.selected_source == "primary" else auxiliary
    record = selected.model_copy(deep=True)
    response = record.response.model_copy(deep=True)
    response.model = f"selector:{primary.response.model}|{auxiliary.response.model}"
    response.strategy = Strategy.AGENTIC
    response.prompt_version = "selector-v1"
    response.trace = {
        **dict(response.trace),
        "selector_model": selector_model,
        "selector_selected_source": decision.selected_source,
        "selector_confidence": decision.confidence,
        "selector_reason": decision.reason,
        "selector_latency_ms": selector_latency_ms,
        "selector_usage": selector_usage.model_dump(mode="json"),
        "selector_primary_run_id": primary.run_id,
        "selector_auxiliary_run_id": auxiliary.run_id,
        "selector_primary_prompt_version": primary.response.prompt_version,
        "selector_auxiliary_prompt_version": auxiliary.response.prompt_version,
        "raw_selector_output": raw_selector_output,
    }
    if selector_errors:
        response.trace["selector_errors"] = selector_errors
    record.run_id = run_id
    record.created_at = datetime.now(UTC)
    record.response = response
    return record


def _load_json(raw: str) -> Any:
    text = raw.strip()
    match = _JSON_BLOCK_RE.search(text)
    if match:
        text = match.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc
