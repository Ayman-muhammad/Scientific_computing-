
---

## F. Task pages (`docs/tasks/`)

Each page is compact and follows the six-section template. Create the
`docs/tasks/` folder and drop these files in.

### `docs/tasks/task02_numpy_arrays.md`

```markdown
# Task 02 — NumPy Arrays and Numerical Computation

**Module:** `bit2118.task02_numpy_arrays`
**Concept:** 1-D arrays and element-wise operations.
**Real-world anchor:** 24-hour weather station.

## 1. Concept
An array is an ordered collection of numbers of the same dtype. A vector
is 1-D; a matrix is 2-D. NumPy evaluates an operation over every element
in one call.

## 2. Mathematical formulation
Given $x = [x_1, \dots, x_n]$ and $f(x) = 1.8x + 32$, NumPy computes
$f(x) = [f(x_1), \dots, f(x_n)]$ without a Python-level loop. Sample mean
$\bar{x} = \frac{1}{n}\sum_i x_i$.

## 3. Algorithm
1. Store the 24 Celsius readings as `np.ndarray(dtype=float)`.
2. Compute mean, min, max via vectorised reductions.
3. Apply `1.8 * x + 32` to the whole array (broadcast).

## 4. Inputs and parameters
| Name | Value | Units | Source |
|------|-------|-------|--------|
| `TEMPERATURES_C` | 24 values | °C | synthetic daily curve |

## 5. Outputs
`results/task02_numpy_arrays.json`: `mean_c`, `min_c`, `max_c`,
`fahrenheit` (vector of 24 converted readings).

## 6. Interpretation
The daily mean of ≈ 23 °C is consistent with a mild spring day. The
Fahrenheit conversion demonstrates that the same arithmetic expression
applies to a whole vector — no loops, no manual indexing.

**Parameter sensitivity.** Changing any single reading alters `mean_c` by
$1/24$ of the perturbation; `min_c`/`max_c` only change if the new value
exceeds the current extremes.