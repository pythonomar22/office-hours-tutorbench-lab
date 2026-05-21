"""Aggregate TutorBench judged records into score reports."""

from __future__ import annotations

import random
from collections import defaultdict
from statistics import mean

from tutorbench_lab.schemas import AggregateScore, JudgedRunRecord, ScoreReport


def build_score_report(
    records: list[JudgedRunRecord],
    *,
    bootstrap_samples: int = 1000,
    seed: int = 7,
) -> ScoreReport:
    if not records:
        raise ValueError("cannot score an empty judged run")

    run_ids = {record.run.run_id for record in records}
    run_id = next(iter(run_ids)) if len(run_ids) == 1 else "mixed"
    judge_models = {record.judge.judge_model for record in records}
    judge_model = next(iter(judge_models)) if len(judge_models) == 1 else "mixed"

    return ScoreReport(
        run_id=run_id,
        judge_model=judge_model,
        overall=_aggregate(
            "overall",
            [record.arrw for record in records],
            bootstrap_samples=bootstrap_samples,
            seed=seed,
        ),
        by_use_case=_grouped(records, lambda r: r.run.example.use_case.value),
        by_modality=_grouped(records, lambda r: r.run.example.modality.value),
        by_subject=_grouped(records, lambda r: r.run.example.subject),
        by_bloom=_grouped(records, lambda r: r.run.example.bloom_taxonomy or "none"),
        negative_weight_review_count=sum(1 for r in records if r.manual_weight_review),
    )


def _grouped(records: list[JudgedRunRecord], key_fn) -> list[AggregateScore]:
    buckets: dict[str, list[float]] = defaultdict(list)
    for record in records:
        buckets[key_fn(record)].append(record.arrw)
    return [
        _aggregate(name, values, bootstrap_samples=500, seed=11)
        for name, values in sorted(buckets.items())
    ]


def _aggregate(
    name: str,
    values: list[float],
    *,
    bootstrap_samples: int,
    seed: int,
) -> AggregateScore:
    score = mean(values)
    ci_low, ci_high = _bootstrap_ci(values, samples=bootstrap_samples, seed=seed)
    return AggregateScore(
        name=name,
        count=len(values),
        mean_arrw=score,
        ci_low=ci_low,
        ci_high=ci_high,
    )


def _bootstrap_ci(
    values: list[float],
    *,
    samples: int,
    seed: int,
) -> tuple[float | None, float | None]:
    if len(values) < 2 or samples <= 0:
        return None, None
    rng = random.Random(seed)
    means = []
    for _ in range(samples):
        draw = [rng.choice(values) for _ in values]
        means.append(mean(draw))
    means.sort()
    low_idx = int(0.025 * (samples - 1))
    high_idx = int(0.975 * (samples - 1))
    return means[low_idx], means[high_idx]
