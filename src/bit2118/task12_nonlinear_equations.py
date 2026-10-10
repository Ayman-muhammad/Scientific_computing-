"""Task 12 — Polynomial and Nonlinear Equation Solving.

Concept
-------
A polynomial equation has the form
:math:`a_n x^n + \\dots + a_1 x + a_0 = 0`. A nonlinear *system* contains
equations that are not all linear in the unknowns. Numerical solvers search
for values that make every residual simultaneously close to zero, using
iterative Newton-like updates.

Mathematical formulation
------------------------
Solve the vector system :math:`F(z) = 0` where
:math:`F : \\mathbb{R}^n \\to \\mathbb{R}^n`. ``scipy.optimize.root``
implements a hybrid (Powell) method that combines Newton steps with
trust-region safeguards. Each initial guess may lead to a different root
of a nonlinear system.

Real-world application
----------------------
Find the intersection points between a circle and a parabola — a typical
task in CAD, geometric constraint solving, and control-system operating
points.

Interpretation of the output
----------------------------
* ``results[i].solution`` — intersection coordinates ``(x, y)``.
* ``results[i].residuals`` — values of both residual equations at the
  solution; near-zero confirms accuracy.
* ``results[i].converged`` — boolean from the solver.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import root

from .io_utils import save_results
from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Inputs
# -----------------------------------------------------------------------------
# Circle:   x² + y² = 4
# Parabola: y = x² - 1
#
# Two intersection points exist (mirror images about the y-axis). We seed
# the solver with one positive-x and one negative-x initial guess to
# retrieve both.
INITIAL_GUESSES: tuple[tuple[float, float], ...] = (
    (1.0, 1.0),
    (-1.0, 1.0),
)


# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------
def equations(z: np.ndarray) -> list[float]:
    """Circle and parabola residuals.

    Parameters
    ----------
    z : array_like, shape (2,)
        ``[x, y]``.

    Returns
    -------
    list of float
        ``[x² + y² - 4, y - (x² - 1)]``. Both are zero at an intersection.
    """
    x, y = z
    return [x**2 + y**2 - 4.0, y - (x**2 - 1.0)]


# -----------------------------------------------------------------------------
# Solving
# -----------------------------------------------------------------------------
def find_intersections(
    guesses: tuple[tuple[float, float], ...] = INITIAL_GUESSES,
) -> list[dict[str, object]]:
    """Solve the system from each initial guess.

    Parameters
    ----------
    guesses : sequence of (float, float)
        Initial ``(x, y)`` guesses.

    Returns
    -------
    list of dict
        One record per guess with keys ``guess``, ``solution``,
        ``residuals``, ``converged``, ``message``.
    """
    rows: list[dict[str, object]] = []
    for guess in guesses:
        sol = root(equations, np.asarray(guess, dtype=float))
        rows.append(
            {
                "guess": list(guess),
                "solution": sol.x,
                "residuals": equations(sol.x),
                "converged": bool(sol.success),
                "message": str(sol.message),
            }
        )
    return rows


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Find both intersections of the circle and parabola.

    Returns
    -------
    dict
        Keys: ``equations`` (as a list of strings for reference),
        ``results``.
    """
    configure_logging()

    results = find_intersections()

    for row in results:
        logger.info(
            "guess=%s → (x, y) = %s  residual=%s  converged=%s",
            row["guess"],
            np.round(row["solution"], 6),
            np.round(row["residuals"], 12),
            row["converged"],
        )

    # Sanity check: both roots should satisfy both equations.
    max_residual = max(max(abs(r) for r in row["residuals"]) for row in results)
    logger.info("Maximum residual across all roots: %.3e", max_residual)

    payload = {
        "equations": [
            "x² + y² - 4 = 0",
            "y - (x² - 1) = 0",
        ],
        "initial_guesses": [list(g) for g in INITIAL_GUESSES],
        "results": results,
        "max_residual": float(max_residual),
    }
    save_results("task12_nonlinear_equations", payload)
    return payload


if __name__ == "__main__":
    main()
