from __future__ import annotations

from tutorbench_lab.dataset import build_manifest, validate_examples


def test_manifest_summarizes_examples(adaptive_example, active_learning_example):
    manifest = build_manifest([adaptive_example, active_learning_example])

    assert manifest["row_count"] == 2
    assert manifest["use_case_counts"]["adaptive"] == 1
    assert manifest["use_case_counts"]["active_learning"] == 1
    assert manifest["negative_weight_candidate_count"] == 1


def test_validate_examples_allows_non_strict_subset(adaptive_example):
    validate_examples([adaptive_example], strict=False)
