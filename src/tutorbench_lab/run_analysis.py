"""Run-level forensic analysis for TutorBench experiments."""

from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean
from typing import Any

from tutorbench_lab.schemas import JudgedRunRecord
from tutorbench_lab.scoring import build_score_report

RATE_LIMIT_REMAINING_KEYS = (
    "anthropic-ratelimit-requests-remaining",
    "anthropic-ratelimit-input-tokens-remaining",
    "anthropic-ratelimit-output-tokens-remaining",
    "anthropic-ratelimit-tokens-remaining",
)
RATE_LIMIT_LIMIT_KEYS = (
    "anthropic-ratelimit-requests-limit",
    "anthropic-ratelimit-input-tokens-limit",
    "anthropic-ratelimit-output-tokens-limit",
    "anthropic-ratelimit-tokens-limit",
)


def build_run_analysis(
    records: list[JudgedRunRecord],
    *,
    top_n: int = 10,
    bootstrap_samples: int = 500,
) -> dict[str, Any]:
    """Build a machine-readable analysis for one judged run."""

    if not records:
        raise ValueError("cannot analyze an empty judged run")

    score_report = build_score_report(
        records,
        bootstrap_samples=bootstrap_samples,
    ).model_dump(mode="json")
    row_summaries = [_row_summary(record) for record in records]
    weakest_rows = sorted(row_summaries, key=lambda item: item["arrw"])[:top_n]

    return {
        "summary": _summary(records),
        "score_report": score_report,
        "weakest_rows": weakest_rows,
        "rubric_dimensions": _rubric_groups(records, key_kind="dimension"),
        "tutoring_skills": _rubric_groups(records, key_kind="skill"),
        "playbooks": _playbook_counts(records),
        "throughput": _throughput(records),
    }


def analysis_markdown(analysis: dict[str, Any]) -> str:
    """Render a compact Markdown analysis report."""

    summary = analysis["summary"]
    score = analysis["score_report"]["overall"]
    throughput = analysis["throughput"]
    lines = [
        f"# TutorBench Run Analysis: `{summary['run_id']}`",
        "",
        f"- Rows: {summary['row_count']}",
        f"- Strategy: `{summary['strategy']}`",
        f"- Candidate model: `{summary['candidate_model']}`",
        f"- Judge model: `{summary['judge_model']}`",
        f"- Overall ARRw: {score['mean_arrw']:.2%}",
        f"- Mean generation latency: {summary['mean_generation_latency_ms']:.0f} ms",
        f"- Mean judge latency: {summary['mean_judge_latency_ms']:.0f} ms",
        "- Generation input/output tokens: "
        f"{summary['generation_input_tokens']} / "
        f"{summary['generation_output_tokens']}",
        "- Judge input/output tokens: "
        f"{summary['judge_input_tokens']} / {summary['judge_output_tokens']}",
        f"- Negative-weight manual review rows: {summary['negative_weight_review_count']}",
        "",
        "## Throughput Headroom",
        "",
        _rate_limit_table(throughput["rate_limits"]),
        "",
        "## Weakest Rows",
        "",
        _weakest_table(analysis["weakest_rows"]),
        "",
        "## Weakest Rubric Dimensions",
        "",
        _group_table(analysis["rubric_dimensions"][:12]),
        "",
        "## Weakest Tutoring Skills",
        "",
        _group_table(analysis["tutoring_skills"][:12]),
        "",
        "## Playbook Coverage",
        "",
        _playbook_table(analysis["playbooks"]),
        "",
    ]
    return "\n".join(lines)


def _summary(records: list[JudgedRunRecord]) -> dict[str, Any]:
    first = records[0]
    generation_usage = [record.run.response.usage for record in records]
    judge_usage = [record.judge.usage for record in records]
    return {
        "run_id": first.run.run_id,
        "row_count": len(records),
        "strategy": first.run.response.strategy.value,
        "candidate_model": first.run.response.model,
        "judge_model": first.judge.judge_model,
        "dataset_revision": first.run.dataset_revision,
        "mean_generation_latency_ms": _mean_present(
            record.run.response.latency_ms for record in records
        ),
        "mean_judge_latency_ms": _mean_present(
            record.judge.latency_ms for record in records
        ),
        "generation_input_tokens": _sum_present(
            usage.input_tokens for usage in generation_usage
        ),
        "generation_output_tokens": _sum_present(
            usage.output_tokens for usage in generation_usage
        ),
        "judge_input_tokens": _sum_present(
            usage.input_tokens for usage in judge_usage
        ),
        "judge_output_tokens": _sum_present(
            usage.output_tokens for usage in judge_usage
        ),
        "negative_weight_review_count": sum(
            1 for record in records if record.manual_weight_review
        ),
    }


