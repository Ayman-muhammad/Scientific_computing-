"""Task 13 — Interpolation.

Concept
-------
Interpolation estimates values *between* known data points. Linear
interpolation draws a straight line between adjacent points. Polynomial
interpolation fits a polynomial through several points. Cubic splines
join smooth cubic segments while preserving continuity of value, first
derivative and second derivative at the knots.

Mathematical formulation
------------------------
Given samples :math:`(x_i, y_i)`, :math:`i = 0, \\dots, n`:

* **Linear.** :math:`S(x) = y_i + \\frac{y_{i+1} - y_i}{x_{i+1} - x_i}
  (x - x_i)` for :math:`x \\in [x_i, x_{i+1}]`.
* **Cubic spline.** Piecewise cubic :math:`S_i(x)` with
  :math:`S_i(x_i) = y_i`, :math:`S_i'(x_{i+1}) = S_{i+1}'(x_{i+1})`,
  :math:`S_i''(x_{i+1}) = S_{i+1}''(x_{i+1})`.

Real-world application
----------------------
Hourly temperature measurements must be upsampled to 10-minute resolution
for a downstream control loop.

Interpretation of the output
----------------------------
* ``linear_at_10_30`` — linear estimate at 10:30.
* ``cubic_at_10_30`` — cubic-spline estimate at the same time.
* The figure overlays both curves against the discrete measurements.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline, interp1d

from .io_utils import save_results
from .logging_config import configure_logging, get_logger
from .paths import FIGURES_DIR, ensure_dirs

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Inputs — 7 hourly temperature readings, 08:00 → 14:00
# -----------------------------------------------------------------------------
HOURS: np.ndarray = np.array([8, 9, 10, 11, 12, 13, 14], dtype=float)
TEMPERATURE: np.ndarray = np.array([18.0, 20.0, 22.5, 24.0, 25.0, 25.5, 25.0])

TARGET_TIME: float = 10.5  # 10:30
SAMPLE_STEP_HOURS: float = 1.0 / 6.0  # every 10 minutes


# -----------------------------------------------------------------------------
# Interpolation helpers
# -----------------------------------------------------------------------------
def build_interpolators(x: np.ndarray, y: np.ndarray) -> tuple[interp1d, CubicSpline]:
    """Return ``(linear, cubic)`` interpolators for the samples."""
    linear = interp1d(x, y, kind="linear")
    cubic = CubicSpline(x, y)
    return linear, cubic


def build_dense_grid(start: float, stop: float, step: float) -> np.ndarray:
    """Uniform grid from ``start`` to ``stop`` inclusive, step ``step``.

    Uses ``np.arange`` but re-appends the endpoint if floating-point drift
    drops the last sample.
    """
    grid = np.arange(start, stop, step, dtype=float)
    if grid.size == 0 or not np.isclose(grid[-1], stop):
        grid = np.append(grid, stop)
    return grid


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
def _plot_interpolation(
    hours: np.ndarray,
    temps: np.ndarray,
    grid: np.ndarray,
    linear_est: np.ndarray,
    cubic_est: np.ndarray,
) -> None:
    ensure_dirs()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(hours, temps, color="black", zorder=3, label="Hourly measurements")
    ax.plot(grid, linear_est, label="Linear", alpha=0.9)
    ax.plot(grid, cubic_est, label="Cubic spline", alpha=0.9)
    ax.set_xlabel("Hour of day")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature interpolation (hourly → 10-minute)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "task13_interpolation.png", dpi=200)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Interpolate hourly temperatures onto a 10-minute grid.

    Returns
    -------
    dict
        Keys: ``hours``, ``temperature``, ``linear_at_10_30``,
        ``cubic_at_10_30``, ``grid``, ``linear_estimates``,
        ``cubic_estimates``.
    """
    configure_logging()

    linear, cubic = build_interpolators(HOURS, TEMPERATURE)
    grid = build_dense_grid(HOURS[0], HOURS[-1], SAMPLE_STEP_HOURS)

    linear_est = linear(grid)
    cubic_est = cubic(grid)

    lin_val = float(linear(TARGET_TIME))
    cub_val = float(cubic(TARGET_TIME))

    logger.info("Samples: %d points from %.0f:00 to %.0f:00", HOURS.size, HOURS[0], HOURS[-1])
    logger.info(
        "Dense grid: %d points at %.0f-minute resolution", grid.size, SAMPLE_STEP_HOURS * 60
    )
    logger.info("Estimate at 10:30 — linear: %.3f °C | cubic: %.3f °C", lin_val, cub_val)
    logger.info("Difference (cubic − linear): %.3f °C", cub_val - lin_val)

    _plot_interpolation(HOURS, TEMPERATURE, grid, linear_est, cubic_est)
    logger.info("Saved figure: %s", FIGURES_DIR / "task13_interpolation.png")

    payload = {
        "hours": HOURS,
        "temperature": TEMPERATURE,
        "target_time": TARGET_TIME,
        "linear_at_10_30": lin_val,
        "cubic_at_10_30": cub_val,
        "grid": grid,
        "linear_estimates": linear_est,
        "cubic_estimates": cubic_est,
    }
    save_results("task13_interpolation", payload)
    return payload


if __name__ == "__main__":
    main()
