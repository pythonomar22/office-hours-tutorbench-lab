# TutorBench Run Analysis: `validation-failure-probe-v5-repair3-v3`

- Rows: 3
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 66.33%
- Mean generation latency: 119720 ms
- Mean judge latency: 3024 ms
- Generation input/output tokens: 98812 / 19173
- Judge input/output tokens: 7724 / 505
- Negative-weight manual review rows: 1

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1995000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19999 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2395000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `681cfdced476aa9b2b4633c7` | 44.44% | assessment / multimodal / Physics | 3 | 0 | crackle derivative assessment |
| `6843120a7996124c02b92b01` | 54.55% | assessment / text / Chemistry | 2 | 0 | weak-acid titration assessment |
| `681a876ab9d767de6644dc12` | 100.00% | assessment / text / Biology | 0 | 0 | start-codon insertion mutation assessment |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| instruction_following | 50.00% | 15.0 | 1 | 0 |
| truthfulness | 67.74% | 10.0 | 1 | 0 |
| student_level_calibration | 81.48% | 5.0 | 1 | 0 |
| conciseness_relevance | 100.00% | 0.0 | 0 | 0 |
| emotional_component | 100.00% | 0.0 | 0 | 0 |
| style_tone | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Step by step help/ analysis | 0.00% | 5.0 | 1 | 0 |
| Identifying correct steps by student | 28.57% | 5.0 | 1 | 0 |
| Identifying incorrect steps by student | 50.00% | 5.0 | 1 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 50.00% | 5.0 | 1 | 0 |
| Identifying Core difficulty/ misconception attribution | 66.67% | 5.0 | 1 | 0 |
| Not applicable | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| crackle derivative assessment | 1 | 44.44% |
| start-codon insertion mutation assessment | 1 | 100.00% |
| weak-acid titration assessment | 1 | 54.55% |
