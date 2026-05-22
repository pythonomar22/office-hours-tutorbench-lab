# TutorBench Run Analysis: `eb925fae-b460-4d43-a43d-9e3827bb9e71`

- Rows: 8
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 73.16%
- Mean generation latency: 95014 ms
- Mean judge latency: 3474 ms
- Generation input/output tokens: 203910 / 37470
- Judge input/output tokens: 14282 / 1791
- Negative-weight manual review rows: 0

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1995000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19998 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2395000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `683e45143a109788e3f7e591` | 27.78% | assessment / multimodal / Statistics | 6 | 0 | z-test vs t-test assessment |
| `6842a1fb5ca82eb2207af64b` | 38.10% | adaptive / text / Biology | 6 | 0 | oxygen/CO2 cellular-respiration adaptive explanation |
| `683e3d8d2b6d2a6c45002caa` | 67.31% | adaptive / multimodal / Chemistry | 5 | 0 | alkylbenzene sulphonation hyperconjugation explanation |
| `683e4516f37c3bccc4ec7e12` | 81.25% | assessment / multimodal / Computer Science | 2 | 0 | kth-smallest sorted-matrix assessment |
| `6843160b61e29735d3565670` | 81.25% | active_learning / text / Statistics | 2 | 0 | two-proportion z-test active-learning hint |
| `684772090f13de1c3fc22137` | 89.58% | active_learning / text / Statistics | 1 | 0 | coffee-shop conditional-probability active hint |
| `6843160a1c3b85b09bea6fd9` | 100.00% | active_learning / text / Statistics | 0 | 0 | penicillin allergy Bayes active-learning hint |
| `683e458c3a109788e3f7e64f` | 100.00% | active_learning / multimodal / Physics | 0 | 0 | rotating charged ring active-learning hint |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| conciseness_relevance | 0.00% | 1.0 | 1 | 0 |
| visual_reasoning | 57.14% | 15.0 | 2 | 0 |
| visual_perception | 60.00% | 10.0 | 1 | 0 |
| student_level_calibration | 61.90% | 40.0 | 5 | 0 |
| truthfulness | 65.62% | 11.0 | 2 | 0 |
| instruction_following | 74.39% | 42.0 | 4 | 0 |
| style_tone | 77.42% | 7.0 | 2 | 0 |
| emotional_component | 93.94% | 2.0 | 2 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 0.00% | 10.0 | 2 | 0 |
| Identifying correct steps by student | 28.57% | 25.0 | 3 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 57.14% | 12.0 | 2 | 0 |
| Identifying incorrect steps by student | 72.22% | 10.0 | 1 | 0 |
| Step by step help/ analysis | 75.00% | 5.0 | 1 | 0 |
| Not applicable | 80.46% | 17.0 | 4 | 0 |
| Identifying Core difficulty/ misconception attribution | 83.33% | 7.0 | 2 | 0 |
| Asks questions to guide students | 100.00% | 0.0 | 0 | 0 |
| Provides alternative solutions/ paths/ | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| alkylbenzene sulphonation hyperconjugation explanation | 1 | 67.31% |
| coffee-shop conditional-probability active hint | 1 | 89.58% |
| kth-smallest sorted-matrix assessment | 1 | 81.25% |
| oxygen/CO2 cellular-respiration adaptive explanation | 1 | 38.10% |
| penicillin allergy Bayes active-learning hint | 1 | 100.00% |
| rotating charged ring active-learning hint | 1 | 100.00% |
| two-proportion z-test active-learning hint | 1 | 81.25% |
| z-test vs t-test assessment | 1 | 27.78% |
