# TutorBench Run Analysis: `validation150-router-gated-delta`

- Rows: 23
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 65.00%
- Mean generation latency: 87215 ms
- Mean judge latency: 4719 ms
- Generation input/output tokens: 510636 / 97900
- Judge input/output tokens: 59742 / 5534
- Negative-weight manual review rows: 6

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1993000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19998 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2393000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `681a876ab9d767de6644dc12` | 16.67% | assessment / text / Biology | 3 | 0 | none |
| `683e458cb4f61c885835b5f8` | 30.43% | active_learning / multimodal / Statistics | 4 | 0 | two-proportion z-test active-learning hint |
| `681a876a23b6cca56a90f2a0` | 35.48% | assessment / text / Biology | 4 | 0 | none |
| `68377546cbb6263fa01c027b` | 49.02% | adaptive / text / Biology | 6 | 0 | none |
| `683e3d8e9394b13fefb08813` | 51.16% | adaptive / multimodal / Biology | 5 | 0 | none |
| `683775dc91fac7d3a4bdc866` | 52.00% | adaptive / multimodal / Biology | 4 | 0 | none |
| `681b80ddb17ff4fba2eec7e8` | 52.38% | adaptive / multimodal / Statistics | 4 | 0 | none |
| `683870523cf028f91cd74ad8` | 52.83% | active_learning / multimodal / Chemistry | 5 | 0 | none |
| `6843120a7996124c02b92b01` | 54.55% | assessment / text / Chemistry | 2 | 0 | none |
| `6847710a62247cf826ecc61b` | 57.14% | adaptive / text / Biology | 1 | 1 | none |
| `684a8cd62e4d9fec5e495e45` | 60.71% | assessment / text / Statistics | 2 | 1 | none |
| `68545549f20ebbefd00e2ce5` | 66.67% | assessment / text / Physics | 1 | 1 | none |
| `683628c73a003524f3d65e16` | 70.59% | adaptive / text / Statistics | 0 | 1 | none |
| `681cffc83d9f33c969b76c6f` | 70.59% | active_learning / multimodal / Physics | 2 | 0 | kinematics active-learning hint |
| `6847710bc4915de7a58b3cb5` | 71.05% | adaptive / text / Biology | 3 | 0 | none |
| `683775dc913c16d05cd33839` | 73.68% | adaptive / multimodal / Computer Science | 1 | 0 | none |
| `68376de0afc2cf08ab22a52e` | 75.81% | assessment / multimodal / Biology | 3 | 0 | plant/animal cell diagram assessment |
| `683e458a9c195766bfe397d3` | 84.13% | active_learning / multimodal / Computer Science | 2 | 0 | none |
| `68387051925f37fe4fe43927` | 85.29% | active_learning / multimodal / Computer Science | 1 | 0 | OOP design / inventory class |
| `68377627c130b33e3079a99e` | 91.18% | assessment / multimodal / Computer Science | 1 | 1 | OOP design / inventory class |
| `683870ee7ae15972ddd10cf9` | 95.65% | active_learning / text / Chemistry | 1 | 0 | none |
| `68545548e6d053a2b0278006` | 97.87% | assessment / text / Statistics | 1 | 0 | none |
| `684a8c40a8da4aded13ef54a` | 100.00% | adaptive / text / Statistics | 0 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| conciseness_relevance | 40.00% | 3.0 | 3 | 0 |
| emotional_component | 61.82% | 21.0 | 5 | 0 |
| truthfulness | 66.07% | 57.0 | 11 | 2 |
| instruction_following | 69.60% | 138.0 | 17 | 3 |
| visual_reasoning | 71.70% | 15.0 | 3 | 0 |
| student_level_calibration | 74.03% | 87.0 | 13 | 1 |
| style_tone | 74.67% | 19.0 | 7 | 0 |
| visual_perception | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Stating definitions/ formulae/ theorems/ laws | 54.84% | 70.0 | 10 | 0 |
| Identifying Core difficulty/ misconception attribution | 64.57% | 62.0 | 10 | 0 |
| Includes examples/ analogy | 72.73% | 3.0 | 3 | 0 |
| Not applicable | 73.27% | 54.0 | 14 | 4 |
| Identifying correct steps by student | 73.33% | 20.0 | 3 | 0 |
| Asks questions to guide students | 80.65% | 6.0 | 2 | 0 |
| Identifying incorrect steps by student | 82.22% | 16.0 | 3 | 0 |
| Provides alternative solutions/ paths/ | 91.67% | 1.0 | 1 | 0 |
| Step by step help/ analysis | 100.00% | 0.0 | 1 | 1 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 18 | 63.42% |
| OOP design / inventory class | 2 | 88.24% |
| kinematics active-learning hint | 1 | 70.59% |
| plant/animal cell diagram assessment | 1 | 75.81% |
| two-proportion z-test active-learning hint | 1 | 30.43% |
