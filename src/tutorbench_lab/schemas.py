"""Typed data contracts for TutorBench examples, runs, and judgments."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator


class UseCase(StrEnum):
    """TutorBench's three task families."""

    ADAPTIVE = "adaptive"
    ASSESSMENT = "assessment"
    ACTIVE_LEARNING = "active_learning"


class Modality(StrEnum):
    TEXT = "text"
    MULTIMODAL = "multimodal"


class Strategy(StrEnum):
    BASELINE = "baseline"
    AGENTIC = "agentic"
    DRY_RUN = "dry-run"


class RubricAttributes(BaseModel):
    """Attributes attached to a TutorBench rubric criterion."""

    explicitness: str | None = None
    objectivity: str | None = None
    severity: str | None = None
    tutoring_skill: str | None = None
    eval_dimension: str | None = None

    model_config = ConfigDict(extra="allow")


_BAD_BEHAVIOR_RE = re.compile(
    r"\b(reveal|reveals|revealed|give away|gives away|gave away|"
    r"solve|solves|solved)\b"
    r".{0,80}\b(final answer|correct answer|answer directly|full answer|solution)\b",
    re.IGNORECASE,
)
_DESIRABLE_NEGATION_RE = re.compile(
    r"\b(must|should|does|do|is|are)\s+not\b|without\s+giving\s+away",
    re.IGNORECASE,
)


class RubricCriterion(BaseModel):
    """A sample-specific pass/fail rubric item."""

    criteria: str
    attributes: RubricAttributes = Field(default_factory=RubricAttributes)

    model_config = ConfigDict(extra="allow")

    @field_validator("criteria")
    @classmethod
    def _criteria_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("rubric criterion cannot be empty")
        return value

    @computed_field
    @property
    def severity(self) -> str:
        return (self.attributes.severity or "not_critical").strip().lower()

    @computed_field
    @property
    def eval_dimensions(self) -> list[str]:
        raw = self.attributes.eval_dimension or ""
        return [part.strip().lower() for part in raw.split(",") if part.strip()]

    @computed_field
    @property
    def tutoring_skill(self) -> str | None:
        raw = self.attributes.tutoring_skill
        if raw is None:
            return None
        cleaned = raw.strip()
        return cleaned or None

    @computed_field
    @property
    def negative_weight_candidate(self) -> bool:
        """Whether this criterion likely describes an undesirable behavior.

        TutorBench's public rows expose severity tags, but the official signed
        rubric weights are not always directly present. This flag keeps likely
        -5 spoiler/failure criteria visible for manual review.
        """

        text = self.criteria
        return bool(_BAD_BEHAVIOR_RE.search(text)) and not bool(
            _DESIRABLE_NEGATION_RE.search(text)
        )

    @computed_field
    @property
    def inferred_weight(self) -> int:
        if self.negative_weight_candidate:
            return -5
        if self.severity == "critical":
            return 5
        return 1


class ImageRef(BaseModel):
    """Reference to a text row's optional multimodal image."""

    url: str | None = None
    path: Path | None = None
    media_type: str = "image/png"

    @computed_field
    @property
    def present(self) -> bool:
        return bool(self.url or self.path)


class TutorBenchExample(BaseModel):
    """Normalized representation of one TutorBench row."""

    task_id: str
    batch: str
    subject: str
    prompt: str
    image: ImageRef = Field(default_factory=ImageRef)
    uc1_initial_explanation: str = ""
    follow_up_prompt: str = ""
    rubrics: list[RubricCriterion]
    bloom_taxonomy: str | None = None

    @field_validator("task_id")
    @classmethod
    def _task_id_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("TASK_ID cannot be empty")
        return value

    @computed_field
    @property
    def use_case(self) -> UseCase:
        if self.batch.startswith("USE_CASE_1"):
            return UseCase.ADAPTIVE
        if self.batch.startswith("USE_CASE_2"):
            return UseCase.ASSESSMENT
        if self.batch.startswith("USE_CASE_3"):
            return UseCase.ACTIVE_LEARNING
        raise ValueError(f"unknown TutorBench batch: {self.batch}")

    @computed_field
    @property
    def modality(self) -> Modality:
        if self.batch.endswith("_MULTIMODAL"):
            return Modality.MULTIMODAL
        return Modality.TEXT

    @computed_field
    @property
    def has_image(self) -> bool:
        return self.image.present

    @classmethod
    def from_hf_row(cls, row: dict[str, Any]) -> TutorBenchExample:
        rubrics_raw = row.get("RUBRICS") or "[]"
        rubrics_payload = json.loads(rubrics_raw)
        image_path = None
        image_obj = row.get("Image")
        if isinstance(image_obj, dict) and image_obj.get("path"):
            image_path = Path(image_obj["path"])
        return cls(
            task_id=row["TASK_ID"],
            batch=row["BATCH"],
            subject=row["SUBJECT"],
            prompt=row.get("PROMPT") or "",
            image=ImageRef(url=row.get("IMAGE_URL") or None, path=image_path),
            uc1_initial_explanation=row.get("UC1_INITIAL_EXPLANATION") or "",
            follow_up_prompt=row.get("FOLLOW_UP_PROMPT") or "",
            rubrics=[RubricCriterion.model_validate(item) for item in rubrics_payload],
            bloom_taxonomy=row.get("bloom_taxonomy") or None,
        )


class TutorTurnInput(BaseModel):
    """Provider-neutral prompt assembled from a TutorBench example."""

    task_id: str
    use_case: UseCase
    modality: Modality
    subject: str
    system_prompt: str
    user_prompt: str
    image: ImageRef = Field(default_factory=ImageRef)
    prompt_version: str


class ModelUsage(BaseModel):
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    estimated_cost_usd: float | None = None


class TutorResponse(BaseModel):
    """Candidate tutor output for one example."""

    task_id: str
    text: str
    model: str
    strategy: Strategy
    prompt_version: str
    latency_ms: int | None = None
    usage: ModelUsage = Field(default_factory=ModelUsage)
    trace: dict[str, Any] = Field(default_factory=dict)


class RunRecord(BaseModel):
    """One JSONL row emitted by `run`."""

    run_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    dataset_revision: str
    example: TutorBenchExample
    turn_input: TutorTurnInput
    response: TutorResponse


class CriterionRating(BaseModel):
    criterion_index: int
    passed: bool
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    rationale: str = ""


class JudgeResult(BaseModel):
    task_id: str
    judge_model: str
    ratings: list[CriterionRating]
    raw_judge_output: str = ""
    latency_ms: int | None = None
    usage: ModelUsage = Field(default_factory=ModelUsage)


class JudgedRunRecord(BaseModel):
    """One JSONL row emitted by `judge`."""

    run: RunRecord
    judge: JudgeResult
    arrw_raw: float
    arrw: float
    manual_weight_review: bool = False


class AggregateScore(BaseModel):
    name: str
    count: int
    mean_arrw: float
    ci_low: float | None = None
    ci_high: float | None = None


class ScoreReport(BaseModel):
    run_id: str
    judge_model: str
    overall: AggregateScore
    by_use_case: list[AggregateScore]
    by_modality: list[AggregateScore]
    by_subject: list[AggregateScore]
    by_bloom: list[AggregateScore]
    negative_weight_review_count: int


class CompareReport(BaseModel):
    left: ScoreReport
    right: ScoreReport
    delta_overall: float
    winner: Literal["left", "right", "tie"]
