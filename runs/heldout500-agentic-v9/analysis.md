# TutorBench Run Analysis: `heldout500-agentic-v9`

- Rows: 500
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 72.78%
- Mean generation latency: 104690 ms
- Mean judge latency: 3957 ms
- Generation input/output tokens: 17961631 / 2599162
- Judge input/output tokens: 1351236 / 127478
- Negative-weight manual review rows: 47

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1987000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19998 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2387000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `68377588415e67c44f4734b6` | 4.55% | assessment / text / Physics | 4 | 1 | inclined box slip-or-tip assessment |
| `683e451455b71d5f5598c49a` | 15.49% | assessment / multimodal / Biology | 12 | 0 | none |
| `683776272f4468651311d6dc` | 16.67% | assessment / multimodal / Calculus | 5 | 1 | none |
| `681cfb9f423b8a534abc79ba` | 18.60% | adaptive / text / Biology | 7 | 0 | meiosis-vs-mitosis gamete explanation |
| `6842a1fbb8f271121fd79472` | 20.00% | adaptive / text / Statistics | 4 | 0 | none |
| `6811d40e6b7f984ce18baebb` | 20.69% | adaptive / multimodal / Computer Science | 7 | 0 | none |
| `684a8c40562837a83a9ac6b2` | 22.22% | adaptive / text / Physics | 5 | 0 | none |
| `6847710ac4590722c4324810` | 23.08% | adaptive / text / Physics | 4 | 0 | none |
| `6843160a0015fc211142fa11` | 23.08% | active_learning / text / Computer Science | 8 | 0 | none |
| `68097912014bb68a4c65e4a1` | 24.59% | assessment / text / Biology | 10 | 0 | none |
| `68377545cbb6263fa01c0268` | 25.00% | adaptive / text / Calculus | 2 | 1 | none |
| `6837754519214e0eed328c96` | 25.00% | adaptive / text / Computer Science | 4 | 0 | none |
| `68376de1c596c43935ed5a4d` | 25.53% | assessment / multimodal / Chemistry | 6 | 1 | none |
| `68096a17d9108896c270f6b6` | 25.93% | adaptive / text / Physics | 4 | 0 | none |
| `683e45109394b13fefb08e44` | 26.09% | assessment / multimodal / Physics | 5 | 0 | none |
| `68376d91c5b329d497cbe8ca` | 26.83% | adaptive / multimodal / Computer Science | 5 | 1 | days-in-month switch adaptive explanation |
| `683e451765e18627c73884df` | 28.57% | assessment / multimodal / Physics | 3 | 0 | none |
| `6847710b9bc321f32d5b5ab8` | 28.95% | adaptive / text / Calculus | 7 | 0 | none |
| `685454ee44fbb3cf43c29765` | 28.95% | adaptive / text / Statistics | 7 | 0 | none |
| `683e3d8d9394b13fefb087f2` | 31.11% | adaptive / multimodal / Statistics | 11 | 0 | none |
| `68545549f8ab7067dd48b799` | 31.82% | assessment / text / Physics | 1 | 2 | none |
| `683e451098da731381469199` | 32.69% | assessment / multimodal / Physics | 7 | 0 | none |
| `684a8cd6f08ce27c3bf577e0` | 33.33% | assessment / text / Chemistry | 6 | 0 | Henry-law mole-fraction assessment |
| `681cfb9f46a1279c844e628e` | 33.33% | adaptive / text / Chemistry | 6 | 0 | none |
| `68477209c4915de7a58b3d02` | 33.96% | active_learning / text / Computer Science | 7 | 0 | none |
| `683e3d9065e18627c7388002` | 34.21% | adaptive / multimodal / Chemistry | 5 | 0 | none |
| `683e4518b4f61c885835b57d` | 34.21% | assessment / multimodal / Chemistry | 8 | 2 | none |
| `683e3d902b6d2a6c45002cec` | 34.62% | adaptive / multimodal / Calculus | 5 | 0 | none |
| `684a8cd60c6c6ac5176925ef` | 35.23% | assessment / text / Statistics | 13 | 0 | none |
| `681b80dd850f62964ac697d2` | 35.29% | adaptive / multimodal / Statistics | 6 | 0 | none |
| `68377627ca52a73e1545735e` | 35.48% | assessment / multimodal / Computer Science | 4 | 0 | recursive factorial assessment |
| `681cfb9fdbed21a8e4bde8fa` | 36.36% | adaptive / text / Calculus | 4 | 1 | none |
| `683775467c71f24d6187a95c` | 36.73% | adaptive / text / Biology | 7 | 0 | none |
| `681cfb9f998b35aadeba36e0` | 38.10% | adaptive / text / Statistics | 5 | 0 | none |
| `68387052b790747a1c2a372e` | 38.24% | active_learning / multimodal / Statistics | 5 | 0 | none |
| `680979013d9d7eb8a361d50a` | 38.36% | assessment / text / Chemistry | 9 | 0 | none |
| `683775dc2f4468651311d6ad` | 39.02% | adaptive / multimodal / Chemistry | 5 | 0 | none |
| `68377627496507faa0915cd6` | 39.13% | assessment / multimodal / Biology | 12 | 0 | none |
| `68377627155e0b0f68c5f402` | 39.39% | assessment / multimodal / Physics | 4 | 0 | none |
| `6847720874c7f1cb6eb0b1d5` | 40.30% | active_learning / text / Computer Science | 8 | 0 | none |
| `683e458d3a109788e3f7e66e` | 40.48% | active_learning / multimodal / Physics | 5 | 0 | kinematics active-learning hint |
| `683e4514fb5afd217fd9d1af` | 40.48% | assessment / multimodal / Physics | 5 | 0 | none |
| `683870ee896f97b90e668cb8` | 41.18% | active_learning / text / Statistics | 2 | 0 | none |
| `683628c7428073c98da6939e` | 41.18% | adaptive / text / Calculus | 2 | 0 | none |
| `681b84ffb87b7f77f2d05477` | 41.86% | assessment / multimodal / Computer Science | 5 | 0 | none |
| `68387052ed1412eef12fffe2` | 42.03% | active_learning / multimodal / Physics | 8 | 0 | none |
| `6847710ae96863adfe49248d` | 42.11% | adaptive / text / Computer Science | 6 | 0 | none |
| `684772091b2bfa550f749674` | 42.31% | active_learning / text / Computer Science | 3 | 0 | none |
| `681cffc846a1279c844e6432` | 42.31% | active_learning / multimodal / Biology | 6 | 0 | trihybrid ideal-peas active-learning hint |
| `683e451365e18627c73884a1` | 42.86% | assessment / multimodal / Calculus | 7 | 1 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| not applicable | 50.00% | 1.0 | 1 | 0 |
| conciseness_relevance | 61.50% | 77.0 | 31 | 0 |
| truthfulness | 69.76% | 1071.0 | 152 | 4 |
| instruction_following | 72.36% | 3106.0 | 341 | 25 |
| visual_reasoning | 75.01% | 445.0 | 67 | 1 |
| student_level_calibration | 76.42% | 1962.0 | 249 | 7 |
| visual_perception | 79.92% | 263.0 | 56 | 2 |
| emotional_component | 80.54% | 290.0 | 78 | 1 |
| style_tone | 81.66% | 328.0 | 103 | 2 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 51.14% | 129.0 | 46 | 0 |
| Provides alternative solutions/ paths/ | 54.29% | 144.0 | 39 | 2 |
| Asks questions to guide students | 59.65% | 374.0 | 67 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 68.66% | 1035.0 | 153 | 0 |
| Step by step help/ analysis | 70.91% | 484.0 | 90 | 6 |
| Not applicable | 72.88% | 1338.0 | 259 | 18 |
| Identifying Core difficulty/ misconception attribution | 75.44% | 728.0 | 132 | 0 |
| Identifying incorrect steps by student | 76.22% | 612.0 | 89 | 5 |
| Identifying correct steps by student | 84.39% | 457.0 | 81 | 3 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 430 | 72.45% |
| chi-square variance-test adaptive explanation | 7 | 88.44% |
| recursive factorial assessment | 7 | 72.50% |
| OOP design / inventory class | 5 | 77.12% |
| inclined box slip-or-tip assessment | 3 | 50.05% |
| AP CSA MemberInfo removeMembers assessment | 2 | 98.65% |
| Henry-law mole-fraction assessment | 2 | 56.85% |
| binary-search midpoint overflow assessment | 2 | 81.29% |
| electricity-rates two-sample CI adaptive explanation | 2 | 90.97% |
| kinematics active-learning hint | 2 | 54.61% |
| logarithmic improper-integral assessment | 2 | 67.75% |
| mean-CI z-vs-t active-learning hint | 2 | 89.66% |
| meiosis-vs-mitosis gamete explanation | 2 | 59.30% |
| sinc integral/removable discontinuity assessment | 2 | 62.25% |
| 12V 3-ohm series/parallel circuit assessment | 1 | 100.00% |
| CLT sample-mean active-learning hint | 1 | 92.86% |
| Gene X methylation/tumor-suppressor active hint | 1 | 65.96% |
| Hardy-Weinberg graph-reading assessment | 1 | 100.00% |
| Mendelian independent-assortment testcross | 1 | 47.06% |
| MovieRating active-learning hint | 1 | 86.11% |
