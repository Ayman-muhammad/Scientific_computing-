# Task 10 — Root Finding: Bisection and Fixed-Point Methods

**Module:** `bit2118.task10_bisection_fixed_point`
**Concept:** Bracketing and fixed-point iteration.
**Real-world anchor:** equilibrium temperature of a nonlinear heat balance.

## 1. Concept
Bisection halves a sign-changing interval; fixed-point iteration solves
$x = g(x)$ by repeated substitution.

## 2. Mathematical formulation
$f(T) = T - 25 - 10 e^{-T/20} = 0$ rewritten as $T = 25 + 10 e^{-T/20}$.

## 3. Algorithm
1. Bracket the root in $[20, 40]$.
2. Bisect with `root_scalar(..., method="bisect")`.
3. Iterate $T_{n+1} = g(T_n)$ from $T_0 = 30$.

## 4. Inputs
| Name | Value |
|------|-------|
| bracket | [20, 40] |
| initial guess | 30 °C |
| tolerance | $10^{-10}$ |

## 5. Outputs
`bisection.{root, iterations, bracket}`,
`fixed_point.{root, iterations, history}`.

## 6. Interpretation
Both methods find ≈ 30.84 °C. Bisection is robust but linear; fixed-point
converges geometrically because $|g'(r)| < 1$.