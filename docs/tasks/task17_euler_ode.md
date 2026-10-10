# Task 17 — Ordinary Differential Equations: Euler Method

**Module:** `bit2118.task17_euler_ode`
**Concept:** First-order explicit time-stepping.
**Real-world anchor:** Newton's law of cooling.

## 1. Concept
Euler steps $y_{n+1} = y_n + h f(t_n, y_n)$. Simple and universal but
only first-order accurate.

## 2. Mathematical formulation
$dT/dt = -k(T - T_\text{ambient})$, closed-form $T(t)$ as in
[mathematical notes](../mathematical_notes.md#task-17--euler-method).

## 3. Algorithm
1. Initialise $T_0 = 90$ °C, $T_\text{amb} = 25$ °C, $k = 0.12$ 1/min.
2. Step with $h = 1$ min for 30 min.
3. Compare to the analytic curve.

## 4. Inputs
See above.

## 5. Outputs
`temperature`, `exact`, `final_euler`, `final_exact`, `final_error`,
`max_error`.

## 6. Interpretation
Final numerical temperature ≈ 27.2 °C versus exact ≈ 27.0 °C — a ~0.2 °C
discretisation bias. Halving $h$ halves that error, confirming first-order
convergence.