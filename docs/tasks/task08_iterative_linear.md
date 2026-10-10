# Task 08 — Iterative Methods for Linear Systems

**Module:** `bit2118.task08_iterative_linear`
**Concept:** Jacobi and Gauss-Seidel.
**Real-world anchor:** 1-D steady-state heat conduction.

## 1. Concept
Iterative solvers start from a guess and refine, stopping when successive
estimates change by less than a tolerance. They suit large, sparse
systems where factorisation is expensive.

## 2. Mathematical formulation
Write $A = D + R$. Jacobi and Gauss-Seidel updates as in
[`mathematical_notes.md`](../mathematical_notes.md#task-08--jacobi--gauss-seidel).

## 3. Algorithm
1. Build a diagonally-dominant 5×5 tridiagonal $A$.
2. Set boundary influence via $b$.
3. Run Jacobi and Gauss-Seidel to $\infty$-norm change $< 10^{-8}$.
4. Compare each solution to the direct `np.linalg.solve`.

## 4. Inputs
| Name | Value |
|------|-------|
| interior grid points | 5 |
| left boundary | 100 °C |
| right boundary | 20 °C |
| tolerance | $10^{-8}$ |

## 5. Outputs
`jacobi.{x, iterations, final_error}`,
`gauss_seidel.{x, iterations, final_error}`, `direct`.

## 6. Interpretation
Gauss-Seidel converges in fewer iterations because it uses updated values
within each sweep. Both match the direct solution to $10^{-6}$.