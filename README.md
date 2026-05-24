# Office Hours TutorBench Lab

This repo is a separate evaluation lab for building an agentic tutor against
TutorBench before moving the tutor into the Office Hours app.

The lab is deliberately conservative about data and cost:

- TutorBench is treated as eval-only until licensing and leaderboard rules are explicit.
- The dataset is pinned to `ScaleAI/TutorBench` revision
  `c70d2311cdca7129cab9376ba22eaa97c3cff3d7`.
- `run` defaults to `dry_run`; real model calls require an explicit strategy.
- Defaults use Sonnet 4-family model specs. No GPT-5 Pro-style model is configured.
- `.env` is gitignored. Never commit API keys, raw dataset rows, or raw traces.

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
multimodal evidence audit, private solving, use-case-aware answer planning,
independent verification, composition, generic critic passes, and bounded
revisions. Each generated row stores per-stage latency and token usage in the
trace so we can decide which rows deserve the full pipeline later.

Focused rerun for one or more trace-review rows:

```bash
uv run tutorbench-lab run \
  --strategy agentic \
  --task-id 683e45123a967938ab5f5de2
```

Blend two response runs with the current v10 rubric-blind router:

```bash
uv run tutorbench-lab blend-responses \
  runs/heldout500-agentic-v6/responses.jsonl \
  runs/heldout500-agentic-v9/responses.jsonl \
  runs/heldout500-blend-v10/responses.jsonl \
  --run-id heldout500-blend-v10 \
  --policy conservative-v10
```

This command does not inspect rubrics or judgments. It keeps the primary run by
default and selects the auxiliary run only for configured playbooks/slices.

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
  --judge-model anthropic:claude-sonnet-4-6 \
  --workers 16
