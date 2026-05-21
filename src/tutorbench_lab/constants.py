"""Project-wide constants for the TutorBench lab."""

from __future__ import annotations

from pathlib import Path

DATASET_ID = "ScaleAI/TutorBench"
DATASET_REVISION = "c70d2311cdca7129cab9376ba22eaa97c3cff3d7"
DATASET_SPLIT = "train"

EXPECTED_ROW_COUNT = 1473
EXPECTED_USE_CASE_COUNTS = {
    "adaptive": 473,
    "assessment": 507,
    "active_learning": 493,
}
EXPECTED_BATCH_COUNTS = {
    "USE_CASE_1_MULTIMODAL": 146,
    "USE_CASE_1_TEXT": 327,
    "USE_CASE_2_MULTIMODAL": 342,
    "USE_CASE_2_TEXT": 165,
    "USE_CASE_3_MULTIMODAL": 329,
    "USE_CASE_3_TEXT": 164,
}
EXPECTED_SUBJECTS = {
    "Biology",
    "Calculus",
    "Chemistry",
    "Computer Science",
    "Physics",
    "Statistics",
}

DEFAULT_DATA_DIR = Path("data")
DEFAULT_RAW_DATASET_DIR = DEFAULT_DATA_DIR / "raw" / "hf_dataset"
DEFAULT_MANIFEST_PATH = DEFAULT_DATA_DIR / "processed" / "manifest.json"
DEFAULT_EXAMPLES_JSONL = DEFAULT_DATA_DIR / "processed" / "examples.jsonl"
DEFAULT_HF_METADATA_PATH = DEFAULT_DATA_DIR / "processed" / "hf_metadata.json"

PROMPT_VERSION = "paper-v1"
AGENT_PROMPT_VERSION = "agentic-v2"

DEFAULT_CANDIDATE_MODEL = "anthropic:claude-sonnet-4-6"
DEFAULT_JUDGE_MODEL = "anthropic:claude-sonnet-4-6"
DEFAULT_SOLVER_MODEL = "anthropic:claude-sonnet-4-6"
DEFAULT_PLANNER_MODEL = "anthropic:claude-sonnet-4-6"
DEFAULT_VERIFIER_MODEL = "anthropic:claude-sonnet-4-6"
DEFAULT_CRITIC_MODEL = "anthropic:claude-sonnet-4-6"
DEFAULT_MAX_REVISION_ATTEMPTS = 2
DEFAULT_REQUEST_TIMEOUT_S = 75.0

LEADERBOARD_TARGET_SCORE = 0.70
