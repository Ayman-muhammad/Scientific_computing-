"""Task 06 — Solution of Systems of Linear Equations.

Concept
-------
Many problems reduce to :math:`A x = b`, where ``A`` holds coefficients,
``x`` holds unknowns, and ``b`` holds known results. Solving the system
means finding the vector ``x`` such that multiplying ``A`` by ``x``
reproduces ``b``.

Mathematical formulation
------------------------
For a square, non-singular matrix :math:`A \\in \\mathbb{R}^{n \\times n}`
the unique solution is :math:`x = A^{-1} b`. Numerically,
``numpy.linalg.solve`` uses LU factorisation with partial pivoting
(LAPACK ``dgesv``), which is both faster and more stable than forming
:math:`A^{-1}` explicitly.

Real-world application
----------------------
Two server types consume different amounts of CPU and memory. Given the
total observed CPU and memory usage, determine how many servers of each
type are active.

Interpretation of the output
----------------------------
* ``solution`` — number of Type A and Type B servers.
* ``residual_norm`` — :math:`\\|b - A x\\|_2`; near zero confirms the
  solve is accurate.
"""

from __future__ import annotations

import numpy as np

from .io_utils import save_results
from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Inputs — server resource model
# -----------------------------------------------------------------------------
# Each row is one resource constraint; columns are [Type A, Type B].
#   Row 1: CPU units per server        → 4 (A), 2  (B)
#   Row 2: Memory (GB) per server      → 8 (A), 12 (B)
# Right-hand side: observed totals (20 CPU units, 72 GB RAM).
A: np.ndarray = np.array([[4.0, 2.0], [8.0, 12.0]])
B: np.ndarray = np.array([20.0, 72.0])


# -----------------------------------------------------------------------------
# Pure functions
# -----------------------------------------------------------------------------
def solve_system(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Solve ``a x = b`` and return ``(x, residual)``.

    Parameters
    ----------
    a : numpy.ndarray
        Square coefficient matrix, shape ``(n, n)``.
    b : numpy.ndarray
        Right-hand side, shape ``(n,)`` or ``(n, k)``.

    Returns
    -------
    x : numpy.ndarray
        Solution vector (or matrix).
    residual : numpy.ndarray
        ``b - a @ x``; near zero indicates a well-conditioned solve.

    Raises
    ------
    numpy.linalg.LinAlgError
        If ``a`` is singular.
    """
    x = np.linalg.solve(a, b)
    residual = b - a @ x
    return x, residual


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Solve the server-allocation system and verify the residual.

    Returns
    -------
    dict
        Keys: ``A``, ``b``, ``solution``, ``residual``, ``residual_norm``,
        ``verification``.
    """
    configure_logging()

    solution, residual = solve_system(A, B)
    residual_norm = float(np.linalg.norm(residual))

    logger.info("Coefficient matrix A:\n%s", A)
    logger.info("Right-hand side b:  %s", B)
    logger.info("Solution x:         %s", np.round(solution, 6))
    logger.info("  → Type A servers: %.4f", solution[0])
    logger.info("  → Type B servers: %.4f", solution[1])
    logger.info("Verification A @ x: %s", A @ solution)
    logger.info("Residual norm ‖b - Ax‖: %.3e", residual_norm)

    payload = {
        "A": A,
        "b": B,
        "solution": solution,
        "residual": residual,
        "residual_norm": residual_norm,
        "verification": A @ solution,
    }
    save_results("task06_linear_systems", payload)
    return payload


if __name__ == "__main__":
    main()
