"""Task 11 — Root Finding: Newton-Raphson and Secant Methods.

Concept
-------
Newton-Raphson improves a guess using the tangent line:

.. math::

    x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}

It converges quadratically near a simple root but requires an analytic
derivative. The secant method replaces ``f'`` with a finite-difference
estimate from two recent iterates and avoids the derivative at the cost
of slightly slower (superlinear, order ≈ 1.618) convergence.

Real-world application
----------------------
Compute the Internal Rate of Return (IRR) of a project: the discount rate
at which net present value is zero.

Interpretation of the output
----------------------------
* ``newton.irr`` / ``secant.irr`` — IRR as a decimal fraction.
* ``newton.iterations`` / ``secant.iterations`` — iterations to
  converge to ``xtol=1e-12``.
* ``npv_at_newton`` — should be numerically zero.
"""

from __future__ import annotations

from scipy.optimize import root_scalar

from .io_utils import save_results
from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Inputs — a small project's cash-flow schedule
# -----------------------------------------------------------------------------
# t = 0 is the initial investment (negative); t = 1..4 are inflows.
CASH_FLOWS: tuple[float, ...] = (-10_000.0, 3_000.0, 3_500.0, 4_000.0, 2_500.0)

NEWTON_X0: float = 0.10
SECANT_X0: float = 0.05
SECANT_X1: float = 0.20
XTOL: float = 1e-12


# -----------------------------------------------------------------------------
# Model functions
# -----------------------------------------------------------------------------
def npv(rate: float) -> float:
    """Net present value of ``CASH_FLOWS`` discounted at ``rate``.

    ``rate`` is expressed as a decimal fraction (0.10 = 10 %).
    """
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(CASH_FLOWS))


def d_npv(rate: float) -> float:
    """Derivative of NPV with respect to ``rate``."""
    return sum(-t * cf / (1.0 + rate) ** (t + 1) for t, cf in enumerate(CASH_FLOWS) if t > 0)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Compute IRR via Newton-Raphson and the secant method.

    Returns
    -------
    dict
        Keys: ``cash_flows``, ``newton``, ``secant``, ``npv_at_newton``.
    """
    configure_logging()

    newton = root_scalar(npv, fprime=d_npv, x0=NEWTON_X0, method="newton", xtol=XTOL)
    secant = root_scalar(npv, x0=SECANT_X0, x1=SECANT_X1, method="secant", xtol=XTOL)

    logger.info("Cash flows: %s", CASH_FLOWS)
    logger.info("IRR (Newton-Raphson): %.6f%%  (iters=%d)", newton.root * 100.0, newton.iterations)
    logger.info("IRR (Secant):         %.6f%%  (iters=%d)", secant.root * 100.0, secant.iterations)
    logger.info("NPV at Newton root:   %.3e", npv(newton.root))
    logger.info("Difference in IRR:    %.3e", abs(newton.root - secant.root))

    payload = {
        "cash_flows": list(CASH_FLOWS),
        "newton": {
            "irr": float(newton.root),
            "iterations": int(newton.iterations),
        },
        "secant": {
            "irr": float(secant.root),
            "iterations": int(secant.iterations),
        },
        "npv_at_newton": float(npv(newton.root)),
    }
    save_results("task11_newton_secant", payload)
    return payload


if __name__ == "__main__":
    main()
