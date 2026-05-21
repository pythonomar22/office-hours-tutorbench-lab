"""Named evaluation set loading."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from tutorbench_lab.io import read_json, write_json
from tutorbench_lab.schemas import TutorBenchExample
from tutorbench_lab.selection import StratifyBy, bucket_key


class EvalSetItem(BaseModel):
    task_id: str
    why: str = ""


class EvalSet(BaseModel):
    name: str
    description: str = ""
    selection_policy: list[str] = Field(default_factory=list)
    task_ids: list[EvalSetItem]

    @property
    def ids(self) -> list[str]:
        return [item.task_id for item in self.task_ids]


def load_eval_set(path: Path) -> EvalSet:
    payload: dict[str, Any] = read_json(path)
    return EvalSet.model_validate(payload)


def examples_for_eval_set(
    examples: list[TutorBenchExample], eval_set: EvalSet
) -> list[TutorBenchExample]:
    by_id = {example.task_id: example for example in examples}
    missing = [task_id for task_id in eval_set.ids if task_id not in by_id]
    if missing:
        raise ValueError(f"eval set references missing task IDs: {missing}")
    return [by_id[task_id] for task_id in eval_set.ids]


def build_eval_set(
    *,
    name: str,
    description: str,
    examples: list[TutorBenchExample],
    selection_policy: list[str],
    stratify_by: StratifyBy | None = None,
) -> EvalSet:
    task_ids = [
        EvalSetItem(
            task_id=example.task_id,
            why=(
                f"{bucket_key(example, stratify_by)}; "
                f"{example.subject}; {example.bloom_taxonomy or 'no-bloom'}"
            )
            if stratify_by
            else f"{example.subject}; {example.use_case.value}; {example.modality.value}",
        )
        for example in examples
    ]
    return EvalSet(
        name=name,
        description=description,
        selection_policy=selection_policy,
        task_ids=task_ids,
    )


def write_eval_set(eval_set: EvalSet, path: Path) -> None:
    write_json(path, eval_set.model_dump(mode="json"))