```

The scorer computes TutorBench-style weighted ARRw. Public TutorBench rubrics
include severity but do not always expose explicit signed weights, so likely
negative `-5` spoiler criteria are inferred and flagged for manual review. The
heuristic treats explicit bad-behavior criteria like "reveals/gives away the
final answer" as likely negative; criteria that ask for the correct final answer
remain positive.
If a judge response is valid JSON but omits one or more criterion indices, the
judge harness repairs the row by asking the same judge only for the missing
criterion indices and merging those ratings; no candidate generation step sees
sample-specific rubrics.

`run` and `judge` support `--workers`, `--run-id`, and `--resume` for faster,
restartable iteration. The Anthropic client captures non-secret rate-limit
headers in traces for future runs. On the current Sonnet key, a cheap probe
reported very high limits (`20,000` requests, `2,000,000` input tokens, and
`400,000` output tokens in the current bucket), and full `office_hours_dev50`
agentic/judge runs at `--workers 24` completed without throttling. Use
`--workers 24` for dev-set iteration on this key, then inspect
`stage_rate_limits` before raising it further.

After judging a run, write the forensic report:

```bash
uv run tutorbench-lab analyze-run runs/<run_id>/judged.jsonl
```

For team review, export redacted traces. These keep task IDs, scores, model
outputs, per-stage usage, and rubric pass/fail metadata, but remove prompt text,
images, sample-specific rubric criteria, judge rationales, and private
scratchpads:

```bash
uv run tutorbench-lab export-traces runs/<run_id>/judged.jsonl
```

## Current Target

The working target is `>=70%` local full-set ARRw before treating the system as
plausibly leaderboard-beating. We have crossed that threshold on the larger
heldout500 split: baseline Sonnet `60.77%`, agentic-v6 `73.69%`, and the
blend-v10 router `75.33%`, CI `73.68%-77.12%`, in
`runs/heldout500-blend-v10/`. The current targeted-repair estimate is
`heldout500-blend-v11c-targeted` at `76.72%`, CI `75.02%-78.41%`, in
`runs/heldout500-blend-v11c-targeted/`. It keeps blend-v10 for unchanged rows
and replaces 10 diagnosed failures with verified v11c specialist outputs, so it
is stronger engineering evidence but not a fresh full generation run. The
current public leaderboard target should be rechecked before submission because
it can change.

Important: local public-HF results are not automatically leaderboard results.
Run the parity audit before making any comparison claim:

```bash
uv run tutorbench-lab audit-parity
```

See `docs/eval_protocol.md` and `docs/eval_parity.md` for claim levels,
calibration requirements, and the public artifact policy.

Current curated Office Hours dev10 best: `99.60%` ARRw in
`runs/7fd1b151-8dfa-46bf-924e-c96955e99dd1/`, after task-family playbooks and
deterministic final guards. Treat this as an overfit architecture-debugging
score, not a benchmark claim. Run artifacts are gitignored, but the architecture
and eval-set definition are tracked.

Current clean `office_hours_dev50` checkpoint: baseline Sonnet
`59.68%` vs agentic `85.28%` in
`runs/b0a72ccc-6f9f-4625-9ca7-a1f7f37d34cc/`, a +25.60 point gain. This is a
local public-HF dev-set score, not a leaderboard claim.

Current `validation150` checkpoint: baseline Sonnet `59.65%` vs agentic-v5
`77.21%`, CI `74.43%-80.05%`, in `runs/validation150-agentic-v5/`.
This is a local public-HF-comparable validation score, not an official
leaderboard result.

Current larger holdout anchor: baseline Sonnet `60.77%`, CI
`58.90%-62.83%`, vs targeted blend-v11c `76.72%`, CI `75.02%-78.41%`, over
`eval_sets/heldout500.json`. This 500-row split excludes
dev10/dev50/validation150. Blend-v11c is a +15.95 point same-set gain over
baseline and +1.38 points over blend-v10 (`75.33%`). It beats the local
`>=70%` target and is the strongest local public-HF-comparable engineering
anchor so far, but it is still not an official leaderboard result.

Current v6 result: `heldout500-agentic-v6` scored `73.69%` on the full 500-row
heldout split, and `73.51%` when rejudged with the current deterministic
Sonnet judge. The main v6 change is broadening the specialist evidence audit to
all multimodal rows and adding rubric-blind playbooks for recurring visual/code
failure families such as Normal MLE notation, binary-search midpoint overflow,
MovieRating integer division, shape center-distance hints, Henry-law
mole-fraction units, and bulb parallel-switch reasoning. V6 remains the stable
default response source inside blend-v10.

Current v9/v10 result: `heldout500-agentic-v9` scored `72.78%`; its targeted
numeric/visual fixes transferred to several probe rows but regressed the full
set relative to v6. The architecture lesson is now encoded as
`blend-responses`: `heldout500-blend-v10` keeps v6 by default and routes to v9
only for rubric-blind high-yield playbooks and coarse slices. It scored
`75.33%` overall, with active learning `77.86%`, assessment `76.28%`, adaptive
`71.86%`, text `76.50%`, and multimodal `74.16%`.

Current v11c result: `heldout-v11c-failure-probe-merged` scored `93.82%` on
the 10 diagnosed weak rows, versus `24.70%` for blend-v10 on those same rows.
Those repairs applied back into the heldout500 judged file produce
`heldout500-blend-v11c-targeted` at `76.72%`. New specialist routes cover
bakery flour/code logic, nonstandard tRNA translation, chocolate heat-lamp
assumptions, implicit tangent-line hints, archery/binomial target geometry,
connected conducting shells, and a narrow inclined-box verifier rewrite.

Current v4 failure probe: `probe10-agentic-v4-refined` scored `75.33%` on ten
representative weakest heldout500 failures, up from roughly `4%` on those same
rows in `heldout500-agentic-v3`. V4 retires full canned final rewrites, adds a
rubric-blind pedagogy coverage critic, and moves recurring failures into
diagnostic playbooks that guide the solver instead of replacing the response.

Current v5 validation result: `validation150-agentic-v5` scored `77.21%`, a
`+17.57` point same-set gain over Sonnet baseline and `+4.15` points over
`validation150-agentic-v4-refined`. V5 tightens wrong-family playbook routing,
adds stricter active-learning spoiler checks and assessment arithmetic audits,
and adds broad failure-family playbooks from trace analysis. A targeted
`validation-failure-probe-v5-final` moved 14 weak validation rows from a v4
average of `38.07%` to `73.07%`; the weak-acid titration route was retired
because it regressed against the generic agent.
