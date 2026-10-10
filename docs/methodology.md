# Methodology

## Choosing inputs

Each task anchors to a **concrete real-world scenario** (weather station,
RC circuit, cloud planner, …). Inputs are chosen so that:

* The expected answer is either **analytically known** (e.g. RC charging,
  cooling) or **independently verifiable** (e.g. `A @ x ≈ b`).
* Values are **physically plausible** — no missing units, no absurd
  magnitudes.
* Every input is **named at the top of the module** as a module-level
  constant so it can be changed in one place.

## Choosing tolerances

| Context | Tolerance | Rationale |
|---------|-----------|-----------|
| Iterative linear solvers | `1e-8` (∞-norm) | Below displayed precision, above FP noise. |
| Root finders | `xtol=1e-10` | Machine-adjacent but stable. |
| ODE integration | `rtol=1e-9`, `atol=1e-11` | Near-exact for smooth problems. |
| FP comparisons | `np.isclose` defaults | 1e-5 relative, 1e-8 absolute. |

## Verification strategy

For each task we verify against one of:

1. **Analytical solution** — e.g. cooling has a closed-form exponential.
2. **Independent SciPy routine** — e.g. `np.linalg.solve` vs LU factor.
3. **Invariant** — e.g. `A v = λ v` for eigenpairs; `A x = b` for linear
   solves; centrality sums to 1.
4. **Monotonicity / physicality** — e.g. temperature decreases over time.

Where possible, more than one is used.