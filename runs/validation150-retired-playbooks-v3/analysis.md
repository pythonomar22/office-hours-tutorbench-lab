# TutorBench Run Analysis: `validation150-retired-playbooks-v3`

- Rows: 150
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 72.13%
- Mean generation latency: 88068 ms
- Mean judge latency: 3997 ms
- Generation input/output tokens: 3324058 / 644223
- Judge input/output tokens: 387626 / 37064
- Negative-weight manual review rows: 29

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1990000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19997 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2390000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `681a876ab9d767de6644dc12` | 16.67% | assessment / text / Biology | 3 | 0 | interphase mutation active-learning hint |
| `683e4516cb225e8f5aa693e1` | 17.86% | assessment / multimodal / Statistics | 7 | 0 | none |
| `6843120a5ca82eb2207b083f` | 23.08% | assessment / text / Physics | 3 | 1 | none |
| `68376d91a3ac2c2617743efe` | 26.67% | adaptive / multimodal / Calculus | 3 | 0 | radical derivative adaptive explanation |
| `6843120a7996124c02b92b01` | 31.82% | assessment / text / Chemistry | 2 | 1 | none |
| `681a876a23b6cca56a90f2a0` | 35.48% | assessment / text / Biology | 4 | 0 | interphase mutation active-learning hint |
| `681b80ddb17ff4fba2eec7e8` | 40.48% | adaptive / multimodal / Statistics | 5 | 0 | none |
| `683e458e8619d1d443f305be` | 43.24% | active_learning / multimodal / Biology | 5 | 0 | none |
| `683e458c225c80e89ef01a27` | 43.40% | active_learning / multimodal / Statistics | 6 | 0 | none |
| `683775dc80920782a0a28297` | 43.86% | adaptive / multimodal / Calculus | 8 | 0 | ellipse rectangle explanation |
| `684771b3c4590722c4324839` | 44.44% | assessment / text / Physics | 2 | 1 | none |
| `681cfdced476aa9b2b4633c7` | 44.44% | assessment / multimodal / Physics | 3 | 0 | none |
| `681a872123b6cca56a90f246` | 44.44% | adaptive / text / Biology | 5 | 0 | none |
| `683e458a9c195766bfe397d3` | 44.44% | active_learning / multimodal / Computer Science | 7 | 0 | none |
| `6843160bc6082b90c7d3518c` | 44.74% | active_learning / text / Biology | 5 | 0 | none |
| `681cfc8cd66359ff7194ddb1` | 47.37% | assessment / text / Calculus | 4 | 0 | none |
| `683e3d8d2c6221565bb39630` | 47.62% | adaptive / multimodal / Biology | 3 | 0 | none |
| `685454ee2ae3f8515f9eaea4` | 48.84% | adaptive / text / Chemistry | 6 | 0 | none |
| `681cffc83d9f33c969b76c6f` | 50.00% | active_learning / multimodal / Physics | 5 | 0 | none |
| `683e45169c195766bfe39791` | 50.98% | assessment / multimodal / Calculus | 4 | 1 | none |
| `685454eead07ff0ed76d4179` | 51.22% | adaptive / text / Chemistry | 3 | 1 | none |
| `683e4517f37c3bccc4ec7e33` | 51.52% | assessment / multimodal / Computer Science | 4 | 0 | none |
| `683775dc91fac7d3a4bdc866` | 52.00% | adaptive / multimodal / Biology | 4 | 0 | interphase mutation active-learning hint |
| `681a852b994a82b9033f6251` | 52.38% | active_learning / text / Calculus | 2 | 0 | none |
| `683870523cf028f91cd74ad8` | 52.83% | active_learning / multimodal / Chemistry | 5 | 0 | none |
| `681cffc8ec58ead1410f5588` | 53.12% | active_learning / multimodal / Biology | 3 | 0 | none |
| `683e3d8e9394b13fefb08813` | 53.49% | adaptive / multimodal / Biology | 4 | 0 | none |
| `68387053482dac7a5c572262` | 54.17% | active_learning / multimodal / Biology | 3 | 0 | none |
| `683870eeee7badec285a7a65` | 54.55% | active_learning / text / Physics | 2 | 0 | none |
| `683e3d8f5f104dac1d4d66ac` | 54.55% | adaptive / multimodal / Chemistry | 2 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| conciseness_relevance | 49.23% | 33.0 | 13 | 0 |
| not applicable | 62.50% | 15.0 | 1 | 0 |
| truthfulness | 65.68% | 431.0 | 62 | 4 |
| visual_reasoning | 73.43% | 110.0 | 18 | 0 |
| student_level_calibration | 74.59% | 647.0 | 84 | 1 |
| instruction_following | 75.03% | 749.0 | 96 | 13 |
| style_tone | 77.74% | 124.0 | 36 | 0 |
| emotional_component | 79.35% | 96.0 | 28 | 0 |
| visual_perception | 81.90% | 61.0 | 15 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 27.03% | 54.0 | 19 | 0 |
| Asks questions to guide students | 52.17% | 88.0 | 12 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 68.87% | 302.0 | 44 | 0 |
| Identifying Core difficulty/ misconception attribution | 73.30% | 216.0 | 42 | 0 |
| Not applicable | 73.55% | 402.0 | 85 | 9 |
| Step by step help/ analysis | 74.15% | 114.0 | 27 | 6 |
| Identifying incorrect steps by student | 77.25% | 187.0 | 30 | 1 |
| Identifying correct steps by student | 81.15% | 148.0 | 24 | 0 |
| Provides alternative solutions/ paths/ | 83.78% | 12.0 | 5 | 1 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 132 | 72.69% |
| OOP design / inventory class | 6 | 81.06% |
| interphase mutation active-learning hint | 6 | 59.02% |
| CLT sample-mean active-learning hint | 2 | 85.67% |
| Gene X methylation/tumor-suppressor active hint | 1 | 83.78% |
| ellipse rectangle explanation | 1 | 43.86% |
| oxygen/CO2 cellular-respiration adaptive explanation | 1 | 57.69% |
| radical derivative adaptive explanation | 1 | 26.67% |
