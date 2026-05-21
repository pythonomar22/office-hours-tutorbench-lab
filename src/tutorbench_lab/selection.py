"""Example selection helpers for controlled evaluation slices."""

from __future__ import annotations

import random
from collections import defaultdict
from enum import StrEnum

from tutorbench_lab.schemas import TutorBenchExample


class StratifyBy(StrEnum):
    USE_CASE = "use-case"
    USE_CASE_MODALITY = "use-case-modality"
    SUBJECT = "subject"
    SUBJECT_MODALITY = "subject-modality"


def select_examples(
    examples: list[TutorBenchExample],
    *,
    limit: int | None = None,
    stratified_per_bucket: int | None = None,
    stratify_by: StratifyBy = StratifyBy.USE_CASE_MODALITY,
    seed: int = 7,
) -> list[TutorBenchExample]:
    """Select examples for a run.

    Plain `limit` preserves dataset order. Stratified sampling shuffles inside
    each bucket deterministically, samples `n` per bucket, then shuffles the
    combined result deterministically.
    """

    if stratified_per_bucket is None:
        return examples[:limit] if limit is not None else examples

    rng = random.Random(seed)
    buckets: dict[str, list[TutorBenchExample]] = defaultdict(list)
    for example in examples:
        buckets[_bucket_key(example, stratify_by)].append(example)

    selected: list[TutorBenchExample] = []
    for key in sorted(buckets):
        bucket = buckets[key][:]
        rng.shuffle(bucket)
        selected.extend(bucket[:stratified_per_bucket])

    rng.shuffle(selected)
    if limit is not None:
        selected = selected[:limit]
    return selected


def _bucket_key(example: TutorBenchExample, stratify_by: StratifyBy) -> str:
    if stratify_by == StratifyBy.USE_CASE:
        return example.use_case.value
    if stratify_by == StratifyBy.USE_CASE_MODALITY:
        return f"{example.use_case.value}:{example.modality.value}"
    if stratify_by == StratifyBy.SUBJECT:
        return example.subject
    if stratify_by == StratifyBy.SUBJECT_MODALITY:
        return f"{example.subject}:{example.modality.value}"
    raise ValueError(f"unsupported stratification: {stratify_by}")
