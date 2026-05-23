# TutorBench Run Analysis: `heldout-v9-regression-probe`

- Rows: 12
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 91.86%
- Mean generation latency: 106177 ms
- Mean judge latency: 4719 ms
- Generation input/output tokens: 445949 / 60865
- Judge input/output tokens: 32150 / 3144
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
| `68477209c4915de7a58b3d02` | 62.26% | active_learning / text / Computer Science | 4 | 0 | none |
| `681a8721d276597945af81e7` | 71.43% | adaptive / text / Computer Science | 2 | 0 | OOP design / inventory class |
| `6814f360736eaea472ce9b26` | 86.49% | adaptive / multimodal / Computer Science | 1 | 0 | none |
| `681cffc846a1279c844e6432` | 90.38% | active_learning / multimodal / Biology | 1 | 0 | trihybrid ideal-peas active-learning hint |
| `68387053806964a2566da1b8` | 94.44% | active_learning / multimodal / Physics | 1 | 0 | tractor-airplane Newton's-law active hint |
| `684771b3cf8ba842e93ec6de` | 97.30% | assessment / text / Computer Science | 1 | 0 | AP CSA MemberInfo removeMembers assessment |
| `683775dc0a6dba7869a5c576` | 100.00% | adaptive / multimodal / Chemistry | 0 | 0 | chlorine PES / bromide binding-energy explanation |
| `683e45172a32fba415085acc` | 100.00% | assessment / multimodal / Biology | 0 | 0 | Hardy-Weinberg graph-reading assessment |
| `683e450e225c80e89ef01948` | 100.00% | assessment / multimodal / Physics | 0 | 0 | 12V 3-ohm series/parallel circuit assessment |
| `685454ee2187108ef9b08a95` | 100.00% | adaptive / text / Biology | 0 | 0 | meiosis-vs-mitosis gamete explanation |
| `683e4589a08f8bb26159787e` | 100.00% | active_learning / multimodal / Statistics | 0 | 0 | mean-CI z-vs-t active-learning hint |
| `683e4510bd7caf8a464501d6` | 100.00% | assessment / multimodal / Physics | 0 | 0 | towing-rope horizontal-components assessment |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| truthfulness | 85.09% | 17.0 | 4 | 0 |
| visual_perception | 86.11% | 5.0 | 1 | 0 |
| instruction_following | 93.33% | 16.0 | 3 | 0 |
| student_level_calibration | 99.26% | 1.0 | 1 | 0 |
| emotional_component | 100.00% | 0.0 | 0 | 0 |
| style_tone | 100.00% | 0.0 | 0 | 0 |
| visual_reasoning | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Stating definitions/ formulae/ theorems/ laws | 86.42% | 11.0 | 3 | 0 |
| Step by step help/ analysis | 87.80% | 5.0 | 1 | 0 |
| Identifying Core difficulty/ misconception attribution | 90.57% | 5.0 | 1 | 0 |
| Provides alternative solutions/ paths/ | 91.30% | 2.0 | 2 | 0 |
| Identifying incorrect steps by student | 92.31% | 5.0 | 1 | 0 |
| Identifying correct steps by student | 92.54% | 5.0 | 1 | 0 |
| Not applicable | 96.00% | 5.0 | 1 | 0 |
| Asks questions to guide students | 100.00% | 0.0 | 0 | 0 |
| Includes examples/ analogy | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 2 | 74.38% |
| 12V 3-ohm series/parallel circuit assessment | 1 | 100.00% |
| AP CSA MemberInfo removeMembers assessment | 1 | 97.30% |
| Hardy-Weinberg graph-reading assessment | 1 | 100.00% |
| OOP design / inventory class | 1 | 71.43% |
| chlorine PES / bromide binding-energy explanation | 1 | 100.00% |
| mean-CI z-vs-t active-learning hint | 1 | 100.00% |
| meiosis-vs-mitosis gamete explanation | 1 | 100.00% |
| towing-rope horizontal-components assessment | 1 | 100.00% |
| tractor-airplane Newton's-law active hint | 1 | 94.44% |
| trihybrid ideal-peas active-learning hint | 1 | 90.38% |
