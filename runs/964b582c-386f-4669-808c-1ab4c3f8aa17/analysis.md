# TutorBench Run Analysis: `964b582c-386f-4669-808c-1ab4c3f8aa17`

- Rows: 1
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 79.17%
- Mean generation latency: 100982 ms
- Mean judge latency: 4389 ms
- Generation input/output tokens: 29212 / 5495
- Judge input/output tokens: 1714 / 204
- Negative-weight manual review rows: 0

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1997000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19999 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2396000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `6842a1fbbdfc0b0552b0553e` | 79.17% | adaptive / text / Physics | 1 | 0 | equilateral-triangle wire magnetic-field adaptive explanation |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| student_level_calibration | 50.00% | 5.0 | 1 | 0 |
| instruction_following | 72.22% | 5.0 | 1 | 0 |
| emotional_component | 100.00% | 0.0 | 0 | 0 |
| style_tone | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Stating definitions/ formulae/ theorems/ laws | 28.57% | 5.0 | 1 | 0 |
| Not applicable | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| equilateral-triangle wire magnetic-field adaptive explanation | 1 | 79.17% |
