# TutorBench Run Analysis: `heldout-v8-regression-probe`

- Rows: 12
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 75.85%
- Mean generation latency: 107576 ms
- Mean judge latency: 4164 ms
- Generation input/output tokens: 483127 / 60883
- Judge input/output tokens: 31843 / 3154
- Negative-weight manual review rows: 0

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
| `683e450e225c80e89ef01948` | 36.89% | assessment / multimodal / Physics | 13 | 0 | none |
| `685454ee2187108ef9b08a95` | 50.00% | adaptive / text / Biology | 3 | 0 | none |
| `68477209c4915de7a58b3d02` | 52.83% | active_learning / text / Computer Science | 5 | 0 | none |
| `681a8721d276597945af81e7` | 71.43% | adaptive / text / Computer Science | 2 | 0 | OOP design / inventory class |
| `683e4510bd7caf8a464501d6` | 72.97% | assessment / multimodal / Physics | 2 | 0 | towing-rope horizontal-components assessment |
| `683e4589a08f8bb26159787e` | 79.31% | active_learning / multimodal / Statistics | 2 | 0 | none |
| `681cffc846a1279c844e6432` | 80.77% | active_learning / multimodal / Biology | 2 | 0 | trihybrid ideal-peas active-learning hint |
| `6814f360736eaea472ce9b26` | 86.49% | adaptive / multimodal / Computer Science | 1 | 0 | none |
| `683775dc0a6dba7869a5c576` | 87.80% | adaptive / multimodal / Chemistry | 1 | 0 | chlorine PES / bromide binding-energy explanation |
| `68387053806964a2566da1b8` | 94.44% | active_learning / multimodal / Physics | 1 | 0 | tractor-airplane Newton's-law active hint |
| `684771b3cf8ba842e93ec6de` | 97.30% | assessment / text / Computer Science | 1 | 0 | AP CSA MemberInfo removeMembers assessment |
| `683e45172a32fba415085acc` | 100.00% | assessment / multimodal / Biology | 0 | 0 | Hardy-Weinberg graph-reading assessment |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| truthfulness | 54.39% | 52.0 | 6 | 0 |
| visual_reasoning | 65.69% | 35.0 | 1 | 0 |
| instruction_following | 77.92% | 53.0 | 8 | 0 |
| visual_perception | 86.11% | 5.0 | 1 | 0 |
| student_level_calibration | 90.37% | 13.0 | 4 | 0 |
| emotional_component | 100.00% | 0.0 | 0 | 0 |
| style_tone | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Step by step help/ analysis | 36.59% | 26.0 | 3 | 0 |
| Includes examples/ analogy | 50.00% | 5.0 | 1 | 0 |
| Identifying correct steps by student | 55.22% | 30.0 | 2 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 74.07% | 21.0 | 4 | 0 |
| Not applicable | 76.00% | 30.0 | 5 | 0 |
| Identifying Core difficulty/ misconception attribution | 79.25% | 11.0 | 2 | 0 |
| Asks questions to guide students | 80.39% | 10.0 | 2 | 0 |
| Identifying incorrect steps by student | 84.62% | 10.0 | 2 | 0 |
| Provides alternative solutions/ paths/ | 91.30% | 2.0 | 2 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 5 | 61.10% |
| AP CSA MemberInfo removeMembers assessment | 1 | 97.30% |
| Hardy-Weinberg graph-reading assessment | 1 | 100.00% |
| OOP design / inventory class | 1 | 71.43% |
| chlorine PES / bromide binding-energy explanation | 1 | 87.80% |
| towing-rope horizontal-components assessment | 1 | 72.97% |
| tractor-airplane Newton's-law active hint | 1 | 94.44% |
| trihybrid ideal-peas active-learning hint | 1 | 80.77% |
