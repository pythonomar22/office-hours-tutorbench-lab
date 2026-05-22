# TutorBench Run Analysis: `b0a72ccc-6f9f-4625-9ca7-a1f7f37d34cc`

- Rows: 50
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 85.28%
- Mean generation latency: 83379 ms
- Mean judge latency: 3767 ms
- Generation input/output tokens: 1113881 / 205018
- Judge input/output tokens: 112637 / 11936
- Negative-weight manual review rows: 4

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1994000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 398000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19997 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2394000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `683e3d90e1480f05f1927713` | 2.50% | adaptive / multimodal / Statistics | 11 | 0 | two-proportion z-test active-learning hint |
| `681cfc8c5db7f3af72e1579d` | 54.17% | assessment / text / Physics | 2 | 1 | none |
| `683e45162f54c21988695290` | 54.55% | assessment / multimodal / Physics | 3 | 0 | none |
| `684a8c403b901ee3995f38f5` | 64.29% | adaptive / text / Calculus | 2 | 0 | radical derivative adaptive explanation |
| `683e3d8db4f61c885835aa80` | 65.62% | adaptive / multimodal / Computer Science | 3 | 0 | none |
| `683e4514f37c3bccc4ec7df3` | 68.75% | assessment / multimodal / Calculus | 2 | 0 | none |
| `684a8c41f2ed21c3af4f5e68` | 70.00% | adaptive / text / Calculus | 2 | 0 | radical derivative adaptive explanation |
| `6811d40e3babd4e8219eb4ff` | 73.21% | adaptive / multimodal / Calculus | 3 | 0 | none |
| `684771b2c4915de7a58b3cdd` | 77.27% | assessment / text / Calculus | 1 | 0 | sinc integral/removable discontinuity assessment |
| `683870ef925f37fe4fe4398c` | 77.27% | active_learning / text / Chemistry | 1 | 0 | none |
| `683e458b98da731381469295` | 78.26% | active_learning / multimodal / Calculus | 1 | 0 | arc-length perimeter active-learning hint |
| `684772090f13de1c3fc22137` | 79.17% | active_learning / text / Statistics | 2 | 0 | coffee-shop conditional-probability active hint |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| emotional_component | 78.29% | 33.0 | 9 | 0 |
| style_tone | 81.67% | 33.0 | 8 | 0 |
| visual_reasoning | 84.16% | 32.0 | 6 | 0 |
| conciseness_relevance | 84.21% | 3.0 | 3 | 0 |
| instruction_following | 84.52% | 154.0 | 25 | 2 |
| student_level_calibration | 85.36% | 113.0 | 18 | 0 |
| truthfulness | 86.86% | 36.0 | 9 | 0 |
| visual_perception | 98.33% | 2.0 | 2 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Provides alternative solutions/ paths/ | 58.62% | 12.0 | 4 | 0 |
| Includes examples/ analogy | 62.79% | 16.0 | 4 | 0 |
| Identifying incorrect steps by student | 77.34% | 46.0 | 6 | 0 |
| Not applicable | 82.72% | 80.0 | 23 | 1 |
| Stating definitions/ formulae/ theorems/ laws | 84.58% | 39.0 | 9 | 0 |
| Identifying correct steps by student | 89.69% | 27.0 | 6 | 0 |
| Identifying Core difficulty/ misconception attribution | 89.96% | 28.0 | 6 | 0 |
| Step by step help/ analysis | 92.11% | 12.0 | 5 | 1 |
| Asks questions to guide students | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 15 | 78.76% |
| interphase mutation active-learning hint | 2 | 98.48% |
| radical derivative adaptive explanation | 2 | 67.14% |
| recursive factorial assessment | 2 | 93.06% |
| two-proportion z-test active-learning hint | 2 | 41.88% |
| Arctic fox coat-color active-learning hint | 1 | 100.00% |
| CLT sample-mean active-learning hint | 1 | 100.00% |
| Gene X methylation/tumor-suppressor active hint | 1 | 100.00% |
| H2/O2 water limiting-reagent visual assessment | 1 | 100.00% |
| Le Chatelier SO2/SO3 assessment | 1 | 79.22% |
| Mendelian independent-assortment testcross | 1 | 97.96% |
| OOP design / inventory class | 1 | 100.00% |
| aerobic respiration assessment | 1 | 82.35% |
| alkylbenzene sulphonation hyperconjugation explanation | 1 | 90.38% |
| arc-length perimeter active-learning hint | 1 | 78.26% |
| binary-tree traversal reconstruction assessment | 1 | 95.65% |
| coffee-shop conditional-probability active hint | 1 | 79.17% |
| conical-pendulum adaptive explanation | 1 | 100.00% |
| dextrose solubility/molarity assessment-hint | 1 | 96.55% |
| equilateral-triangle wire magnetic-field adaptive explanation | 1 | 79.17% |
