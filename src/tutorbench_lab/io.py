"""Small JSON/JSONL helpers used by the CLI."""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl(path: Path, records: Iterable[BaseModel | dict[str, Any]]) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            if isinstance(record, BaseModel):
                payload = record.model_dump(mode="json")
            else:
                payload = record
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def append_jsonl(path: Path, record: BaseModel | dict[str, Any]) -> None:
    ensure_parent(path)
    payload = record.model_dump(mode="json") if isinstance(record, BaseModel) else record
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                yield json.loads(stripped)


def read_model_jsonl(path: Path, model: type[T]) -> Iterator[T]:
    for payload in read_jsonl(path):
        yield model.model_validate(payload)
