# TutorBench Run Analysis: `validation150-router-gated-v2`

- Rows: 150
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 69.36%
- Mean generation latency: 87091 ms
- Mean judge latency: 3831 ms
- Generation input/output tokens: 3308896 / 641040
- Judge input/output tokens: 385987 / 37049
- Negative-weight manual review rows: 29

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1991000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19996 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2391000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `681cffc86183be99a10c4fdf` | 3.23% | active_learning / multimodal / Statistics | 12 | 0 | coffee-shop conditional-probability active hint |
| `68387054645e685361fd4ebd` | 4.55% | active_learning / multimodal / Computer Science | 10 | 0 | two's-complement negative-number active hint |
| `681a876ab9d767de6644dc12` | 16.67% | assessment / text / Biology | 3 | 0 | interphase mutation active-learning hint |
| `683e4516cb225e8f5aa693e1` | 17.86% | assessment / multimodal / Statistics | 7 | 0 | none |
| `68376d91a3ac2c2617743efe` | 26.67% | adaptive / multimodal / Calculus | 3 | 0 | radical derivative adaptive explanation |
| `683e458cb4f61c885835b5f8` | 30.43% | active_learning / multimodal / Statistics | 4 | 0 | two-proportion z-test active-learning hint |
| `6843120a7996124c02b92b01` | 31.82% | assessment / text / Chemistry | 2 | 1 | none |
| `681a872123b6cca56a90f246` | 33.33% | adaptive / text / Biology | 6 | 0 | none |
| `681cfc8cd66359ff7194ddb1` | 34.21% | assessment / text / Calculus | 5 | 0 | none |
| `681a876a23b6cca56a90f2a0` | 35.48% | assessment / text / Biology | 4 | 0 | interphase mutation active-learning hint |
| `684771b2de93ff93d7ba42c0` | 35.71% | assessment / text / Statistics | 7 | 0 | regression residual assessment |
| `681b80ddb17ff4fba2eec7e8` | 40.48% | adaptive / multimodal / Statistics | 5 | 0 | none |
| `683870ee806964a2566da1fd` | 41.18% | active_learning / text / Biology | 8 | 0 | none |
| `683e3d8e9394b13fefb08813` | 41.86% | adaptive / multimodal / Biology | 5 | 0 | none |
| `6843160bc6082b90c7d3518c` | 42.11% | active_learning / text / Biology | 6 | 0 | none |
| `683e3d8d2c6221565bb39630` | 42.86% | adaptive / multimodal / Biology | 4 | 0 | none |
| `683e458e8619d1d443f305be` | 43.24% | active_learning / multimodal / Biology | 5 | 0 | none |
| `68133830e566f93318db74d5` | 43.24% | active_learning / multimodal / Calculus | 5 | 0 | none |
| `681cfdced476aa9b2b4633c7` | 44.44% | assessment / multimodal / Physics | 3 | 0 | none |
| `683e45172d501a5ab198c53f` | 44.44% | assessment / multimodal / Physics | 4 | 0 | none |
| `683e451300c66429fabd7419` | 44.74% | assessment / multimodal / Biology | 5 | 0 | none |
| `683e458c98da7313814692b4` | 45.45% | active_learning / multimodal / Physics | 4 | 0 | none |
| `68376d91af9be190d433bd70` | 45.65% | adaptive / multimodal / Statistics | 5 | 0 | none |
| `683870eeb790747a1c2a3772` | 46.43% | active_learning / text / Calculus | 3 | 0 | none |
| `683775dc913c16d05cd33839` | 47.37% | adaptive / multimodal / Computer Science | 2 | 0 | none |
| `68387052d0567185c898a786` | 47.46% | active_learning / multimodal / Chemistry | 7 | 0 | none |
| `681cfb9f958a9ebd9b65f9ac` | 48.84% | adaptive / text / Calculus | 6 | 0 | none |
| `680fb68ef04842cb7d05cea7` | 50.00% | active_learning / text / Physics | 4 | 0 | none |
| `684a8c408708c5dec8f441d7` | 50.00% | adaptive / text / Chemistry | 6 | 0 | none |
| `6843120a0015fc211142f9cd` | 50.00% | assessment / text / Calculus | 5 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| conciseness_relevance | 43.08% | 37.0 | 13 | 0 |
| not applicable | 50.00% | 20.0 | 1 | 0 |
| truthfulness | 63.54% | 458.0 | 62 | 4 |
| visual_reasoning | 69.57% | 126.0 | 18 | 0 |
| student_level_calibration | 71.13% | 735.0 | 81 | 3 |
| instruction_following | 72.03% | 839.0 | 100 | 15 |
| style_tone | 74.15% | 144.0 | 36 | 1 |
| emotional_component | 74.19% | 120.0 | 27 | 1 |
| visual_perception | 78.93% | 71.0 | 17 | 1 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 25.68% | 55.0 | 19 | 0 |
| Step by step help/ analysis | 62.36% | 166.0 | 31 | 6 |
| Asks questions to guide students | 63.04% | 68.0 | 11 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 65.15% | 338.0 | 54 | 1 |
| Identifying Core difficulty/ misconception attribution | 70.09% | 242.0 | 45 | 0 |
| Provides alternative solutions/ paths/ | 71.62% | 21.0 | 6 | 1 |
| Not applicable | 71.84% | 428.0 | 90 | 10 |
| Identifying correct steps by student | 75.92% | 189.0 | 26 | 0 |
| Identifying incorrect steps by student | 77.13% | 188.0 | 33 | 3 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 129 | 71.16% |
| interphase mutation active-learning hint | 6 | 56.64% |
| OOP design / inventory class | 5 | 74.99% |
| CLT sample-mean active-learning hint | 2 | 100.00% |
| Gene X methylation/tumor-suppressor active hint | 1 | 83.78% |
| coffee-shop conditional-probability active hint | 1 | 3.23% |
| oxygen/CO2 cellular-respiration adaptive explanation | 1 | 57.69% |
| plant/animal cell diagram assessment | 1 | 67.74% |
| radical derivative adaptive explanation | 1 | 26.67% |
| regression residual assessment | 1 | 35.71% |
| two's-complement negative-number active hint | 1 | 4.55% |
| two-proportion z-test active-learning hint | 1 | 30.43% |
