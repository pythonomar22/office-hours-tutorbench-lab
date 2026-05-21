# Office Hours TutorBench Lab

This repo is a separate evaluation lab for building an agentic tutor against
TutorBench before moving the tutor into the Office Hours app.

The lab is deliberately conservative about data and cost:

- TutorBench is treated as eval-only until licensing and leaderboard rules are explicit.
- The dataset is pinned to `ScaleAI/TutorBench` revision
  `c70d2311cdca7129cab9376ba22eaa97c3cff3d7`.
- `run` defaults to `dry_run`; real model calls require an explicit strategy.
- Defaults use Sonnet 4-family model specs. No GPT-5 Pro-style model is configured.
- `.env` is gitignored. Never commit API keys or model outputs.

## Setup

```bash
uv sync
cp .env.example .env
```

Fill only the keys you intend to use. If keys have ever been pasted into chat,
rotate them before relying on them.

The CLI loads `.env` from the current working directory by default. To use a
different file:

```bash
uv run tutorbench-lab --env-file /path/to/.env doctor
```

Cheap key diagnostics:

```bash
uv run tutorbench-lab doctor
uv run tutorbench-lab doctor --ping
```

`--ping` calls provider model-list endpoints only; it does not generate text.

## Dataset

Fetch only Hugging Face metadata:

```bash
uv run tutorbench-lab fetch --metadata-only
```

Download and validate the pinned full dataset:

```bash
uv run tutorbench-lab fetch
```

This writes:

- `data/raw/hf_dataset/`: local Hugging Face dataset cache
- `data/processed/examples.jsonl`: normalized row records
- `data/processed/manifest.json`: distribution and integrity summary

Expected distribution:

- UC1 adaptive explanation: `473`
- UC2 assessment and feedback: `507`
- UC3 active learning: `493`
- Total rows: `1473`

## Run Candidates

Smoke test without model APIs:

```bash
uv run tutorbench-lab run --strategy dry-run --limit 5
```

Single-model baseline:

```bash
uv run tutorbench-lab run \
  --strategy baseline \
  --model anthropic:claude-sonnet-4-6 \
  --limit 20
```

Agentic tutor:

```bash
uv run tutorbench-lab run \
  --strategy agentic \
  --model anthropic:claude-sonnet-4-6 \
  --solver-model anthropic:claude-sonnet-4-6 \
  --critic-model anthropic:claude-sonnet-4-6 \
  --stratified-per-bucket 1 \
  --stratify-by use-case-modality
```

Curated Office Hours dev set:

```bash
uv run tutorbench-lab run \
  --strategy agentic \
  --eval-set eval_sets/office_hours_dev10.json \
  --model anthropic:claude-sonnet-4-6 \
  --solver-model anthropic:claude-sonnet-4-6 \
  --planner-model anthropic:claude-sonnet-4-6 \
  --verifier-model anthropic:claude-sonnet-4-6 \
  --critic-model anthropic:claude-sonnet-4-6 \
  --max-revision-attempts 2
```

Candidate generation never sees sample-specific rubrics.

The current agentic route is not a single prompt. It can run visual
perception, local visual probes for labelled diagrams, a specialist
multimodal-assessment audit, private solving, use-case-aware answer planning,
independent verification, composition, generic critic passes, and bounded
revisions. Each generated row stores per-stage latency and token usage in the
trace so we can decide which rows deserve the full pipeline later.

Focused rerun for one or more trace-review rows:

```bash
uv run tutorbench-lab run \
  --strategy agentic \
  --task-id 683e45123a967938ab5f5de2
```

## Judge And Score

Plumbing check with deterministic heuristic judge:

```bash
uv run tutorbench-lab judge runs/<run-id>/responses.jsonl --judge-model heuristic
uv run tutorbench-lab score runs/<run-id>/judged.jsonl
uv run tutorbench-lab report runs/<run-id>/scores.json
```

Real rubric judge:

```bash
uv run tutorbench-lab judge \
  runs/<run-id>/responses.jsonl \
  --judge-model anthropic:claude-sonnet-4-6
```

The scorer computes TutorBench-style weighted ARRw. Public TutorBench rubrics
include severity but do not always expose explicit signed weights, so likely
negative `-5` spoiler criteria are inferred and flagged for manual review.

## Current Target

The working target is `>=70%` local full-set ARRw before treating the system as
plausibly leaderboard-beating. The public leaderboard target should be rechecked
before submission because it can change.

Current curated Office Hours dev10 best: `81.18%` ARRw in
`runs/5f9a7c7e-04a6-4824-9183-d1d1f2a0a4ff/`, using the routed visual-probe
architecture. Run artifacts are gitignored, but the architecture and eval-set
definition are tracked.
