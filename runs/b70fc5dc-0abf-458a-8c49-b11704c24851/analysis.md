# TutorBench Run Analysis: `b70fc5dc-0abf-458a-8c49-b11704c24851`

- Rows: 7
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 72.70%
- Mean generation latency: 97008 ms
- Mean judge latency: 3794 ms
- Generation input/output tokens: 185745 / 33999
- Judge input/output tokens: 13810 / 1814
- Negative-weight manual review rows: 1

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1996000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19999 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2396000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `683e45141eb8a249fd792b93` | 58.82% | assessment / multimodal / Biology | 7 | 0 | aerobic respiration assessment |
| `6843160a493da3d4b37fee61` | 62.96% | active_learning / text / Biology | 2 | 0 | Gene X methylation/tumor-suppressor active hint |
| `681cfd7b3c96c09201619a49` | 64.29% | adaptive / multimodal / Chemistry | 4 | 0 | weak-acid titration pKa adaptive explanation |
| `681cfb9f785e9bceace0e139` | 72.00% | adaptive / text / Physics | 3 | 0 | conical-pendulum adaptive explanation |
| `683776289fb2fd83d696cc90` | 73.91% | assessment / multimodal / Computer Science | 2 | 0 | binary-tree traversal reconstruction assessment |
| `6842a1fbbdfc0b0552b0553e` | 79.17% | adaptive / text / Physics | 1 | 0 | equilateral-triangle wire magnetic-field adaptive explanation |
| `683e45892667944fdee50634` | 97.73% | active_learning / multimodal / Biology | 1 | 0 | Arctic fox coat-color active-learning hint |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| visual_reasoning | 54.55% | 25.0 | 3 | 0 |
| conciseness_relevance | 58.33% | 5.0 | 1 | 0 |
| truthfulness | 65.57% | 21.0 | 2 | 0 |
| student_level_calibration | 66.91% | 46.0 | 5 | 0 |
| visual_perception | 68.75% | 5.0 | 1 | 0 |
| emotional_component | 75.00% | 6.0 | 2 | 0 |
| instruction_following | 79.82% | 22.0 | 6 | 0 |
| style_tone | 80.65% | 6.0 | 2 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Identifying Core difficulty/ misconception attribution | 50.00% | 20.0 | 2 | 0 |
| Identifying incorrect steps by student | 54.55% | 10.0 | 1 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 63.24% | 25.0 | 2 | 0 |
| Identifying correct steps by student | 66.67% | 10.0 | 2 | 0 |
| Not applicable | 80.82% | 14.0 | 5 | 0 |
| Asks questions to guide students | 85.71% | 5.0 | 1 | 0 |
| Includes examples/ analogy | 100.00% | 0.0 | 0 | 0 |
| Provides alternative solutions/ paths/ | 100.00% | 0.0 | 0 | 0 |
| Step by step help/ analysis | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| Arctic fox coat-color active-learning hint | 1 | 97.73% |
| Gene X methylation/tumor-suppressor active hint | 1 | 62.96% |
| aerobic respiration assessment | 1 | 58.82% |
| binary-tree traversal reconstruction assessment | 1 | 73.91% |
| conical-pendulum adaptive explanation | 1 | 72.00% |
| equilateral-triangle wire magnetic-field adaptive explanation | 1 | 79.17% |
| weak-acid titration pKa adaptive explanation | 1 | 64.29% |
