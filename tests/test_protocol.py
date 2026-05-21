from __future__ import annotations

from tutorbench_lab.protocol import build_turn_input
from tutorbench_lab.schemas import UseCase


def test_adaptive_protocol_includes_initial_explanation_and_followup(adaptive_example):
    turn = build_turn_input(adaptive_example)

    assert turn.use_case == UseCase.ADAPTIVE
    assert "initial tutor explanation" in turn.user_prompt.lower()
    assert "HI is strongest" in turn.user_prompt
    assert "fluorine is most electronegative" in turn.user_prompt
    assert "follow-up" in turn.system_prompt.lower()


def test_active_learning_protocol_warns_against_full_answer(active_learning_example):
    turn = build_turn_input(active_learning_example)

    assert turn.use_case == UseCase.ACTIVE_LEARNING
    assert "without giving away the full answer" in turn.system_prompt
    assert "Give a targeted hint" in turn.user_prompt
