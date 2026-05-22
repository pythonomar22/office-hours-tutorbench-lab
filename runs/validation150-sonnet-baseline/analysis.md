# TutorBench Run Analysis: `validation150-sonnet-baseline`

- Rows: 150
- Strategy: `baseline`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 59.65%
- Mean generation latency: 10445 ms
- Mean judge latency: 3916 ms
- Generation input/output tokens: 146602 / 69560
- Judge input/output tokens: 326690 / 37064
- Negative-weight manual review rows: 29

## Throughput Headroom

No rate-limit headers were captured.

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `6842a1fbba6af9cb6614fe61` | 2.63% | adaptive / text / Calculus | 9 | 0 | none |
| `6843120a5ca82eb2207b083f` | 3.85% | assessment / text / Physics | 4 | 1 | none |
| `684771b3c4590722c4324839` | 7.41% | assessment / text / Physics | 4 | 1 | none |
| `683e451300c66429fabd7419` | 15.79% | assessment / multimodal / Biology | 8 | 0 | none |
| `681a876ab9d767de6644dc12` | 16.67% | assessment / text / Biology | 3 | 0 | none |
| `681b80ddb17ff4fba2eec7e8` | 16.67% | adaptive / multimodal / Statistics | 7 | 0 | none |
| `683e4516cb225e8f5aa693e1` | 17.86% | assessment / multimodal / Statistics | 7 | 0 | none |
| `6847710a62247cf826ecc61b` | 21.43% | adaptive / text / Biology | 2 | 1 | none |
| `683e45169c195766bfe39791` | 21.57% | assessment / multimodal / Calculus | 8 | 0 | none |
| `681a872123b6cca56a90f246` | 22.22% | adaptive / text / Biology | 7 | 0 | none |
| `68097912014bb68a4c65e49d` | 25.93% | assessment / text / Calculus | 4 | 0 | none |
| `68376d91a3ac2c2617743efe` | 26.67% | adaptive / multimodal / Calculus | 3 | 0 | none |
| `681a852b994a82b9033f6251` | 28.57% | active_learning / text / Calculus | 3 | 0 | none |
| `681cfc8cd66359ff7194ddb1` | 28.95% | assessment / text / Calculus | 7 | 0 | none |
| `681cfcca0e130c4d40215f09` | 29.73% | active_learning / text / Biology | 6 | 0 | none |
| `6843120a7996124c02b92b01` | 31.82% | assessment / text / Chemistry | 2 | 1 | none |
| `683e3d8fd3bdf2dc57e04da2` | 32.35% | adaptive / multimodal / Statistics | 7 | 0 | none |
| `6843120a0015fc211142f9cd` | 32.35% | assessment / text / Calculus | 7 | 0 | none |
| `68376d91a815e847ea7c9875` | 33.33% | adaptive / multimodal / Calculus | 6 | 0 | none |
| `68376de0afc2cf08ab22a52e` | 33.87% | assessment / multimodal / Biology | 9 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| conciseness_relevance | 43.08% | 37.0 | 12 | 0 |
| truthfulness | 43.31% | 712.0 | 80 | 4 |
| student_level_calibration | 60.64% | 1002.0 | 98 | 0 |
| visual_reasoning | 61.11% | 161.0 | 21 | 0 |
| not applicable | 62.50% | 15.0 | 1 | 0 |
| instruction_following | 63.60% | 1092.0 | 110 | 9 |
| style_tone | 66.07% | 189.0 | 53 | 1 |
| emotional_component | 66.67% | 155.0 | 38 | 1 |
| visual_perception | 80.42% | 66.0 | 16 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 24.32% | 56.0 | 20 | 0 |
| Asks questions to guide students | 40.76% | 109.0 | 15 | 0 |
| Provides alternative solutions/ paths/ | 41.89% | 43.0 | 10 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 50.52% | 480.0 | 60 | 0 |
| Identifying incorrect steps by student | 53.41% | 383.0 | 48 | 1 |
| Step by step help/ analysis | 57.14% | 189.0 | 36 | 3 |
| Not applicable | 63.75% | 551.0 | 91 | 10 |
| Identifying Core difficulty/ misconception attribution | 66.87% | 268.0 | 49 | 0 |
| Identifying correct steps by student | 74.78% | 198.0 | 33 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 150 | 59.65% |
