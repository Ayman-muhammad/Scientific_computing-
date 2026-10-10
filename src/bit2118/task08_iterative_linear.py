"""Task 08 — Iterative Methods for Linear Systems (Jacobi & Gauss-Seidel).

Concept
-------
Jacobi and Gauss-Seidel start with an initial guess and repeatedly improve
it. For each equation, solve for one unknown using current estimates of
the others. Stop when the change between successive iterates falls below a
chosen tolerance. For diagonally-dominant systems both methods converge;
Gauss-Seidel typically converges about twice as fast because it uses the
latest available values within each sweep.

Mathematical formulation
------------------------
Write :math:`A = D + R` with :math:`D = \\mathrm{diag}(A)` and :math:`R`
the off-diagonal remainder.

* Jacobi: :math:`x^{(k+1)} = D^{-1}(b - R x^{(k)})`.
* Gauss-Seidel: :math:`x_i^{(k+1)} = \\bigl(b_i - \\sum_{j<i} A_{ij} x_j^{(k+1)}
  - \\sum_{j>i} A_{ij} x_j^{(k)}\\bigr) / A_{ii}`.

Real-world application
----------------------
Steady-state temperature on a 1-D grid with fixed boundary temperatures.
The system is large and sparse; iterative solvers avoid forming or
factoring the full matrix.

Interpretation of the output
----------------------------
* ``jacobi.x`` / ``gauss_seidel.x`` — interior temperatures in °C.
* ``jacobi.iterations`` / ``gauss_seidel.iterations`` — number of sweeps
  needed to reach :math:`\\|\\Delta x\\|_\\infty < 10^{-8}`.
* ``direct`` — reference solution from ``numpy.linalg.solve``.
* The figure plots the :math:`\\infty`-norm of the change per iteration
  on a logarithmic axis.
"""

from __future__ import annotations

import matplotlib

# Use the non-interactive Agg backend so the module runs on CI and
# headless Windows shells without requiring a display.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .io_utils import save_results
from .logging_config import configure_logging, get_logger
from .paths import FIGURES_DIR, ensure_dirs

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Inputs — 5-point 1-D steady-state heat conduction model
# -----------------------------------------------------------------------------
# Tridiagonal, symmetric, diagonally dominant. Interior grid points 1..5.
A: np.ndarray = np.array(
    [
        [2.0, -1.0, 0.0, 0.0, 0.0],
        [-1.0, 2.0, -1.0, 0.0, 0.0],
        [0.0, -1.0, 2.0, -1.0, 0.0],
        [0.0, 0.0, -1.0, 2.0, -1.0],
        [0.0, 0.0, 0.0, -1.0, 2.0],
    ],
    dtype=float,
)

# Boundary influence: left boundary = 100 °C, right boundary = 20 °C.
B: np.ndarray = np.array([100.0, 0.0, 0.0, 0.0, 20.0])

TOLERANCE: float = 1e-8
MAX_ITER: int = 500


# -----------------------------------------------------------------------------
# Iterative solvers
# -----------------------------------------------------------------------------
def jacobi(
    a: np.ndarray,
    b: np.ndarray,
    *,
    tol: float = TOLERANCE,
    max_iter: int = MAX_ITER,
) -> tuple[np.ndarray, list[float]]:
    """Jacobi iteration.

    Each new iterate uses only values from the previous sweep — perfectly
    parallelisable.

    Parameters
    ----------
    a : numpy.ndarray
        Coefficient matrix (diagonally dominant expected).
    b : numpy.ndarray
        Right-hand side.
    tol : float, optional
        Convergence threshold on the :math:`\\infty`-norm of the update.
    max_iter : int, optional
        Maximum number of sweeps.

    Returns
    -------
    x : numpy.ndarray
        Approximate solution.
    errors : list of float
        History of :math:`\\|x^{(k+1)} - x^{(k)}\\|_\\infty`.
    """
    d = np.diag(a)
    r = a - np.diagflat(d)
    x = np.zeros_like(b)
    errors: list[float] = []
    for _ in range(max_iter):
        x_new = (b - r @ x) / d
        err = float(np.linalg.norm(x_new - x, ord=np.inf))
        errors.append(err)
        if err < tol:
            return x_new, errors
        x = x_new
    return x, errors


def gauss_seidel(
    a: np.ndarray,
    b: np.ndarray,
    *,
    tol: float = TOLERANCE,
    max_iter: int = MAX_ITER,
) -> tuple[np.ndarray, list[float]]:
    """Gauss-Seidel iteration.

    Uses updated values as soon as they are computed, giving faster
    convergence at the cost of sequential dependency within a sweep.
    """
    x = np.zeros_like(b)
    errors: list[float] = []
    for _ in range(max_iter):
        old = x.copy()
        for i in range(len(b)):
            x[i] = (b[i] - a[i, :i] @ x[:i] - a[i, i + 1 :] @ old[i + 1 :]) / a[i, i]
        err = float(np.linalg.norm(x - old, ord=np.inf))
        errors.append(err)
        if err < tol:
            return x, errors
    return x, errors


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
def _plot_convergence(
    err_j: list[float],
    err_gs: list[float],
) -> None:
    """Log-scale convergence history for both methods."""
    ensure_dirs()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.semilogy(err_j, label="Jacobi", marker="o", markersize=3)
    ax.semilogy(err_gs, label="Gauss-Seidel", marker="s", markersize=3)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Maximum change (∞-norm)")
    ax.set_title("Convergence of iterative temperature solution")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "task08_iterative_convergence.png", dpi=200)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Solve the 1-D steady-state temperature model by both methods.

    Returns
    -------
    dict
        Keys: ``A``, ``b``, ``jacobi``, ``gauss_seidel``, ``direct``.
    """
    configure_logging()

    x_j, err_j = jacobi(A, B)
    x_gs, err_gs = gauss_seidel(A, B)
    x_direct = np.linalg.solve(A, B)

    logger.info("Jacobi solution:       %s (iters=%d)", np.round(x_j, 6), len(err_j))
    logger.info("Gauss-Seidel solution: %s (iters=%d)", np.round(x_gs, 6), len(err_gs))
    logger.info("Direct solution:       %s", np.round(x_direct, 6))
    logger.info(
        "Jacobi error vs direct:       %.3e", float(np.linalg.norm(x_j - x_direct, ord=np.inf))
    )
    logger.info(
        "Gauss-Seidel error vs direct: %.3e", float(np.linalg.norm(x_gs - x_direct, ord=np.inf))
    )

    _plot_convergence(err_j, err_gs)
    logger.info("Saved figure: %s", FIGURES_DIR / "task08_iterative_convergence.png")

    payload = {
        "A": A,
        "b": B,
        "jacobi": {"x": x_j, "iterations": len(err_j), "final_error": err_j[-1]},
        "gauss_seidel": {"x": x_gs, "iterations": len(err_gs), "final_error": err_gs[-1]},
        "direct": x_direct,
    }
    save_results("task08_iterative_linear", payload)
    return payload


if __name__ == "__main__":
    main()
