# TutorBench Run Analysis: `heldout500-sonnet-baseline`

- Rows: 500
- Strategy: `baseline`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 60.77%
- Mean generation latency: 10633 ms
- Mean judge latency: 3946 ms
- Generation input/output tokens: 518898 / 234790
- Judge input/output tokens: 1119503 / 127518
- Negative-weight manual review rows: 47

## Throughput Headroom

No rate-limit headers were captured.

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `6843120a9fab58968f2128c9` | 0.00% | assessment / text / Chemistry | 2 | 1 | none |
| `684a8cd6a8da4aded13ef58d` | 0.00% | assessment / text / Calculus | 5 | 1 | none |
| `683e458f8103655aef73fd55` | 1.75% | active_learning / multimodal / Chemistry | 12 | 0 | none |
| `681904ae013a6ffe335931b0` | 2.44% | adaptive / text / Chemistry | 8 | 0 | none |
| `683e458eac89e71e0ce600c6` | 2.78% | active_learning / multimodal / Computer Science | 7 | 0 | none |
| `683e3d8f3482feddb4d05e86` | 4.26% | adaptive / multimodal / Physics | 9 | 0 | none |
| `681cfd7a46a1279c844e62ca` | 4.65% | adaptive / multimodal / Biology | 9 | 0 | none |
| `6843120a2b986bd2d9ca5f3f` | 6.25% | assessment / text / Chemistry | 6 | 0 | none |
| `681a8721b07ca4da41ff1d4e` | 8.33% | adaptive / text / Statistics | 9 | 0 | none |
| `68377627d27550109b72e510` | 10.45% | assessment / multimodal / Chemistry | 12 | 0 | none |
| `68376de1c596c43935ed5a4d` | 12.77% | assessment / multimodal / Chemistry | 9 | 0 | none |
| `683775dc2f4468651311d6ad` | 14.63% | adaptive / multimodal / Chemistry | 7 | 0 | none |
| `6847710b9bc321f32d5b5ab8` | 15.79% | adaptive / text / Calculus | 8 | 0 | none |
| `683e4514225c80e89ef01988` | 16.22% | assessment / multimodal / Physics | 6 | 1 | none |
| `684771b3cf8ba842e93ec6de` | 16.22% | assessment / text / Computer Science | 7 | 0 | none |
| `68097912014bb68a4c65e4a1` | 16.39% | assessment / text / Biology | 11 | 0 | none |
| `683776272f4468651311d6dc` | 16.67% | assessment / multimodal / Calculus | 5 | 1 | none |
| `681cfdce5db7f3af72e15829` | 17.74% | assessment / multimodal / Biology | 11 | 0 | none |
| `684a8cd6f08ce27c3bf577e0` | 17.78% | assessment / text / Chemistry | 9 | 0 | none |
| `683e3d8d9394b13fefb087f2` | 17.78% | adaptive / multimodal / Statistics | 13 | 0 | none |
| `683e45162d501a5ab198c520` | 17.86% | assessment / multimodal / Chemistry | 10 | 0 | none |
| `6810216fbe57055e015742ec` | 18.18% | assessment / multimodal / Statistics | 7 | 0 | none |
| `683e4510bd7caf8a464501d6` | 18.92% | assessment / multimodal / Physics | 6 | 0 | none |
| `683e45172d5e3eede3bfbe03` | 18.97% | assessment / multimodal / Chemistry | 11 | 0 | none |
| `683e450e225c80e89ef01948` | 20.39% | assessment / multimodal / Physics | 18 | 0 | none |
| `6811d40e6b7f984ce18baebb` | 20.69% | adaptive / multimodal / Computer Science | 7 | 0 | none |
| `683e451398da7313814691f6` | 20.83% | assessment / multimodal / Calculus | 10 | 0 | none |
| `683e451455b71d5f5598c49a` | 22.54% | assessment / multimodal / Biology | 11 | 0 | none |
| `681cffc846a1279c844e6432` | 23.08% | active_learning / multimodal / Biology | 8 | 0 | none |
| `683e458c2e254199a0fa2e02` | 24.39% | active_learning / multimodal / Computer Science | 6 | 1 | none |
| `6847720874c7f1cb6eb0b1d5` | 25.37% | active_learning / text / Computer Science | 10 | 0 | none |
| `68096a17d9108896c270f6b6` | 25.93% | adaptive / text / Physics | 4 | 0 | none |
| `684a8c40562837a83a9ac6b2` | 25.93% | adaptive / text / Physics | 4 | 0 | none |
| `683e45109394b13fefb08e44` | 26.09% | assessment / multimodal / Physics | 5 | 0 | none |
| `681904ae47ec182ef081cc59` | 26.32% | adaptive / text / Calculus | 14 | 0 | none |
| `680c443acc8fba6dcbac6606` | 26.83% | active_learning / text / Physics | 6 | 0 | none |
| `68376d91c5b329d497cbe8ca` | 26.83% | adaptive / multimodal / Computer Science | 5 | 1 | none |
| `681cfc8cb4e0809f6fae0767` | 27.03% | assessment / text / Calculus | 7 | 0 | none |
| `68377588415e67c44f4734b6` | 27.27% | assessment / text / Physics | 4 | 0 | none |
| `6811d993d391e676ed896378` | 27.27% | assessment / multimodal / Biology | 8 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| visual_reasoning | 45.03% | 979.0 | 116 | 1 |
| not applicable | 50.00% | 1.0 | 1 | 0 |
| truthfulness | 52.57% | 1680.0 | 196 | 3 |
| conciseness_relevance | 60.00% | 80.0 | 31 | 0 |
| instruction_following | 60.44% | 4445.0 | 383 | 20 |
| student_level_calibration | 61.81% | 3177.0 | 316 | 7 |
| visual_perception | 69.39% | 401.0 | 82 | 3 |
| style_tone | 73.10% | 481.0 | 166 | 2 |
| emotional_component | 73.76% | 391.0 | 109 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Provides alternative solutions/ paths/ | 35.56% | 203.0 | 52 | 3 |
| Asks questions to guide students | 43.04% | 528.0 | 72 | 0 |
| Includes examples/ analogy | 43.56% | 149.0 | 47 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 54.00% | 1519.0 | 185 | 0 |
| Identifying incorrect steps by student | 56.18% | 1128.0 | 139 | 4 |
| Step by step help/ analysis | 56.19% | 729.0 | 115 | 5 |
| Identifying Core difficulty/ misconception attribution | 62.25% | 1119.0 | 182 | 0 |
| Not applicable | 62.58% | 1846.0 | 317 | 14 |
| Identifying correct steps by student | 70.77% | 856.0 | 128 | 3 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 500 | 60.77% |
