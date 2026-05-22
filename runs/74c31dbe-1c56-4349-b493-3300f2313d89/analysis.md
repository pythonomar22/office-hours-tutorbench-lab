# TutorBench Run Analysis: `74c31dbe-1c56-4349-b493-3300f2313d89`

- Rows: 50
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 82.32%
- Mean generation latency: 83926 ms
- Mean judge latency: 4085 ms
- Generation input/output tokens: 1081394 / 203738
- Judge input/output tokens: 116823 / 11956
- Negative-weight manual review rows: 4

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1993000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19997 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2393000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `6842a1fb5ca82eb2207af64b` | 28.57% | adaptive / text / Biology | 6 | 0 | aerobic respiration assessment |
| `683e3d8d2b6d2a6c45002caa` | 32.69% | adaptive / multimodal / Chemistry | 7 | 0 | none |
| `683e4516f37c3bccc4ec7e12` | 53.12% | assessment / multimodal / Computer Science | 3 | 0 | OOP design / inventory class |
| `6843160b61e29735d3565670` | 53.12% | active_learning / text / Statistics | 3 | 0 | two-proportion z-test active-learning hint |
| `681cfc8c5db7f3af72e1579d` | 54.17% | assessment / text / Physics | 2 | 1 | none |
| `6843160a1c3b85b09bea6fd9` | 54.55% | active_learning / text / Statistics | 2 | 0 | none |
| `683e45162f54c21988695290` | 54.55% | assessment / multimodal / Physics | 3 | 0 | none |
| `684772090f13de1c3fc22137` | 58.33% | active_learning / text / Statistics | 4 | 0 | none |
| `683e458c3a109788e3f7e64f` | 58.33% | active_learning / multimodal / Physics | 2 | 0 | none |
| `683e45143a109788e3f7e591` | 58.33% | assessment / multimodal / Statistics | 3 | 0 | two-proportion z-test active-learning hint |
| `683e45141eb8a249fd792b93` | 58.82% | assessment / multimodal / Biology | 7 | 0 | none |
| `684a8c41f2ed21c3af4f5e68` | 65.00% | adaptive / text / Calculus | 3 | 0 | radical derivative adaptive explanation |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| emotional_component | 65.79% | 52.0 | 12 | 0 |
| truthfulness | 75.18% | 68.0 | 8 | 0 |
| style_tone | 76.67% | 42.0 | 10 | 0 |
| visual_reasoning | 82.67% | 35.0 | 5 | 0 |
| instruction_following | 83.62% | 163.0 | 27 | 2 |
| student_level_calibration | 84.97% | 116.0 | 17 | 0 |
| conciseness_relevance | 89.47% | 2.0 | 2 | 0 |
| visual_perception | 91.67% | 10.0 | 2 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 62.79% | 16.0 | 4 | 0 |
| Not applicable | 71.27% | 133.0 | 23 | 1 |
| Provides alternative solutions/ paths/ | 75.86% | 7.0 | 3 | 0 |
| Identifying incorrect steps by student | 77.83% | 45.0 | 6 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 81.42% | 47.0 | 6 | 0 |
| Asks questions to guide students | 85.85% | 15.0 | 2 | 0 |
| Step by step help/ analysis | 89.47% | 16.0 | 5 | 1 |
| Identifying Core difficulty/ misconception attribution | 91.04% | 25.0 | 3 | 0 |
| Identifying correct steps by student | 93.89% | 16.0 | 4 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 20 | 75.98% |
| two-proportion z-test active-learning hint | 3 | 70.49% |
| OOP design / inventory class | 2 | 76.56% |
| interphase mutation active-learning hint | 2 | 82.86% |
| radical derivative adaptive explanation | 2 | 82.50% |
| recursive factorial assessment | 2 | 96.53% |
| Arctic fox coat-color active-learning hint | 1 | 100.00% |
| CLT sample-mean active-learning hint | 1 | 100.00% |
| Gene X methylation/tumor-suppressor active hint | 1 | 100.00% |
| H2/O2 water limiting-reagent visual assessment | 1 | 100.00% |
| Le Chatelier SO2/SO3 assessment | 1 | 79.22% |
| Mendelian independent-assortment testcross | 1 | 93.88% |
| aerobic respiration assessment | 1 | 28.57% |
| arc-length perimeter active-learning hint | 1 | 78.26% |
| binary-tree traversal reconstruction assessment | 1 | 100.00% |
| conical-pendulum adaptive explanation | 1 | 100.00% |
| dextrose solubility/molarity assessment-hint | 1 | 96.55% |
| equilateral-triangle wire magnetic-field adaptive explanation | 1 | 79.17% |
| extremophile multi-part metabolism hint | 1 | 100.00% |
| heat-exchange active-learning hint | 1 | 100.00% |