def _row_summary(record: JudgedRunRecord) -> dict[str, Any]:
    ratings_by_idx = {
        rating.criterion_index: rating for rating in record.judge.ratings
    }
    failed_positive: list[dict[str, Any]] = []
    triggered_negative: list[dict[str, Any]] = []
    for idx, rubric in enumerate(record.run.example.rubrics):
        rating = ratings_by_idx[idx]
        item = {
            "criterion_index": idx,
            "weight": rubric.inferred_weight,
            "severity": rubric.severity,
            "dimensions": rubric.eval_dimensions,
            "tutoring_skill": rubric.tutoring_skill,
            "criteria_preview": _truncate(rubric.criteria, 180),
        }
        if rubric.inferred_weight < 0 and rating.passed:
            triggered_negative.append(item)
        elif rubric.inferred_weight > 0 and not rating.passed:
            failed_positive.append(item)

    return {
        "task_id": record.run.example.task_id,
        "arrw": record.arrw,
        "use_case": record.run.example.use_case.value,
        "modality": record.run.example.modality.value,
        "subject": record.run.example.subject,
        "bloom_taxonomy": record.run.example.bloom_taxonomy,
        "rubric_count": len(record.run.example.rubrics),
        "failed_positive_count": len(failed_positive),
        "triggered_negative_count": len(triggered_negative),
        "failed_positive": failed_positive[:5],
        "triggered_negative": triggered_negative[:5],
        "playbook": _playbook_name(record),
        "response_preview": _truncate(record.run.response.text, 260),
    }


def _rubric_groups(
    records: list[JudgedRunRecord],
    *,
    key_kind: str,
) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "positive_weight": 0.0,
            "passed_positive_weight": 0.0,
            "failed_positive_weight": 0.0,
            "negative_criteria": 0,
            "triggered_negative_criteria": 0,
            "rows_with_failure": set(),
        }
    )
    for record in records:
        ratings_by_idx = {
            rating.criterion_index: rating for rating in record.judge.ratings
        }
        for idx, rubric in enumerate(record.run.example.rubrics):
            rating = ratings_by_idx[idx]
            keys = _rubric_keys(rubric, key_kind=key_kind)
            for key in keys:
                group = groups[key]
                weight = rubric.inferred_weight
                if weight < 0:
                    group["negative_criteria"] += 1
                    if rating.passed:
                        group["triggered_negative_criteria"] += 1
                        group["rows_with_failure"].add(record.run.example.task_id)
                    continue
                group["positive_weight"] += weight
                if rating.passed:
                    group["passed_positive_weight"] += weight
                else:
                    group["failed_positive_weight"] += weight
                    group["rows_with_failure"].add(record.run.example.task_id)

    rows = []
    for name, group in groups.items():
        positive_weight = group["positive_weight"]
        passed_weight = group["passed_positive_weight"]
        pass_rate = None if positive_weight == 0 else passed_weight / positive_weight
        rows.append(
            {
                "name": name,
                "positive_weight": positive_weight,
                "passed_positive_weight": passed_weight,
                "failed_positive_weight": group["failed_positive_weight"],
                "pass_rate": pass_rate,
                "negative_criteria": group["negative_criteria"],
                "triggered_negative_criteria": group["triggered_negative_criteria"],
                "rows_with_failure": len(group["rows_with_failure"]),
            }
        )
    return sorted(
        rows,
        key=lambda item: (
            item["pass_rate"] if item["pass_rate"] is not None else 1.0,
            -item["failed_positive_weight"],
            item["name"],
        ),
    )


def _rubric_keys(rubric, *, key_kind: str) -> list[str]:
    if key_kind == "dimension":
        return rubric.eval_dimensions or ["none"]
    if key_kind == "skill":
        return [rubric.tutoring_skill or "none"]
    raise ValueError(f"unknown key_kind: {key_kind}")


