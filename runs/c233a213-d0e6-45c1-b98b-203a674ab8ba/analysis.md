# TutorBench Run Analysis: `c233a213-d0e6-45c1-b98b-203a674ab8ba`

- Rows: 3
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 86.48%
- Mean generation latency: 99626 ms
- Mean judge latency: 4517 ms
- Generation input/output tokens: 79761 / 15011
- Judge input/output tokens: 6538 / 750
- Negative-weight manual review rows: 0

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
| `683e45143a109788e3f7e591` | 83.33% | assessment / multimodal / Statistics | 2 | 0 | z-test vs t-test assessment |
| `6842a1fb5ca82eb2207af64b` | 85.71% | adaptive / text / Biology | 2 | 0 | oxygen/CO2 cellular-respiration adaptive explanation |
| `683e3d8d2b6d2a6c45002caa` | 90.38% | adaptive / multimodal / Chemistry | 1 | 0 | alkylbenzene sulphonation hyperconjugation explanation |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| visual_reasoning | 75.00% | 5.0 | 1 | 0 |
| instruction_following | 82.46% | 10.0 | 2 | 0 |
| student_level_calibration | 90.91% | 5.0 | 1 | 0 |
| emotional_component | 90.91% | 1.0 | 1 | 0 |
| style_tone | 90.91% | 1.0 | 1 | 0 |
| truthfulness | 96.30% | 1.0 | 1 | 0 |
| visual_perception | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Identifying correct steps by student | 75.00% | 5.0 | 1 | 0 |
| Identifying Core difficulty/ misconception attribution | 76.19% | 5.0 | 1 | 0 |
| Not applicable | 83.33% | 6.0 | 2 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 95.65% | 1.0 | 1 | 0 |
| Identifying incorrect steps by student | 100.00% | 0.0 | 0 | 0 |
| Includes examples/ analogy | 100.00% | 0.0 | 0 | 0 |
| Step by step help/ analysis | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| alkylbenzene sulphonation hyperconjugation explanation | 1 | 90.38% |
| oxygen/CO2 cellular-respiration adaptive explanation | 1 | 85.71% |
| z-test vs t-test assessment | 1 | 83.33% |
