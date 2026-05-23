# TutorBench Run Analysis: `validation-failure-probe-v5-final`

- Rows: 14
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 73.07%
- Mean generation latency: 107492 ms
- Mean judge latency: 3947 ms
- Generation input/output tokens: 440782 / 75083
- Judge input/output tokens: 36935 / 3317
- Negative-weight manual review rows: 1

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
| `6843120a7996124c02b92b01` | 31.82% | assessment / text / Chemistry | 2 | 1 | weak-acid titration assessment |
| `683775dc913c16d05cd33839` | 47.37% | adaptive / multimodal / Computer Science | 2 | 0 | none |
| `681b80ddb17ff4fba2eec7e8` | 52.38% | adaptive / multimodal / Statistics | 4 | 0 | chi-square variance-test adaptive explanation |
| `683e4516cb225e8f5aa693e1` | 53.57% | assessment / multimodal / Statistics | 5 | 0 | qualitative survey-variable assessment |
| `683e451300c66429fabd7419` | 57.89% | assessment / multimodal / Biology | 4 | 0 | none |
| `681a876a23b6cca56a90f2a0` | 67.74% | assessment / text / Biology | 2 | 0 | natural-selection misconception assessment |
| `683e458a9c195766bfe397d3` | 68.25% | active_learning / multimodal / Computer Science | 4 | 0 | fastPower exponentiation active-learning hint |
| `681a872123b6cca56a90f246` | 75.56% | adaptive / text / Biology | 3 | 0 | lac-operon CAP-cAMP adaptive explanation |
| `683870ee806964a2566da1fd` | 85.29% | active_learning / text / Biology | 2 | 0 | non-palindromic restriction-enzyme active hint |
| `681cfc8cd66359ff7194ddb1` | 86.84% | assessment / text / Calculus | 1 | 0 | sideways-parabola enclosed-area assessment |
| `6814f3603103a8e315cd7d95` | 96.30% | adaptive / multimodal / Physics | 1 | 0 | velocity-time signed-area adaptive explanation |
| `681a876ab9d767de6644dc12` | 100.00% | assessment / text / Biology | 0 | 0 | start-codon insertion mutation assessment |
| `68376d91a3ac2c2617743efe` | 100.00% | adaptive / multimodal / Calculus | 0 | 0 | trig u-substitution adaptive explanation |
| `681cfdced476aa9b2b4633c7` | 100.00% | assessment / multimodal / Physics | 0 | 0 | crackle derivative assessment |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| conciseness_relevance | 28.57% | 5.0 | 1 | 0 |
| visual_perception | 58.33% | 5.0 | 1 | 0 |
| visual_reasoning | 68.75% | 5.0 | 1 | 0 |
| emotional_component | 69.23% | 16.0 | 3 | 0 |
| student_level_calibration | 71.43% | 68.0 | 7 | 0 |
| truthfulness | 72.78% | 43.0 | 6 | 0 |
| instruction_following | 75.22% | 57.0 | 10 | 1 |
| style_tone | 77.08% | 11.0 | 2 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 5.88% | 16.0 | 2 | 0 |
| Asks questions to guide students | 54.55% | 5.0 | 1 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 67.09% | 26.0 | 5 | 0 |
| Identifying correct steps by student | 75.00% | 16.0 | 3 | 0 |
| Identifying Core difficulty/ misconception attribution | 75.90% | 20.0 | 4 | 0 |
| Not applicable | 77.42% | 28.0 | 6 | 0 |
| Identifying incorrect steps by student | 82.14% | 10.0 | 2 | 1 |
| Step by step help/ analysis | 88.10% | 5.0 | 1 | 0 |
| Provides alternative solutions/ paths/ | 100.00% | 0.0 | 0 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 2 | 52.63% |
| chi-square variance-test adaptive explanation | 1 | 52.38% |
| crackle derivative assessment | 1 | 100.00% |
| fastPower exponentiation active-learning hint | 1 | 68.25% |
| lac-operon CAP-cAMP adaptive explanation | 1 | 75.56% |
| natural-selection misconception assessment | 1 | 67.74% |
| non-palindromic restriction-enzyme active hint | 1 | 85.29% |
| qualitative survey-variable assessment | 1 | 53.57% |
| sideways-parabola enclosed-area assessment | 1 | 86.84% |
| start-codon insertion mutation assessment | 1 | 100.00% |
| trig u-substitution adaptive explanation | 1 | 100.00% |
| velocity-time signed-area adaptive explanation | 1 | 96.30% |
| weak-acid titration assessment | 1 | 31.82% |