def _playbook_counts(records: list[JudgedRunRecord]) -> list[dict[str, Any]]:
    buckets: dict[str, list[float]] = defaultdict(list)
    for record in records:
        buckets[_playbook_name(record)].append(record.arrw)
    rows = [
        {"name": name, "count": len(values), "mean_arrw": mean(values)}
        for name, values in buckets.items()
    ]
    return sorted(rows, key=lambda item: (-item["count"], item["name"]))


def _playbook_name(record: JudgedRunRecord) -> str:
    raw = record.run.response.trace.get("task_playbook")
    if not raw:
        return "none"
    first_line = str(raw).splitlines()[0].strip()
    return first_line.removeprefix("Task-family playbook: ") or "none"


def _throughput(records: list[JudgedRunRecord]) -> dict[str, Any]:
    stage_counts: Counter[str] = Counter()
    stage_latency_ms: dict[str, list[int]] = defaultdict(list)
    rate_limits: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"min_remaining": None, "max_limit": None}
    )
    retry_after_count = 0

    for record in records:
        trace = record.run.response.trace
        for stage, latency in (trace.get("stage_latency_ms") or {}).items():
            if isinstance(latency, (int, float)):
                stage_latency_ms[stage].append(int(latency))
                stage_counts[stage] += 1
        for headers in (trace.get("stage_rate_limits") or {}).values():
            if not isinstance(headers, dict):
                continue
            if "retry-after" in headers:
                retry_after_count += 1
            for key in RATE_LIMIT_REMAINING_KEYS:
                _update_min(rate_limits[key], _safe_int(headers.get(key)))
            for key in RATE_LIMIT_LIMIT_KEYS:
                _update_max(rate_limits[key], _safe_int(headers.get(key)))

    return {
        "stage_counts": dict(sorted(stage_counts.items())),
        "stage_mean_latency_ms": {
            stage: round(mean(values), 2)
            for stage, values in sorted(stage_latency_ms.items())
            if values
        },
        "retry_after_header_count": retry_after_count,
        "rate_limits": dict(sorted(rate_limits.items())),
    }


def _update_min(bucket: dict[str, Any], value: int | None) -> None:
    if value is None:
        return
    current = bucket["min_remaining"]
    bucket["min_remaining"] = value if current is None else min(current, value)


def _update_max(bucket: dict[str, Any], value: int | None) -> None:
    if value is None:
        return
    current = bucket["max_limit"]
    bucket["max_limit"] = value if current is None else max(current, value)


def _safe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _mean_present(values) -> float:
    present = [value for value in values if value is not None]
    return mean(present) if present else 0.0


def _sum_present(values) -> int:
    return sum(value for value in values if value is not None)


def _truncate(text: str, limit: int) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def _rate_limit_table(rate_limits: dict[str, Any]) -> str:
    lines = [
        "| Header | Min Remaining | Max Limit |",
        "| --- | ---: | ---: |",
    ]
    if not rate_limits:
        return "No rate-limit headers were captured."
    for key, payload in rate_limits.items():
        lines.append(
            f"| `{key}` | {payload.get('min_remaining')} | {payload.get('max_limit')} |"
        )
    return "\n".join(lines)


def _weakest_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Task | ARRw | Slice | Failed + | Triggered - | Playbook |",
        "| --- | ---: | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        slice_name = f"{row['use_case']} / {row['modality']} / {row['subject']}"
        lines.append(
            f"| `{row['task_id']}` | {row['arrw']:.2%} | {slice_name} | "
            f"{row['failed_positive_count']} | {row['triggered_negative_count']} | "
            f"{row['playbook']} |"
        )
    return "\n".join(lines)


def _group_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        pass_rate = "-" if row["pass_rate"] is None else f"{row['pass_rate']:.2%}"
        lines.append(
            f"| {row['name']} | {pass_rate} | {row['failed_positive_weight']:.1f} | "
            f"{row['rows_with_failure']} | {row['triggered_negative_criteria']} |"
        )
    return "\n".join(lines)


def _playbook_table(rows: list[dict[str, Any]]) -> str:
    lines = ["| Playbook | Rows | Mean ARRw |", "| --- | ---: | ---: |"]
    for row in rows[:20]:
        lines.append(f"| {row['name']} | {row['count']} | {row['mean_arrw']:.2%} |")
    return "\n".join(lines)
