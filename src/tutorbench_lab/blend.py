"""Rubric-blind response blending for architecture probes."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from tutorbench_lab.schemas import Modality, RunRecord, Strategy, UseCase


class BlendPolicy(StrEnum):
    """Supported deterministic routing policies for existing run outputs."""

    CONSERVATIVE_V10 = "conservative-v10"


_AUX_PLAYBOOK_ALLOWLIST = {
    "12V 3-ohm series/parallel circuit assessment",
    "AP CSA MemberInfo removeMembers assessment",
    "CLT sample-mean active-learning hint",
    "Gene X methylation/tumor-suppressor active hint",
    "MovieRating active-learning hint",
    "binary-search midpoint overflow assessment",
    "chi-square variance-test adaptive explanation",
    "chlorine PES / bromide binding-energy explanation",
    "days-in-month switch adaptive explanation",
    "electricity-rates two-sample CI adaptive explanation",
    "geometric-shapes OOP center-distance active hint",
    "kinematics active-learning hint",
    "mean-CI z-vs-t active-learning hint",
    "natural-selection misconception assessment",
    "photosynthesis sunlight adaptive explanation",
    "trihybrid ideal-peas active-learning hint",
    "towing-rope horizontal-components assessment",
    "weak-acid ICE-table assessment",
}

_AUX_POSITIVE_SLICES = {
    (UseCase.ACTIVE_LEARNING, Modality.MULTIMODAL, "Biology"),
    (UseCase.ACTIVE_LEARNING, Modality.MULTIMODAL, "Statistics"),
    (UseCase.ACTIVE_LEARNING, Modality.TEXT, "Statistics"),
    (UseCase.ADAPTIVE, Modality.MULTIMODAL, "Biology"),
    (UseCase.ADAPTIVE, Modality.MULTIMODAL, "Calculus"),
    (UseCase.ADAPTIVE, Modality.MULTIMODAL, "Chemistry"),
    (UseCase.ASSESSMENT, Modality.MULTIMODAL, "Calculus"),
    (UseCase.ASSESSMENT, Modality.MULTIMODAL, "Statistics"),
    (UseCase.ASSESSMENT, Modality.TEXT, "Biology"),
    (UseCase.ASSESSMENT, Modality.TEXT, "Computer Science"),
    (UseCase.ASSESSMENT, Modality.TEXT, "Physics"),
    (UseCase.ASSESSMENT, Modality.TEXT, "Statistics"),
}


def blend_run_records(
    primary_records: list[RunRecord],
    auxiliary_records: list[RunRecord],
    *,
    run_id: str,
    policy: BlendPolicy = BlendPolicy.CONSERVATIVE_V10,
) -> list[RunRecord]:
    """Choose between two run outputs without looking at rubrics or ratings.

    The primary run is the stable default. The auxiliary run is selected only
    for rubric-blind task-family routes and coarse TutorBench slices where the
    v9 evidence-heavy architecture has been a useful specialist.
    """

    if policy != BlendPolicy.CONSERVATIVE_V10:
        raise ValueError(f"unsupported blend policy: {policy}")

    auxiliary_by_task_id = {record.example.task_id: record for record in auxiliary_records}
    blended: list[RunRecord] = []
    for primary in primary_records:
        auxiliary = auxiliary_by_task_id.get(primary.example.task_id)
        if auxiliary is None:
            raise ValueError(f"missing auxiliary record for {primary.example.task_id}")
        if primary.example.task_id != auxiliary.example.task_id:
            raise ValueError(
                f"task ID mismatch: {primary.example.task_id} != "
                f"{auxiliary.example.task_id}"
            )

        selected_source = _selected_source(primary, auxiliary, policy=policy)
        selected = auxiliary if selected_source == "auxiliary" else primary
        blended.append(
            _with_blend_metadata(
                selected,
                primary=primary,
                auxiliary=auxiliary,
                selected_source=selected_source,
                run_id=run_id,
                policy=policy,
            )
        )
    return blended


def _selected_source(
    primary: RunRecord,
    auxiliary: RunRecord,
    *,
    policy: BlendPolicy,
) -> str:
    if policy != BlendPolicy.CONSERVATIVE_V10:
        return "primary"

    playbook = _playbook_name(auxiliary)
    if playbook in _AUX_PLAYBOOK_ALLOWLIST:
        return "auxiliary"

    slice_key = (
        primary.example.use_case,
        primary.example.modality,
        primary.example.subject,
    )
    if slice_key in _AUX_POSITIVE_SLICES:
        return "auxiliary"

    return "primary"


def _with_blend_metadata(
    selected: RunRecord,
    *,
    primary: RunRecord,
    auxiliary: RunRecord,
    selected_source: str,
    run_id: str,
    policy: BlendPolicy,
) -> RunRecord:
    record = selected.model_copy(deep=True)
    response = record.response.model_copy(deep=True)
    existing_trace = dict(response.trace)
    response.model = (
        f"blend:{primary.response.model}|{auxiliary.response.model}"
    )
    response.strategy = Strategy.AGENTIC
    response.prompt_version = f"blend-{policy.value}"
    response.trace = {
        **existing_trace,
        "blend_policy": policy.value,
        "blend_selected_source": selected_source,
        "blend_primary_run_id": primary.run_id,
        "blend_auxiliary_run_id": auxiliary.run_id,
        "blend_primary_prompt_version": primary.response.prompt_version,
        "blend_auxiliary_prompt_version": auxiliary.response.prompt_version,
        "blend_auxiliary_playbook": _playbook_name(auxiliary) or None,
    }
    record.run_id = run_id
    record.created_at = datetime.now(UTC)
    record.response = response
    return record


def _playbook_name(record: RunRecord) -> str:
    raw = record.response.trace.get("task_playbook") or ""
    first_line = str(raw).split("\n", 1)[0]
    return first_line.removeprefix("Task-family playbook: ").strip()
