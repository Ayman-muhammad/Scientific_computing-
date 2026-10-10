"""Task 07 — Gaussian Elimination and LU Decomposition.

Concept
-------
Gaussian elimination transforms ``A x = b`` into an equivalent upper-
triangular system by eliminating variables one row at a time, then solves
by back-substitution. LU decomposition writes ``A = L U`` (or ``P A = L U``
with partial pivoting), where ``L`` is lower-triangular and ``U`` is
upper-triangular. Once ``A`` is factored, many different right-hand sides
``b`` can be solved cheaply with forward and back substitution.

Mathematical formulation
------------------------
For a fixed :math:`A \\in \\mathbb{R}^{n \\times n}`, factor once:

.. math::

    P A = L U

Then, for each :math:`b_k`, solve in two triangular sweeps:

.. math::

    L y = P b_k \\quad \\text{(forward)}, \\qquad
    U x = y       \\quad \\text{(back)}

Cost: :math:`O(n^3)` once for the factorisation, then :math:`O(n^2)`
per right-hand side — versus :math:`O(n^3)` per solve for naive
Gaussian elimination.

Real-world application
----------------------
A simulation reuses the same coefficient matrix ``A`` every second but
receives a new measurement vector ``b``. Factor once, solve many.

Interpretation of the output
----------------------------
* ``results[i].solution`` — the solution vector for the ``i``-th ``b``.
* ``results[i].residual_norm`` — :math:`\\|b - A x\\|_2`; near-zero
  confirms accuracy.
* ``direct_first`` — reference solution via ``numpy.linalg.solve`` used
  to validate the LU path.
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import lu_factor, lu_solve

from .io_utils import save_results
from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Inputs — a fixed 3×3 SPD-like system reused across several measurements
# -----------------------------------------------------------------------------
A: np.ndarray = np.array(
    [
        [4.0, -1.0, 0.0],
        [-1.0, 4.0, -1.0],
        [0.0, -1.0, 3.0],
    ],
    dtype=float,
)

MEASUREMENT_SETS: list[np.ndarray] = [
    np.array([15.0, 10.0, 10.0]),
    np.array([16.0, 11.0, 9.0]),
    np.array([14.0, 12.0, 11.0]),
]


# -----------------------------------------------------------------------------
# Pure functions
# -----------------------------------------------------------------------------
def factor_once(a: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return ``(lu, piv)`` from a single LU factorisation of ``a``."""
    lu, piv = lu_factor(a)
    return lu, piv


def solve_with_factor(
    lu: np.ndarray,
    piv: np.ndarray,
    a: np.ndarray,
    b: np.ndarray,
) -> tuple[np.ndarray, float]:
    """Solve ``a x = b`` using precomputed LU factors.

    Parameters
    ----------
    lu, piv : numpy.ndarray
        Output of :func:`factor_once`.
    a : numpy.ndarray
        The original coefficient matrix (used only for the residual).
    b : numpy.ndarray
        Right-hand side.

    Returns
    -------
    x : numpy.ndarray
        Solution vector.
    residual_norm : float
        :math:`\\|b - a x\\|_2`.
    """
    x = lu_solve((lu, piv), b)
    residual_norm = float(np.linalg.norm(b - a @ x))
    return x, residual_norm


def solve_all(
    a: np.ndarray,
    bs: list[np.ndarray],
) -> list[dict[str, object]]:
    """Factor ``a`` once and solve for every ``b`` in ``bs``."""
    lu, piv = factor_once(a)
    rows: list[dict[str, object]] = []
    for index, b in enumerate(bs, start=1):
        x, residual_norm = solve_with_factor(lu, piv, a, b)
        rows.append(
            {
                "set": index,
                "b": b,
                "solution": x,
                "residual_norm": residual_norm,
            }
        )
    return rows


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Demonstrate LU reuse across multiple right-hand sides.

    Returns
    -------
    dict
        Keys: ``A``, ``results`` (list of per-measurement dicts),
        ``direct_first``.
    """
    configure_logging()

    results = solve_all(A, MEASUREMENT_SETS)
    direct_first = np.linalg.solve(A, MEASUREMENT_SETS[0])

    logger.info("Coefficient matrix A:\n%s", A)
    logger.info(
        "LU factorisation computed once; solving %d right-hand sides.", len(MEASUREMENT_SETS)
    )

    for row in results:
        logger.info("Set %d", row["set"])
        logger.info("  b           = %s", row["b"])
        logger.info("  x           = %s", np.round(row["solution"], 6))
        logger.info("  ‖b − Ax‖    = %.3e", row["residual_norm"])

    logger.info("Direct solve for set 1 (validation): %s", np.round(direct_first, 6))

    payload = {
        "A": A,
        "results": results,
        "direct_first": direct_first,
    }
    save_results("task07_gaussian_lu", payload)
    return payload


if __name__ == "__main__":
    main()
