# Task 11 — Root Finding: Newton-Raphson and Secant Methods

**Module:** `bit2118.task11_newton_secant`
**Concept:** Derivative-aware and derivative-free root finders.
**Real-world anchor:** internal rate of return (IRR).

## 1. Concept
Newton uses the tangent line; secant uses a finite-difference slope.
Both converge faster than bisection near a simple root.

## 2. Mathematical formulation
$\mathrm{NPV}(r) = \sum_t \mathrm{CF}_t / (1+r)^t$. IRR solves $\mathrm{NPV}(r) = 0$.

## 3. Algorithm
1. Define NPV and its analytic derivative.
2. `root_scalar(..., method="newton")`.
3. `root_scalar(..., method="secant", x0=0.05, x1=0.20)`.

## 4. Inputs
| Name | Value |
|------|-------|
| cash flows | −10k, 3k, 3.5k, 4k, 2.5k |
| Newton start | 0.10 |
| Secant starts | 0.05, 0.20 |

## 5. Outputs
`newton.{irr, iterations}`, `secant.{irr, iterations}`, `npv_at_newton`.

## 6. Interpretation
Both methods converge to the same IRR (≈ 11.4%). NPV at the root is
< $10^{-9}$.