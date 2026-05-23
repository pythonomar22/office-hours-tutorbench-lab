# TutorBench Run Analysis: `heldout500-blend-v10`

- Rows: 500
- Strategy: `agentic`
- Candidate model: `blend:anthropic:claude-sonnet-4-6|anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 75.33%
- Mean generation latency: 106621 ms
- Mean judge latency: 3982 ms
- Generation input/output tokens: 17561366 / 2609597
- Judge input/output tokens: 1355187 / 127991
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
| `68377588415e67c44f4734b6` | 4.55% | assessment / text / Physics | 4 | 1 | inclined box slip-or-tip assessment |
| `683776272f4468651311d6dc` | 16.67% | assessment / multimodal / Calculus | 5 | 1 | none |
| `6811d40e6b7f984ce18baebb` | 20.69% | adaptive / multimodal / Computer Science | 7 | 0 | none |
| `6847710ac4590722c4324810` | 23.08% | adaptive / text / Physics | 4 | 0 | none |
| `68097912014bb68a4c65e4a1` | 24.59% | assessment / text / Biology | 10 | 0 | none |
| `68377545cbb6263fa01c0268` | 25.00% | adaptive / text / Calculus | 3 | 0 | none |
| `68096a17d9108896c270f6b6` | 25.93% | adaptive / text / Physics | 4 | 0 | none |
| `683e45109394b13fefb08e44` | 26.09% | assessment / multimodal / Physics | 5 | 0 | none |
| `68376d91c5b329d497cbe8ca` | 26.83% | adaptive / multimodal / Computer Science | 5 | 1 | days-in-month switch adaptive explanation |
| `681b84ff94969ef6e11908e0` | 27.42% | assessment / multimodal / Physics | 9 | 0 | none |
| `685454ef513ee4759d9bd93a` | 28.57% | adaptive / text / Physics | 4 | 0 | none |
| `683e4510fb5afd217fd9d159` | 28.57% | assessment / multimodal / Biology | 4 | 0 | none |
| `6847710b9bc321f32d5b5ab8` | 28.95% | adaptive / text / Calculus | 7 | 0 | none |
| `681cfb9f423b8a534abc79ba` | 30.23% | adaptive / text / Biology | 6 | 0 | none |
| `684772095817461e60913ee8` | 30.56% | active_learning / text / Computer Science | 10 | 0 | none |
| `683e3d8d9394b13fefb087f2` | 31.11% | adaptive / multimodal / Statistics | 11 | 0 | none |
| `68545549f8ab7067dd48b799` | 31.82% | assessment / text / Physics | 1 | 2 | none |
| `683e451098da731381469199` | 32.69% | assessment / multimodal / Physics | 7 | 0 | none |
| `6847720874c7f1cb6eb0b1d5` | 32.84% | active_learning / text / Computer Science | 9 | 0 | none |
| `683e3d9065e18627c7388002` | 34.21% | adaptive / multimodal / Chemistry | 5 | 0 | none |
| `683e4518b4f61c885835b57d` | 34.21% | assessment / multimodal / Chemistry | 10 | 0 | none |
| `684a8cd60c6c6ac5176925ef` | 35.23% | assessment / text / Statistics | 13 | 0 | none |
| `683e3d8fa08f8bb26159720b` | 35.29% | adaptive / multimodal / Statistics | 6 | 1 | chi-square variance-test adaptive explanation |
| `681b80dd850f62964ac697d2` | 35.29% | adaptive / multimodal / Statistics | 6 | 0 | none |
| `68377627ca52a73e1545735e` | 35.48% | assessment / multimodal / Computer Science | 4 | 0 | recursive factorial assessment |
| `68376de1c596c43935ed5a4d` | 36.17% | assessment / multimodal / Chemistry | 5 | 1 | none |
| `68477209e96863adfe492508` | 37.50% | active_learning / text / Calculus | 4 | 0 | none |
| `68387052b790747a1c2a372e` | 38.24% | active_learning / multimodal / Statistics | 5 | 0 | none |
| `683e3d902b6d2a6c45002cec` | 38.46% | adaptive / multimodal / Calculus | 4 | 0 | none |
| `683775dc2f4468651311d6ad` | 39.02% | adaptive / multimodal / Chemistry | 5 | 0 | none |
| `68377627496507faa0915cd6` | 39.13% | assessment / multimodal / Biology | 12 | 0 | none |
| `6811d40ea1d9c30bb57338c2` | 39.29% | adaptive / multimodal / Physics | 5 | 0 | none |
| `6842a1fbb8f271121fd79472` | 40.00% | adaptive / text / Statistics | 3 | 0 | none |
| `683e458d3a109788e3f7e66e` | 40.48% | active_learning / multimodal / Physics | 5 | 0 | kinematics active-learning hint |
| `683e4514fb5afd217fd9d1af` | 40.48% | assessment / multimodal / Physics | 5 | 0 | none |
| `684a8c40562837a83a9ac6b2` | 40.74% | adaptive / text / Physics | 4 | 0 | none |
| `683870ee896f97b90e668cb8` | 41.18% | active_learning / text / Statistics | 2 | 0 | none |
| `684772091b2bfa550f749674` | 42.31% | active_learning / text / Computer Science | 3 | 0 | none |
| `681cffc846a1279c844e6432` | 42.31% | active_learning / multimodal / Biology | 6 | 0 | trihybrid ideal-peas active-learning hint |
| `6843160a0015fc211142fa11` | 42.31% | active_learning / text / Computer Science | 6 | 0 | none |
| `681cfb9f998b35aadeba36e0` | 42.86% | adaptive / text / Statistics | 4 | 0 | none |
| `683e451365e18627c73884a1` | 42.86% | assessment / multimodal / Calculus | 7 | 1 | none |
| `681cfc8cb4e0809f6fae0767` | 43.24% | assessment / text / Calculus | 5 | 0 | sinc integral/removable discontinuity assessment |
| `683e451455b71d5f5598c49a` | 43.66% | assessment / multimodal / Biology | 8 | 0 | none |
| `683e3d8d9906d6b295d9044d` | 44.44% | adaptive / multimodal / Calculus | 3 | 0 | none |
| `684a8cd6a8da4aded13ef58d` | 44.44% | assessment / text / Calculus | 2 | 1 | none |
| `6811d40e36d04d3bc7965f72` | 44.74% | adaptive / multimodal / Chemistry | 5 | 0 | none |
| `681904ae3f170328e61a5e3c` | 44.83% | adaptive / text / Statistics | 4 | 0 | chi-square variance-test adaptive explanation |
| `6811d993d391e676ed896378` | 45.45% | assessment / multimodal / Biology | 6 | 0 | none |
| `683775dd144eb8ef82cd50d4` | 45.45% | adaptive / multimodal / Chemistry | 4 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| not applicable | 50.00% | 1.0 | 1 | 0 |
| conciseness_relevance | 62.00% | 76.0 | 30 | 0 |
| truthfulness | 70.53% | 1044.0 | 145 | 3 |
| instruction_following | 75.04% | 2805.0 | 312 | 25 |
| visual_reasoning | 77.04% | 409.0 | 62 | 1 |
| student_level_calibration | 78.19% | 1814.0 | 228 | 7 |
| emotional_component | 82.42% | 262.0 | 73 | 1 |
| style_tone | 82.55% | 312.0 | 99 | 2 |
| visual_perception | 82.98% | 223.0 | 51 | 2 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Provides alternative solutions/ paths/ | 50.48% | 156.0 | 44 | 3 |
| Includes examples/ analogy | 54.17% | 121.0 | 42 | 0 |
| Asks questions to guide students | 62.46% | 348.0 | 58 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 70.41% | 977.0 | 141 | 0 |
| Step by step help/ analysis | 72.24% | 462.0 | 85 | 6 |
| Not applicable | 75.31% | 1218.0 | 243 | 16 |
| Identifying Core difficulty/ misconception attribution | 78.21% | 646.0 | 116 | 0 |
| Identifying incorrect steps by student | 79.41% | 530.0 | 79 | 5 |
| Identifying correct steps by student | 85.76% | 417.0 | 76 | 3 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 436 | 75.17% |
| chi-square variance-test adaptive explanation | 7 | 82.56% |
| recursive factorial assessment | 7 | 71.29% |
| OOP design / inventory class | 4 | 87.34% |
| binary-search midpoint overflow assessment | 3 | 83.02% |
| inclined box slip-or-tip assessment | 3 | 50.05% |
| AP CSA MemberInfo removeMembers assessment | 2 | 98.65% |
| Henry-law mole-fraction assessment | 2 | 82.44% |
| electricity-rates two-sample CI adaptive explanation | 2 | 90.97% |
| kinematics active-learning hint | 2 | 54.61% |
| mean-CI z-vs-t active-learning hint | 2 | 89.66% |
| sinc integral/removable discontinuity assessment | 2 | 62.25% |
| 12V 3-ohm series/parallel circuit assessment | 1 | 99.03% |
| CLT sample-mean active-learning hint | 1 | 92.86% |
| Gene X methylation/tumor-suppressor active hint | 1 | 65.96% |
| Mendelian independent-assortment testcross | 1 | 47.06% |
| MovieRating active-learning hint | 1 | 86.11% |
| Normal MLE assessment | 1 | 93.42% |
| U-238/Pb-206 mass-ratio adaptive explanation | 1 | 100.00% |
| bulbs-in-parallel switch adaptive explanation | 1 | 78.72% |
