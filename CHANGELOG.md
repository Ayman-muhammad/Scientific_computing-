# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- (nothing yet)

### Changed
- (nothing yet)

### Fixed
- (nothing yet)

---

## [1.0.0] — 2025-01-01

### Added

- **Initial release.** Tasks 02 → 20 implemented as a `src/`-layout Python
  package under `bit2118`.
- **Package core.**
  - `paths.py` — canonical filesystem locations for figures and results.
  - `logging_config.py` — shared logger setup with timestamped format.
  - `io_utils.py` — JSON persistence with NumPy-aware serialisation.
  - `registry.py` — task registry used by the batch runner.
  - `__main__.py` — `python -m bit2118` executes every task.
- **Task modules (19 total).**
  - `task02_numpy_arrays` — vectorised weather-station statistics.
  - `task03_vectorization` — latency pipeline benchmark (loop vs vector).
  - `task04_floating_point` — FP error demo + stability rewrite.
  - `task05_matrix_algebra` — 2-D graphics transform (rotate + scale).
  - `task06_linear_systems` — server resource allocation via `A x = b`.
  - `task07_gaussian_lu` — LU factor-once, solve-many.
  - `task08_iterative_linear` — Jacobi vs Gauss-Seidel convergence.
  - `task09_eigenvalues` — eigenvector centrality on a small network.
  - `task10_bisection_fixed_point` — heat-balance equilibrium.
  - `task11_newton_secant` — internal rate of return.
  - `task12_nonlinear_equations` — circle ∩ parabola intersections.
  - `task13_interpolation` — linear vs cubic spline upsampling.
  - `task14_curve_fitting` — quadratic response-time model.
  - `task15_numerical_differentiation` — GPS speed estimation.
  - `task16_numerical_integration` — smart-meter energy totals.
  - `task17_euler_ode` — Newton's law of cooling.
  - `task18_scipy_ode` — RC circuit charging with `solve_ivp`.
  - `task19_optimization` — cloud capacity planning (SLSQP + integer).
  - `task20_monte_carlo` — server-overload risk estimation.
- **Tests.** Pytest suite covering each task's mathematical core, plus
  utility modules (`paths`, `io_utils`).
- **Documentation.**
  - `docs/architecture.md` — package design rationale.
  - `docs/mathematical_notes.md` — derivations.
  - `docs/methodology.md` — input and tolerance choices.
  - `docs/reproducibility.md` — reproduction checklist.
  - `docs/tasks/*.md` — one page per task.
- **Report scaffolding.** `report/report.md` and `report/figures/`.
- **Results contract.** `results/*.json` with a common schema.
- **Continuous integration.** `.github/workflows/ci.yml` runs ruff + pytest
  across Python 3.10, 3.11, 3.12.
- **Developer ergonomics.** `Makefile` targets: `install`, `run`, `test`,
  `lint`, `format`, `clean`, `tree`.

### Security

- No network I/O, no shell execution, no dynamic code evaluation.

[Unreleased]: https://github.com/Ayman-muhammad/Scientific_computing-/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Ayman-muhammad/Scientific_computing-/releases/tag/v1.0.0