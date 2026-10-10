# Task 16 — Numerical Integration

**Module:** `bit2118.task16_numerical_integration`
**Concept:** Trapezoidal and Simpson quadrature.
**Real-world anchor:** energy from smart-meter power readings.

## 1. Concept
Numerical integration sums small contributions of a discrete signal to
approximate the area under the curve.

## 2. Mathematical formulation
Trapezoidal and Simpson rules as in
[mathematical notes](../mathematical_notes.md#task-16--numerical-integration).

## 3. Algorithm
1. Read 7 power samples over 12 hours.
2. `np.trapezoid` and `scipy.integrate.simpson`.
3. Report both and their difference.

## 4. Inputs
2-hour sampling; power 0.8 → 1.8 kW.

## 5. Outputs
`trapezoidal_kwh`, `simpson_kwh`, `difference_kwh`.

## 6. Interpretation
The two rules agree closely. The difference is a proxy for how
under-resolved the data is; a large difference signals a need for
higher-frequency sampling.