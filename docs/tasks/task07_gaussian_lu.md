# Task 07 — Gaussian Elimination and LU Decomposition

**Module:** `bit2118.task07_gaussian_lu`
**Concept:** Factor once, solve many.
**Real-world anchor:** repeated measurement solves in a simulation.

## 1. Concept
LU writes $P A = L U$. Once factored, many right-hand sides solve in
$O(n^2)$ each via forward/back substitution.

## 2. Mathematical formulation
$P A = L U$, then $L y = P b$, then $U x = y$.

## 3. Algorithm
1. `lu_factor(A)` → `(lu, piv)`.
2. For each $b$: `lu_solve((lu, piv), b)`.
3. Compute residual $\|b - A x\|_2$.
4. Compare the first solution to `np.linalg.solve` for validation.

## 4. Inputs
| Name | Value |
|------|-------|
| `A` | 3×3 SPD-like matrix |
| `MEASUREMENT_SETS` | 3 vectors |

## 5. Outputs
Per-set: `solution`, `residual_norm`. Also `direct_first` for validation.

## 6. Interpretation
All three solves reuse one factorisation. All residuals are below
$10^{-10}$, confirming accuracy. The savings matter more as $n$ grows.