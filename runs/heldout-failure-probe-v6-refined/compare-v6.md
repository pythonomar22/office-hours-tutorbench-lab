# Heldout Failure Probe V6 Refined vs V6

- Source rows: same ten weakest rows from `heldout500-agentic-v5`.
- `heldout-failure-probe-v6` average: `64.42%`.
- `heldout-failure-probe-v6-refined` average: `59.12%`.
- Delta: `-5.30` points.

| Task | v6 | v6 refined | Delta |
| --- | ---: | ---: | ---: |
| `683e4517a08f8bb261597839` | 80.26% | 93.42% | +13.16 |
| `6843120a2b986bd2d9ca5f3f` | 6.25% | 21.88% | +15.62 |
| `6843120a9fab58968f2128c9` | 54.55% | 54.55% | +0.00 |
| `68376d91c5b329d497cbe8ca` | 26.83% | 24.39% | -2.44 |
| `683e4516d3bdf2dc57e053e3` | 90.38% | 90.38% | +0.00 |
| `683e458c2e254199a0fa2e02` | 51.22% | 26.83% | -24.39 |
| `683e3d8f3482feddb4d05e86` | 78.72% | 78.72% | +0.00 |
| `683e458eac89e71e0ce600c6` | 100.00% | 58.33% | -41.67 |
| `683e45162d501a5ab198c520` | 89.29% | 98.21% | +8.93 |
| `684a8cd6f08ce27c3bf577e0` | 66.67% | 44.44% | -22.22 |

The refinement helped several assessment rows but hurt active-learning rows, so
it should be validated on a larger split before being treated as a default win.
