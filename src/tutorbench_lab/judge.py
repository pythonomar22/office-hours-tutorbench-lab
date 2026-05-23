"""Rubric-based judging and ARRw scoring."""

from __future__ import annotations

import json
import re
import time
from textwrap import dedent

from tutorbench_lab.providers import make_client
from tutorbench_lab.schemas import (
    CriterionRating,
    JudgedRunRecord,
    JudgeResult,
    ModelUsage,
    RunRecord,
    TutorTurnInput,
)

_JSON_BLOCK_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


class JudgeRatingsMismatch(ValueError):
    """Raised when judge JSON is valid but does not cover the requested indices."""

    def __init__(
        self,
        *,
        missing: list[int],
        extra: list[int],
        ratings: list[CriterionRating],
    ):
        super().__init__(f"judge ratings mismatch; missing={missing}, extra={extra}")
        self.missing = missing
        self.extra = extra
        self.ratings = ratings


def judge_run_record(
    run: RunRecord,
    *,
    judge_model: str,
    max_tokens: int = 2000,
    request_timeout_s: float | None = None,
) -> JudgedRunRecord:
    """Judge one run record with either a real LLM judge or heuristic mode."""

    if judge_model == "heuristic":
        judge = heuristic_judge(run)
    else:
        judge = llm_judge(
            run,
            judge_model=judge_model,
            max_tokens=max_tokens,
            request_timeout_s=request_timeout_s,
        )
    arrw_raw, arrw, manual_review = compute_arrw(run, judge)
    return JudgedRunRecord(
        run=run,
        judge=judge,
        arrw_raw=arrw_raw,
        arrw=arrw,
        manual_weight_review=manual_review,
    )


