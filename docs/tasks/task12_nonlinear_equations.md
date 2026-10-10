# Task 12 — Polynomial and Nonlinear Equation Solving

**Module:** `bit2118.task12_nonlinear_equations`
**Concept:** Multi-equation root finding.
**Real-world anchor:** geometric intersection problems.

## 1. Concept
Nonlinear systems require iterative solvers that drive all residuals
toward zero. Multiple initial guesses may discover distinct roots.

## 2. Mathematical formulation
Circle: $x^2 + y^2 = 4$; parabola: $y = x^2 - 1$.

## 3. Algorithm
1. Define residuals as a 2-vector function of `[x, y]`.
2. Call `root` from two initial guesses to pick up both intersections.
3. Verify both residuals are near zero.

## 4. Inputs
Initial guesses: `(1, 1)` and `(-1, 1)`.

## 5. Outputs
Per guess: `solution`, `residuals`, `converged`.

## 6. Interpretation
Two symmetric intersections with residuals < $10^{-10}$. Extrapolating to
CAD or robot kinematics is direct: the same solver handles many such
constraint systems.