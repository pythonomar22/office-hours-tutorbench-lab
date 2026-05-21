from __future__ import annotations

from tutorbench_lab.eval_sets import EvalSet, examples_for_eval_set


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
