from __future__ import annotations

import json

from tutorbench_lab.protocol import build_turn_input
from tutorbench_lab.response_selector import (
    build_selector_turn,
    parse_selector_decision,
)
from tutorbench_lab.schemas import Strategy, TutorResponse
from tutorbench_lab.tutor import record_for_response


def test_parse_selector_decision_accepts_json_block() -> None:
    decision = parse_selector_decision(
        """```json
        {"selected_source": "auxiliary", "confidence": 0.72, "reason": "more grounded"}
        ```"""
    )

    assert decision.selected_source == "auxiliary"
    assert decision.confidence == 0.72


def test_selector_turn_excludes_rubric_text(adaptive_example) -> None:
    primary = _record(adaptive_example, run_id="primary", text="Primary response")
    auxiliary = _record(adaptive_example, run_id="aux", text="Aux response")

    turn = build_selector_turn(primary, auxiliary)
    payload = json.dumps(turn.model_dump(mode="json"))

    assert "Primary response" in turn.user_prompt
    assert "Aux response" in turn.user_prompt
    assert adaptive_example.rubrics[0].criteria not in payload
    assert adaptive_example.rubrics[1].criteria not in payload


def _record(example, *, run_id: str, text: str):
    turn = build_turn_input(example, prompt_version="test")
    response = TutorResponse(
        task_id=example.task_id,
        text=text,
        model="test-model",
        strategy=Strategy.AGENTIC,
        prompt_version=run_id,
    )
    return record_for_response(
        example=example,
        turn=turn,
        response=response,
        run_id=run_id,
    )
