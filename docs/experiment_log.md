# Experiment Log

This log records claim-relevant TutorBench lab checkpoints. Scores below are
local public-HF/dev-set results unless explicitly marked as official.

## 2026-05-21/22 Dev50 Iteration

- Baseline Sonnet run: `be000157-89b3-4563-910f-4053ad259c1e`
  - Score: `59.68%` over 50 rows, CI `54.27%-65.13%`.
- First clean agentic checkpoint: `2ddb82f0-4947-46e6-be98-f8fa4901eacd`
  - Score: `74.72%`, CI `68.47%-81.10%`.
  - Delta vs baseline: `+15.04` points.
- Throughput/audit checkpoint:
  - Anthropic probe reported bucket headers near `20,000` requests,
    `2,000,000` input tokens, and `400,000` output tokens.
  - `--workers 24` completed full dev50 generation and judging without
    throttling.
  - Added `analyze-run` to log weak rows, rubric dimensions/skills, playbook
    coverage, usage, latency, and rate-limit headroom.
- Post-analysis agentic checkpoint: `74c31dbe-1c56-4349-b493-3300f2313d89`
  - Score: `82.32%`, CI `76.75%-87.33%`.
  - Delta vs baseline: `+22.64` points.
  - Main changes: pKa titration, Arctic fox denaturation, Gene X methylation,
    cellular respiration, conical pendulum, magnetic triangle, binary-tree
    traversal, and multimodal late playbook routing.
- Current clean dev50 checkpoint: `b0a72ccc-6f9f-4625-9ca7-a1f7f37d34cc`
  - Score: `85.28%`, CI `80.11%-89.66%`.
  - Delta vs baseline: `+25.60` points.
  - Use-case scores: active learning `90.98%`, adaptive `79.56%`, assessment
    `84.59%`.
  - Modality scores: text `87.48%`, multimodal `83.08%`.
  - Main additional changes: rubric-blind playbooks/templates for
    sulphonation hyperconjugation, Bayes/conditional probability, z-test vs
    t-test feedback, kth-smallest matrix search, and rotating charged ring
    potential.

## Current Claim Status

- Claim level: validation-set result, not official leaderboard.
- Parity level: `public-hf-comparable`, not leaderboard-exact.
- Current validation set: `eval_sets/validation150.json`, 150 rows excluding
  dev10/dev50, balanced as 25 rows per use-case/modality bucket.
- Current validation checkpoint: `validation150-retired-playbooks-v3`
  - Score: `72.13%`, CI `69.02%-75.35%`.
  - Same-set Sonnet baseline: `59.65%`, CI `56.14%-63.22%`.
  - Delta vs baseline: `+12.48` points.
  - Use-case scores: active learning `75.65%`, adaptive `72.24%`, assessment
    `68.49%`.
  - Modality scores: text `74.87%`, multimodal `69.38%`.
  - Main changes since dev50: narrowed playbook routing by use case, added
    parallel error logging/resume safety, and retired brittle deterministic
    playbooks for coffee/under-filling, two-proportion hints, regression
    residuals, and two's-complement hints after validation showed the generic
    agent beat those rewrites.
- Blockers before any benchmark claim:
  - Run full pinned public-HF dataset.
  - Calibrate local judge by reproducing at least one published baseline/model
    ordering on the same protocol.
  - Use Scale's official submission path for a true leaderboard claim.
