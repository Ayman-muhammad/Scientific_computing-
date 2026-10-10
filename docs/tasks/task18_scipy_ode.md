# Task 18 — Numerical Solution of ODEs Using SciPy

**Module:** `bit2118.task18_scipy_ode`
**Concept:** Adaptive RK45 integration via `solve_ivp`.
**Real-world anchor:** RC circuit charging.

## 1. Concept
Adaptive higher-order solvers refine step sizes to keep local error below
a tolerance. For smooth problems they match the analytic solution to
near machine precision.

## 2. Mathematical formulation
$dV/dt = (V_s - V)/(R C)$ with closed-form
$V(t) = V_s (1 - e^{-t/(RC)})$.

## 3. Algorithm
1. Define `rc_circuit(t, V)`.
2. `solve_ivp(..., rtol=1e-9, atol=1e-11, t_eval=...)`.
3. Compare against exact.

## 4. Inputs
| Name | Value |
|------|-------|
| Vs | 5 V |
| R | 1000 Ω |
| C | 1 mF |
| τ = RC | 1 s |

## 5. Outputs
`v`, `exact`, `max_error`, `success`, `nfev`.

## 6. Interpretation
Solver success; max error ≤ $10^{-6}$ V. The capacitor reaches ≈ 5 V
after 5τ, as expected from first-order dynamics.