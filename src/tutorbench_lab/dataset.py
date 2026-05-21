"""TutorBench dataset loading, validation, and manifest creation."""

from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import Any

from datasets import Dataset, load_dataset, load_from_disk
from huggingface_hub import HfApi

from tutorbench_lab.constants import (
    DATASET_ID,
    DATASET_REVISION,
    DATASET_SPLIT,
    EXPECTED_BATCH_COUNTS,
    EXPECTED_ROW_COUNT,
    EXPECTED_SUBJECTS,
    EXPECTED_USE_CASE_COUNTS,
)
from tutorbench_lab.io import read_jsonl, write_json, write_jsonl
from tutorbench_lab.schemas import TutorBenchExample


class DatasetValidationError(RuntimeError):
    """Raised when the pinned TutorBench dataset does not match expectations."""


def load_tutorbench(
    *,
    dataset_id: str = DATASET_ID,
    revision: str = DATASET_REVISION,
    split: str = DATASET_SPLIT,
    raw_dataset_dir: Path | None = None,
) -> Dataset:
    """Load TutorBench from disk if present, otherwise from Hugging Face."""

    if raw_dataset_dir is not None and raw_dataset_dir.exists():
        loaded = load_from_disk(str(raw_dataset_dir))
        if not isinstance(loaded, Dataset):
            raise DatasetValidationError(f"expected Dataset at {raw_dataset_dir}")
        return loaded

    dataset = load_dataset(dataset_id, revision=revision, split=split)
    if not isinstance(dataset, Dataset):
        raise DatasetValidationError("expected a single Hugging Face Dataset split")
    return dataset


def save_dataset(dataset: Dataset, raw_dataset_dir: Path) -> None:
    """Persist the HF dataset to disk for reproducible local runs."""

    raw_dataset_dir.parent.mkdir(parents=True, exist_ok=True)
    dataset.save_to_disk(str(raw_dataset_dir))


def iter_examples(dataset: Dataset, *, limit: int | None = None) -> list[TutorBenchExample]:
    """Normalize rows into typed examples."""

    examples: list[TutorBenchExample] = []
    for idx, row in enumerate(dataset):
        if limit is not None and idx >= limit:
            break
        examples.append(TutorBenchExample.from_hf_row(dict(row)))
    return examples


def validate_examples(examples: list[TutorBenchExample], *, strict: bool = True) -> None:
    """Validate row counts and known TutorBench distribution."""

    if strict and len(examples) != EXPECTED_ROW_COUNT:
        raise DatasetValidationError(
            f"expected {EXPECTED_ROW_COUNT} rows, found {len(examples)}"
        )

    batch_counts = Counter(example.batch for example in examples)
    use_case_counts = Counter(example.use_case.value for example in examples)
    subjects = {example.subject for example in examples}

    expected_batches = dict(sorted(EXPECTED_BATCH_COUNTS.items()))
    if strict and dict(sorted(batch_counts.items())) != expected_batches:
        raise DatasetValidationError(
            "batch distribution mismatch: "
            f"expected {EXPECTED_BATCH_COUNTS}, found {dict(batch_counts)}"
        )

    if strict and dict(sorted(use_case_counts.items())) != dict(
        sorted(EXPECTED_USE_CASE_COUNTS.items())
    ):
        raise DatasetValidationError(
            "use-case distribution mismatch: "
            f"expected {EXPECTED_USE_CASE_COUNTS}, found {dict(use_case_counts)}"
        )

    if strict and subjects != EXPECTED_SUBJECTS:
        raise DatasetValidationError(
            f"subject set mismatch: expected {EXPECTED_SUBJECTS}, found {subjects}"
        )


def build_manifest(
    examples: list[TutorBenchExample],
    *,
    dataset_id: str = DATASET_ID,
    revision: str = DATASET_REVISION,
) -> dict[str, Any]:
    """Build a compact manifest that can be committed without dataset rows."""

    batch_counts = Counter(example.batch for example in examples)
    use_case_counts = Counter(example.use_case.value for example in examples)
    subject_counts = Counter(example.subject for example in examples)
    modality_counts = Counter(example.modality.value for example in examples)
    bloom_counts = Counter(example.bloom_taxonomy or "none" for example in examples)
    rubric_counts = [len(example.rubrics) for example in examples]
    image_count = sum(1 for example in examples if example.has_image)
    negative_weight_candidates = sum(
        1
        for example in examples
        for rubric in example.rubrics
        if rubric.negative_weight_candidate
    )

    task_hash = hashlib.sha256(
        "\n".join(sorted(example.task_id for example in examples)).encode("utf-8")
    ).hexdigest()

    return {
        "dataset_id": dataset_id,
        "revision": revision,
        "row_count": len(examples),
        "task_id_sha256": task_hash,
        "image_count": image_count,
        "text_only_count": len(examples) - image_count,
        "rubric_count_total": sum(rubric_counts),
        "rubric_count_min": min(rubric_counts) if rubric_counts else 0,
        "rubric_count_max": max(rubric_counts) if rubric_counts else 0,
        "rubric_count_mean": (
            round(sum(rubric_counts) / len(rubric_counts), 4) if rubric_counts else 0
        ),
        "negative_weight_candidate_count": negative_weight_candidates,
        "batch_counts": dict(sorted(batch_counts.items())),
        "use_case_counts": dict(sorted(use_case_counts.items())),
        "modality_counts": dict(sorted(modality_counts.items())),
        "subject_counts": dict(sorted(subject_counts.items())),
        "bloom_counts": dict(sorted(bloom_counts.items())),
    }


def write_examples_jsonl(examples: list[TutorBenchExample], path: Path) -> None:
    write_jsonl(path, examples)


def write_manifest(manifest: dict[str, Any], path: Path) -> None:
    write_json(path, manifest)


def fetch_dataset_metadata(
    *, dataset_id: str = DATASET_ID, revision: str = DATASET_REVISION
) -> dict[str, Any]:
    """Fetch cheap repo metadata from Hugging Face without downloading parquet."""

    api = HfApi()
    info = api.dataset_info(dataset_id, revision=revision)
    siblings = sorted(s.rfilename for s in info.siblings or [])
    return {
        "dataset_id": info.id,
        "sha": info.sha,
        "last_modified": info.last_modified.isoformat() if info.last_modified else None,
        "private": info.private,
        "gated": info.gated,
        "tags": sorted(info.tags or []),
        "siblings": siblings,
    }


def load_examples_jsonl(path: Path) -> list[TutorBenchExample]:
    path = Path(path)
    return [TutorBenchExample.model_validate(row) for row in read_jsonl(path)]
