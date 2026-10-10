"""Task 16 — Numerical Integration.

Concept
-------
An integral represents an accumulated quantity — the area under a curve.
When the integrand is known only at discrete samples, we approximate the
area with quadrature rules. The trapezoidal rule approximates the curve
with straight segments; Simpson's rule uses parabolic segments and is
usually more accurate for smooth data.

Mathematical formulation
------------------------
Uniform spacing ``h``, samples :math:`f_0, \\dots, f_n`:

* Trapezoidal: :math:`\\displaystyle \\int_a^b f \\, dx \\approx
  \\frac{h}{2}\\bigl(f_0 + 2\\sum_{i=1}^{n-1} f_i + f_n\\bigr)`
* Simpson (n even): :math:`\\displaystyle \\int_a^b f \\, dx \\approx
  \\frac{h}{3}\\bigl(f_0 + 4\\!\\!\\sum_{\\text{odd}} f_i
  + 2\\!\\!\\sum_{\\text{even}, \\, i \\neq 0,n} f_i + f_n\\bigr)`

Real-world application
----------------------
A smart meter records average power at two-hour intervals; we integrate
power over time to estimate total electrical energy consumed.

Interpretation of the output
----------------------------
* ``trapezoidal_kwh`` / ``simpson_kwh`` — total energy in kilowatt-hours.
* ``difference_kwh`` — the two estimates differ by a small amount; a
  large difference signals under-resolved data.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import simpson

from .io_utils import save_results
from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Inputs — smart-meter power readings at 2-hour intervals
# -----------------------------------------------------------------------------
TIME_HOURS: np.ndarray = np.array([0, 2, 4, 6, 8, 10, 12], dtype=float)
POWER_KW: np.ndarray = np.array([0.8, 1.0, 1.4, 1.8, 1.6, 1.2, 0.9])


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Compute energy with trapezoidal and Simpson rules.

    Returns
    -------
    dict
        Keys: ``time_hours``, ``power_kw``, ``trapezoidal_kwh``,
        ``simpson_kwh``, ``difference_kwh``.
    """
    configure_logging()

    energy_trap = float(np.trapezoid(POWER_KW, TIME_HOURS))
    energy_simp = float(simpson(POWER_KW, x=TIME_HOURS))
    difference = abs(energy_simp - energy_trap)

    logger.info(
        "Time grid: %d samples covering %.0f hours", TIME_HOURS.size, TIME_HOURS[-1] - TIME_HOURS[0]
    )
    logger.info("Trapezoidal energy: %.4f kWh", energy_trap)
    logger.info("Simpson energy:     %.4f kWh", energy_simp)
    logger.info("Difference:         %.4f kWh", difference)

    payload = {
        "time_hours": TIME_HOURS,
        "power_kw": POWER_KW,
        "trapezoidal_kwh": energy_trap,
        "simpson_kwh": energy_simp,
        "difference_kwh": difference,
    }
    save_results("task16_numerical_integration", payload)
    return payload


if __name__ == "__main__":
    main()
