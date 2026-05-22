# TutorBench Run Analysis: `heldout500-agentic-v3`

- Rows: 500
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 68.23%
- Mean generation latency: 86957 ms
- Mean judge latency: 3780 ms
- Generation input/output tokens: 11240063 / 2146122
- Judge input/output tokens: 1318368 / 127513
- Negative-weight manual review rows: 47

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1986000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19998 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2386000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `684a8cd60f2d31d3b4e0979f` | 0.00% | assessment / text / Statistics | 9 | 0 | z-test vs t-test assessment |
| `683e45172d5e3eede3bfbe03` | 0.00% | assessment / multimodal / Chemistry | 14 | 0 | H2/O2 water limiting-reagent visual assessment |
| `681b9468c537a889cd24aac7` | 2.38% | active_learning / multimodal / Calculus | 9 | 0 | arc-length perimeter active-learning hint |
| `681904ae013a6ffe335931b0` | 2.44% | adaptive / text / Chemistry | 8 | 0 | none |
| `683e3d905f104dac1d4d66cc` | 3.12% | adaptive / multimodal / Biology | 7 | 0 | oxygen/CO2 cellular-respiration adaptive explanation |
| `68377588415e67c44f4734b6` | 4.55% | assessment / text / Physics | 4 | 1 | none |
| `6810216fbe57055e015742ec` | 6.06% | assessment / multimodal / Statistics | 7 | 0 | none |
| `6843120a2b986bd2d9ca5f3f` | 6.25% | assessment / text / Chemistry | 6 | 0 | none |
| `684772099a6b1451d91de1bd` | 6.90% | active_learning / text / Calculus | 7 | 0 | arc-length perimeter active-learning hint |
| `681a8721b07ca4da41ff1d4e` | 8.33% | adaptive / text / Statistics | 9 | 0 | none |
| `6843120a9fab58968f2128c9` | 9.09% | assessment / text / Chemistry | 1 | 1 | none |
| `683e458f8103655aef73fd55` | 10.53% | active_learning / multimodal / Chemistry | 11 | 0 | none |
| `683e450e225c80e89ef01948` | 12.62% | assessment / multimodal / Physics | 18 | 0 | none |
| `683e4516d3bdf2dc57e053e3` | 13.46% | assessment / multimodal / Computer Science | 9 | 0 | OOP design / inventory class |
| `683e458c2e254199a0fa2e02` | 14.63% | active_learning / multimodal / Computer Science | 6 | 1 | OOP design / inventory class |
| `68376d91c5b329d497cbe8ca` | 14.63% | adaptive / multimodal / Computer Science | 6 | 1 | none |
| `6847710b9bc321f32d5b5ab8` | 15.79% | adaptive / text / Calculus | 8 | 0 | radical derivative adaptive explanation |
| `681cfc8cb4e0809f6fae0767` | 16.22% | assessment / text / Calculus | 7 | 0 | sinc integral/removable discontinuity assessment |
| `683776272f4468651311d6dc` | 16.67% | assessment / multimodal / Calculus | 5 | 1 | none |
| `683e45162d501a5ab198c520` | 17.86% | assessment / multimodal / Chemistry | 10 | 0 | none |
| `6843120af2decb7f190ec363` | 18.75% | assessment / text / Calculus | 6 | 0 | sinc integral/removable discontinuity assessment |
| `6838705313dd25f48fb17dfa` | 18.92% | active_learning / multimodal / Calculus | 6 | 0 | arc-length perimeter active-learning hint |
| `683e4510bd7caf8a464501d6` | 18.92% | assessment / multimodal / Physics | 6 | 0 | none |
| `6842a1fbb8f271121fd79472` | 20.00% | adaptive / text / Statistics | 4 | 0 | none |
| `6811d40e6b7f984ce18baebb` | 20.69% | adaptive / multimodal / Computer Science | 7 | 0 | none |
| `683e3d9065e18627c7388002` | 21.05% | adaptive / multimodal / Chemistry | 6 | 0 | none |
| `683e4518b4f61c885835b57d` | 21.05% | assessment / multimodal / Chemistry | 12 | 0 | none |
| `6843160a0015fc211142fa11` | 21.15% | active_learning / text / Computer Science | 9 | 0 | none |
| `681cfb9fdbed21a8e4bde8fa` | 21.21% | adaptive / text / Calculus | 5 | 1 | none |
| `683e45163a967938ab5f5e20` | 21.43% | assessment / multimodal / Chemistry | 11 | 0 | second ionization energy assessment |
| `6847710ac4590722c4324810` | 23.08% | adaptive / text / Physics | 4 | 0 | none |
| `68377545cbb6263fa01c0268` | 25.00% | adaptive / text / Calculus | 2 | 1 | radical derivative adaptive explanation |
| `6847720874c7f1cb6eb0b1d5` | 25.37% | active_learning / text / Computer Science | 10 | 0 | none |
| `68096a17d9108896c270f6b6` | 25.93% | adaptive / text / Physics | 4 | 0 | none |
| `683e45109394b13fefb08e44` | 26.09% | assessment / multimodal / Physics | 5 | 0 | none |
| `6843120a2e9311de43e068f9` | 26.23% | assessment / text / Chemistry | 8 | 1 | none |
| `683775dc0a6dba7869a5c576` | 26.83% | adaptive / multimodal / Chemistry | 6 | 0 | none |
| `683775dc2f4468651311d6ad` | 26.83% | adaptive / multimodal / Chemistry | 6 | 0 | none |
| `681b84ff94969ef6e11908e0` | 27.42% | assessment / multimodal / Physics | 9 | 0 | none |
| `683e458c5f104dac1d4d6e7a` | 28.30% | active_learning / multimodal / Biology | 10 | 0 | none |
| `6836292325d9d55d0df0462c` | 28.57% | assessment / text / Calculus | 4 | 0 | none |
| `683e458d2a32fba415085b4c` | 28.57% | active_learning / multimodal / Statistics | 4 | 0 | none |
| `685454ef513ee4759d9bd93a` | 28.57% | adaptive / text / Physics | 4 | 0 | none |
| `683e451765e18627c73884df` | 28.57% | assessment / multimodal / Physics | 3 | 0 | none |
| `681cfcca41f2915eaf79891b` | 29.31% | active_learning / text / Statistics | 9 | 0 | penicillin allergy Bayes active-learning hint |
| `68376de04d48dbcf9aa0d0b3` | 29.55% | assessment / multimodal / Computer Science | 7 | 0 | recursive factorial assessment |
| `683e45108103655aef73fc0f` | 29.82% | assessment / multimodal / Statistics | 8 | 0 | none |
| `681cfb9f423b8a534abc79ba` | 30.23% | adaptive / text / Biology | 6 | 0 | none |
| `683870ef328fdda5d51a6203` | 30.23% | active_learning / text / Statistics | 6 | 0 | none |
| `68545549f8ab7067dd48b799` | 31.82% | assessment / text / Physics | 1 | 2 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| not applicable | 50.00% | 1.0 | 1 | 0 |
| truthfulness | 63.58% | 1290.0 | 166 | 4 |
| visual_reasoning | 65.81% | 609.0 | 82 | 2 |
| conciseness_relevance | 67.50% | 65.0 | 31 | 0 |
| instruction_following | 67.83% | 3615.0 | 341 | 28 |
| student_level_calibration | 71.11% | 2403.0 | 269 | 10 |
| visual_perception | 75.80% | 317.0 | 61 | 3 |
| emotional_component | 78.32% | 323.0 | 88 | 1 |
| style_tone | 79.42% | 368.0 | 119 | 2 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Provides alternative solutions/ paths/ | 45.71% | 171.0 | 45 | 3 |
| Asks questions to guide students | 48.87% | 474.0 | 71 | 0 |
| Includes examples/ analogy | 54.92% | 119.0 | 40 | 0 |
| Step by step help/ analysis | 64.78% | 586.0 | 99 | 7 |
| Stating definitions/ formulae/ theorems/ laws | 64.99% | 1156.0 | 159 | 0 |
| Identifying incorrect steps by student | 69.62% | 782.0 | 107 | 6 |
| Not applicable | 69.86% | 1487.0 | 280 | 20 |
| Identifying Core difficulty/ misconception attribution | 71.09% | 857.0 | 146 | 0 |
| Identifying correct steps by student | 78.21% | 638.0 | 96 | 3 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 408 | 69.67% |
| OOP design / inventory class | 35 | 69.82% |
| interphase mutation active-learning hint | 21 | 72.07% |
| radical derivative adaptive explanation | 13 | 56.49% |
| recursive factorial assessment | 6 | 70.30% |
| arc-length perimeter active-learning hint | 3 | 9.40% |
| ellipse rectangle explanation | 3 | 79.48% |
| sinc integral/removable discontinuity assessment | 2 | 17.48% |
| CLT sample-mean active-learning hint | 1 | 60.71% |
| Gene X methylation/tumor-suppressor active hint | 1 | 57.45% |
| H2/O2 water limiting-reagent visual assessment | 1 | 0.00% |
| hydrogen halide acid strength | 1 | 57.89% |
| kinematics active-learning hint | 1 | 40.48% |
| oxygen/CO2 cellular-respiration adaptive explanation | 1 | 3.12% |
| penicillin allergy Bayes active-learning hint | 1 | 29.31% |
| second ionization energy assessment | 1 | 21.43% |
| z-test vs t-test assessment | 1 | 0.00% |
