# TutorBench Run Analysis: `heldout-failure-probe-v6`

- Rows: 10
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 64.42%
- Mean generation latency: 123666 ms
- Mean judge latency: 4880 ms
- Generation input/output tokens: 490161 / 63042
- Judge input/output tokens: 37982 / 2618
- Negative-weight manual review rows: 5

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1981000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19999 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2381000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `6843120a2b986bd2d9ca5f3f` | 6.25% | assessment / text / Chemistry | 6 | 0 | weak-acid ICE-table assessment |
| `68376d91c5b329d497cbe8ca` | 26.83% | adaptive / multimodal / Computer Science | 5 | 1 | days-in-month switch adaptive explanation |
| `683e458c2e254199a0fa2e02` | 51.22% | active_learning / multimodal / Computer Science | 3 | 1 | geometric-shapes OOP center-distance active hint |
| `6843120a9fab58968f2128c9` | 54.55% | assessment / text / Chemistry | 0 | 1 | hydrogen iodide to iodoethylene assessment |
| `684a8cd6f08ce27c3bf577e0` | 66.67% | assessment / text / Chemistry | 3 | 0 | Henry-law mole-fraction assessment |
| `683e3d8f3482feddb4d05e86` | 78.72% | adaptive / multimodal / Physics | 2 | 0 | bulbs-in-parallel switch adaptive explanation |
| `683e4517a08f8bb261597839` | 80.26% | assessment / multimodal / Statistics | 3 | 0 | Normal MLE assessment |
| `683e45162d501a5ab198c520` | 89.29% | assessment / multimodal / Chemistry | 1 | 1 | Henry-law mole-fraction assessment |
| `683e4516d3bdf2dc57e053e3` | 90.38% | assessment / multimodal / Computer Science | 1 | 0 | binary-search midpoint overflow assessment |
| `683e458eac89e71e0ce600c6` | 100.00% | active_learning / multimodal / Computer Science | 0 | 0 | MovieRating active-learning hint |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| visual_reasoning | 66.67% | 25.0 | 2 | 0 |
| instruction_following | 68.42% | 60.0 | 7 | 2 |
| student_level_calibration | 69.19% | 65.0 | 4 | 1 |
| visual_perception | 72.73% | 15.0 | 4 | 1 |
| truthfulness | 82.76% | 15.0 | 2 | 1 |
| emotional_component | 95.65% | 1.0 | 1 | 0 |
| style_tone | 96.55% | 1.0 | 1 | 0 |
| conciseness_relevance | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Identifying incorrect steps by student | 58.33% | 50.0 | 3 | 0 |
| Identifying Core difficulty/ misconception attribution | 69.23% | 20.0 | 4 | 0 |
| Step by step help/ analysis | 76.92% | 15.0 | 3 | 1 |
| Identifying correct steps by student | 77.27% | 15.0 | 4 | 1 |
| Stating definitions/ formulae/ theorems/ laws | 80.00% | 10.0 | 2 | 0 |
| Not applicable | 88.24% | 6.0 | 3 | 2 |
| Asks questions to guide students | 100.00% | 0.0 | 0 | 0 |
| Includes examples/ analogy | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| Henry-law mole-fraction assessment | 2 | 77.98% |
| MovieRating active-learning hint | 1 | 100.00% |
| Normal MLE assessment | 1 | 80.26% |
| binary-search midpoint overflow assessment | 1 | 90.38% |
| bulbs-in-parallel switch adaptive explanation | 1 | 78.72% |
| days-in-month switch adaptive explanation | 1 | 26.83% |
| geometric-shapes OOP center-distance active hint | 1 | 51.22% |
| hydrogen iodide to iodoethylene assessment | 1 | 54.55% |
| weak-acid ICE-table assessment | 1 | 6.25% |