def llm_judge(
    run: RunRecord,
    *,
    judge_model: str,
    max_tokens: int = 2000,
    max_parse_attempts: int = 2,
    request_timeout_s: float | None = None,
) -> JudgeResult:
    """Run an LLM judge against sample-specific rubrics."""

    turn = build_judge_turn(run)
    client = make_client(judge_model, timeout_s=request_timeout_s)
    errors = []
    total_latency_ms = 0
    last_text = ""
    best_partial: JudgeRatingsMismatch | None = None
    last_usage = ModelUsage()
    for attempt in range(max_parse_attempts + 1):
        start = time.monotonic()
        result = client.generate(turn, max_tokens=max_tokens)
        total_latency_ms += int((time.monotonic() - start) * 1000)
        last_text = result.text
        last_usage = result.usage
        try:
            ratings = parse_judge_json(
                result.text,
                expected_count=len(run.example.rubrics),
            )
        except JudgeRatingsMismatch as exc:
            errors.append(f"attempt {attempt + 1}: {exc}")
            if exc.ratings and not exc.extra:
                best_partial = exc
            continue
        except ValueError as exc:
            errors.append(f"attempt {attempt + 1}: {exc}")
            continue
        return JudgeResult(
            task_id=run.example.task_id,
            judge_model=judge_model,
            ratings=ratings,
            raw_judge_output=result.text,
            latency_ms=total_latency_ms,
            usage=result.usage,
        )
    if best_partial:
        repair_turn = build_missing_judge_turn(run, best_partial.missing)
        start = time.monotonic()
        repair = client.generate(repair_turn, max_tokens=max(1000, max_tokens // 2))
        total_latency_ms += int((time.monotonic() - start) * 1000)
        repair_ratings = parse_judge_json_for_indices(
            repair.text,
            expected_indices=set(best_partial.missing),
        )
        ratings_by_idx = {
            rating.criterion_index: rating for rating in best_partial.ratings
        }
        ratings_by_idx.update(
            {rating.criterion_index: rating for rating in repair_ratings}
        )
        ratings = [ratings_by_idx[idx] for idx in sorted(ratings_by_idx)]
        return JudgeResult(
            task_id=run.example.task_id,
            judge_model=judge_model,
            ratings=ratings,
            raw_judge_output=(
                last_text
                + "\n\n--- missing-rating-repair ---\n"
                + repair.text
            ),
            latency_ms=total_latency_ms,
            usage=_merge_usage(last_usage, repair.usage),
        )
    raise ValueError(
        "judge output could not be parsed after retries: "
        + "; ".join(errors)
        + f"; last output preview={last_text[:500]!r}"
    )


def build_judge_turn(run: RunRecord) -> TutorTurnInput:
    rubric_lines = []
    for idx, rubric in enumerate(run.example.rubrics):
        weight_note = (
            "LIKELY_NEGATIVE_WEIGHT: pass means the undesirable behavior is present"
            if rubric.negative_weight_candidate
            else "POSITIVE_WEIGHT: pass means the response satisfies this criterion"
        )
        rubric_lines.append(
            f"{idx}. [{rubric.severity}; {weight_note}] {rubric.criteria}"
        )

    user_prompt = dedent(
        f"""\
        Original TutorBench task:
        {run.turn_input.user_prompt}

        Candidate tutor response:
        {run.response.text}

        Rubric criteria:
        {chr(10).join(rubric_lines)}

        Grade each criterion independently as pass/fail. Return JSON only.
        Do not include rationale text; free-form rationale strings often make
        JSON invalid. Use exactly this compact shape:
        {{
          "ratings": [
            {{"criterion_index": 0, "passed": true, "confidence": 0.9}}
          ]
        }}
        """
    ).strip()

    return TutorTurnInput(
        task_id=run.example.task_id,
        use_case=run.example.use_case,
        modality=run.example.modality,
        subject=run.example.subject,
        system_prompt=dedent(
            """\
            You are a careful TutorBench judge. Apply only the provided
            sample-specific criteria to the candidate response. Criteria may
            describe either desirable behavior or undesirable behavior; follow
            the weight note attached to each criterion. Do not reward facts that
            are not present in the candidate response. Return strict JSON only,
            without rationale strings or explanatory text.
            """
        ).strip(),
        user_prompt=user_prompt,
        image=run.example.image,
        prompt_version="judge-v1",
    )


def build_missing_judge_turn(run: RunRecord, missing_indices: list[int]) -> TutorTurnInput:
    rubric_lines = []
    for idx in missing_indices:
        rubric = run.example.rubrics[idx]
        weight_note = (
            "LIKELY_NEGATIVE_WEIGHT: pass means the undesirable behavior is present"
            if rubric.negative_weight_candidate
            else "POSITIVE_WEIGHT: pass means the response satisfies this criterion"
        )
        rubric_lines.append(
            f"{idx}. [{rubric.severity}; {weight_note}] {rubric.criteria}"
        )

    user_prompt = dedent(
        f"""\
        Original TutorBench task:
        {run.turn_input.user_prompt}

        Candidate tutor response:
        {run.response.text}

        Missing rubric criteria to grade:
        {chr(10).join(rubric_lines)}

        Grade only these missing criterion indices independently as pass/fail.
        Return JSON only. The ratings list must contain exactly these indices:
        {missing_indices}

        Use exactly this compact shape:
        {{
          "ratings": [
            {{"criterion_index": {missing_indices[0]}, "passed": true, "confidence": 0.9}}
          ]
        }}
        """
    ).strip()

    return TutorTurnInput(
        task_id=run.example.task_id,
        use_case=run.example.use_case,
        modality=run.example.modality,
        subject=run.example.subject,
        system_prompt=dedent(
            """\
            You are a careful TutorBench judge repairing an incomplete
            judgment. Apply only the provided missing criterion or criteria to
            the candidate response. Return strict JSON only, without rationale
            strings or explanatory text.
            """
        ).strip(),
        user_prompt=user_prompt,
        image=run.example.image,
        prompt_version="judge-v1-missing-repair",
    )


def parse_judge_json(raw: str, *, expected_count: int) -> list[CriterionRating]:
    ratings = _load_judge_ratings(raw)
    return _validate_judge_indices(ratings, expected_indices=set(range(expected_count)))


def parse_judge_json_for_indices(
    raw: str, *, expected_indices: set[int]
) -> list[CriterionRating]:
    ratings = _load_judge_ratings(raw)
    return _validate_judge_indices(ratings, expected_indices=expected_indices)


def _load_judge_ratings(raw: str) -> list[CriterionRating]:
    payload_text = _extract_json(raw)
    payload = json.loads(payload_text)
    ratings_raw = payload.get("ratings")
    if not isinstance(ratings_raw, list):
        raise ValueError("judge output must contain a ratings list")
    return [CriterionRating.model_validate(item) for item in ratings_raw]


def _validate_judge_indices(
    ratings: list[CriterionRating], *, expected_indices: set[int]
) -> list[CriterionRating]:
    seen = {rating.criterion_index for rating in ratings}
    if seen != expected_indices:
        missing = sorted(expected_indices - seen)
        extra = sorted(seen - expected_indices)
        raise JudgeRatingsMismatch(missing=missing, extra=extra, ratings=ratings)
    return sorted(ratings, key=lambda item: item.criterion_index)


def _merge_usage(first: ModelUsage, second: ModelUsage) -> ModelUsage:
    return ModelUsage(
        input_tokens=_sum_optional(first.input_tokens, second.input_tokens),
        output_tokens=_sum_optional(first.output_tokens, second.output_tokens),
        total_tokens=_sum_optional(first.total_tokens, second.total_tokens),
        estimated_cost_usd=_sum_optional(
            first.estimated_cost_usd, second.estimated_cost_usd
        ),
    )


def _sum_optional(first: float | int | None, second: float | int | None):
    if first is None and second is None:
        return None
    return (first or 0) + (second or 0)


def compute_arrw(run: RunRecord, judge: JudgeResult) -> tuple[float, float, bool]:
    """Compute TutorBench-style weighted ARRw.

    Public rubrics expose severity but not always explicit signed weights. We
    infer +5/+1 and flag likely negative -5 criteria for manual review.
    """

    ratings_by_idx = {rating.criterion_index: rating for rating in judge.ratings}
    numerator = 0.0
    denominator = 0.0
    manual_review = False

    for idx, rubric in enumerate(run.example.rubrics):
        weight = rubric.inferred_weight
        rating = ratings_by_idx[idx]
        if weight < 0:
            manual_review = True
        else:
            denominator += weight
        if rating.passed:
            numerator += weight

    raw = 0.0 if denominator == 0 else numerator / denominator
    return raw, max(0.0, min(1.0, raw)), manual_review


def heuristic_judge(run: RunRecord) -> JudgeResult:
    """A deterministic placeholder judge for plumbing tests.

    It is intentionally simple and not a benchmark substitute.
    """

    lower = run.response.text.lower()
    ratings: list[CriterionRating] = []
    for idx, rubric in enumerate(run.example.rubrics):
        if rubric.negative_weight_candidate:
            passed = "final answer" in lower or "the answer is" in lower
        else:
            keywords = _keyword_set(rubric.criteria)
            passed = not keywords or any(keyword in lower for keyword in keywords)
        ratings.append(
            CriterionRating(
                criterion_index=idx,
                passed=passed,
                confidence=0.5,
                rationale="heuristic placeholder",
            )
        )
    return JudgeResult(
        task_id=run.example.task_id,
        judge_model="heuristic",
        ratings=ratings,
        raw_judge_output="heuristic placeholder",
        latency_ms=0,
        usage=ModelUsage(),
    )


def _extract_json(raw: str) -> str:
    stripped = raw.strip()
    match = _JSON_BLOCK_RE.search(stripped)
    if match:
        return match.group(1).strip()
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("could not find JSON object in judge output")
    return stripped[start : end + 1]


def _keyword_set(criteria: str) -> set[str]:
    words = re.findall(r"[A-Za-z][A-Za-z]{4,}", criteria.lower())
    stop = {
        "response",
        "student",
        "should",
        "must",
        "correctly",
        "include",
        "identify",
        "explain",
        "state",
        "states",
    }
    return {word for word in words if word not in stop}
