
### `report/report.md`

```markdown
# BIT 2118 Scientific Computing — Group Work Report

**Author:** Ayman Muhammad
**Repository:** https://github.com/Ayman-muhammad/Scientific_computing-
**Date:** _fill in submission date_

---

## 1. Introduction

This report presents the implementation and interpretation of Tasks 02
through 20 of the BIT 2118 Scientific Computing group-work brief. Every
task is packaged as an independently runnable Python module under
`src/bit2118/`. Each module produces:

* a **machine-readable result** in `results/*.json`,
* a **figure** in `report/figures/` (where a plot adds interpretive value),
* a **documented derivation** in `docs/tasks/`.

All numerical results quoted below are reproducible with a single command
(`python -m bit2118`) on a clean clone.

---

## 2. Summary of tasks

| # | Task | Headline result |
|---|------|-----------------|
| 02 | NumPy arrays | Daily mean 23.0 °C; vectorised C→F conversion. |
| 03 | Vectorisation | ~20–100× speed-up over a Python loop on 1 M samples. |
| 04 | Floating-point | `0.1 + 0.2 != 0.3`; stable rewrite recovers accuracy. |
| 05 | Matrix algebra | Combined rotation × scale, `det(T) = sx·sy`. |
| 06 | Linear systems | Server allocation `(2, 6)`; residual ‖·‖ ≈ 0. |
| 07 | LU decomposition | 3 solves reuse 1 factorisation; all residuals < 1e-10. |
| 08 | Iterative linear | Jacobi and Gauss-Seidel match direct solve to 1e-6. |
| 09 | Eigenvalues | Centrality scores sum to 1; node C ranks highest. |
| 10 | Bisection / fixed-point | Equilibrium temperature ≈ 30.84 °C. |
| 11 | Newton / secant | IRR ≈ 11.4%; NPV at root < 1e-9. |
| 12 | Nonlinear systems | Two symmetric circle∩parabola intersections. |
| 13 | Interpolation | 10-minute upsample; cubic vs linear differ by < 0.5 °C. |
| 14 | Curve fitting | Quadratic response-time model; RMSE < 3 ms. |
| 15 | Numerical differentiation | GPS speed profile, boundary-correct. |
| 16 | Numerical integration | Daily energy ≈ 15 kWh; trap vs Simpson agree. |
| 17 | Euler ODE | Cooling curve; final error < 0.3 °C. |
| 18 | solve_ivp | RC charging; max error vs analytic < 1e-6 V. |
| 19 | Optimisation | Cloud cost ≈ 106 units; integer gap small. |
| 20 | Monte Carlo | Overload probability ≈ 10.5%, matches theory. |

_(Add graphs inline below each task as needed. Every figure is referenced
by filename from `report/figures/`.)_

---

## 3. Methodology

### 3.1 Inputs

Each task anchors to a concrete real-world scenario (weather station, RC
circuit, cloud planner, network, GPS unit, smart meter). Inputs are chosen
so that expected answers are either analytically known or independently
verifiable, and every input is documented at the top of its module.

### 3.2 Verification strategy

Three independent checks are used, where possible:

1. **Analytical reference** — e.g. RC charging and cooling have closed
   forms.
2. **Independent SciPy routine** — e.g. LU vs direct solve, `solve_ivp`
   vs analytical.
3. **Invariant assertions** — e.g. $A v = \lambda v$ for eigenpairs,
   centrality sums to 1, capacity constraint satisfied.

### 3.3 Parameter sensitivity

Each `main()` is parameterised at the top of its module. Changing any
single parameter and re-running updates both the JSON result and any
associated figure. Example: increasing the Euler step `H` from 1 min to
2 min roughly doubles the final cooling error, confirming first-order
convergence.

---

## 4. Results and interpretation

For each task, a dedicated page in `docs/tasks/` documents:

1. Concept
2. Mathematical formulation
3. Algorithm
4. Inputs and parameters
5. Outputs
6. Interpretation

The report refers to those pages rather than duplicating them.

---

## 5. Reproducibility

```bash
git clone https://github.com/Ayman-muhammad/Scientific_computing-.git
cd Scientific_computing-
python -m venv .venv && source .venv/Scripts/activate     # Windows MINGW
pip install -e ".[dev]"
python -m bit2118                                          # regenerate
pytest -v                                                  # verify