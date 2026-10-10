# Task 13 — Interpolation

**Module:** `bit2118.task13_interpolation`
**Concept:** Linear vs. cubic-spline interpolation.
**Real-world anchor:** upsampling hourly sensor data to 10-minute
resolution.

## 1. Concept
Interpolation estimates values between known samples. Cubic splines
preserve smoothness, avoiding the piecewise-linear "corners".

## 2. Mathematical formulation
See [mathematical notes](../mathematical_notes.md#task-13--interpolation).

## 3. Algorithm
1. Build `interp1d(kind="linear")` and `CubicSpline`.
2. Evaluate both on a 10-minute grid.
3. Report values at 10:30.

## 4. Inputs
7 hourly temperatures, 18 → 25 °C.

## 5. Outputs
`linear_at_10_30`, `cubic_at_10_30`, plus dense grid and estimates.

## 6. Interpretation
Both estimates ≈ 23.2 °C, differing by a few tenths of a degree. Cubic
splines are preferable when the downstream model assumes smooth signals.