from __future__ import annotations

from tutorbench_lab.eval_sets import EvalSet, build_eval_set, examples_for_eval_set
from tutorbench_lab.selection import StratifyBy


def test_eval_set_preserves_order(adaptive_example, active_learning_example):
    eval_set = EvalSet(
        name="test",
        task_ids=[
            {"task_id": active_learning_example.task_id, "why": "active"},
            {"task_id": adaptive_example.task_id, "why": "adaptive"},
        ],
    )

    selected = examples_for_eval_set(
        [adaptive_example, active_learning_example],
        eval_set,
    )

    assert [example.task_id for example in selected] == [
        active_learning_example.task_id,
        adaptive_example.task_id,
    ]


def test_build_eval_set_records_selection_policy(adaptive_example):
    eval_set = build_eval_set(
        name="dev",
        description="test split",
        examples=[adaptive_example],
        selection_policy=["seed=1"],
        stratify_by=StratifyBy.USE_CASE_MODALITY,
    )

    assert eval_set.name == "dev"
    assert eval_set.selection_policy == ["seed=1"]
    assert eval_set.task_ids[0].task_id == adaptive_example.task_id
    assert "adaptive:text" in eval_set.task_ids[0].why
