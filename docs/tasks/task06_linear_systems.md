# Task 06 — Solution of Systems of Linear Equations

**Module:** `bit2118.task06_linear_systems`
**Concept:** $A x = b$ via LU with partial pivoting.
**Real-world anchor:** server resource allocation.

## 1. Concept
Many problems reduce to $A x = b$. Solving means finding $x$ such that
multiplying $A$ by $x$ reproduces $b$.

## 2. Mathematical formulation
Unique solution $x = A^{-1} b$ for non-singular $A$.
`np.linalg.solve` uses LAPACK `dgesv`.

## 3. Algorithm
1. Form $A$ (rows = resource constraints; columns = server types).
2. Form $b$ (observed totals).
3. Solve with `np.linalg.solve`; verify with residual.

## 4. Inputs
| Name | Value | Units |
|------|-------|-------|
| CPU per A / B | 4 / 2 | units |
| RAM per A / B | 8 / 12 | GB |
| Total CPU / RAM | 20 / 72 | units / GB |

## 5. Outputs
`solution` (server counts), `residual`, `residual_norm`.

## 6. Interpretation
Solution `[2, 6]` means 2 Type-A and 6 Type-B servers. Residual norm
≈ 0 confirms exact satisfaction of both resource totals.