# TutorBench Run Analysis: `heldout-failure-probe-v6-refined`

- Rows: 10
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 59.12%
- Mean generation latency: 117467 ms
- Mean judge latency: 4201 ms
- Generation input/output tokens: 445321 / 59884
- Judge input/output tokens: 38393 / 2618
- Negative-weight manual review rows: 5

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1989000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19999 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2388000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `6843120a2b986bd2d9ca5f3f` | 21.88% | assessment / text / Chemistry | 5 | 0 | weak-acid ICE-table assessment |
| `68376d91c5b329d497cbe8ca` | 24.39% | adaptive / multimodal / Computer Science | 6 | 1 | days-in-month switch adaptive explanation |
| `683e458c2e254199a0fa2e02` | 26.83% | active_learning / multimodal / Computer Science | 5 | 1 | geometric-shapes OOP center-distance active hint |
| `684a8cd6f08ce27c3bf577e0` | 44.44% | assessment / text / Chemistry | 5 | 0 | Henry-law mole-fraction assessment |
| `6843120a9fab58968f2128c9` | 54.55% | assessment / text / Chemistry | 0 | 1 | hydrogen iodide to iodoethylene assessment |
| `683e458eac89e71e0ce600c6` | 58.33% | active_learning / multimodal / Computer Science | 3 | 0 | MovieRating active-learning hint |
| `683e3d8f3482feddb4d05e86` | 78.72% | adaptive / multimodal / Physics | 2 | 0 | bulbs-in-parallel switch adaptive explanation |
| `683e4516d3bdf2dc57e053e3` | 90.38% | assessment / multimodal / Computer Science | 1 | 0 | binary-search midpoint overflow assessment |
| `683e4517a08f8bb261597839` | 93.42% | assessment / multimodal / Statistics | 1 | 0 | Normal MLE assessment |
| `683e45162d501a5ab198c520` | 98.21% | assessment / multimodal / Chemistry | 1 | 0 | Henry-law mole-fraction assessment |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| instruction_following | 55.26% | 85.0 | 8 | 2 |
| student_level_calibration | 59.72% | 85.0 | 5 | 1 |
| visual_reasoning | 66.67% | 25.0 | 2 | 0 |
| visual_perception | 72.73% | 15.0 | 4 | 1 |
| truthfulness | 88.51% | 10.0 | 1 | 0 |
| style_tone | 93.10% | 2.0 | 2 | 0 |
| emotional_component | 95.65% | 1.0 | 1 | 0 |
| conciseness_relevance | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Identifying incorrect steps by student | 50.00% | 60.0 | 3 | 0 |
| Step by step help/ analysis | 53.85% | 30.0 | 3 | 1 |
| Asks questions to guide students | 66.67% | 5.0 | 1 | 0 |
| Identifying Core difficulty/ misconception attribution | 69.23% | 20.0 | 4 | 0 |
| Identifying correct steps by student | 84.85% | 10.0 | 3 | 1 |
| Not applicable | 86.27% | 7.0 | 4 | 1 |
| Stating definitions/ formulae/ theorems/ laws | 90.00% | 5.0 | 1 | 0 |
| Includes examples/ analogy | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| Henry-law mole-fraction assessment | 2 | 71.33% |
| MovieRating active-learning hint | 1 | 58.33% |
| Normal MLE assessment | 1 | 93.42% |
| binary-search midpoint overflow assessment | 1 | 90.38% |
| bulbs-in-parallel switch adaptive explanation | 1 | 78.72% |
| days-in-month switch adaptive explanation | 1 | 24.39% |
| geometric-shapes OOP center-distance active hint | 1 | 26.83% |
| hydrogen iodide to iodoethylene assessment | 1 | 54.55% |
| weak-acid ICE-table assessment | 1 | 21.88% |
