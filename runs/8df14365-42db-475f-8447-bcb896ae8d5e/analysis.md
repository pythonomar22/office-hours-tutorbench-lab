# TutorBench Run Analysis: `8df14365-42db-475f-8447-bcb896ae8d5e`

- Rows: 7
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 90.50%
- Mean generation latency: 86339 ms
- Mean judge latency: 3944 ms
- Generation input/output tokens: 155610 / 29561
- Judge input/output tokens: 13800 / 1794
- Negative-weight manual review rows: 1

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1996000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19998 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2396000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `6842a1fbbdfc0b0552b0553e` | 54.17% | adaptive / text / Physics | 3 | 0 | equilateral-triangle wire magnetic-field adaptive explanation |
| `683e45141eb8a249fd792b93` | 88.24% | assessment / multimodal / Biology | 2 | 0 | aerobic respiration assessment |
| `681cfd7b3c96c09201619a49` | 91.07% | adaptive / multimodal / Chemistry | 1 | 0 | weak-acid titration pKa adaptive explanation |
| `681cfb9f785e9bceace0e139` | 100.00% | adaptive / text / Physics | 0 | 0 | conical-pendulum adaptive explanation |
| `6843160a493da3d4b37fee61` | 100.00% | active_learning / text / Biology | 0 | 0 | Gene X methylation/tumor-suppressor active hint |
| `683776289fb2fd83d696cc90` | 100.00% | assessment / multimodal / Computer Science | 0 | 0 | binary-tree traversal reconstruction assessment |
| `683e45892667944fdee50634` | 100.00% | active_learning / multimodal / Biology | 0 | 0 | Arctic fox coat-color active-learning hint |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| emotional_component | 79.17% | 5.0 | 1 | 0 |
| style_tone | 83.87% | 5.0 | 1 | 0 |
| instruction_following | 89.91% | 11.0 | 2 | 0 |
| visual_reasoning | 90.91% | 5.0 | 1 | 0 |
| truthfulness | 91.80% | 5.0 | 1 | 0 |
| student_level_calibration | 92.81% | 10.0 | 2 | 0 |
| conciseness_relevance | 100.00% | 0.0 | 0 | 0 |
| visual_perception | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Identifying incorrect steps by student | 77.27% | 5.0 | 1 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 77.94% | 15.0 | 2 | 0 |
| Not applicable | 91.78% | 6.0 | 1 | 0 |
| Asks questions to guide students | 100.00% | 0.0 | 0 | 0 |
| Identifying Core difficulty/ misconception attribution | 100.00% | 0.0 | 0 | 0 |
| Identifying correct steps by student | 100.00% | 0.0 | 0 | 0 |
| Includes examples/ analogy | 100.00% | 0.0 | 0 | 0 |
| Provides alternative solutions/ paths/ | 100.00% | 0.0 | 0 | 0 |
| Step by step help/ analysis | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| Arctic fox coat-color active-learning hint | 1 | 100.00% |
| Gene X methylation/tumor-suppressor active hint | 1 | 100.00% |
| aerobic respiration assessment | 1 | 88.24% |
| binary-tree traversal reconstruction assessment | 1 | 100.00% |
| conical-pendulum adaptive explanation | 1 | 100.00% |
| equilateral-triangle wire magnetic-field adaptive explanation | 1 | 54.17% |
| weak-acid titration pKa adaptive explanation | 1 | 91.07% |
