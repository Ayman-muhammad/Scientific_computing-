# Task 03 — Mathematical Functions and Vectorization

**Module:** `bit2118.task03_vectorization`
**Concept:** Vectorised arithmetic.
**Real-world anchor:** 1 M network latency samples.

## 1. Concept
Vectorisation applies an operation to an array at once. NumPy evaluates
`(x / 1000)**2` in C over the entire array without a Python loop.

## 2. Mathematical formulation
$y_i = (x_i / 1000)^2$ element-wise.

## 3. Algorithm
1. Draw 1,000,000 uniform samples in `[5, 250]` ms with a fixed seed.
2. Time a pure-Python `for` loop that converts and squares.
3. Time the equivalent vectorised NumPy expression.
4. Report `speedup = loop_time / vector_time`.

## 4. Inputs and parameters
| Name | Value | Units |
|------|-------|-------|
| `N_SAMPLES` | 1,000,000 | samples |
| `SEED` | 42 | — |
| latency range | 5 – 250 | ms |

## 5. Outputs
`loop_time_s`, `vector_time_s`, `speedup`, `first_five`.

## 6. Interpretation
A speedup of 20–100× is typical on a laptop. The figure is conceptual
(the bar chart in the report): vectorised code wins by exploiting SIMD
and avoiding per-element Python overhead.