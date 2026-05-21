from __future__ import annotations

from tutorbench_lab.schemas import RubricCriterion, TutorBenchExample
from tutorbench_lab.selection import StratifyBy, select_examples


def _example(task_id: str, batch: str, subject: str = "Chemistry") -> TutorBenchExample:
    return TutorBenchExample(
        task_id=task_id,
        batch=batch,
        subject=subject,
        prompt="Prompt",
        follow_up_prompt="Follow-up",
        rubrics=[RubricCriterion(criteria="The response must be correct.")],
    )


def test_stratified_sampling_takes_per_bucket():
    examples = [
        _example("a1", "USE_CASE_1_TEXT"),
        _example("a2", "USE_CASE_1_TEXT"),
        _example("b1", "USE_CASE_1_MULTIMODAL"),
        _example("c1", "USE_CASE_2_TEXT"),
        _example("d1", "USE_CASE_3_TEXT"),
    ]

    selected = select_examples(
        examples,
        stratified_per_bucket=1,
        stratify_by=StratifyBy.USE_CASE_MODALITY,
        seed=1,
    )

    assert len(selected) == 4
    assert {
        f"{example.use_case.value}:{example.modality.value}" for example in selected
    } == {
        "adaptive:text",
        "adaptive:multimodal",
        "assessment:text",
        "active_learning:text",
    }


def test_stratified_limit_trims_balanced_buckets():
    examples = []
    batches = ["USE_CASE_1_TEXT", "USE_CASE_2_TEXT", "USE_CASE_3_TEXT"]
    for bucket_index, batch in enumerate(batches):
        for item_index in range(4):
            examples.append(_example(f"{bucket_index}-{item_index}", batch))

    selected = select_examples(
        examples,
        limit=8,
        stratified_per_bucket=4,
        stratify_by=StratifyBy.USE_CASE,
        seed=7,
    )

    counts: dict[str, int] = {}
    for example in selected:
        counts[example.use_case.value] = counts.get(example.use_case.value, 0) + 1

    assert sorted(counts.values()) == [2, 3, 3]
