# Evaluation Parity

The lab has two goals that must stay separate:

1. Improve the Office Hours tutor architecture quickly.
2. Make fair claims against the public TutorBench leaderboard.

The first goal can use small curated dev sets. The second goal requires parity
with the benchmark protocol and enough baseline calibration that our local judge
is not grading a different task.

## Current Public-Facing Facts

As of May 21, 2026, the Scale TutorBench leaderboard page reports:

- Leaderboard target: Muse Spark at `68.55±0.95`.
- Benchmark overview: `1,490` examples, `828` multimodal examples, and
  `15,220` rubric criteria.
- Judge family: Claude-4-Sonnet.

The pinned public Hugging Face dataset in this lab is:

- Dataset: `ScaleAI/TutorBench`
- Revision: `c70d2311cdca7129cab9376ba22eaa97c3cff3d7`
- Local manifest: `1,473` rows, `817` multimodal rows, `811` image-present
  rows, and `15,043` rubric criteria.

This means local full-set scores are useful for engineering and public-HF
comparison, but they are not exact leaderboard scores.

## Claim Levels

Use these labels when discussing results:

- **dev-set result**: tuned/inspected rows such as `office_hours_dev10`.
- **public-HF result**: all rows in the pinned Hugging Face release, judged by
  our local judge and scoring implementation.
- **calibrated public-HF result**: public-HF result plus published-model baseline
  reproduction showing local ordering and rough scores match known results.
- **leaderboard result**: Scale evaluates the system or response file through
  the official submission path.

Only the last category can support a leaderboard-beating claim.

## Parity Checklist

Before claiming improvement over leaderboard models, record:

- Dataset ID, revision, row count, task ID hash, image count, rubric count.
- Exact run strategy and candidate model IDs.
- Whether the candidate saw sample-specific rubrics. It must not.
- Prompt version and use-case message format.
- Image attachment behavior and multimodal failure policy.
- Judge model and judge prompt version.
- Signed rubric handling, especially `-5` spoiler criteria.
- ARRw formula and confidence-interval method.
- Failed API-call, skipped-row, and retry policy.
- Cost, latency, and raw response trace retention.

Run:

```bash
uv run tutorbench-lab audit-parity \
  --output-path data/processed/parity_audit.json
```

Expected current level: `public-hf-comparable`, not `leaderboard-exact`.

## Recommended Evaluation Ladder

1. `office_hours_dev10`: fast architecture debugging only.
2. `office_hours_dev50`: broader iteration set, no final claims.
3. `validation150`: sparse inspection; do not overfit row-by-row.
4. Full public-HF run: run after freezing architecture.
5. Baseline calibration: run at least one known published model and one cheaper
   baseline on the same sets.
6. Official submission: required for any leaderboard claim.

## Baseline Calibration

At minimum, compare:

- `baseline` single-model Sonnet-style tutor.
- `agentic` current Office Hours tutor.
- One published leaderboard model if affordable and available through API.

A fair comparison requires that our local judge ranks published baselines in the
same rough order as Scale. If not, improve judge parity before optimizing the
tutor further.

## Current Caution

The current dev10 score is intentionally overfit. It is useful because it exposed
real tutoring failure modes, but it should not be cited as benchmark performance.
The next meaningful score is `office_hours_dev50`, then `validation150`, then the
full public-HF release.
