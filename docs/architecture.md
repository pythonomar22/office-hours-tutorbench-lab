# Architecture

## Core Flow

1. `fetch` downloads and validates the pinned TutorBench dataset.
2. `run` converts each row into a use-case-specific tutor turn and generates a candidate response.
3. `judge` grades each candidate response against sample-specific rubrics.
4. `score` computes weighted ARRw and slice reports by use case, modality, subject, and Bloom taxonomy.
5. `report` and `compare` produce Markdown artifacts for iteration.

## Use-Case Protocol

- UC1 adaptive explanation: input is the original prompt, optional image, the
  provided initial explanation, and the student's follow-up question.
- UC2 assessment and feedback: input is the original prompt plus student
  solution/work from text or image.
- UC3 active learning: input is the problem plus partial student work; output
  should be a hint or guiding question and must avoid giving the full answer.

## Agentic Tutor V6

The agentic strategy is rubric-blind:

- Perception: for image rows, transcribes visible problem text, diagrams,
  labels, code, student work, and ambiguity before any solving.
- Specialist evidence audit: for all multimodal rows, performs a routed visual
  audit before solving. Numbered diagrams are audited by marker endpoint as
  drawn; code images are audited for exact lines, compile/runtime issues,
  corrected-code expectations, tests, and edge cases. Adaptive rows use the
  audit to answer the follow-up without pivoting away from the conversation;
  active-learning rows use it to identify the stuck point and the final target
  that must remain withheld.
- Solver/diagnoser: privately solves the task, identifies misconceptions, and
  recomputes arithmetic/code/diagram facts using the specialist audit when
  present.
- Planner/contract: writes a rubric-blind, use-case-aware answer contract with
  anchors, disclosure boundaries, required concepts/formulas/examples, and
  avoid-list. UC2 assessment is allowed and expected to show corrected final
  results/code/tables; UC3 active learning withholds only the final requested
  target while allowing useful intermediate checkpoints.
- Domain verifier: independently checks math, code, diagram labels, units,
  signs, and active-learning disclosure before composition.
- Composer: writes the student-facing response using the diagnosis, contract,
  and verifier notes.
- Critic: checks the draft against the contract, verifier notes, truthfulness,
  calibration, acknowledgement, structure, and spoiler risk.
- Pedagogy coverage critic: separately checks TutorBench-style tutoring
  coverage, including exact misconception identification, correct-work
  acknowledgement, examples/analogies, definitions/formulas, guiding questions,
  multimodal anchoring, and wrong-family playbook leakage.
- Revision loop: runs up to `TUTORBENCH_MAX_REVISION_ATTEMPTS` if the critic
  returns `REVISE`, and uses the full composer policy during revisions.
- Task-family playbooks: deterministic, rubric-blind guidance for recurring
  TutorBench tutoring patterns such as hydrogen-halide acidity, ellipse area
  optimization, recursive factorial feedback, CLT sample-mean hints,
  Bonferroni corrections, chemistry equilibrium reasoning, ionization-energy
  feedback, plant/animal cell diagrams, Normal MLE feedback, binary-search
  overflow, MovieRating integer division hints, shape center-distance OOP hints,
  Henry-law mole-fraction units, and bulbs-in-parallel switch reasoning.
  Playbook routing is intentionally conservative: validation150 showed that
  several specific deterministic rewrites underperformed the generic agent, so
  coffee/under-filling, two-proportion, regression-residual, two's-complement,
  and weak-acid titration-assessment routes are retired.
- Deterministic final guards: narrow post-composition repairs for brittle
  task-family anchors that the LLM critic may miss, such as exact visual
  anchors, exact factorial verification, and crackle derivative-order audits.

No candidate step receives sample-specific TutorBench rubrics. Rubrics are used
only in the judge.

The trace for each agentic response stores these stages as
`route_plan`, `stage_latency_ms`, `stage_usage`, `stage_rate_limits`,
`perception_transcript`, `specialist_audit`, `solver_analysis`, `answer_contract`,
`domain_verification`, `draft`, `critic_attempts`, and
`revision_attempts`.

## Throughput

The CLI supports concurrent `run` and `judge` execution via `--workers`, plus
`--run-id` and `--resume` for interrupted runs. Parallel failures are logged to
run-local error JSONL files so completed rows are preserved and only missing
task IDs need to be resumed. Anthropic calls capture non-secret rate-limit
headers so high-parallel runs can be audited after the fact. A cheap Sonnet
probe on the current key reported bucket limits of
`20,000` requests, `2,000,000` input tokens, and `400,000` output tokens. Full
`office_hours_dev50` agentic and judge runs at `--workers 24` completed without
throttling, with minimum observed remaining headers still near the top of the
bucket. Use `--workers 24` for dev-set iteration on this account; move higher
only after checking trace `stage_rate_limits`.

