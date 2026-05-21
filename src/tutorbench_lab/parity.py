"""Evaluation-parity checks for leaderboard-style TutorBench claims."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from tutorbench_lab.constants import DATASET_ID, DATASET_REVISION, EXPECTED_ROW_COUNT

PUBLIC_LEADERBOARD_FACTS = {
    "row_count": 1490,
    "multimodal_count": 828,
    "rubric_count_total": 15220,
    "judge_family": "Claude-4-Sonnet",
    "leaderboard_target": "Muse Spark 68.55±0.95",
}


class ParityStatus(StrEnum):
    PASS = "pass"
    WARN = "warn"
    BLOCKER = "blocker"


@dataclass(frozen=True)
class ParityCheck:
    name: str
    status: ParityStatus
    expected: str
    observed: str
    detail: str


def build_parity_checks(
    *,
    manifest: dict[str, Any],
    metadata: dict[str, Any] | None = None,
    judge_model: str,
    candidate_rubric_visibility: bool = False,
) -> list[ParityCheck]:
    """Return checks that explain whether local evals are leaderboard-comparable."""

    metadata = metadata or {}
    checks = [
        _check_equal(
            "Dataset ID",
            expected=DATASET_ID,
            observed=str(manifest.get("dataset_id")),
            blocker=True,
            detail="Use the official Hugging Face dataset namespace.",
        ),
        _check_equal(
            "Dataset revision",
            expected=DATASET_REVISION,
            observed=str(manifest.get("revision")),
            blocker=True,
            detail="Pinning prevents silent data drift during iteration.",
        ),
        _check_equal(
            "Pinned public row count",
            expected=str(EXPECTED_ROW_COUNT),
            observed=str(manifest.get("row_count")),
            blocker=True,
            detail="The local public-HF slice should match the pinned manifest.",
        ),
        _check_equal(
            "Leaderboard row count",
            expected=str(PUBLIC_LEADERBOARD_FACTS["row_count"]),
            observed=str(manifest.get("row_count")),
            blocker=False,
            detail=(
                "Scale's public leaderboard overview lists 1,490 examples. The "
                "pinned public HF release currently has 1,473 rows, so local "
                "full-set scores are not leaderboard-exact."
            ),
        ),
        _check_equal(
            "Leaderboard multimodal count",
            expected=str(PUBLIC_LEADERBOARD_FACTS["multimodal_count"]),
            observed=str(manifest.get("modality_counts", {}).get("multimodal")),
            blocker=False,
            detail=(
                "The leaderboard overview lists 828 multimodal examples. The "
                "pinned public HF manifest has 817 multimodal rows."
            ),
        ),
        _check_equal(
            "Leaderboard rubric count",
            expected=str(PUBLIC_LEADERBOARD_FACTS["rubric_count_total"]),
            observed=str(manifest.get("rubric_count_total")),
            blocker=False,
            detail=(
                "Rubric count mismatch is expected with the public-HF row-count "
                "difference, but it prevents exact leaderboard claims."
            ),
        ),
        _check_contains(
            "Judge family",
            expected="Claude/Sonnet 4-family",
            observed=judge_model,
            needle="sonnet",
            detail=(
                "The paper/leaderboard describe a Claude-4-Sonnet judge. Exact "
                "model IDs may not be externally reproducible, but the family "
                "should match for calibration runs."
            ),
        ),
        ParityCheck(
            name="Rubric visibility",
            status=ParityStatus.BLOCKER if candidate_rubric_visibility else ParityStatus.PASS,
            expected="Candidate tutor never sees sample-specific rubrics",
            observed="visible" if candidate_rubric_visibility else "hidden",
            detail=(
                "Rubrics must remain evaluator-only. Playbooks may use task "
                "content and broad task-family knowledge, not row-specific rubrics."
            ),
        ),
        ParityCheck(
            name="Signed negative weights",
            status=ParityStatus.WARN,
            expected="Official signed weights including -5 criteria",
            observed=(
                f"inferred; {manifest.get('negative_weight_candidate_count')} "
                "negative candidates flagged"
            ),
            detail=(
                "The public rows expose severity but not always official signed "
                "weights. Local ARRw is close but not guaranteed identical."
            ),
        ),
    ]

    if metadata:
        checks.append(
            _check_equal(
                "HF metadata SHA",
                expected=DATASET_REVISION,
                observed=str(metadata.get("sha")),
                blocker=False,
                detail="Cheap metadata check for the currently published HF revision.",
            )
        )

    return checks


def parity_level(checks: list[ParityCheck]) -> str:
    if any(check.status == ParityStatus.BLOCKER for check in checks):
        return "blocked"
    if any(check.status == ParityStatus.WARN for check in checks):
        return "public-hf-comparable"
    return "leaderboard-exact"


def checks_to_json(checks: list[ParityCheck]) -> list[dict[str, str]]:
    return [
        {
            "name": check.name,
            "status": check.status.value,
            "expected": check.expected,
            "observed": check.observed,
            "detail": check.detail,
        }
        for check in checks
    ]


def _check_equal(
    name: str,
    *,
    expected: str,
    observed: str,
    blocker: bool,
    detail: str,
) -> ParityCheck:
    if expected == observed:
        status = ParityStatus.PASS
    else:
        status = ParityStatus.BLOCKER if blocker else ParityStatus.WARN
    return ParityCheck(
        name=name,
        status=status,
        expected=expected,
        observed=observed,
        detail=detail,
    )


def _check_contains(
    name: str,
    *,
    expected: str,
    observed: str,
    needle: str,
    detail: str,
) -> ParityCheck:
    return ParityCheck(
        name=name,
        status=ParityStatus.PASS if needle.lower() in observed.lower() else ParityStatus.WARN,
        expected=expected,
        observed=observed,
        detail=detail,
    )
