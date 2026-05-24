# TutorBench Run Analysis: `heldout500-selector-v11`

- Rows: 500
- Strategy: `agentic`
- Candidate model: `selector:anthropic:claude-sonnet-4-6|anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 73.14%
- Mean generation latency: 106435 ms
- Mean judge latency: 3754 ms
- Generation input/output tokens: 17966547 / 2625088
- Judge input/output tokens: 1357356 / 127473
- Negative-weight manual review rows: 47

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1987000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 398000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19998 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2387000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `68377588415e67c44f4734b6` | 4.55% | assessment / text / Physics | 4 | 1 | inclined box slip-or-tip assessment |
| `6843160a0015fc211142fa11` | 13.46% | active_learning / text / Computer Science | 9 | 0 | none |
| `683e3d902b6d2a6c45002cec` | 15.38% | adaptive / multimodal / Calculus | 6 | 0 | none |
| `684771b3cf8ba842e93ec6de` | 16.22% | assessment / text / Computer Science | 7 | 0 | none |
| `683776272f4468651311d6dc` | 16.67% | assessment / multimodal / Calculus | 5 | 1 | none |
| `681cfb9f423b8a534abc79ba` | 18.60% | adaptive / text / Biology | 7 | 0 | meiosis-vs-mitosis gamete explanation |
| `683e4510bd7caf8a464501d6` | 18.92% | assessment / multimodal / Physics | 6 | 0 | none |
| `6842a1fbb8f271121fd79472` | 20.00% | adaptive / text / Statistics | 4 | 0 | none |
| `6811d40e6b7f984ce18baebb` | 20.69% | adaptive / multimodal / Computer Science | 7 | 0 | none |
| `681a876b69aba25329fa1450` | 22.22% | assessment / text / Statistics | 5 | 0 | none |
| `684a8c40562837a83a9ac6b2` | 22.22% | adaptive / text / Physics | 5 | 0 | none |
| `6847710ac4590722c4324810` | 23.08% | adaptive / text / Physics | 4 | 0 | none |
| `68477209c4915de7a58b3d02` | 24.53% | active_learning / text / Computer Science | 8 | 0 | none |
| `68097912014bb68a4c65e4a1` | 24.59% | assessment / text / Biology | 10 | 0 | none |
| `68377545cbb6263fa01c0268` | 25.00% | adaptive / text / Calculus | 3 | 0 | none |
| `6837754519214e0eed328c96` | 25.00% | adaptive / text / Computer Science | 4 | 0 | none |
| `68376de1c596c43935ed5a4d` | 25.53% | assessment / multimodal / Chemistry | 6 | 1 | none |
| `68096a17d9108896c270f6b6` | 25.93% | adaptive / text / Physics | 4 | 0 | none |
| `684a8cd6a8da4aded13ef58d` | 25.93% | assessment / text / Calculus | 3 | 1 | none |
| `683e45109394b13fefb08e44` | 26.09% | assessment / multimodal / Physics | 5 | 0 | none |
| `68376d91c5b329d497cbe8ca` | 26.83% | adaptive / multimodal / Computer Science | 5 | 1 | days-in-month switch adaptive explanation |
| `683e4510fb5afd217fd9d159` | 28.57% | assessment / multimodal / Biology | 4 | 0 | none |
| `683e451765e18627c73884df` | 28.57% | assessment / multimodal / Physics | 3 | 0 | none |
| `6847710b9bc321f32d5b5ab8` | 28.95% | adaptive / text / Calculus | 7 | 0 | none |
| `685454ee44fbb3cf43c29765` | 28.95% | adaptive / text / Statistics | 7 | 0 | none |
| `683e458c5f104dac1d4d6e7a` | 30.19% | active_learning / multimodal / Biology | 9 | 0 | none |
| `683e3d8d65e18627c7387f93` | 30.43% | adaptive / multimodal / Calculus | 4 | 0 | none |
| `684a8cd60c6c6ac5176925ef` | 30.68% | assessment / text / Statistics | 13 | 0 | none |
| `68545549f8ab7067dd48b799` | 31.82% | assessment / text / Physics | 1 | 2 | none |
| `683e451098da731381469199` | 32.69% | assessment / multimodal / Physics | 7 | 0 | none |
| `684a8cd6f08ce27c3bf577e0` | 33.33% | assessment / text / Chemistry | 6 | 0 | Henry-law mole-fraction assessment |
| `683e4518b4f61c885835b57d` | 34.21% | assessment / multimodal / Chemistry | 10 | 0 | none |
| `68387052ed1412eef12fffe2` | 34.78% | active_learning / multimodal / Physics | 9 | 0 | none |
| `681b80dd850f62964ac697d2` | 35.29% | adaptive / multimodal / Statistics | 6 | 0 | none |
| `68377627ca52a73e1545735e` | 35.48% | assessment / multimodal / Computer Science | 4 | 0 | recursive factorial assessment |
| `681cfb9fdbed21a8e4bde8fa` | 36.36% | adaptive / text / Calculus | 4 | 1 | none |
| `681904ae47ec182ef081cc59` | 36.84% | adaptive / text / Calculus | 12 | 0 | none |
| `68387052b790747a1c2a372e` | 38.24% | active_learning / multimodal / Statistics | 5 | 0 | none |
| `6847720874c7f1cb6eb0b1d5` | 38.81% | active_learning / text / Computer Science | 9 | 0 | none |
| `683775dc2f4468651311d6ad` | 39.02% | adaptive / multimodal / Chemistry | 5 | 0 | none |
| `68377627496507faa0915cd6` | 39.13% | assessment / multimodal / Biology | 12 | 0 | none |
| `68377627155e0b0f68c5f402` | 39.39% | assessment / multimodal / Physics | 4 | 0 | none |
| `68387053fd0caa1cb84ff6db` | 39.39% | active_learning / multimodal / Computer Science | 8 | 0 | none |
| `683e458d3a109788e3f7e66e` | 40.48% | active_learning / multimodal / Physics | 5 | 0 | kinematics active-learning hint |
| `683e4514fb5afd217fd9d1af` | 40.48% | assessment / multimodal / Physics | 5 | 0 | none |
| `683870ee896f97b90e668cb8` | 41.18% | active_learning / text / Statistics | 2 | 0 | none |
| `681b84ffb87b7f77f2d05477` | 41.86% | assessment / multimodal / Computer Science | 5 | 0 | none |
| `683870ef328fdda5d51a6203` | 41.86% | active_learning / text / Statistics | 5 | 0 | none |
| `6847710ae96863adfe49248d` | 42.11% | adaptive / text / Computer Science | 6 | 0 | none |
| `681cffc846a1279c844e6432` | 42.31% | active_learning / multimodal / Biology | 6 | 0 | trihybrid ideal-peas active-learning hint |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| not applicable | 50.00% | 1.0 | 1 | 0 |
| conciseness_relevance | 58.50% | 83.0 | 32 | 0 |
| truthfulness | 69.96% | 1064.0 | 150 | 2 |
| instruction_following | 72.79% | 3058.0 | 337 | 24 |
| visual_reasoning | 75.46% | 437.0 | 64 | 1 |
| student_level_calibration | 76.62% | 1945.0 | 241 | 7 |
| emotional_component | 80.54% | 290.0 | 78 | 1 |
| visual_perception | 81.07% | 248.0 | 53 | 2 |
| style_tone | 81.32% | 334.0 | 101 | 2 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 53.41% | 123.0 | 43 | 0 |
| Provides alternative solutions/ paths/ | 54.92% | 142.0 | 36 | 2 |
| Asks questions to guide students | 55.56% | 412.0 | 65 | 0 |
| Step by step help/ analysis | 69.89% | 501.0 | 94 | 6 |
| Stating definitions/ formulae/ theorems/ laws | 70.14% | 986.0 | 144 | 0 |
| Not applicable | 73.79% | 1293.0 | 257 | 15 |
| Identifying incorrect steps by student | 75.64% | 627.0 | 91 | 5 |
| Identifying Core difficulty/ misconception attribution | 75.91% | 714.0 | 127 | 0 |
| Identifying correct steps by student | 85.08% | 437.0 | 84 | 3 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 437 | 72.85% |
| chi-square variance-test adaptive explanation | 7 | 89.32% |
| recursive factorial assessment | 7 | 73.81% |
| OOP design / inventory class | 4 | 74.53% |
| binary-search midpoint overflow assessment | 3 | 83.02% |
| Henry-law mole-fraction assessment | 2 | 65.77% |
| electricity-rates two-sample CI adaptive explanation | 2 | 90.97% |
| inclined box slip-or-tip assessment | 2 | 49.49% |
| kinematics active-learning hint | 2 | 54.61% |
| meiosis-vs-mitosis gamete explanation | 2 | 59.30% |
| sinc integral/removable discontinuity assessment | 2 | 62.25% |
| 12V 3-ohm series/parallel circuit assessment | 1 | 99.03% |
| CLT sample-mean active-learning hint | 1 | 92.86% |
| Gene X methylation/tumor-suppressor active hint | 1 | 65.96% |
| Mendelian independent-assortment testcross | 1 | 47.06% |
| MovieRating active-learning hint | 1 | 86.11% |
| Normal MLE assessment | 1 | 93.42% |
| U-238/Pb-206 mass-ratio adaptive explanation | 1 | 100.00% |
| bulbs-in-parallel switch adaptive explanation | 1 | 68.09% |
| chlorine PES / bromide binding-energy explanation | 1 | 100.00% |
