# TutorBench Run Analysis: `heldout500-blend-v10`

- Rows: 500
- Strategy: `agentic`
- Candidate model: `blend:anthropic:claude-sonnet-4-6|anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 76.72%
- Mean generation latency: 106961 ms
- Mean judge latency: 3979 ms
- Generation input/output tokens: 17736768 / 2620931
- Judge input/output tokens: 1356048 / 127986
- Negative-weight manual review rows: 44

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
| `68377545cbb6263fa01c0268` | 25.00% | adaptive / text / Calculus | 4 | 0 | none |
| `68096a17d9108896c270f6b6` | 25.93% | adaptive / text / Physics | 4 | 0 | none |
| `68376d91c5b329d497cbe8ca` | 26.83% | adaptive / multimodal / Computer Science | 5 | 0 | days-in-month switch adaptive explanation |
| `685454ef513ee4759d9bd93a` | 28.57% | adaptive / text / Physics | 4 | 0 | none |
| `683e4510fb5afd217fd9d159` | 28.57% | assessment / multimodal / Biology | 4 | 0 | none |
| `6847710b9bc321f32d5b5ab8` | 28.95% | adaptive / text / Calculus | 7 | 0 | none |
| `681cfb9f423b8a534abc79ba` | 30.23% | adaptive / text / Biology | 6 | 0 | none |
| `684772095817461e60913ee8` | 30.56% | active_learning / text / Computer Science | 10 | 0 | none |
| `68545549f8ab7067dd48b799` | 31.82% | assessment / text / Physics | 1 | 0 | none |
| `683e451098da731381469199` | 32.69% | assessment / multimodal / Physics | 7 | 0 | none |
| `6847720874c7f1cb6eb0b1d5` | 32.84% | active_learning / text / Computer Science | 9 | 0 | none |
| `683e3d9065e18627c7388002` | 34.21% | adaptive / multimodal / Chemistry | 5 | 0 | none |
| `683e4518b4f61c885835b57d` | 34.21% | assessment / multimodal / Chemistry | 12 | 0 | none |
| `684a8cd60c6c6ac5176925ef` | 35.23% | assessment / text / Statistics | 13 | 0 | none |
| `681b80dd850f62964ac697d2` | 35.29% | adaptive / multimodal / Statistics | 6 | 0 | none |
| `68377627ca52a73e1545735e` | 35.48% | assessment / multimodal / Computer Science | 4 | 0 | recursive factorial assessment |
| `68376de1c596c43935ed5a4d` | 36.17% | assessment / multimodal / Chemistry | 5 | 0 | none |
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
| `683e451365e18627c73884a1` | 42.86% | assessment / multimodal / Calculus | 7 | 0 | none |
| `681cfc8cb4e0809f6fae0767` | 43.24% | assessment / text / Calculus | 5 | 0 | sinc integral/removable discontinuity assessment |
| `683e451455b71d5f5598c49a` | 43.66% | assessment / multimodal / Biology | 8 | 0 | none |
| `683e3d8d9906d6b295d9044d` | 44.44% | adaptive / multimodal / Calculus | 3 | 0 | none |
| `684a8cd6a8da4aded13ef58d` | 44.44% | assessment / text / Calculus | 2 | 0 | none |
| `6811d40e36d04d3bc7965f72` | 44.74% | adaptive / multimodal / Chemistry | 5 | 0 | none |
| `681904ae3f170328e61a5e3c` | 44.83% | adaptive / text / Statistics | 4 | 0 | chi-square variance-test adaptive explanation |
| `6811d993d391e676ed896378` | 45.45% | assessment / multimodal / Biology | 6 | 0 | none |
| `683775dd144eb8ef82cd50d4` | 45.45% | adaptive / multimodal / Chemistry | 4 | 0 | none |
| `6814f360736eaea472ce9b26` | 45.95% | adaptive / multimodal / Computer Science | 4 | 0 | none |
| `68477209a30ca13e9cde77a9` | 46.15% | active_learning / text / Statistics | 5 | 0 | none |
| `685454ee8639de96a3d235d4` | 46.43% | adaptive / text / Statistics | 3 | 0 | none |
| `681a87214c3f3a64bb787392` | 46.43% | adaptive / text / Physics | 2 | 0 | none |
| `681cfcca41f2915eaf79891b` | 46.55% | active_learning / text / Statistics | 7 | 0 | penicillin allergy Bayes active-learning hint |
| `68545548714d62d3ac325d31` | 46.81% | assessment / text / Biology | 5 | 0 | none |
| `68387053fd0caa1cb84ff6db` | 46.97% | active_learning / multimodal / Computer Science | 7 | 0 | none |
| `681904ae38eb27c158f618cb` | 47.06% | adaptive / text / Computer Science | 6 | 0 | none |
| `681cfd7a41f2915eaf798959` | 47.06% | adaptive / multimodal / Biology | 5 | 0 | Mendelian independent-assortment testcross |
| `681904ae47ec182ef081cc59` | 47.37% | adaptive / text / Calculus | 10 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| not applicable | 50.00% | 1.0 | 1 | 0 |
| conciseness_relevance | 64.50% | 71.0 | 29 | 0 |
| truthfulness | 70.90% | 1039.0 | 143 | 1 |
| instruction_following | 76.17% | 2717.0 | 296 | 0 |
| student_level_calibration | 78.55% | 1797.0 | 221 | 0 |
| visual_reasoning | 78.67% | 382.0 | 57 | 0 |
| style_tone | 82.79% | 308.0 | 99 | 0 |
| emotional_component | 83.21% | 251.0 | 69 | 0 |
| visual_perception | 83.68% | 217.0 | 47 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Provides alternative solutions/ paths/ | 53.11% | 151.0 | 40 | 0 |
| Includes examples/ analogy | 56.44% | 115.0 | 40 | 0 |
| Asks questions to guide students | 62.46% | 348.0 | 58 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 71.13% | 952.0 | 137 | 1 |
| Step by step help/ analysis | 74.41% | 436.0 | 77 | 0 |
| Not applicable | 75.87% | 1220.0 | 238 | 0 |
| Identifying Core difficulty/ misconception attribution | 78.88% | 627.0 | 112 | 0 |
| Identifying incorrect steps by student | 79.69% | 530.0 | 74 | 0 |
| Identifying correct steps by student | 87.75% | 361.0 | 69 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 428 | 76.09% |
| chi-square variance-test adaptive explanation | 7 | 88.63% |
| recursive factorial assessment | 7 | 71.29% |
| OOP design / inventory class | 4 | 87.34% |
| binary-search midpoint overflow assessment | 3 | 83.02% |
| inclined box slip-or-tip assessment | 3 | 81.87% |
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
| archery target binomial-geometry explanation | 1 | 100.00% |
