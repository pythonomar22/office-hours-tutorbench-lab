# TutorBench Run Analysis: `08e7707a-e7ee-4a4f-a608-63aea18b29a1`

- Rows: 150
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 69.44%
- Mean generation latency: 86132 ms
- Mean judge latency: 3932 ms
- Generation input/output tokens: 3320113 / 643054
- Judge input/output tokens: 383820 / 37094
- Negative-weight manual review rows: 29

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1992000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19997 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2392000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `68377546cbb6263fa01c027b` | 0.00% | adaptive / text / Biology | 11 | 0 | Gene X methylation/tumor-suppressor active hint |
| `683775dc913c16d05cd33839` | 0.00% | adaptive / multimodal / Computer Science | 7 | 0 | recursive factorial assessment |
| `683e3d8e9394b13fefb08813` | 0.00% | adaptive / multimodal / Biology | 11 | 0 | Gene X methylation/tumor-suppressor active hint |
| `681cffc86183be99a10c4fdf` | 3.23% | active_learning / multimodal / Statistics | 12 | 0 | coffee-shop conditional-probability active hint |
| `6843120a7996124c02b92b01` | 4.55% | assessment / text / Chemistry | 5 | 0 | weak-acid titration pKa adaptive explanation |
| `68387053482dac7a5c572262` | 16.67% | active_learning / multimodal / Biology | 4 | 0 | none |
| `683e4516cb225e8f5aa693e1` | 17.86% | assessment / multimodal / Statistics | 7 | 0 | none |
| `68376d91a3ac2c2617743efe` | 20.00% | adaptive / multimodal / Calculus | 4 | 0 | radical derivative adaptive explanation |
| `684771b2de93ff93d7ba42c0` | 26.19% | assessment / text / Statistics | 7 | 0 | regression residual assessment |
| `683e458cb4f61c885835b5f8` | 30.43% | active_learning / multimodal / Statistics | 4 | 0 | two-proportion z-test active-learning hint |
| `683e3d8f5f104dac1d4d66ac` | 31.82% | adaptive / multimodal / Chemistry | 3 | 0 | none |
| `684a8c408708c5dec8f441d7` | 36.36% | adaptive / text / Chemistry | 8 | 0 | none |
| `683e3d8f9394b13fefb08833` | 38.89% | adaptive / multimodal / Physics | 3 | 0 | none |
| `68387052d0567185c898a786` | 38.98% | active_learning / multimodal / Chemistry | 8 | 0 | none |
| `681b80ddb17ff4fba2eec7e8` | 40.48% | adaptive / multimodal / Statistics | 5 | 0 | CLT sample-mean active-learning hint |
| `683e458e8619d1d443f305be` | 43.24% | active_learning / multimodal / Biology | 5 | 0 | none |
| `681cfdced476aa9b2b4633c7` | 44.44% | assessment / multimodal / Physics | 3 | 0 | none |
| `681a872123b6cca56a90f246` | 44.44% | adaptive / text / Biology | 5 | 0 | none |
| `683e45172d501a5ab198c53f` | 44.44% | assessment / multimodal / Physics | 4 | 0 | none |
| `683e451300c66429fabd7419` | 44.74% | assessment / multimodal / Biology | 5 | 0 | none |
| `684a8c40a8da4aded13ef54a` | 45.45% | adaptive / text / Statistics | 2 | 0 | z-test vs t-test assessment |
| `683870537ae15972ddd10cb4` | 46.43% | active_learning / multimodal / Computer Science | 2 | 1 | none |
| `6842a1fbba6af9cb6614fe61` | 47.37% | adaptive / text / Calculus | 4 | 0 | none |
| `681cfc8cd66359ff7194ddb1` | 47.37% | assessment / text / Calculus | 4 | 0 | none |
| `6843160bc6082b90c7d3518c` | 47.37% | active_learning / text / Biology | 4 | 0 | none |
| `683e3d8d2c6221565bb39630` | 47.62% | adaptive / multimodal / Biology | 3 | 0 | none |
| `683775dc91fac7d3a4bdc866` | 48.00% | adaptive / multimodal / Biology | 5 | 0 | interphase mutation active-learning hint |
| `685454ee2ae3f8515f9eaea4` | 48.84% | adaptive / text / Chemistry | 6 | 0 | none |
| `680fb68ef04842cb7d05cea7` | 50.00% | active_learning / text / Physics | 4 | 0 | none |
| `683775dc496507faa0915cb4` | 50.00% | adaptive / multimodal / Calculus | 4 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| not applicable | 50.00% | 20.0 | 1 | 0 |
| conciseness_relevance | 52.31% | 31.0 | 11 | 0 |
| truthfulness | 64.73% | 443.0 | 57 | 4 |
| instruction_following | 71.03% | 869.0 | 100 | 13 |
| student_level_calibration | 71.76% | 719.0 | 85 | 3 |
| emotional_component | 74.41% | 119.0 | 27 | 1 |
| style_tone | 74.51% | 142.0 | 34 | 1 |
| visual_reasoning | 78.26% | 90.0 | 15 | 0 |
| visual_perception | 84.57% | 52.0 | 14 | 1 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 18.92% | 60.0 | 19 | 0 |
| Asks questions to guide students | 60.33% | 73.0 | 10 | 0 |
| Provides alternative solutions/ paths/ | 62.16% | 28.0 | 9 | 1 |
| Step by step help/ analysis | 66.89% | 146.0 | 30 | 6 |
| Stating definitions/ formulae/ theorems/ laws | 68.87% | 302.0 | 47 | 1 |
| Identifying Core difficulty/ misconception attribution | 69.34% | 248.0 | 44 | 0 |
| Not applicable | 71.25% | 437.0 | 84 | 9 |
| Identifying incorrect steps by student | 76.52% | 193.0 | 33 | 2 |
| Identifying correct steps by student | 79.62% | 160.0 | 25 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 117 | 72.47% |
| CLT sample-mean active-learning hint | 6 | 78.93% |
| interphase mutation active-learning hint | 6 | 74.49% |
| OOP design / inventory class | 4 | 76.12% |
| Gene X methylation/tumor-suppressor active hint | 3 | 27.93% |
| hydrogen halide acid strength | 2 | 76.78% |
| kinematics active-learning hint | 2 | 83.33% |
| recursive factorial assessment | 2 | 34.13% |
| coffee-shop conditional-probability active hint | 1 | 3.23% |
| oxygen/CO2 cellular-respiration adaptive explanation | 1 | 57.69% |
| plant/animal cell diagram assessment | 1 | 51.61% |
| radical derivative adaptive explanation | 1 | 20.00% |
| regression residual assessment | 1 | 26.19% |
| two-proportion z-test active-learning hint | 1 | 30.43% |
| weak-acid titration pKa adaptive explanation | 1 | 4.55% |
| z-test vs t-test assessment | 1 | 45.45% |
