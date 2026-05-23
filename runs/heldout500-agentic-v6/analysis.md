# TutorBench Run Analysis: `heldout500-agentic-v6`

- Rows: 500
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 73.69%
- Mean generation latency: 107733 ms
- Mean judge latency: 4274 ms
- Generation input/output tokens: 17240921 / 2609804
- Judge input/output tokens: 1357783 / 127398
- Negative-weight manual review rows: 47

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1986000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 398000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19998 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2385000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `68377588415e67c44f4734b6` | 4.55% | assessment / text / Physics | 4 | 1 | none |
| `6843120a2b986bd2d9ca5f3f` | 6.25% | assessment / text / Chemistry | 6 | 0 | weak-acid ICE-table assessment |
| `683e3d902b6d2a6c45002cec` | 15.38% | adaptive / multimodal / Calculus | 6 | 0 | none |
| `684771b3cf8ba842e93ec6de` | 16.22% | assessment / text / Computer Science | 7 | 0 | none |
| `683776272f4468651311d6dc` | 16.67% | assessment / multimodal / Calculus | 5 | 1 | none |
| `683e4510bd7caf8a464501d6` | 18.92% | assessment / multimodal / Physics | 6 | 0 | none |
| `6811d40e6b7f984ce18baebb` | 20.69% | adaptive / multimodal / Computer Science | 7 | 0 | none |
| `683e3d9065e18627c7388002` | 21.05% | adaptive / multimodal / Chemistry | 6 | 0 | none |
| `683775dd144eb8ef82cd50d4` | 22.73% | adaptive / multimodal / Chemistry | 5 | 0 | none |
| `6847710ac4590722c4324810` | 23.08% | adaptive / text / Physics | 4 | 0 | none |
| `681cffc846a1279c844e6432` | 23.08% | active_learning / multimodal / Biology | 8 | 0 | none |
| `68376d91c5b329d497cbe8ca` | 24.39% | adaptive / multimodal / Computer Science | 6 | 1 | days-in-month switch adaptive explanation |
| `6847720874c7f1cb6eb0b1d5` | 25.37% | active_learning / text / Computer Science | 10 | 0 | none |
| `68096a17d9108896c270f6b6` | 25.93% | adaptive / text / Physics | 4 | 0 | none |
| `683e45109394b13fefb08e44` | 26.09% | assessment / multimodal / Physics | 5 | 0 | none |
| `68097912014bb68a4c65e4a1` | 26.23% | assessment / text / Biology | 9 | 0 | none |
| `681b84ff94969ef6e11908e0` | 27.42% | assessment / multimodal / Physics | 9 | 0 | none |
| `683e4589a08f8bb26159787e` | 27.59% | active_learning / multimodal / Statistics | 5 | 0 | none |
| `683e458c5f104dac1d4d6e7a` | 28.30% | active_learning / multimodal / Biology | 10 | 0 | none |
| `685454ef513ee4759d9bd93a` | 28.57% | adaptive / text / Physics | 4 | 0 | none |
| `683e4510fb5afd217fd9d159` | 28.57% | assessment / multimodal / Biology | 4 | 0 | none |
| `683e458d3a109788e3f7e66e` | 28.57% | active_learning / multimodal / Physics | 6 | 0 | kinematics active-learning hint |
| `6847710b9bc321f32d5b5ab8` | 28.95% | adaptive / text / Calculus | 7 | 0 | none |
| `683e45108103655aef73fc0f` | 29.82% | assessment / multimodal / Statistics | 8 | 0 | none |
| `681cfb9f423b8a534abc79ba` | 30.23% | adaptive / text / Biology | 6 | 0 | none |
| `683e3d8d65e18627c7387f93` | 30.43% | adaptive / multimodal / Calculus | 4 | 0 | none |
| `684772095817461e60913ee8` | 30.56% | active_learning / text / Computer Science | 10 | 0 | none |
| `684a8cd60c6c6ac5176925ef` | 30.68% | assessment / text / Statistics | 13 | 0 | none |
| `683e45893a109788e3f7e5f2` | 31.34% | active_learning / multimodal / Biology | 10 | 0 | none |
| `68545549f8ab7067dd48b799` | 31.82% | assessment / text / Physics | 1 | 2 | none |
| `683e451098da731381469199` | 32.69% | assessment / multimodal / Physics | 7 | 0 | none |
| `681008c282c35b63b6d9c68f` | 33.33% | adaptive / multimodal / Calculus | 6 | 0 | radical derivative adaptive explanation |
| `683e4518b4f61c885835b57d` | 34.21% | assessment / multimodal / Chemistry | 10 | 0 | none |
| `683870ee896f97b90e668cb8` | 35.29% | active_learning / text / Statistics | 3 | 0 | none |
| `681b80dd850f62964ac697d2` | 35.29% | adaptive / multimodal / Statistics | 6 | 0 | none |
| `68377627ca52a73e1545735e` | 35.48% | assessment / multimodal / Computer Science | 4 | 0 | recursive factorial assessment |
| `68376de1c596c43935ed5a4d` | 36.17% | assessment / multimodal / Chemistry | 5 | 1 | none |
| `68477209e96863adfe492508` | 37.50% | active_learning / text / Calculus | 4 | 0 | none |
| `683e3d8f38791d6d309f6cd1` | 37.84% | adaptive / multimodal / Statistics | 7 | 0 | none |
| `68387052b790747a1c2a372e` | 38.24% | active_learning / multimodal / Statistics | 5 | 0 | none |
| `68377627496507faa0915cd6` | 39.13% | assessment / multimodal / Biology | 12 | 0 | none |
| `6811d40ea1d9c30bb57338c2` | 39.29% | adaptive / multimodal / Physics | 5 | 0 | none |
| `6842a1fbb8f271121fd79472` | 40.00% | adaptive / text / Statistics | 3 | 0 | none |
| `683e4514fb5afd217fd9d1af` | 40.48% | assessment / multimodal / Physics | 5 | 0 | none |
| `681a876b69aba25329fa1450` | 40.74% | assessment / text / Statistics | 4 | 0 | none |
| `684a8c40562837a83a9ac6b2` | 40.74% | adaptive / text / Physics | 4 | 0 | none |
| `683e458e5ac03bbadfe24389` | 41.67% | active_learning / multimodal / Statistics | 5 | 0 | none |
| `683870ef328fdda5d51a6203` | 41.86% | active_learning / text / Statistics | 5 | 0 | none |
| `681904ae47ec182ef081cc59` | 42.11% | adaptive / text / Calculus | 11 | 0 | none |
| `683e3d8f2b6d2a6c45002ccc` | 42.31% | adaptive / multimodal / Chemistry | 3 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| not applicable | 50.00% | 1.0 | 1 | 0 |
| truthfulness | 67.96% | 1135.0 | 149 | 2 |
| conciseness_relevance | 69.50% | 61.0 | 28 | 0 |
| instruction_following | 72.99% | 3035.0 | 315 | 24 |
| visual_reasoning | 75.97% | 428.0 | 64 | 2 |
| student_level_calibration | 76.42% | 1962.0 | 234 | 7 |
| visual_perception | 80.38% | 257.0 | 56 | 2 |
| emotional_component | 81.81% | 271.0 | 75 | 1 |
| style_tone | 82.10% | 320.0 | 102 | 2 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 48.48% | 136.0 | 45 | 0 |
| Provides alternative solutions/ paths/ | 54.29% | 144.0 | 41 | 3 |
| Asks questions to guide students | 56.20% | 406.0 | 60 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 68.93% | 1026.0 | 144 | 0 |
| Step by step help/ analysis | 70.55% | 490.0 | 87 | 7 |
| Not applicable | 73.65% | 1300.0 | 243 | 14 |
| Identifying Core difficulty/ misconception attribution | 75.91% | 714.0 | 123 | 0 |
| Identifying incorrect steps by student | 75.91% | 620.0 | 89 | 5 |
| Identifying correct steps by student | 85.96% | 411.0 | 78 | 3 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 452 | 73.75% |
| recursive factorial assessment | 7 | 75.85% |
| chi-square variance-test adaptive explanation | 6 | 84.66% |
| OOP design / inventory class | 4 | 87.34% |
| binary-search midpoint overflow assessment | 3 | 77.97% |
| Henry-law mole-fraction assessment | 2 | 82.44% |
| electricity-rates two-sample CI adaptive explanation | 2 | 84.72% |
| sinc integral/removable discontinuity assessment | 2 | 62.25% |
| CLT sample-mean active-learning hint | 1 | 75.00% |
| Gene X methylation/tumor-suppressor active hint | 1 | 57.45% |
| MovieRating active-learning hint | 1 | 72.22% |
| Normal MLE assessment | 1 | 93.42% |
| U-238/Pb-206 mass-ratio adaptive explanation | 1 | 100.00% |
| bulbs-in-parallel switch adaptive explanation | 1 | 78.72% |
| copper/KMnO4 redox active-learning hint | 1 | 71.93% |
| days-in-month switch adaptive explanation | 1 | 24.39% |
| geometric-shapes OOP center-distance active hint | 1 | 51.22% |
| hydrogen halide acid strength | 1 | 57.89% |
| hydrogen iodide to iodoethylene assessment | 1 | 54.55% |
| kinematics active-learning hint | 1 | 28.57% |
