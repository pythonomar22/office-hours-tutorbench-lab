# TutorBench Run Analysis: `validation150-agentic-v5`

- Rows: 150
- Strategy: `agentic`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Judge model: `anthropic:claude-sonnet-4-6`
- Overall ARRw: 77.21%
- Mean generation latency: 100978 ms
- Mean judge latency: 3946 ms
- Generation input/output tokens: 4671115 / 749590
- Judge input/output tokens: 397648 / 37079
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
| `6843120a7996124c02b92b01` | 31.82% | assessment / text / Chemistry | 2 | 1 | none |
| `681cffc8ec58ead1410f5588` | 37.50% | active_learning / multimodal / Biology | 4 | 0 | none |
| `683e4518bd7caf8a46450290` | 41.18% | assessment / multimodal / Computer Science | 1 | 1 | none |
| `683e3d8d2c6221565bb39630` | 42.86% | adaptive / multimodal / Biology | 4 | 0 | none |
| `683870efee7badec285a7a85` | 44.44% | active_learning / text / Calculus | 3 | 0 | none |
| `683e45172d501a5ab198c53f` | 44.44% | assessment / multimodal / Physics | 4 | 0 | none |
| `6843160bc6082b90c7d3518c` | 44.74% | active_learning / text / Biology | 5 | 0 | none |
| `683775dc913c16d05cd33839` | 47.37% | adaptive / multimodal / Computer Science | 2 | 0 | none |
| `680fb68ef04842cb7d05cea7` | 50.00% | active_learning / text / Physics | 4 | 0 | none |
| `683e458c98da7313814692b4` | 50.00% | active_learning / multimodal / Physics | 3 | 0 | none |
| `683e3d8f5f104dac1d4d66ac` | 50.00% | adaptive / multimodal / Chemistry | 3 | 0 | none |
| `6847710a62247cf826ecc61b` | 50.00% | adaptive / text / Biology | 2 | 1 | none |
| `683e45169c195766bfe39791` | 50.98% | assessment / multimodal / Calculus | 4 | 1 | none |
| `68376de0afc2cf08ab22a52e` | 51.61% | assessment / multimodal / Biology | 6 | 0 | none |
| `683775dc91fac7d3a4bdc866` | 52.00% | adaptive / multimodal / Biology | 4 | 0 | none |
| `685454ee2ae3f8515f9eaea4` | 53.49% | adaptive / text / Chemistry | 4 | 0 | none |
| `683e4516cb225e8f5aa693e1` | 53.57% | assessment / multimodal / Statistics | 5 | 0 | qualitative survey-variable assessment |
| `685454eee805192d91587860` | 55.32% | adaptive / text / Chemistry | 4 | 1 | none |
| `683775dc496507faa0915cb4` | 56.25% | adaptive / multimodal / Calculus | 3 | 0 | none |
| `68387051635e201ec4afa315` | 57.14% | active_learning / multimodal / Biology | 5 | 0 | none |
| `683e451300c66429fabd7419` | 57.89% | assessment / multimodal / Biology | 4 | 0 | none |
| `685455c722969a049b1c9def` | 58.33% | active_learning / text / Physics | 4 | 0 | none |
| `68377546cbb6263fa01c027b` | 58.82% | adaptive / text / Biology | 5 | 0 | none |
| `68545548a675fc48d54e7f7d` | 59.46% | assessment / text / Physics | 3 | 0 | none |
| `684a8cd62e4d9fec5e495e45` | 60.71% | assessment / text / Statistics | 2 | 1 | none |
| `684a8c408708c5dec8f441d7` | 61.36% | adaptive / text / Chemistry | 5 | 0 | none |
| `6843120a5ca82eb2207b083f` | 61.54% | assessment / text / Physics | 1 | 1 | none |
| `681b84ffec36498056e41856` | 61.54% | assessment / multimodal / Calculus | 4 | 0 | none |
| `6847710be39680cf6ef16b5f` | 61.54% | adaptive / text / Biology | 2 | 0 | oxygen/CO2 cellular-respiration adaptive explanation |
| `683870523cf028f91cd74ad8` | 62.26% | active_learning / multimodal / Chemistry | 4 | 0 | none |
| `683e4510cb225e8f5aa69359` | 62.50% | assessment / multimodal / Chemistry | 5 | 1 | none |
| `683e3d8e9394b13fefb08813` | 62.79% | adaptive / multimodal / Biology | 4 | 0 | none |
| `684771b3c4590722c4324839` | 62.96% | assessment / text / Physics | 1 | 1 | none |
| `681cfdced476aa9b2b4633c7` | 62.96% | assessment / multimodal / Physics | 2 | 0 | crackle derivative assessment |
| `685454eead07ff0ed76d4179` | 63.41% | adaptive / text / Chemistry | 2 | 1 | U-238/Pb-206 mass-ratio adaptive explanation |
| `68376de02ee86c4fcacd99fb` | 63.41% | assessment / multimodal / Chemistry | 3 | 0 | none |
| `681cfdce93aea527f9f5b613` | 64.29% | assessment / multimodal / Calculus | 3 | 0 | none |
| `6843120a493da3d4b37fead1` | 64.29% | assessment / text / Statistics | 3 | 0 | none |
| `681b84ff66386206bca129e1` | 64.29% | assessment / multimodal / Calculus | 3 | 0 | none |
| `683870eeb790747a1c2a3772` | 64.29% | active_learning / text / Calculus | 2 | 0 | none |
| `683e3d8fd3bdf2dc57e04da2` | 64.71% | adaptive / multimodal / Statistics | 4 | 0 | none |
| `6843120a0015fc211142f9cd` | 64.71% | assessment / text / Calculus | 4 | 0 | none |
| `68376d91a3ac2c2617743efe` | 66.67% | adaptive / multimodal / Calculus | 1 | 0 | trig u-substitution adaptive explanation |
| `683e3d8f9394b13fefb08833` | 66.67% | adaptive / multimodal / Physics | 2 | 0 | none |
| `683e4517f37c3bccc4ec7e33` | 66.67% | assessment / multimodal / Computer Science | 3 | 0 | none |
| `68545549f20ebbefd00e2ce5` | 66.67% | assessment / text / Physics | 1 | 1 | none |
| `683e451455b71d5f5598c49c` | 67.03% | assessment / multimodal / Chemistry | 6 | 0 | none |
| `68376d91af9be190d433bd70` | 67.39% | adaptive / multimodal / Statistics | 3 | 0 | none |
| `68096a1768607997d185125f` | 67.39% | adaptive / text / Biology | 2 | 1 | none |
| `683e45152667944fdee50611` | 67.74% | assessment / multimodal / Physics | 2 | 0 | none |