## Evaluation Parity

Run `tutorbench-lab audit-parity` before treating a score as comparable to the
public leaderboard. The current pinned public Hugging Face release is
public-HF-comparable but not leaderboard-exact because the local manifest has
`1473` rows and `15043` rubrics, while Scale's overview describes `1490` rows
and `15220` rubrics. See `docs/eval_parity.md`.

## Current Iteration Notes

The 10-row Office Hours dev set exposed a useful architectural lesson:
generic verification improved text/adaptive and statistics hinting, but
multimodal assessment needs specialized audits. The biology cell-label sample
failed because the model tried to preserve the student's labels by suggesting
arrow moves, while the benchmark expects correction of the current marker-label
mapping. The new specialist audit makes marker endpoints authoritative and
feeds that into solving, planning, verification, composition, and criticism.
Adding the local visual probe raised the curated dev10 score to `81.18%`, up
from the prior best `77.57%` and the previous planner/verifier architecture
`76.27%`.
We also tested a generic UC3 active-learning gate. It improved the statistics
row but regressed the active-learning subset overall (`78.07%` to `64.98%` on
the four-row slice), mostly by damaging the calculus hint. That gate is not in
the default route; the lesson is that hint verification likely needs
subject/task-specific gates rather than one broad UC3 gate.

The dev10 loop later reached `99.60%`, but that is an intentionally overfit
debug set. The current comparison ladder is:

1. `office_hours_dev10` for quick trace debugging.
2. `office_hours_dev50` for architecture iteration, excluding dev10 rows.
3. `validation150` for sparse inspection.
4. Full public-HF run after architecture freeze.
5. Official Scale submission for leaderboard claims.

The first dev50 sanity slice showed baseline Sonnet at `69.63%` and the agentic
tutor at `72.14%` across three rows. It also exposed a statistics active-learning
regression on a CLT sample-mean hint; adding a CLT playbook moved that row from
`44.4%` to `100%` locally.

The current clean `office_hours_dev50` checkpoint is baseline Sonnet `59.68%`
versus agentic `85.28%` over 50 rows, a +25.60 point gain. That run includes
the forensic `analyze-run` report, late playbook routing after multimodal
specialist audit, and task-family playbooks/templates for pKa titration,
Arctic fox coat-color, Gene X methylation, cellular respiration, conical
pendulum, binary-tree reconstruction, Bayes/conditional probability, matrix
search, sulphonation hyperconjugation, charged-ring potential, and z-test vs
t-test feedback. It remains a local public-HF dev-set score, not a leaderboard
claim.

The current clean `validation150` checkpoint is baseline Sonnet `59.65%` versus
agentic-v5 `77.21%` over 150 rows, a +17.57 point same-set gain and +4.15
points over v4. The main v5 architectural lesson was route hygiene plus
enforcement: wrong-family playbooks can poison otherwise good reasoning, and
playbook requirements need critic/guard enforcement when the model is tempted
to fall back to a plausible but benchmark-wrong school-level interpretation.
This is still a local public-HF-comparable result, not an official leaderboard
claim.

The current larger holdout checkpoint is baseline Sonnet `60.77%` versus
agentic-v5 `71.84%` over 500 rows, a +11.07 point same-set gain on a split
disjoint from dev10/dev50/validation150. The strongest remaining failure pattern
is not generic pedagogy but multimodal evidence grounding: the tutor often gives
a polished response to a wrong read of the image. Agentic-v6 therefore broadens
the specialist evidence audit to all multimodal rows and adds targeted,
rubric-blind failure-family playbooks. On the ten weakest v5 heldout rows,
`heldout-failure-probe-v6` moved the average from `12.64%` to `64.42%`; the
follow-up refined probe scored `59.12%`, showing that stricter playbook wording
helps some assessment rows but can still regress active-learning rows.

## Office Hours Transfer Path

Once the lab tutor is strong, move it behind a backend tutor abstraction in the
Office Hours API. The current app has clear seams at `HintService` and
`VoiceService`, which call `ClaudeClient` directly. The first integration should
add a feature flag such as `TUTOR_ENGINE=claude|agentic` and adapt the lab
`TutorResponse` into the existing hint/voice response contracts before changing
Swift UI behavior.
