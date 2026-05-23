# TutorBench Run Analysis: `probe10-agentic-v4-refined`

- Rows: 10
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 75.33%
- Mean generation latency: 115354 ms
- Mean judge latency: 3908 ms
- Generation input/output tokens: 384203 / 62691
- Judge input/output tokens: 31619 / 2498
- Negative-weight manual review rows: 3

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1994000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19998 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2394000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `68377588415e67c44f4734b6` | 4.55% | assessment / text / Physics | 4 | 1 | none |
| `6843120a2b986bd2d9ca5f3f` | 37.50% | assessment / text / Chemistry | 4 | 0 | weak-acid ICE-table assessment |
| `683e458f8103655aef73fd55` | 80.70% | active_learning / multimodal / Chemistry | 3 | 0 | copper/KMnO4 redox active-learning hint |
| `684a8cd60f2d31d3b4e0979f` | 81.82% | assessment / text / Statistics | 2 | 0 | z-test vs t-test assessment |
| `6810216fbe57055e015742ec` | 81.82% | assessment / multimodal / Statistics | 2 | 0 | trig accumulation probability assessment |
| `683e3d905f104dac1d4d66cc` | 84.38% | adaptive / multimodal / Biology | 1 | 0 | photosynthesis sunlight adaptive explanation |
| `681b9468c537a889cd24aac7` | 88.10% | active_learning / multimodal / Calculus | 1 | 0 | parametric arc-length active-learning hint |
| `681a8721b07ca4da41ff1d4e` | 94.44% | adaptive / text / Statistics | 2 | 0 | electricity-rates two-sample CI adaptive explanation |
| `681904ae013a6ffe335931b0` | 100.00% | adaptive / text / Chemistry | 0 | 0 | U-238/Pb-206 mass-ratio adaptive explanation |
| `683e45172d5e3eede3bfbe03` | 100.00% | assessment / multimodal / Chemistry | 0 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| truthfulness | 72.73% | 27.0 | 3 | 0 |
| visual_perception | 80.00% | 5.0 | 1 | 0 |
| student_level_calibration | 80.11% | 37.0 | 5 | 0 |
| instruction_following | 80.71% | 38.0 | 7 | 1 |
| emotional_component | 94.12% | 1.0 | 1 | 0 |
| style_tone | 94.74% | 1.0 | 1 | 0 |
| conciseness_relevance | 100.00% | 0.0 | 0 | 0 |
| visual_reasoning | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 0.00% | 1.0 | 1 | 0 |
| Identifying Core difficulty/ misconception attribution | 67.74% | 10.0 | 2 | 0 |
| Identifying incorrect steps by student | 68.63% | 16.0 | 3 | 0 |
| Step by step help/ analysis | 76.09% | 11.0 | 1 | 0 |
| Not applicable | 84.72% | 11.0 | 3 | 1 |
| Identifying correct steps by student | 85.98% | 15.0 | 3 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 88.89% | 7.0 | 3 | 0 |
| Asks questions to guide students | 100.00% | 0.0 | 0 | 0 |
| Provides alternative solutions/ paths/ | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 2 | 52.27% |
| U-238/Pb-206 mass-ratio adaptive explanation | 1 | 100.00% |
| copper/KMnO4 redox active-learning hint | 1 | 80.70% |
| electricity-rates two-sample CI adaptive explanation | 1 | 94.44% |
| parametric arc-length active-learning hint | 1 | 88.10% |
| photosynthesis sunlight adaptive explanation | 1 | 84.38% |
| trig accumulation probability assessment | 1 | 81.82% |
| weak-acid ICE-table assessment | 1 | 37.50% |
| z-test vs t-test assessment | 1 | 81.82% |
