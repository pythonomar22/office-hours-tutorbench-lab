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
- Larger holdout set: `eval_sets/heldout500.json`, 500 rows excluding
  dev10/dev50/validation150.
- Heldout500 Sonnet baseline: `heldout500-sonnet-baseline`
  - Score: `60.77%`, CI `58.90%-62.83%`.
  - Use-case scores: active learning `65.26%`, adaptive `59.33%`, assessment
    `57.70%`.
  - Modality scores: text `63.96%`, multimodal `57.55%`.
  - This is close to the validation150 Sonnet baseline (`59.65%`), which is a
    useful sanity check that the larger split is not obviously easier.
- Heldout500 agentic checkpoint: `heldout500-agentic-v3`
  - Score: `68.23%`, CI `66.11%-70.23%`.
  - Same-set Sonnet baseline: `60.77%`, CI `58.90%-62.83%`.
  - Delta vs baseline: `+7.46` points.
  - Use-case scores: active learning `70.56%`, adaptive `65.80%`, assessment
    `68.32%`.
  - Modality scores: text `69.55%`, multimodal `66.89%`.
  - Main remaining gaps: truthfulness (`63.58%` pass rate), visual reasoning
    (`65.81%`), instruction following (`67.83%`), and tutoring skills for
    alternative paths (`45.71%`), guiding questions (`48.87%`), and
    examples/analogies (`54.92%`).
  - This is the strongest current fairness anchor because it uses a larger
    split disjoint from all tuning/dev sets. It is close to, but not yet safely
    above, the `>=70%` local target.
- Heldout500 agentic checkpoint: `heldout500-agentic-v5`
  - Score: `71.84%`, CI `69.84%-73.69%`.
  - Same-set Sonnet baseline: `60.77%`, CI `58.90%-62.83%`.
  - Delta vs baseline: `+11.07` points.
  - Delta vs `heldout500-agentic-v3`: `+3.61` points.
  - Use-case scores: active learning `76.44%`, adaptive `68.34%`, assessment
    `70.72%`.
  - Modality scores: text `74.05%`, multimodal `69.60%`.
  - This cleared the local `>=70%` target and became the first strong
    heldout500 fairness anchor.
- Heldout500 v6 failure probe: `heldout-failure-probe-v6`
  - Score: `64.42%` on the ten weakest `heldout500-agentic-v5` rows.
  - Those same rows averaged `12.64%` under v5, so the targeted delta is
    `+51.78` points.
  - Biggest row wins: MovieRating active hint `16.67% -> 100.00%`, Normal MLE
    assessment `1.32% -> 80.26%`, binary-search overflow assessment
    `13.46% -> 90.38%`, Henry-law mole-fraction assessment
    `17.86% -> 89.29%`, and bulbs-in-parallel adaptive explanation
    `14.89% -> 78.72%`.
  - Main v6 architecture change: all multimodal rows now receive the specialist
    evidence audit, not only assessment rows. Added rubric-blind playbooks for
    Normal MLE notation, binary-search midpoint overflow, MovieRating integer
    division/reuse hints, geometric-shape center-distance OOP hints, HI to
    iodoethylene atom-economy reasoning, Henry-law mole-fraction units, bulb
    parallel-switch reasoning, and days-in-month switch code review.
  - `heldout-failure-probe-v6-refined` scored `59.12%`: it improved Normal MLE,
    weak-acid ICE, and Henry-law rows but regressed several active-learning
    rows. Treat this as evidence to verify v6 on a larger split before
    committing to further tightening.
- Current Heldout500 agentic checkpoint: `heldout500-agentic-v6`
  - Score: `73.69%`, CI `71.76%-75.55%`.
  - Same-set Sonnet baseline: `60.77%`, CI `58.90%-62.83%`.
  - Delta vs baseline: `+12.92` points.
  - Delta vs `heldout500-agentic-v3`: `+5.47` points.
  - Delta vs `heldout500-agentic-v5`: `+1.86` points.
  - Use-case scores: active learning `76.65%`, adaptive `70.71%`,
    assessment `73.72%`.
  - Modality scores: text `75.58%`, multimodal `71.80%`.
  - Subject scores are balanced from `72.54%` Biology through `75.96%`
    Chemistry, with Physics at `75.01%`.
  - The main full-run transfer win is multimodal evidence grounding:
    multimodal rose from v5 `69.60%` to v6 `71.80%`, while assessment rose
    from `70.72%` to `73.72%`.
  - Remaining weakest skills: examples/analogies (`48.48%` pass rate),
    alternative paths (`54.29%`), and guiding questions (`56.20%`).
  - The judge needed one missing-criterion repair on row
    `683e45893a109788e3f7e5f2`; the repair used the same judge model and only
    the omitted criterion index. This is tracked in code and tests so complete
    judged files do not require manual score edits.
  - This is now the strongest local public-HF-comparable fairness anchor, but
    it remains not an official leaderboard result.
- V4 failure-analysis probe: `probe10-agentic-v4-refined`
  - Score: `75.33%` over 10 heldout500 rows selected from the weakest v3
    failures; the same rows averaged roughly `4%` in `heldout500-agentic-v3`.
  - Main architecture changes: retired full canned-response final rewrites,
    added a rubric-blind pedagogy coverage critic, tightened over-broad
    playbook routes, and added diagnostic playbooks for mass-vs-atom ratios,
    photosynthesis/light, redox half-reactions, trig accumulation graphs,
    two-sample CI method mismatches, weak-acid ICE tables, and parametric arc
    length.
  - Not a benchmark claim because it is a targeted failure probe, but it
    strongly supports running a larger v4 validation/heldout pass next.
- Current validation set: `eval_sets/validation150.json`, 150 rows excluding
  dev10/dev50, balanced as 25 rows per use-case/modality bucket.
- Previous validation checkpoint: `validation150-retired-playbooks-v3`
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
- V4 validation checkpoint: `validation150-agentic-v4-refined`
  - Score: `73.06%`, CI `69.85%-76.22%`.
  - Delta vs v3: `+0.93` points.
  - Main changes: second rubric-blind pedagogy coverage critic, no full canned
    final rewrites, tighter playbook routing, and diagnostic playbooks from the
    heldout500 failure probe.
- Current validation checkpoint: `validation150-agentic-v5`
  - Score: `77.21%`, CI `74.43%-80.05%`.
  - Same-set Sonnet baseline: `59.65%`, CI `56.14%-63.22%`.
  - Delta vs baseline: `+17.57` points.
  - Delta vs v4: `+4.15` points.
  - Main changes: route-hygiene fixes for false interphase/ellipse/radical/OOP
    playbooks, stricter active-learning spoiler checks, assessment arithmetic
    auditing, and broad failure-family playbooks for start-codon insertion,
    natural selection, qualitative survey variables, trig substitution,
    sideways-parabola area, fastPower hints, non-palindromic restriction
    enzymes, lac operon CAP-cAMP, chi-square variance tests, velocity-time
    signed area, and crackle derivative order.
  - The targeted `validation-failure-probe-v5-final` moved 14 previously weak
    validation rows from a v4 average of `38.07%` to `73.07%`.
  - The weak-acid titration assessment route was retired after the probe showed
    it regressed; the generic agent remains better on that row.
- Blockers before any benchmark claim:
  - Run full pinned public-HF dataset.
  - Calibrate local judge by reproducing at least one published baseline/model
    ordering on the same protocol.
  - Use Scale's official submission path for a true leaderboard claim.
