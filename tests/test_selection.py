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
