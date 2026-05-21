"""Environment loading and model defaults."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from tutorbench_lab.constants import (
    DEFAULT_CANDIDATE_MODEL,
    DEFAULT_CRITIC_MODEL,
    DEFAULT_JUDGE_MODEL,
    DEFAULT_MAX_REVISION_ATTEMPTS,
    DEFAULT_PLANNER_MODEL,
    DEFAULT_REQUEST_TIMEOUT_S,
    DEFAULT_SOLVER_MODEL,
    DEFAULT_VERIFIER_MODEL,
)


def load_environment(env_file: Path | None = None) -> Path | None:
    """Load environment variables from a local .env file.

    Returns the file that was loaded, if one exists. Existing shell variables
    keep precedence over .env values.
    """

    if env_file is not None:
        if env_file.exists():
            load_dotenv(env_file, override=False)
            return env_file
        return None

    default = Path(".env")
    if default.exists():
        load_dotenv(default, override=False)
        return default
    load_dotenv(override=False)
    return None


def candidate_model_default() -> str:
    return os.getenv("TUTORBENCH_CANDIDATE_MODEL", DEFAULT_CANDIDATE_MODEL)


def solver_model_default() -> str:
    return os.getenv("TUTORBENCH_SOLVER_MODEL", DEFAULT_SOLVER_MODEL)


def planner_model_default() -> str:
    return os.getenv("TUTORBENCH_PLANNER_MODEL", DEFAULT_PLANNER_MODEL)


def verifier_model_default() -> str:
    return os.getenv("TUTORBENCH_VERIFIER_MODEL", DEFAULT_VERIFIER_MODEL)


def critic_model_default() -> str:
    return os.getenv("TUTORBENCH_CRITIC_MODEL", DEFAULT_CRITIC_MODEL)


def max_revision_attempts_default() -> int:
    raw = os.getenv("TUTORBENCH_MAX_REVISION_ATTEMPTS")
    if raw is None:
        return DEFAULT_MAX_REVISION_ATTEMPTS
    return int(raw)


def judge_model_default() -> str:
    return os.getenv("TUTORBENCH_JUDGE_MODEL", DEFAULT_JUDGE_MODEL)


def request_timeout_default() -> float:
    raw = os.getenv("TUTORBENCH_REQUEST_TIMEOUT_S")
    if raw is None:
        return DEFAULT_REQUEST_TIMEOUT_S
    return float(raw)
