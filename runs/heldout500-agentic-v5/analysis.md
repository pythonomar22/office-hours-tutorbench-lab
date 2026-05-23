# TutorBench Run Analysis: `heldout500-agentic-v5`

- Rows: 500
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 71.84%
- Mean generation latency: 101928 ms
- Mean judge latency: 3917 ms
- Generation input/output tokens: 15382892 / 2455481
- Judge input/output tokens: 1347986 / 127638
- Negative-weight manual review rows: 47

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1989000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 398000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19998 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2389000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `683e4517a08f8bb261597839` | 1.32% | assessment / multimodal / Statistics | 15 | 0 | none |
| `6843120a2b986bd2d9ca5f3f` | 6.25% | assessment / text / Chemistry | 6 | 0 | weak-acid ICE-table assessment |
| `6843120a9fab58968f2128c9` | 9.09% | assessment / text / Chemistry | 1 | 1 | none |
| `68376d91c5b329d497cbe8ca` | 12.20% | adaptive / multimodal / Computer Science | 7 | 1 | none |
| `683e4516d3bdf2dc57e053e3` | 13.46% | assessment / multimodal / Computer Science | 9 | 0 | none |
| `683e458c2e254199a0fa2e02` | 14.63% | active_learning / multimodal / Computer Science | 6 | 1 | none |
| `683e3d8f3482feddb4d05e86` | 14.89% | adaptive / multimodal / Physics | 8 | 0 | none |
| `683e458eac89e71e0ce600c6` | 16.67% | active_learning / multimodal / Computer Science | 6 | 0 | none |
| `683e45162d501a5ab198c520` | 17.86% | assessment / multimodal / Chemistry | 10 | 0 | none |
| `684a8cd6f08ce27c3bf577e0` | 20.00% | assessment / text / Chemistry | 8 | 0 | none |
| `6811d40e6b7f984ce18baebb` | 20.69% | adaptive / multimodal / Computer Science | 7 | 0 | none |
| `6842a1fbeec1338496adc799` | 20.75% | adaptive / text / Computer Science | 10 | 0 | none |
| `684a8c40562837a83a9ac6b2` | 22.22% | adaptive / text / Physics | 5 | 0 | none |
| `6847710ac4590722c4324810` | 23.08% | adaptive / text / Physics | 4 | 0 | none |
| `68545548714d62d3ac325d31` | 25.53% | assessment / text / Biology | 7 | 0 | none |
| `681b84ff94969ef6e11908e0` | 25.81% | assessment / multimodal / Physics | 10 | 0 | none |
| `68096a17d9108896c270f6b6` | 25.93% | adaptive / text / Physics | 4 | 0 | none |
| `683e45109394b13fefb08e44` | 26.09% | assessment / multimodal / Physics | 5 | 0 | none |
| `683775dc0a6dba7869a5c576` | 26.83% | adaptive / multimodal / Chemistry | 6 | 0 | none |
| `683775dc2f4468651311d6ad` | 26.83% | adaptive / multimodal / Chemistry | 6 | 0 | none |
| `68377588415e67c44f4734b6` | 27.27% | assessment / text / Physics | 4 | 0 | none |
| `68377627496507faa0915cd6` | 28.26% | assessment / multimodal / Biology | 14 | 0 | none |
| `6836292325d9d55d0df0462c` | 28.57% | assessment / text / Calculus | 4 | 0 | none |
| `683e458d3a109788e3f7e66e` | 28.57% | active_learning / multimodal / Physics | 6 | 0 | kinematics active-learning hint |
| `683e451765e18627c73884df` | 28.57% | assessment / multimodal / Physics | 3 | 0 | none |
| `6847710b9bc321f32d5b5ab8` | 28.95% | adaptive / text / Calculus | 7 | 0 | none |
| `684771b3cf8ba842e93ec6de` | 29.73% | assessment / text / Computer Science | 6 | 0 | none |
| `683e458c5f104dac1d4d6e7a` | 30.19% | active_learning / multimodal / Biology | 9 | 0 | none |
| `681cfb9f423b8a534abc79ba` | 30.23% | adaptive / text / Biology | 6 | 0 | none |
| `683870ef328fdda5d51a6203` | 30.23% | active_learning / text / Statistics | 6 | 0 | none |
| `683776272f4468651311d6dc` | 30.56% | assessment / multimodal / Calculus | 4 | 1 | none |
| `68545549f8ab7067dd48b799` | 31.82% | assessment / text / Physics | 1 | 2 | none |
| `683e4514225c80e89ef01988` | 32.43% | assessment / multimodal / Physics | 4 | 1 | none |
| `683e4510bd7caf8a464501d6` | 32.43% | assessment / multimodal / Physics | 5 | 0 | none |
| `683e451098da731381469199` | 32.69% | assessment / multimodal / Physics | 7 | 0 | none |
| `683e45112667944fdee505b4` | 32.79% | assessment / multimodal / Physics | 9 | 0 | none |
| `6847720874c7f1cb6eb0b1d5` | 32.84% | active_learning / text / Computer Science | 9 | 0 | none |
| `683e3d9065e18627c7388002` | 34.21% | adaptive / multimodal / Chemistry | 5 | 0 | none |
| `683e3d8c5f104dac1d4d666a` | 34.43% | adaptive / multimodal / Chemistry | 12 | 0 | none |
| `68387052b790747a1c2a372e` | 35.29% | active_learning / multimodal / Statistics | 6 | 0 | none |
| `68377627ca52a73e1545735e` | 35.48% | assessment / multimodal / Computer Science | 4 | 0 | recursive factorial assessment |
| `681cfba0516d8f36be368b74` | 36.36% | adaptive / text / Chemistry | 5 | 0 | none |
| `680979013d9d7eb8a361d50a` | 36.99% | assessment / text / Chemistry | 10 | 0 | none |
| `683e3d8f38791d6d309f6cd1` | 37.84% | adaptive / multimodal / Statistics | 7 | 0 | none |
| `681cfb9f998b35aadeba36e0` | 38.10% | adaptive / text / Statistics | 5 | 0 | none |
| `681b80dd850f62964ac697d2` | 38.24% | adaptive / multimodal / Statistics | 5 | 0 | none |
| `683e3d902b6d2a6c45002cec` | 38.46% | adaptive / multimodal / Calculus | 4 | 0 | none |
| `683e45108103655aef73fc0f` | 38.60% | assessment / multimodal / Statistics | 7 | 0 | none |
| `6847710ae96863adfe49248d` | 39.47% | adaptive / text / Computer Science | 7 | 0 | none |
| `681a876b69aba25329fa1450` | 40.74% | assessment / text / Statistics | 4 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| not applicable | 50.00% | 1.0 | 1 | 0 |
| truthfulness | 66.52% | 1186.0 | 147 | 2 |
| visual_reasoning | 66.65% | 594.0 | 76 | 0 |
| conciseness_relevance | 67.00% | 66.0 | 28 | 0 |
| instruction_following | 71.79% | 3170.0 | 330 | 25 |
| student_level_calibration | 73.87% | 2174.0 | 244 | 7 |
| visual_perception | 77.56% | 294.0 | 55 | 2 |
| emotional_component | 80.94% | 284.0 | 77 | 1 |
| style_tone | 81.99% | 322.0 | 103 | 2 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 52.65% | 125.0 | 43 | 0 |
| Asks questions to guide students | 55.99% | 408.0 | 69 | 0 |
| Provides alternative solutions/ paths/ | 57.14% | 135.0 | 34 | 3 |
| Stating definitions/ formulae/ theorems/ laws | 68.02% | 1056.0 | 152 | 0 |
| Step by step help/ analysis | 69.77% | 503.0 | 84 | 5 |
| Identifying incorrect steps by student | 70.71% | 754.0 | 102 | 6 |
| Not applicable | 72.13% | 1375.0 | 256 | 15 |
| Identifying Core difficulty/ misconception attribution | 74.16% | 766.0 | 130 | 0 |
| Identifying correct steps by student | 82.21% | 521.0 | 86 | 2 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 464 | 71.67% |
| chi-square variance-test adaptive explanation | 7 | 82.82% |
| recursive factorial assessment | 7 | 71.19% |
| sinc integral/removable discontinuity assessment | 3 | 80.04% |
| electricity-rates two-sample CI adaptive explanation | 2 | 89.93% |
| CLT sample-mean active-learning hint | 1 | 75.00% |
| Gene X methylation/tumor-suppressor active hint | 1 | 78.72% |
| OOP design / inventory class | 1 | 76.19% |
| U-238/Pb-206 mass-ratio adaptive explanation | 1 | 100.00% |
| copper/KMnO4 redox active-learning hint | 1 | 54.39% |
| hydrogen halide acid strength | 1 | 55.26% |
| kinematics active-learning hint | 1 | 28.57% |
| natural-selection misconception assessment | 1 | 68.75% |
| oxygen/CO2 cellular-respiration adaptive explanation | 1 | 84.38% |
| parametric arc-length active-learning hint | 1 | 76.19% |
| penicillin allergy Bayes active-learning hint | 1 | 82.76% |
| second ionization energy assessment | 1 | 78.57% |
| sideways-parabola enclosed-area assessment | 1 | 85.92% |
| start-codon insertion mutation assessment | 1 | 66.67% |
| trig accumulation probability assessment | 1 | 66.67% |
