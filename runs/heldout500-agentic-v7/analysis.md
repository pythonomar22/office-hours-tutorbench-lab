# TutorBench Run Analysis: `heldout500-agentic-v7`

- Rows: 500
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 72.49%
- Mean generation latency: 106871 ms
- Mean judge latency: 4028 ms
- Generation input/output tokens: 17354620 / 2623628
- Judge input/output tokens: 1361569 / 127468
- Negative-weight manual review rows: 47

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1988000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19997 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2388000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `68377588415e67c44f4734b6` | 4.55% | assessment / text / Physics | 4 | 1 | inclined box slip-or-tip assessment |
| `68387053806964a2566da1b8` | 11.11% | active_learning / multimodal / Physics | 4 | 0 | none |
| `683775dc0a6dba7869a5c576` | 14.63% | adaptive / multimodal / Chemistry | 7 | 0 | none |
| `6811d40e6b7f984ce18baebb` | 20.69% | adaptive / multimodal / Computer Science | 7 | 0 | none |
| `68477209c4915de7a58b3d02` | 22.64% | active_learning / text / Computer Science | 9 | 0 | none |
| `6847710ac4590722c4324810` | 23.08% | adaptive / text / Physics | 4 | 0 | none |
| `68376d91c5b329d497cbe8ca` | 24.39% | adaptive / multimodal / Computer Science | 6 | 1 | days-in-month switch adaptive explanation |
| `68377545cbb6263fa01c0268` | 25.00% | adaptive / text / Calculus | 2 | 1 | none |
| `681b84ff94969ef6e11908e0` | 25.81% | assessment / multimodal / Physics | 10 | 0 | none |
| `68096a17d9108896c270f6b6` | 25.93% | adaptive / text / Physics | 4 | 0 | none |
| `684a8c40562837a83a9ac6b2` | 25.93% | adaptive / text / Physics | 4 | 0 | none |
| `683e45109394b13fefb08e44` | 26.09% | assessment / multimodal / Physics | 5 | 0 | none |
| `683e450e225c80e89ef01948` | 26.21% | assessment / multimodal / Physics | 16 | 0 | none |
| `68097912014bb68a4c65e4a1` | 26.23% | assessment / text / Biology | 9 | 0 | none |
| `683e4518b4f61c885835b57d` | 27.63% | assessment / multimodal / Chemistry | 11 | 0 | none |
| `683e458c5f104dac1d4d6e7a` | 28.30% | active_learning / multimodal / Biology | 10 | 0 | none |
| `685454ef513ee4759d9bd93a` | 28.57% | adaptive / text / Physics | 4 | 0 | none |
| `681b84ffb87b7f77f2d05477` | 30.23% | assessment / multimodal / Computer Science | 6 | 0 | none |
| `684772095817461e60913ee8` | 30.56% | active_learning / text / Computer Science | 10 | 0 | none |
| `683776272f4468651311d6dc` | 30.56% | assessment / multimodal / Calculus | 4 | 1 | none |
| `683e3d9065e18627c7388002` | 31.58% | adaptive / multimodal / Chemistry | 6 | 0 | none |
| `685454ee2187108ef9b08a95` | 31.82% | adaptive / text / Biology | 3 | 0 | none |
| `68545549f8ab7067dd48b799` | 31.82% | assessment / text / Physics | 1 | 2 | none |
| `683e451098da731381469199` | 32.69% | assessment / multimodal / Physics | 7 | 0 | none |
| `6847720874c7f1cb6eb0b1d5` | 32.84% | active_learning / text / Computer Science | 9 | 0 | none |
| `681cfb9f998b35aadeba36e0` | 33.33% | adaptive / text / Statistics | 6 | 0 | none |
| `683e45105f104dac1d4d6d47` | 33.33% | assessment / multimodal / Statistics | 6 | 0 | none |
| `681cfba0516d8f36be368b74` | 33.33% | adaptive / text / Chemistry | 6 | 0 | none |
| `68377627496507faa0915cd6` | 33.70% | assessment / multimodal / Biology | 13 | 0 | none |
| `683e3d902b6d2a6c45002cec` | 34.62% | adaptive / multimodal / Calculus | 5 | 0 | none |
| `684a8cd60c6c6ac5176925ef` | 35.23% | assessment / text / Statistics | 13 | 0 | none |
| `68377627ca52a73e1545735e` | 35.48% | assessment / multimodal / Computer Science | 4 | 0 | recursive factorial assessment |
| `6843120a2b986bd2d9ca5f3f` | 37.50% | assessment / text / Chemistry | 3 | 1 | weak-acid ICE-table assessment |
| `68477209e96863adfe492508` | 37.50% | active_learning / text / Calculus | 4 | 0 | none |
| `68387052b790747a1c2a372e` | 38.24% | active_learning / multimodal / Statistics | 5 | 0 | none |
| `681b80dd850f62964ac697d2` | 38.24% | adaptive / multimodal / Statistics | 5 | 0 | none |
| `680979013d9d7eb8a361d50a` | 38.36% | assessment / text / Chemistry | 9 | 0 | none |
| `683e45108103655aef73fc0f` | 38.60% | assessment / multimodal / Statistics | 7 | 0 | none |
| `683775dc2f4468651311d6ad` | 39.02% | adaptive / multimodal / Chemistry | 5 | 0 | none |
| `683e45172a32fba415085acc` | 39.39% | assessment / multimodal / Biology | 8 | 0 | none |
| `683870525afc1229ea941253` | 40.30% | active_learning / multimodal / Statistics | 8 | 0 | none |
| `683e458d3a109788e3f7e66e` | 40.48% | active_learning / multimodal / Physics | 5 | 0 | kinematics active-learning hint |
| `681a876b69aba25329fa1450` | 40.74% | assessment / text / Statistics | 4 | 0 | none |
| `68376de04d48dbcf9aa0d0b3` | 40.91% | assessment / multimodal / Computer Science | 6 | 0 | recursive factorial assessment |
| `683e45112667944fdee505b4` | 40.98% | assessment / multimodal / Physics | 8 | 0 | none |
| `683870ee896f97b90e668cb8` | 41.18% | active_learning / text / Statistics | 2 | 0 | none |
| `683628c7428073c98da6939e` | 41.18% | adaptive / text / Calculus | 2 | 0 | none |
| `683e458f65e18627c73885bc` | 41.86% | active_learning / multimodal / Statistics | 5 | 0 | none |
| `681cfb9f423b8a534abc79ba` | 41.86% | adaptive / text / Biology | 5 | 0 | none |
| `683870ef328fdda5d51a6203` | 41.86% | active_learning / text / Statistics | 5 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| not applicable | 50.00% | 1.0 | 1 | 0 |
| conciseness_relevance | 68.50% | 63.0 | 30 | 0 |
| visual_reasoning | 69.12% | 550.0 | 75 | 1 |
| truthfulness | 69.59% | 1077.0 | 144 | 3 |
| instruction_following | 72.69% | 3069.0 | 338 | 28 |
| student_level_calibration | 75.65% | 2026.0 | 252 | 8 |
| visual_perception | 78.09% | 287.0 | 58 | 3 |
| emotional_component | 79.13% | 311.0 | 88 | 1 |
| style_tone | 80.48% | 349.0 | 120 | 2 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Provides alternative solutions/ paths/ | 49.84% | 158.0 | 42 | 3 |
| Asks questions to guide students | 57.82% | 391.0 | 63 | 0 |
| Includes examples/ analogy | 57.95% | 111.0 | 39 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 68.99% | 1024.0 | 148 | 0 |
| Step by step help/ analysis | 71.09% | 481.0 | 85 | 6 |
| Not applicable | 71.64% | 1399.0 | 265 | 19 |
| Identifying Core difficulty/ misconception attribution | 75.03% | 740.0 | 127 | 0 |
| Identifying incorrect steps by student | 75.10% | 641.0 | 92 | 6 |
| Identifying correct steps by student | 84.26% | 461.0 | 81 | 3 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 440 | 72.65% |
| chi-square variance-test adaptive explanation | 8 | 73.90% |
| OOP design / inventory class | 7 | 75.19% |
| recursive factorial assessment | 7 | 63.96% |
| inclined box slip-or-tip assessment | 3 | 64.48% |
| AP CSA MemberInfo removeMembers assessment | 2 | 83.02% |
| Henry-law mole-fraction assessment | 2 | 82.44% |
| binary-search midpoint overflow assessment | 2 | 73.72% |
| electricity-rates two-sample CI adaptive explanation | 2 | 89.93% |
| logarithmic improper-integral assessment | 2 | 67.75% |
| sinc integral/removable discontinuity assessment | 2 | 69.00% |
| CLT sample-mean active-learning hint | 1 | 75.00% |
| Gene X methylation/tumor-suppressor active hint | 1 | 46.81% |
| MovieRating active-learning hint | 1 | 72.22% |
| Normal MLE assessment | 1 | 93.42% |
| U-238/Pb-206 mass-ratio adaptive explanation | 1 | 97.56% |
| bulbs-in-parallel switch adaptive explanation | 1 | 68.09% |
| copper/KMnO4 redox active-learning hint | 1 | 45.61% |
| days-in-month switch adaptive explanation | 1 | 24.39% |
| geometric-shapes OOP center-distance active hint | 1 | 51.22% |
