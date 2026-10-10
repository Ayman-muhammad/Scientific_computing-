"""Task 19 — Numerical Optimization.

Concept
-------
Optimisation finds the input values that minimise or maximise an objective
function, subject to constraints and bounds. The Sequential Least Squares
Programming (SLSQP) algorithm handles smooth nonlinear objectives with
equality and inequality constraints and box bounds.

Mathematical formulation
------------------------
Minimise :math:`f(z)` subject to

.. math::

    g(z) &\\ge 0 \\quad \\text{(inequality constraint)} \\\\
    a &\\le z \\le b \\quad \\text{(bounds)}

Here we solve a cloud capacity-planning problem:

.. math::

    \\min_{x, y} \\; 12 x + 18 y
    \\quad \\text{s.t.} \\quad 100 x + 170 y \\ge 1000,\\; x, y \\ge 0

Where :math:`x` and :math:`y` are allocation units of two server types.

Real-world application
----------------------
Cloud capacity planning: choose server counts of two types to minimise
cost while meeting a minimum processing capacity.

Interpretation of the output
----------------------------
* ``continuous`` — optimal fractional allocation, cost and success flag.
* ``integer`` — best integer allocation found by brute-force search over
  a small grid; the true deployment uses whole servers, so this is the
  operationally-relevant answer.
* If the integer and continuous costs differ noticeably, the LP relaxation
  is not tight and a mixed-integer solver would be needed for larger
  problems.
"""

from __future__ import annotations

from itertools import product

import numpy as np
from scipy.optimize import minimize

from .io_utils import save_results
from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Problem constants
# -----------------------------------------------------------------------------
COST_A: float = 12.0
COST_B: float = 18.0
CAP_A: float = 100.0
CAP_B: float = 170.0
REQUIRED_CAPACITY: float = 1000.0

X0: tuple[float, float] = (5.0, 3.0)
INTEGER_SEARCH_LIMIT: int = 20


# -----------------------------------------------------------------------------
# Objective and constraints
# -----------------------------------------------------------------------------
def cost(z: np.ndarray) -> float:
    """Operating cost ``12 x + 18 y``."""
    x, y = z
    return COST_A * x + COST_B * y


def capacity_constraint(z: np.ndarray) -> float:
    """Inequality ``100 x + 170 y − 1000 ≥ 0``.

    SLSQP expects the inequality in the "≥ 0" convention, so no sign
    flip is required.
    """
    x, y = z
    return CAP_A * x + CAP_B * y - REQUIRED_CAPACITY


# -----------------------------------------------------------------------------
# Solvers
# -----------------------------------------------------------------------------
def solve_continuous() -> dict[str, object]:
    """Run SLSQP for the continuous relaxation."""
    result = minimize(
        cost,
        x0=np.asarray(X0, dtype=float),
        method="SLSQP",
        bounds=[(0.0, None), (0.0, None)],
        constraints={"type": "ineq", "fun": capacity_constraint},
    )
    x, y = result.x
    return {
        "x": float(x),
        "y": float(y),
        "cost": float(result.fun),
        "capacity": float(CAP_A * x + CAP_B * y),
        "success": bool(result.success),
        "message": str(result.message),
        "iterations": int(result.nit),
    }


def solve_integer(limit: int = INTEGER_SEARCH_LIMIT) -> dict[str, object]:
    """Brute-force best integer allocation within ``[0, limit]²``.

    For a two-variable problem with a small search box this is exact.
    For larger problems one would switch to a MILP solver.
    """
    best: tuple[float, int, int, float] | None = None
    for a, b in product(range(limit + 1), repeat=2):
        capacity = CAP_A * a + CAP_B * b
        if capacity < REQUIRED_CAPACITY:
            continue
        total = COST_A * a + COST_B * b
        if best is None or total < best[0]:
            best = (total, a, b, capacity)
    if best is None:
        raise RuntimeError("No feasible integer allocation within search limit.")
    total_cost, a, b, capacity = best
    return {"a": a, "b": b, "cost": total_cost, "capacity": capacity}


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Solve the continuous and integer versions of the allocation problem.

    Returns
    -------
    dict
        Keys: ``constants``, ``continuous``, ``integer``, ``gap``.
    """
    configure_logging()

    continuous = solve_continuous()
    integer = solve_integer()
    gap = abs(continuous["cost"] - integer["cost"])

    logger.info(
        "Constants: cost_A=%.0f, cost_B=%.0f, cap_A=%.0f, cap_B=%.0f, need=%.0f",
        COST_A,
        COST_B,
        CAP_A,
        CAP_B,
        REQUIRED_CAPACITY,
    )
    logger.info(
        "Continuous solution: x=%.4f, y=%.4f → cost=%.4f, capacity=%.4f",
        continuous["x"],
        continuous["y"],
        continuous["cost"],
        continuous["capacity"],
    )
    logger.info(
        "Integer solution:    a=%d, b=%d → cost=%.2f, capacity=%.1f",
        integer["a"],
        integer["b"],
        integer["cost"],
        integer["capacity"],
    )
    logger.info("Cost gap (integer − continuous): %.2f", gap)
    logger.info(
        "SLSQP converged: %s in %d iterations", continuous["success"], continuous["iterations"]
    )

    payload = {
        "constants": {
            "cost_A": COST_A,
            "cost_B": COST_B,
            "cap_A": CAP_A,
            "cap_B": CAP_B,
            "required_capacity": REQUIRED_CAPACITY,
        },
        "continuous": continuous,
        "integer": integer,
        "gap": float(gap),
    }
    save_results("task19_optimization", payload)
    return payload


if __name__ == "__main__":
    main()
