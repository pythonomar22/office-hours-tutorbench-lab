from __future__ import annotations

from tutorbench_lab.numeric_probe import build_numeric_probe
from tutorbench_lab.protocol import build_turn_input
from tutorbench_lab.schemas import RubricCriterion, TutorBenchExample


def test_numeric_probe_catches_scientific_notation_subtraction() -> None:
    example = TutorBenchExample(
        task_id="tractor",
        batch="USE_CASE_3_TEXT",
        subject="Physics",
        prompt=(
            "A tractor exerts 1.85×10⁴ N and resisting forces total 2300 N. "
            "The acceleration is 0.140 m/s² and the tractor mass is 1950 kg."
        ),
        follow_up_prompt=(
            "m_a = (1.85×10⁴ N − 2300 N) / 0.140 m/s² − 1950 kg"
        ),
        rubrics=[RubricCriterion(criteria="The response should help.")],
    )

    probe = build_numeric_probe(build_turn_input(example))

    assert probe is not None
    assert "1.85×10⁴ = 18500" in probe
    assert "1.85×10⁴ − 2300 = 16200" in probe


def test_numeric_probe_returns_none_without_visible_arithmetic(
    adaptive_example: TutorBenchExample,
) -> None:
    probe = build_numeric_probe(build_turn_input(adaptive_example))

    assert probe is None
