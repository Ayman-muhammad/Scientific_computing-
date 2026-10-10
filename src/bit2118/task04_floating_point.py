"""Task 04 — Floating-Point Arithmetic and Numerical Errors.

Concept
-------
IEEE-754 double precision cannot represent most real numbers exactly, so
``0.1 + 0.2 != 0.3``. Absolute error is :math:`|\\text{true} -
\\text{approx}|`; relative error is :math:`\\text{absolute} /
|\\text{true}|`. Truncation error comes from replacing an exact process
with an approximation; round-off error comes from finite computer
precision.

Mathematical formulation
------------------------
Two algebraically equivalent expressions can differ dramatically in
floating-point accuracy:

.. math::

    \\text{unstable}(x) &= \\frac{\\sqrt{1 + x} - 1}{x} \\\\
    \\text{stable}(x)   &= \\frac{1}{\\sqrt{1 + x} + 1}

Both equal :math:`1/(\\sqrt{1+x} + 1)` in exact arithmetic, but the first
suffers catastrophic cancellation for small :math:`x`.

Real-world application
----------------------
Banking, GPS, engineering design and any iterative algorithm where
accumulated round-off error can change a decision.
"""

from __future__ import annotations

import numpy as np

from .io_utils import save_results
from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
SQRT2_APPROX: float = 1.414
STABILITY_X_VALUES: tuple[float, ...] = (1e-4, 1e-8, 1e-12)


# -----------------------------------------------------------------------------
# Pure functions
# -----------------------------------------------------------------------------
def absolute_error(true: float, approx: float) -> float:
    """Return :math:`|\\text{true} - \\text{approx}|`."""
    return abs(true - approx)


def relative_error(true: float, approx: float) -> float:
    """Return :math:`|\\text{true} - \\text{approx}| / |\\text{true}|`.

    Raises
    ------
    ZeroDivisionError
        If ``true`` is zero — relative error is undefined.
    """
    if true == 0.0:
        raise ZeroDivisionError("relative_error is undefined when true == 0")
    return absolute_error(true, approx) / abs(true)


def unstable_sqrt_identity(x: float) -> float:
    """Catastrophically cancelling form ``(√(1+x) − 1) / x``.

    For small ``x`` the subtraction ``√(1+x) − 1`` loses most of its
    significant digits to cancellation.
    """
    return (np.sqrt(1.0 + x) - 1.0) / x


def stable_sqrt_identity(x: float) -> float:
    """Numerically stable form ``1 / (√(1+x) + 1)``.

    Algebraically identical to :func:`unstable_sqrt_identity` but avoids
    subtraction of nearly equal numbers.
    """
    return 1.0 / (np.sqrt(1.0 + x) + 1.0)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Demonstrate FP comparison pitfalls and stability rewriting.

    Returns
    -------
    dict
        Nested keys: ``fp_demo``, ``sqrt2``, ``stability``.
    """
    configure_logging()

    # ------------------------------------------------------------------
    # 1. The classic 0.1 + 0.2 != 0.3 demonstration.
    # ------------------------------------------------------------------
    calculated = 0.1 + 0.2
    expected = 0.3
    exact_cmp = calculated == expected
    tolerance_cmp = bool(np.isclose(calculated, expected))

    logger.info("0.1 + 0.2 = %r", calculated)
    logger.info("Exact comparison:      %s", exact_cmp)
    logger.info("Tolerance comparison:  %s", tolerance_cmp)

    # ------------------------------------------------------------------
    # 2. Absolute vs relative error for sqrt(2).
    # ------------------------------------------------------------------
    true_value = float(np.sqrt(2.0))
    approx_value = SQRT2_APPROX
    abs_err = absolute_error(true_value, approx_value)
    rel_err = relative_error(true_value, approx_value)

    logger.info("√2 true value:    %.10f", true_value)
    logger.info("√2 approximation: %.10f", approx_value)
    logger.info("Absolute error:   %.8f", abs_err)
    logger.info("Relative error:   %.6f%%", rel_err * 100.0)

    # ------------------------------------------------------------------
    # 3. Stability comparison across shrinking x.
    # ------------------------------------------------------------------
    stability_rows: list[dict[str, float]] = []
    for x in STABILITY_X_VALUES:
        direct = float(unstable_sqrt_identity(x))
        stable = float(stable_sqrt_identity(x))
        delta = abs(direct - stable)
        stability_rows.append({"x": x, "direct": direct, "stable": stable, "delta": delta})
        logger.info(
            "x=%8.0e | direct=%.12f | stable=%.12f | Δ=%.3e",
            x,
            direct,
            stable,
            delta,
        )

    payload = {
        "fp_demo": {
            "calculated": calculated,
            "expected": expected,
            "exact_comparison": exact_cmp,
            "tolerance_comparison": tolerance_cmp,
        },
        "sqrt2": {
            "true_value": true_value,
            "approx_value": approx_value,
            "absolute_error": abs_err,
            "relative_error": rel_err,
        },
        "stability": stability_rows,
    }
    save_results("task04_floating_point", payload)
    return payload


if __name__ == "__main__":
    main()