## Weakest Rubric Dimensions

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| conciseness_relevance | 49.23% | 33.0 | 13 | 0 |
| not applicable | 62.50% | 15.0 | 1 | 0 |
| truthfulness | 75.88% | 303.0 | 49 | 6 |
| student_level_calibration | 79.46% | 523.0 | 73 | 3 |
| style_tone | 79.71% | 113.0 | 29 | 1 |
| instruction_following | 79.83% | 605.0 | 89 | 14 |
| emotional_component | 80.43% | 91.0 | 22 | 1 |
| visual_reasoning | 83.09% | 70.0 | 12 | 0 |
| visual_perception | 86.35% | 46.0 | 14 | 0 |

## Weakest Tutoring Skills

| Group | Pass Rate | Failed Weight | Rows With Failure | Triggered - |
| --- | ---: | ---: | ---: | ---: |
| Includes examples/ analogy | 44.59% | 41.0 | 18 | 0 |
| Asks questions to guide students | 63.59% | 67.0 | 9 | 0 |
| Stating definitions/ formulae/ theorems/ laws | 73.61% | 256.0 | 41 | 1 |
| Step by step help/ analysis | 74.60% | 112.0 | 25 | 5 |
| Not applicable | 77.37% | 344.0 | 78 | 12 |
| Identifying Core difficulty/ misconception attribution | 80.96% | 154.0 | 30 | 0 |
| Identifying incorrect steps by student | 86.50% | 111.0 | 21 | 2 |
| Identifying correct steps by student | 88.15% | 93.0 | 16 | 0 |
| Provides alternative solutions/ paths/ | 90.54% | 7.0 | 4 | 1 |

## Playbook Coverage

| Playbook | Rows | Mean ARRw |
| --- | ---: | ---: |
| none | 129 | 76.46% |
| chi-square variance-test adaptive explanation | 3 | 84.31% |
| CLT sample-mean active-learning hint | 2 | 100.00% |
| Gene X methylation/tumor-suppressor active hint | 1 | 70.27% |
| U-238/Pb-206 mass-ratio adaptive explanation | 1 | 63.41% |
| crackle derivative assessment | 1 | 62.96% |
| fastPower exponentiation active-learning hint | 1 | 76.19% |
| kinematics active-learning hint | 1 | 100.00% |
| lac-operon CAP-cAMP adaptive explanation | 1 | 75.56% |
| natural-selection misconception assessment | 1 | 67.74% |
| non-palindromic restriction-enzyme active hint | 1 | 100.00% |
| oxygen/CO2 cellular-respiration adaptive explanation | 1 | 61.54% |
| qualitative survey-variable assessment | 1 | 53.57% |
| sideways-parabola enclosed-area assessment | 1 | 84.21% |
| start-codon insertion mutation assessment | 1 | 100.00% |
| trig accumulation probability assessment | 1 | 83.61% |
| trig u-substitution adaptive explanation | 1 | 66.67% |
| velocity-time signed-area adaptive explanation | 1 | 100.00% |
| z-test vs t-test assessment | 1 | 100.00% |
