# TutorBench Run Analysis: `2ddb82f0-4947-46e6-be98-f8fa4901eacd`

- Rows: 50
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 74.72%
- Mean generation latency: 81472 ms
- Mean judge latency: 3637 ms
- Generation input/output tokens: 1075005 / 201547
- Judge input/output tokens: 118085 / 11946
- Negative-weight manual review rows: 4

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1994000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19998 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2393000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `681cfd7b3c96c09201619a49` | 0.00% | adaptive / multimodal / Chemistry | 12 | 0 | dextrose solubility/molarity assessment-hint |
| `683e45892667944fdee50634` | 18.18% | active_learning / multimodal / Biology | 8 | 0 | none |
| `681cfb9f785e9bceace0e139` | 28.00% | adaptive / text / Physics | 6 | 0 | kinematics active-learning hint |
| `683e45141eb8a249fd792b93` | 29.41% | assessment / multimodal / Biology | 12 | 0 | none |
| `6843160a493da3d4b37fee61` | 44.44% | active_learning / text / Biology | 3 | 0 | none |
| `684a8c41f2ed21c3af4f5e68` | 45.00% | adaptive / text / Calculus | 3 | 0 | radical derivative adaptive explanation |
| `6842a1fbbdfc0b0552b0553e` | 50.00% | adaptive / text / Physics | 4 | 0 | none |
| `683e3d8d2b6d2a6c45002caa` | 51.92% | adaptive / multimodal / Chemistry | 5 | 0 | none |
| `683776289fb2fd83d696cc90` | 52.17% | assessment / multimodal / Computer Science | 3 | 0 | none |
| `6843160b61e29735d3565670` | 53.12% | active_learning / text / Statistics | 3 | 0 | two-proportion z-test active-learning hint |
| `683e45162f54c21988695290` | 54.55% | assessment / multimodal / Physics | 3 | 0 | none |
| `681cfc8c5db7f3af72e1579d` | 58.33% | assessment / text / Physics | 1 | 1 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| visual_reasoning | 64.85% | 71.0 | 8 | 0 |
| conciseness_relevance | 68.42% | 6.0 | 2 | 0 |
| emotional_component | 69.08% | 47.0 | 10 | 0 |
| truthfulness | 69.34% | 84.0 | 11 | 0 |
| instruction_following | 73.27% | 266.0 | 31 | 2 |
| student_level_calibration | 75.65% | 188.0 | 19 | 0 |
| style_tone | 78.89% | 38.0 | 9 | 0 |
| visual_perception | 91.67% | 10.0 | 2 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Provides alternative solutions/ paths/ | 44.83% | 16.0 | 4 | 0 |
| Asks questions to guide students | 57.55% | 45.0 | 5 | 0 |
| Includes examples/ analogy | 62.79% | 16.0 | 4 | 0 |
| Not applicable | 66.52% | 155.0 | 28 | 1 |
| Stating definitions/ formulae/ theorems/ laws | 67.19% | 83.0 | 10 | 0 |
| Identifying incorrect steps by student | 70.44% | 60.0 | 7 | 0 |
| Identifying Core difficulty/ misconception attribution | 81.72% | 51.0 | 6 | 0 |
| Identifying correct steps by student | 87.40% | 33.0 | 7 | 0 |
| Step by step help/ analysis | 89.47% | 16.0 | 5 | 1 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 25 | 66.29% |
| two-proportion z-test active-learning hint | 3 | 84.38% |
| dextrose solubility/molarity assessment-hint | 2 | 48.28% |
| interphase mutation active-learning hint | 2 | 90.67% |
| kinematics active-learning hint | 2 | 64.00% |
| radical derivative adaptive explanation | 2 | 72.50% |
| recursive factorial assessment | 2 | 93.06% |
| CLT sample-mean active-learning hint | 1 | 100.00% |
| H2/O2 water limiting-reagent visual assessment | 1 | 100.00% |
| Le Chatelier SO2/SO3 assessment | 1 | 66.23% |
| Mendelian independent-assortment testcross | 1 | 73.47% |
| OOP design / inventory class | 1 | 100.00% |
| arc-length perimeter active-learning hint | 1 | 78.26% |
| extremophile multi-part metabolism hint | 1 | 100.00% |
| heat-exchange active-learning hint | 1 | 100.00% |
| regression residual assessment | 1 | 97.30% |
| second ionization energy assessment | 1 | 100.00% |
| sinc integral/removable discontinuity assessment | 1 | 77.27% |
| two's-complement negative-number active hint | 1 | 95.83% |
