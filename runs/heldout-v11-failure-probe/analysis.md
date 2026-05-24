# TutorBench Run Analysis: `heldout-v11-failure-probe`

- Rows: 10
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 74.75%
- Mean generation latency: 131521 ms
- Mean judge latency: 4424 ms
- Generation input/output tokens: 507660 / 68146
- Judge input/output tokens: 34009 / 2567
- Negative-weight manual review rows: 3

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1993000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19998 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2393000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `683e45109394b13fefb08e44` | 26.09% | assessment / multimodal / Physics | 5 | 0 | none |
| `6811d40e6b7f984ce18baebb` | 41.38% | adaptive / multimodal / Computer Science | 5 | 0 | bakery flour check adaptive explanation |
| `68377588415e67c44f4734b6` | 50.00% | assessment / text / Physics | 2 | 1 | inclined box slip-or-tip assessment |
| `683e3d8fa08f8bb26159720b` | 70.59% | adaptive / multimodal / Statistics | 5 | 0 | chi-square variance-test adaptive explanation |
| `68097912014bb68a4c65e4a1` | 83.61% | assessment / text / Biology | 2 | 0 | nonstandard tRNA translation assessment |
| `683776272f4468651311d6dc` | 86.11% | assessment / multimodal / Calculus | 0 | 1 | composition constant-range assessment |
| `681b84ff94969ef6e11908e0` | 91.94% | assessment / multimodal / Physics | 1 | 0 | series/parallel circuit assessment |
| `683e3d8d9394b13fefb087f2` | 97.78% | adaptive / multimodal / Statistics | 1 | 0 | archery target binomial-geometry explanation |
| `6847710ac4590722c4324810` | 100.00% | adaptive / text / Physics | 0 | 0 | chocolate-orb heat-pulse assumption explanation |
| `68477209e96863adfe492508` | 100.00% | active_learning / text / Calculus | 0 | 0 | implicit tangent-line active hint |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| visual_perception | 68.18% | 7.0 | 3 | 0 |
| visual_reasoning | 73.91% | 12.0 | 3 | 0 |
| instruction_following | 82.41% | 38.0 | 8 | 2 |
| conciseness_relevance | 85.71% | 1.0 | 1 | 0 |
| student_level_calibration | 87.50% | 15.0 | 4 | 0 |
| truthfulness | 91.18% | 3.0 | 2 | 0 |
| emotional_component | 100.00% | 0.0 | 0 | 0 |
| style_tone | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 16.67% | 5.0 | 1 | 0 |
| Identifying correct steps by student | 77.61% | 15.0 | 2 | 0 |
| Identifying Core difficulty/ misconception attribution | 77.78% | 6.0 | 2 | 0 |
| Not applicable | 80.87% | 22.0 | 5 | 1 |
| Stating definitions/ formulae/ theorems/ laws | 85.00% | 6.0 | 4 | 0 |
| Step by step help/ analysis | 86.54% | 7.0 | 3 | 0 |
| Identifying incorrect steps by student | 100.00% | 0.0 | 1 | 1 |
| Provides alternative solutions/ paths/ | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| archery target binomial-geometry explanation | 1 | 97.78% |
| bakery flour check adaptive explanation | 1 | 41.38% |
| chi-square variance-test adaptive explanation | 1 | 70.59% |
| chocolate-orb heat-pulse assumption explanation | 1 | 100.00% |
| composition constant-range assessment | 1 | 86.11% |
| implicit tangent-line active hint | 1 | 100.00% |
| inclined box slip-or-tip assessment | 1 | 50.00% |
| none | 1 | 26.09% |
| nonstandard tRNA translation assessment | 1 | 83.61% |
| series/parallel circuit assessment | 1 | 91.94% |
