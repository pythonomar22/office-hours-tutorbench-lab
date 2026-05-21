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

## Agentic Tutor V1

The agentic strategy is rubric-blind:

- Perception: for image rows, transcribes visible problem text, diagrams,
  labels, code, student work, and ambiguity before any solving.
- Specialist audit: for multimodal assessment rows, performs a routed visual
  audit before solving. Numbered diagrams are audited by marker endpoint as
  drawn; code images are audited for exact lines, compile/runtime issues,
  corrected-code expectations, tests, and edge cases.
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
- Revision loop: runs up to `TUTORBENCH_MAX_REVISION_ATTEMPTS` if the critic
  returns `REVISE`, and uses the full composer policy during revisions.

No candidate step receives sample-specific TutorBench rubrics. Rubrics are used
only in the judge.

The trace for each agentic response stores these stages as
`route_plan`, `stage_latency_ms`, `stage_usage`, `perception_transcript`,
`specialist_audit`, `solver_analysis`, `answer_contract`,
`domain_verification`, `draft`, `critic_attempts`, and
`revision_attempts`.

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

## Office Hours Transfer Path

Once the lab tutor is strong, move it behind a backend tutor abstraction in the
Office Hours API. The current app has clear seams at `HintService` and
`VoiceService`, which call `ClaudeClient` directly. The first integration should
add a feature flag such as `TUTOR_ENGINE=claude|agentic` and adapt the lab
`TutorResponse` into the existing hint/voice response contracts before changing
Swift UI behavior.
