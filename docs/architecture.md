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

- Solver/diagnoser: privately solves the problem and identifies misconceptions.
- Composer: writes the student-facing response for the use case.
- Critic: checks truthfulness, calibration, acknowledgement, structure, and spoiler risk.
- Revision pass: only runs if the critic returns `REVISE`.

No candidate step receives sample-specific TutorBench rubrics. Rubrics are used
only in the judge.

## Office Hours Transfer Path

Once the lab tutor is strong, move it behind a backend tutor abstraction in the
Office Hours API. The current app has clear seams at `HintService` and
`VoiceService`, which call `ClaudeClient` directly. The first integration should
add a feature flag such as `TUTOR_ENGINE=claude|agentic` and adapt the lab
`TutorResponse` into the existing hint/voice response contracts before changing
Swift UI behavior.
