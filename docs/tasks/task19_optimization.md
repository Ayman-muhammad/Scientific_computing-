# Task 19 — Numerical Optimization

**Module:** `bit2118.task19_optimization`
**Concept:** Constrained continuous and integer optimisation.
**Real-world anchor:** cloud capacity planning.

## 1. Concept
Minimise a cost function subject to inequality constraints and bounds.
SLSQP handles smooth nonlinear problems; for whole-server deployment we
search integer combinations.

## 2. Mathematical formulation
$\min 12x + 18y$ s.t. $100x + 170y \ge 1000$, $x, y \ge 0$.

## 3. Algorithm
1. Run SLSQP on the continuous relaxation.
2. Enumerate integer allocations in a small box.
3. Report cost gap between the two.

## 4. Inputs
| Name | Value |
|------|-------|
| cost_A / cost_B | 12 / 18 |
| cap_A / cap_B | 100 / 170 |
| required capacity | 1000 |

## 5. Outputs
`continuous.{x, y, cost, capacity}`, `integer.{a, b, cost, capacity}`,
`gap`.

## 6. Interpretation
Continuous optimum ≈ 105.9; integer optimum = 106. A small gap suggests
the LP relaxation is nearly tight — operationally, whole-server costs are
close to the theoretical minimum.