from __future__ import annotations

from tutorbench_lab.parity import build_parity_checks, parity_level


def test_parity_flags_public_hf_vs_leaderboard_gap() -> None:
    checks = build_parity_checks(
        manifest={
            "dataset_id": "ScaleAI/TutorBench",
            "revision": "c70d2311cdca7129cab9376ba22eaa97c3cff3d7",
            "row_count": 1473,
            "modality_counts": {"multimodal": 817},
            "rubric_count_total": 15043,
            "negative_weight_candidate_count": 194,
        },
        metadata={"sha": "c70d2311cdca7129cab9376ba22eaa97c3cff3d7"},
        judge_model="anthropic:claude-sonnet-4-6",
    )

    by_name = {check.name: check for check in checks}
    assert by_name["Pinned public row count"].status == "pass"
    assert by_name["Leaderboard row count"].status == "warn"
    assert by_name["Rubric visibility"].status == "pass"
    assert parity_level(checks) == "public-hf-comparable"


def test_parity_blocks_rubric_visibility() -> None:
    checks = build_parity_checks(
        manifest={
            "dataset_id": "ScaleAI/TutorBench",
            "revision": "c70d2311cdca7129cab9376ba22eaa97c3cff3d7",
            "row_count": 1473,
            "modality_counts": {"multimodal": 817},
            "rubric_count_total": 15043,
            "negative_weight_candidate_count": 194,
        },
        judge_model="anthropic:claude-sonnet-4-6",
        candidate_rubric_visibility=True,
    )

    assert parity_level(checks) == "blocked"
