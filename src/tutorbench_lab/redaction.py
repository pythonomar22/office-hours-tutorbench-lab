"""Redacted, shareable exports for judged TutorBench traces."""

from __future__ import annotations

from collections import Counter
from typing import Any

from pydantic import BaseModel

from tutorbench_lab.schemas import JudgedRunRecord, ModelUsage

REDACTED_TRACE_SCHEMA_VERSION = "redacted-trace-v1"
REDACTION_POLICY = (
    "Dataset prompts, follow-up prompts, initial explanations, images, rubric "
    "criteria, judge rationales, and private agent scratchpads are removed."
)


def build_redacted_trace(
    record: JudgedRunRecord,
    *,
    include_response_text: bool = True,
    include_ratings: bool = True,
) -> dict[str, Any]:
    """Build one shareable trace row without redistributing TutorBench content."""

    run = record.run
    example = run.example
    response = run.response
    judge = record.judge
    payload: dict[str, Any] = {
        "schema_version": REDACTED_TRACE_SCHEMA_VERSION,
        "redaction_policy": REDACTION_POLICY,
        "run_id": run.run_id,
        "created_at": run.created_at.isoformat(),
        "dataset_revision": run.dataset_revision,
        "task": {
            "task_id": example.task_id,
            "batch": example.batch,
            "use_case": example.use_case.value,
            "subject": example.subject,
            "modality": example.modality.value,
            "has_image": example.has_image,
            "bloom_taxonomy": example.bloom_taxonomy,
            "rubric_count": len(example.rubrics),
        },
        "candidate": {
            "model": response.model,
            "strategy": response.strategy.value,
            "prompt_version": response.prompt_version,
            "latency_ms": response.latency_ms,
            "usage": _usage(response.usage),
        },
        "judge": {
            "model": judge.judge_model,
            "latency_ms": judge.latency_ms,
            "usage": _usage(judge.usage),
            "ratings_count": len(judge.ratings),
        },
        "score": {
            "arrw_raw": record.arrw_raw,
            "arrw": record.arrw,
            "manual_weight_review": record.manual_weight_review,
        },
        "failure_summary": _failure_summary(record),
        "trace_summary": _trace_summary(record),
    }
    if include_response_text:
        payload["response_text"] = response.text
    if include_ratings:
        payload["ratings"] = _rating_summaries(record)
    return payload


def build_redacted_traces(
    records: list[JudgedRunRecord],
    *,
    include_response_text: bool = True,
    include_ratings: bool = True,
) -> list[dict[str, Any]]:
    return [
        build_redacted_trace(
            record,
            include_response_text=include_response_text,
            include_ratings=include_ratings,
        )
        for record in records
    ]


def _failure_summary(record: JudgedRunRecord) -> dict[str, Any]:
    ratings_by_idx = {rating.criterion_index: rating for rating in record.judge.ratings}
    failed_dimensions: Counter[str] = Counter()
    failed_skills: Counter[str] = Counter()
    failed_positive_count = 0
    failed_positive_weight = 0
    triggered_negative_count = 0
    triggered_negative_weight = 0

    for idx, rubric in enumerate(record.run.example.rubrics):
        rating = ratings_by_idx[idx]
        if rubric.inferred_weight < 0 and rating.passed:
            triggered_negative_count += 1
            triggered_negative_weight += abs(rubric.inferred_weight)
            for dimension in rubric.eval_dimensions or ["none"]:
                failed_dimensions[dimension] += 1
            failed_skills[rubric.tutoring_skill or "none"] += 1
        elif rubric.inferred_weight > 0 and not rating.passed:
            failed_positive_count += 1
            failed_positive_weight += rubric.inferred_weight
            for dimension in rubric.eval_dimensions or ["none"]:
                failed_dimensions[dimension] += 1
            failed_skills[rubric.tutoring_skill or "none"] += 1

    return {
        "failed_positive_count": failed_positive_count,
        "failed_positive_weight": failed_positive_weight,
        "triggered_negative_count": triggered_negative_count,
        "triggered_negative_weight": triggered_negative_weight,
        "failed_dimensions": dict(sorted(failed_dimensions.items())),
        "failed_tutoring_skills": dict(sorted(failed_skills.items())),
    }


def _rating_summaries(record: JudgedRunRecord) -> list[dict[str, Any]]:
    ratings_by_idx = {rating.criterion_index: rating for rating in record.judge.ratings}
    rows = []
    for idx, rubric in enumerate(record.run.example.rubrics):
        rating = ratings_by_idx[idx]
        rows.append(
            {
                "criterion_index": idx,
                "passed": rating.passed,
                "confidence": rating.confidence,
                "inferred_weight": rubric.inferred_weight,
                "severity": rubric.severity,
                "eval_dimensions": rubric.eval_dimensions,
                "tutoring_skill": rubric.tutoring_skill,
                "negative_weight_candidate": rubric.negative_weight_candidate,
            }
        )
    return rows


def _trace_summary(record: JudgedRunRecord) -> dict[str, Any]:
    trace = record.run.response.trace
    stage_rate_limits = trace.get("stage_rate_limits") or {}
    return {
        "models": {
            "solver": trace.get("solver_model"),
            "planner": trace.get("planner_model"),
            "verifier": trace.get("verifier_model"),
            "critic": trace.get("critic_model"),
        },
        "route_plan": _jsonable(trace.get("route_plan")),
        "stage_latency_ms": _jsonable(trace.get("stage_latency_ms") or {}),
        "stage_usage": _jsonable(trace.get("stage_usage") or {}),
        "stage_rate_limit_headers_present": bool(stage_rate_limits),
        "task_playbook": _playbook_name(trace.get("task_playbook")),
        "selector_selected_source": trace.get("selector_selected_source"),
        "selector_confidence": trace.get("selector_confidence"),
        "blend_selected_source": trace.get("blend_selected_source"),
        "blend_policy": trace.get("blend_policy"),
        "revision_attempt_count": len(trace.get("revision_attempts") or []),
        "critic_attempt_count": len(trace.get("critic_attempts") or []),
        "stopped_due_to_revision_limit": bool(
            trace.get("stopped_due_to_revision_limit")
        ),
        "deterministic_guards": _jsonable(trace.get("deterministic_guards") or []),
    }


def _playbook_name(raw: Any) -> str | None:
    if not raw:
        return None
    first_line = str(raw).splitlines()[0].strip()
    return first_line.removeprefix("Task-family playbook: ") or None


def _usage(usage: ModelUsage) -> dict[str, Any]:
    return usage.model_dump(mode="json")


def _jsonable(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    return value
