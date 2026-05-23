# TutorBench Run Analysis: `validation150-agentic-v4-refined`

- Rows: 150
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 73.06%
- Mean generation latency: 101515 ms
- Mean judge latency: 12237 ms
- Generation input/output tokens: 4628395 / 751389
- Judge input/output tokens: 401358 / 37054
- Negative-weight manual review rows: 29

## Throughput Headroom

| Header | Min Remaining | Max Limit |
| --- | ---: | ---: |
| `anthropic-ratelimit-input-tokens-limit` | None | 2000000 |
| `anthropic-ratelimit-input-tokens-remaining` | 1991000 | None |
| `anthropic-ratelimit-output-tokens-limit` | None | 400000 |
| `anthropic-ratelimit-output-tokens-remaining` | 399000 | None |
| `anthropic-ratelimit-requests-limit` | None | 20000 |
| `anthropic-ratelimit-requests-remaining` | 19998 | None |
| `anthropic-ratelimit-tokens-limit` | None | 2400000 |
| `anthropic-ratelimit-tokens-remaining` | 2391000 | None |

## Weakest Rows

| Task | ARRw | Slice | Failed + | Triggered - | Playbook |
| --- | ---: | --- | ---: | ---: | --- |
| `681a876ab9d767de6644dc12` | 16.67% | assessment / text / Biology | 3 | 0 | interphase mutation active-learning hint |
| `683e4516cb225e8f5aa693e1` | 17.86% | assessment / multimodal / Statistics | 7 | 0 | none |
| `68376d91a3ac2c2617743efe` | 20.00% | adaptive / multimodal / Calculus | 4 | 0 | radical derivative adaptive explanation |
| `683e458a9c195766bfe397d3` | 28.57% | active_learning / multimodal / Computer Science | 9 | 0 | none |
| `681cfc8cd66359ff7194ddb1` | 34.21% | assessment / text / Calculus | 5 | 0 | none |
| `681a876a23b6cca56a90f2a0` | 35.48% | assessment / text / Biology | 4 | 0 | interphase mutation active-learning hint |
| `683e3d8f9394b13fefb08833` | 38.89% | adaptive / multimodal / Physics | 3 | 0 | none |
| `681b80ddb17ff4fba2eec7e8` | 40.48% | adaptive / multimodal / Statistics | 5 | 0 | none |
| `683628c73a003524f3d65e16` | 41.18% | adaptive / text / Statistics | 0 | 2 | none |
| `684a8c40900d45c5e9de2180` | 41.18% | adaptive / text / Chemistry | 5 | 1 | none |
| `683870ee806964a2566da1fd` | 41.18% | active_learning / text / Biology | 8 | 0 | none |
| `683e3d8e9394b13fefb08813` | 41.86% | adaptive / multimodal / Biology | 5 | 0 | none |
| `683e3d8d2c6221565bb39630` | 42.86% | adaptive / multimodal / Biology | 4 | 0 | none |
| `681a872123b6cca56a90f246` | 44.44% | adaptive / text / Biology | 5 | 0 | none |
| `6814f3603103a8e315cd7d95` | 44.44% | adaptive / multimodal / Physics | 3 | 0 | none |
| `683e451300c66429fabd7419` | 44.74% | assessment / multimodal / Biology | 5 | 0 | none |
| `683775dc913c16d05cd33839` | 47.37% | adaptive / multimodal / Computer Science | 2 | 0 | OOP design / inventory class |
| `6843160bc6082b90c7d3518c` | 47.37% | active_learning / text / Biology | 4 | 0 | none |
| `6847710a62247cf826ecc61b` | 50.00% | adaptive / text / Biology | 2 | 1 | interphase mutation active-learning hint |
| `681b84ff458c75d9b6647055` | 50.82% | assessment / multimodal / Statistics | 6 | 0 | trig accumulation probability assessment |
| `683e45169c195766bfe39791` | 50.98% | assessment / multimodal / Calculus | 4 | 1 | none |
| `685454ee2ae3f8515f9eaea4` | 51.16% | adaptive / text / Chemistry | 5 | 0 | none |
| `68376de02ee86c4fcacd99fb` | 51.22% | assessment / multimodal / Chemistry | 4 | 0 | none |
| `683775dc91fac7d3a4bdc866` | 52.00% | adaptive / multimodal / Biology | 4 | 0 | interphase mutation active-learning hint |
| `681a852b994a82b9033f6251` | 52.38% | active_learning / text / Calculus | 2 | 0 | none |
| `683775dc80920782a0a28297` | 52.63% | adaptive / multimodal / Calculus | 6 | 1 | none |
| `6843120a0015fc211142f9cd` | 52.94% | assessment / text / Calculus | 4 | 0 | none |
| `681cffc8ec58ead1410f5588` | 53.12% | active_learning / multimodal / Biology | 3 | 0 | none |
| `683e3d8f5f104dac1d4d66ac` | 54.55% | adaptive / multimodal / Chemistry | 2 | 0 | none |
| `6843120a7996124c02b92b01` | 54.55% | assessment / text / Chemistry | 2 | 0 | none |
| `6842a1fbba6af9cb6614fe61` | 55.26% | adaptive / text / Calculus | 5 | 0 | none |
| `685454eee805192d91587860` | 55.32% | adaptive / text / Chemistry | 4 | 1 | none |
| `683775dc496507faa0915cb4` | 56.25% | adaptive / multimodal / Calculus | 3 | 0 | none |
| `68376d91af9be190d433bd70` | 56.52% | adaptive / multimodal / Statistics | 4 | 0 | none |
| `683e458e8619d1d443f305be` | 56.76% | active_learning / multimodal / Biology | 4 | 0 | none |
| `683e45172d501a5ab198c53f` | 58.33% | assessment / multimodal / Physics | 3 | 0 | none |
| `68545548a675fc48d54e7f7d` | 59.46% | assessment / text / Physics | 3 | 0 | none |
| `68133830e566f93318db74d5` | 59.46% | active_learning / multimodal / Calculus | 3 | 0 | none |
| `681338309db9af3562c6ad8b` | 60.78% | active_learning / multimodal / Calculus | 4 | 0 | none |
| `684a8c408708c5dec8f441d7` | 61.36% | adaptive / text / Chemistry | 5 | 0 | none |
| `6843120a5ca82eb2207b083f` | 61.54% | assessment / text / Physics | 1 | 1 | none |
| `681b84ffec36498056e41856` | 61.54% | assessment / multimodal / Calculus | 4 | 0 | none |
| `68377627c130b33e3079a99e` | 61.76% | assessment / multimodal / Computer Science | 5 | 1 | OOP design / inventory class |
| `680979015bb01ceb7a8c82c6` | 61.76% | assessment / text / Chemistry | 5 | 1 | none |
| `683775457c71f24d6187a946` | 62.50% | adaptive / text / Chemistry | 6 | 0 | none |
| `683e4510cb225e8f5aa69359` | 62.50% | assessment / multimodal / Chemistry | 5 | 1 | none |
| `681cfb9f958a9ebd9b65f9ac` | 62.79% | adaptive / text / Calculus | 4 | 0 | none |
| `684771b3c4590722c4324839` | 62.96% | assessment / text / Physics | 1 | 1 | none |
| `683870efee7badec285a7a85` | 62.96% | active_learning / text / Calculus | 2 | 0 | none |
| `681cfdced476aa9b2b4633c7` | 62.96% | assessment / multimodal / Physics | 2 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| not applicable | 50.00% | 20.0 | 1 | 0 |
| conciseness_relevance | 52.31% | 31.0 | 11 | 0 |
| truthfulness | 64.49% | 446.0 | 59 | 5 |
| student_level_calibration | 75.29% | 629.0 | 75 | 1 |
| instruction_following | 75.83% | 725.0 | 94 | 13 |
| style_tone | 79.71% | 113.0 | 30 | 1 |
| visual_reasoning | 80.43% | 81.0 | 12 | 0 |
| emotional_component | 81.08% | 88.0 | 23 | 1 |
| visual_perception | 86.65% | 45.0 | 13 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 24.32% | 56.0 | 21 | 0 |
| Asks questions to guide students | 65.76% | 63.0 | 9 | 0 |
| Step by step help/ analysis | 68.71% | 138.0 | 32 | 6 |
| Stating definitions/ formulae/ theorems/ laws | 68.97% | 301.0 | 42 | 1 |
| Not applicable | 74.80% | 383.0 | 82 | 10 |
| Identifying Core difficulty/ misconception attribution | 75.77% | 196.0 | 38 | 0 |
| Provides alternative solutions/ paths/ | 77.03% | 17.0 | 6 | 1 |
| Identifying incorrect steps by student | 77.74% | 183.0 | 32 | 1 |
| Identifying correct steps by student | 84.20% | 124.0 | 19 | 0 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 130 | 74.03% |
| OOP design / inventory class | 6 | 76.09% |
| interphase mutation active-learning hint | 6 | 51.87% |
| CLT sample-mean active-learning hint | 2 | 93.02% |
| Gene X methylation/tumor-suppressor active hint | 1 | 70.27% |
| U-238/Pb-206 mass-ratio adaptive explanation | 1 | 63.41% |
| oxygen/CO2 cellular-respiration adaptive explanation | 1 | 76.92% |
| radical derivative adaptive explanation | 1 | 20.00% |
| trig accumulation probability assessment | 1 | 50.82% |
| z-test vs t-test assessment | 1 | 100.00% |
