# TutorBench Run Analysis: `heldout-v11b-failure-probe`

- Rows: 10
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 93.82%
- Mean generation latency: 136627 ms
- Mean judge latency: 4742 ms
- Generation input/output tokens: 604198 / 71845
- Judge input/output tokens: 33577 / 2562
- Negative-weight manual review rows: 0

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
| `anthropic-ratelimit-tokens-remaining` | 2389000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `683e3d8fa08f8bb26159720b` | 77.78% | adaptive / multimodal / Statistics | 4 | 0 | chi-square variance-test adaptive explanation |
| `6811d40e6b7f984ce18baebb` | 82.76% | adaptive / multimodal / Computer Science | 1 | 0 | bakery flour check adaptive explanation |
| `68097912014bb68a4c65e4a1` | 83.61% | assessment / text / Biology | 2 | 0 | nonstandard tRNA translation assessment |
| `683e45109394b13fefb08e44` | 95.65% | assessment / multimodal / Physics | 1 | 0 | connected conducting-shell potential assessment |
| `681b84ff94969ef6e11908e0` | 98.39% | assessment / multimodal / Physics | 1 | 0 | series/parallel circuit assessment |
| `6847710ac4590722c4324810` | 100.00% | adaptive / text / Physics | 0 | 0 | chocolate-orb heat-pulse assumption explanation |
| `68477209e96863adfe492508` | 100.00% | active_learning / text / Calculus | 0 | 0 | implicit tangent-line active hint |
| `68377588415e67c44f4734b6` | 100.00% | assessment / text / Physics | 0 | 0 | inclined box slip-or-tip assessment |
| `683776272f4468651311d6dc` | 100.00% | assessment / multimodal / Calculus | 0 | 0 | composition constant-range assessment |
| `683e3d8d9394b13fefb087f2` | 100.00% | adaptive / multimodal / Statistics | 0 | 0 | archery target binomial-geometry explanation |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| truthfulness | 82.35% | 6.0 | 2 | 0 |
| conciseness_relevance | 85.71% | 1.0 | 1 | 0 |
| student_level_calibration | 89.17% | 13.0 | 3 | 0 |
| instruction_following | 95.07% | 11.0 | 2 | 0 |
| visual_perception | 95.45% | 1.0 | 1 | 0 |
| style_tone | 96.43% | 1.0 | 1 | 0 |
| visual_reasoning | 97.83% | 1.0 | 1 | 0 |
| emotional_component | 100.00% | 0.0 | 0 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Identifying incorrect steps by student | 87.80% | 5.0 | 1 | 0 |
| Step by step help/ analysis | 88.46% | 6.0 | 2 | 0 |
| Not applicable | 93.16% | 8.0 | 3 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 95.00% | 2.0 | 2 | 0 |
| Identifying Core difficulty/ misconception attribution | 100.00% | 0.0 | 0 | 0 |
| Identifying correct steps by student | 100.00% | 0.0 | 0 | 0 |
| Includes examples/ analogy | 100.00% | 0.0 | 0 | 0 |
| Provides alternative solutions/ paths/ | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| archery target binomial-geometry explanation | 1 | 100.00% |
| bakery flour check adaptive explanation | 1 | 82.76% |
| chi-square variance-test adaptive explanation | 1 | 77.78% |
| chocolate-orb heat-pulse assumption explanation | 1 | 100.00% |
| composition constant-range assessment | 1 | 100.00% |
| connected conducting-shell potential assessment | 1 | 95.65% |
| implicit tangent-line active hint | 1 | 100.00% |
| inclined box slip-or-tip assessment | 1 | 100.00% |
| nonstandard tRNA translation assessment | 1 | 83.61% |
| series/parallel circuit assessment | 1 | 98.39% |
