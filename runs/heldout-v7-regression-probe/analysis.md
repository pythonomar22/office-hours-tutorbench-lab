# TutorBench Run Analysis: `heldout-v7-regression-probe`

- Rows: 10
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 67.43%
- Mean generation latency: 135569 ms
- Mean judge latency: 4942 ms
- Generation input/output tokens: 497006 / 69554
- Judge input/output tokens: 31426 / 2911
- Negative-weight manual review rows: 3

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1994000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19999 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2394000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `6843120a2b986bd2d9ca5f3f` | 21.88% | assessment / text / Chemistry | 5 | 0 | weak-acid ICE-table assessment |
| `68377588415e67c44f4734b6` | 27.27% | assessment / text / Physics | 4 | 0 | inclined box slip-or-tip assessment |
| `683e3d902b6d2a6c45002cec` | 38.46% | adaptive / multimodal / Calculus | 4 | 0 | piecewise graph nondifferentiability explanation |
| `684772095817461e60913ee8` | 65.28% | active_learning / text / Computer Science | 5 | 0 | none |
| `684a8cd69bca034aa640fe78` | 73.91% | assessment / text / Calculus | 2 | 0 | logarithmic improper-integral assessment |
| `681cffc846a1279c844e6432` | 80.77% | active_learning / multimodal / Biology | 2 | 0 | trihybrid ideal-peas active-learning hint |
| `6854554822969a049b1c9dc4` | 83.33% | assessment / text / Physics | 3 | 0 | inclined box slip-or-tip assessment |
| `683776272f4468651311d6dc` | 86.11% | assessment / multimodal / Calculus | 0 | 1 | composition constant-range assessment |
| `684771b3cf8ba842e93ec6de` | 97.30% | assessment / text / Computer Science | 1 | 0 | AP CSA MemberInfo removeMembers assessment |
| `683e4510bd7caf8a464501d6` | 100.00% | assessment / multimodal / Physics | 0 | 0 | towing-rope horizontal-components assessment |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| visual_reasoning | 47.62% | 11.0 | 1 | 0 |
| student_level_calibration | 57.03% | 55.0 | 5 | 0 |
| instruction_following | 70.09% | 70.0 | 8 | 1 |
| visual_perception | 76.19% | 5.0 | 1 | 0 |
| truthfulness | 78.23% | 27.0 | 4 | 0 |
| emotional_component | 93.33% | 1.0 | 1 | 0 |
| style_tone | 96.00% | 1.0 | 1 | 0 |
| conciseness_relevance | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Identifying incorrect steps by student | 58.82% | 35.0 | 5 | 1 |
| Identifying Core difficulty/ misconception attribution | 67.39% | 15.0 | 3 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 69.12% | 21.0 | 3 | 0 |
| Identifying correct steps by student | 77.08% | 11.0 | 3 | 0 |
| Step by step help/ analysis | 80.00% | 10.0 | 1 | 0 |
| Not applicable | 80.72% | 16.0 | 3 | 0 |
| Provides alternative solutions/ paths/ | 83.33% | 1.0 | 1 | 0 |
| Asks questions to guide students | 85.71% | 5.0 | 1 | 0 |
| Includes examples/ analogy | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| inclined box slip-or-tip assessment | 2 | 55.30% |
| AP CSA MemberInfo removeMembers assessment | 1 | 97.30% |
| composition constant-range assessment | 1 | 86.11% |
| logarithmic improper-integral assessment | 1 | 73.91% |
| none | 1 | 65.28% |
| piecewise graph nondifferentiability explanation | 1 | 38.46% |
| towing-rope horizontal-components assessment | 1 | 100.00% |
| trihybrid ideal-peas active-learning hint | 1 | 80.77% |
| weak-acid ICE-table assessment | 1 | 21.88% |
