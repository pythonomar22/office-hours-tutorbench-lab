# TutorBench Evaluation Protocol

This document defines what counts as a fair local TutorBench comparison in this
lab. It is intentionally conservative: local results are engineering evidence,
not leaderboard claims, until Scale evaluates the system or we reproduce their
submission protocol exactly.

## Dataset

- Source: `ScaleAI/TutorBench` on Hugging Face.
- Pinned revision: `c70d2311cdca7129cab9376ba22eaa97c3cff3d7`.
- Local full public-HF size: 1,473 rows.
- Dataset use: evaluation only.
- Public repo policy: do not commit raw dataset rows, images, prompt text,
  follow-up text, initial explanations, or sample-specific rubric criteria.

## Generation Rules

- The candidate tutor receives only the task protocol input assembled by
  `tutorbench_lab.protocol.build_turn_input`.
- Sample-specific rubrics are evaluator-only and must not be visible to the
  candidate tutor, planner, verifier, critic, or deterministic guards.
- Agentic traces may use rubric-blind task-family playbooks, but only when they
  are derived from broad task content and not from row-specific rubric wording.
- For multimodal rows, image content may be sent to candidate models when the
  model supports vision. Image files and URLs are not published in public run
  artifacts.

## Judging Rules

- Default judge: `anthropic:claude-sonnet-4-6`, chosen to stay close to the
  paper's Claude Sonnet 4-family judge.
- Scoring uses weighted ARRw over pass/fail rubric ratings.
- Public rows expose severity tags but not always the official signed weights,
  so this lab infers:
  - critical positive criteria: `+5`
  - non-critical positive criteria: `+1`
  - likely spoiler/failure criteria: `-5`
- Rows with inferred negative criteria are counted as manual-review rows and
  must be called out in reports.

## Split Discipline

- `office_hours_dev10`: quick trace debugging.
- `office_hours_dev50`: architecture iteration and prompt debugging.
- `validation150`: sparse validation only; avoid row-by-row tuning after the
  current checkpoint.
- `heldout500`: larger public-HF holdout, excluding the above inspected sets.
- Full public-HF run: final local evidence once the architecture is frozen.

## Claim Levels

- `engineering-smoke`: small dev split, useful only for debugging.
- `public-HF-comparable`: pinned public Hugging Face rows, local judge, documented
  scoring, and no rubric leakage during generation.
- `leaderboard-calibrated`: local judge reproduces published model ordering on
  the same split closely enough to trust deltas.
- `leaderboard-exact`: Scale-side evaluation or an official submission protocol.

Any external claim should use the most conservative applicable label. The
current validation checkpoint is `public-HF-comparable`, not
`leaderboard-exact`.

## Shareable Artifacts

Safe to publish:

- `scores*.json`
- `analysis.md` / `analysis.json`
- `report*.md`
- `compare*.md`
- `redacted_traces*.jsonl`

Not safe to publish publicly:

- `responses*.jsonl`
- `judged*.jsonl`
- raw `data/processed/*.jsonl`
- raw Hugging Face dataset files
- `.env`

Use `tutorbench-lab export-traces` to create redacted trace JSONL for team
review.

## Calibration Plan

Before treating a large local score as leaderboard evidence:

1. Run at least two published single-model baselines on the same held-out split.
2. Judge them with the same judge settings used for the agentic tutor.
3. Verify that local ordering and approximate gaps are directionally consistent
   with the paper/leaderboard.
4. Only then compare the agentic tutor against the calibrated local baselines.

The key success condition is not just a high agent score. It is a high agent
score under a protocol where known public models behave approximately as
expected.
