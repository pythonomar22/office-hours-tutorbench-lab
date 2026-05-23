# TutorBench Run Analysis: `validation-failure-probe-v5-repair3-v2`

- Rows: 3
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 77.27%
- Mean generation latency: 118469 ms
- Mean judge latency: 2893 ms
- Generation input/output tokens: 99236 / 19105
- Judge input/output tokens: 7389 / 505
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
| `anthropic-ratelimit-tokens-remaining` | 2395000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `6843120a7996124c02b92b01` | 31.82% | assessment / text / Chemistry | 2 | 1 | weak-acid titration assessment |
| `681a876ab9d767de6644dc12` | 100.00% | assessment / text / Biology | 0 | 0 | start-codon insertion mutation assessment |
| `681cfdced476aa9b2b4633c7` | 100.00% | assessment / multimodal / Physics | 0 | 0 | crackle derivative assessment |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| truthfulness | 67.74% | 10.0 | 1 | 0 |
| student_level_calibration | 81.48% | 5.0 | 1 | 0 |
| conciseness_relevance | 100.00% | 0.0 | 0 | 0 |
| emotional_component | 100.00% | 0.0 | 0 | 0 |
| instruction_following | 100.00% | 0.0 | 1 | 1 |
| style_tone | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Identifying incorrect steps by student | 50.00% | 5.0 | 1 | 1 |
| Identifying Core difficulty/ misconception attribution | 66.67% | 5.0 | 1 | 0 |
| Identifying correct steps by student | 100.00% | 0.0 | 0 | 0 |
| Not applicable | 100.00% | 0.0 | 0 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 100.00% | 0.0 | 0 | 0 |
| Step by step help/ analysis | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| crackle derivative assessment | 1 | 100.00% |
| start-codon insertion mutation assessment | 1 | 100.00% |
| weak-acid titration assessment | 1 | 31.82% |
