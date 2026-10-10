# Task 15 — Numerical Differentiation

**Module:** `bit2118.task15_numerical_differentiation`
**Concept:** Forward / central / backward differences.
**Real-world anchor:** GPS speed estimation.

## 1. Concept
Approximate derivatives from nearby samples. Central differences are
second-order accurate; one-sided forms are first-order.

## 2. Mathematical formulation
See [mathematical notes](../mathematical_notes.md#task-15--numerical-differentiation).

## 3. Algorithm
1. Forward at the first sample.
2. Central at every interior sample.
3. Backward at the last sample.

## 4. Inputs
7 GPS samples at 1-second intervals.

## 5. Outputs
`time`, `position`, `speed`, `max_speed`, `mean_speed`.

## 6. Interpretation
The estimated speed profile is smooth and monotone; the boundary
treatment avoids the usual start/end truncation bias.