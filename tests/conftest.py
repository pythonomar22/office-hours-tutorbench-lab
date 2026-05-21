from __future__ import annotations

import pytest

from tutorbench_lab.schemas import RubricCriterion, TutorBenchExample


@pytest.fixture
def adaptive_example() -> TutorBenchExample:
    return TutorBenchExample(
        task_id="abc123",
        batch="USE_CASE_1_TEXT",
        subject="Chemistry",
        prompt="Rank HF, HCl, and HI from weakest to strongest acid.",
        uc1_initial_explanation="HI is strongest because the H-I bond is weakest.",
        follow_up_prompt=(
            "I thought fluorine is most electronegative, so why is HF not strongest?"
        ),
        rubrics=[
            RubricCriterion(
                criteria="The response must acknowledge the student's confusion.",
                attributes={"severity": "critical", "eval_dimension": "style_tone"},
            ),
            RubricCriterion(
                criteria=(
                    "The response must explain that bond strength dominates "
                    "for hydrogen halides."
                ),
                attributes={"severity": "critical", "eval_dimension": "truthfulness"},
            ),
        ],
        bloom_taxonomy="Understand",
    )


@pytest.fixture
def active_learning_example() -> TutorBenchExample:
    return TutorBenchExample(
        task_id="def456",
        batch="USE_CASE_3_TEXT",
        subject="Statistics",
        prompt="Calculate the mean and standard deviation from a frequency table.",
        follow_up_prompt="I multiplied some values but I am stuck.",
        rubrics=[
            RubricCriterion(
                criteria=(
                    "The response should ask the student to compute each hours "
                    "times frequency product."
                ),
                attributes={"severity": "not_critical"},
            ),
            RubricCriterion(
                criteria="The response reveals the final answer directly.",
                attributes={"severity": "critical"},
            ),
        ],
        bloom_taxonomy="Apply",
    )
