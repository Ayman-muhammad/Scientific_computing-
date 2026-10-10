"""Task 15 — Numerical Differentiation.

Concept
-------
A derivative measures how quickly a quantity changes. When an analytic
derivative is unavailable, we approximate it from nearby samples. The
forward difference uses the current and next sample; the central
difference uses symmetric neighbours and is typically an order of
magnitude more accurate for the same step size.

Mathematical formulation
------------------------
* Forward:  :math:`f'(x_i) \\approx \\dfrac{f(x_{i+1}) - f(x_i)}{h}`
* Central:  :math:`f'(x_i) \\approx \\dfrac{f(x_{i+1}) - f(x_{i-1})}{2h}`
* Backward: :math:`f'(x_i) \\approx \\dfrac{f(x_i) - f(x_{i-1})}{h}`

For smooth ``f`` with uniform spacing ``h``, the central difference has
truncation error :math:`O(h^2)` versus :math:`O(h)` for the one-sided
forms.

Real-world application
----------------------
Estimate instantaneous vehicle speed from GPS position samples taken at
one-second intervals.

Interpretation of the output
----------------------------
* ``speed`` — estimated speed in m/s at each timestamp.
* The figure plots the speed profile over time; monotonic increases
  indicate sustained acceleration, plateaus indicate cruise.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .io_utils import save_results
from .logging_config import configure_logging, get_logger
from .paths import FIGURES_DIR, ensure_dirs

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Inputs — GPS samples: time (s), position (m)
# -----------------------------------------------------------------------------
TIME: np.ndarray = np.array([0, 1, 2, 3, 4, 5, 6], dtype=float)
POSITION: np.ndarray = np.array([0.0, 4.8, 10.2, 16.1, 22.7, 30.0, 38.0])


# -----------------------------------------------------------------------------
# Numerical differentiation
# -----------------------------------------------------------------------------
def numerical_speed(time: np.ndarray, position: np.ndarray) -> np.ndarray:
    """Compute speed via forward / central / backward differences.

    Uses:

    * **Forward** at the first sample.
    * **Central** at every interior sample (higher accuracy).
    * **Backward** at the last sample.

    Parameters
    ----------
    time : numpy.ndarray
        Monotonically increasing sample times, shape ``(n,)``.
    position : numpy.ndarray
        Position samples, same shape as ``time``.

    Returns
    -------
    numpy.ndarray
        Estimated speed, same shape as ``position``.

    Raises
    ------
    ValueError
        If ``time`` and ``position`` differ in length, or ``time`` has
        fewer than two samples.
    """
    if time.shape != position.shape:
        raise ValueError("time and position must have the same shape")
    if time.size < 2:
        raise ValueError("At least two samples are required")

    speed = np.zeros_like(position, dtype=float)

    # Forward difference at the first sample.
    speed[0] = (position[1] - position[0]) / (time[1] - time[0])

    # Central difference at every interior sample.
    for i in range(1, time.size - 1):
        speed[i] = (position[i + 1] - position[i - 1]) / (time[i + 1] - time[i - 1])

    # Backward difference at the last sample.
    speed[-1] = (position[-1] - position[-2]) / (time[-1] - time[-2])
    return speed


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
def _plot_speed(time: np.ndarray, speed: np.ndarray) -> None:
    ensure_dirs()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(time, speed, marker="o", color="navy", linewidth=1.8)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Estimated speed (m/s)")
    ax.set_title("Speed estimated from GPS position data")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "task15_differentiation.png", dpi=200)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Estimate speed from GPS samples and plot the profile.

    Returns
    -------
    dict
        Keys: ``time``, ``position``, ``speed``, ``max_speed``,
        ``mean_speed``.
    """
    configure_logging()

    speed = numerical_speed(TIME, POSITION)

    for t, x, v in zip(TIME, POSITION, speed, strict=False):
        logger.info("t=%.0fs  x=%.2fm  v≈%.4f m/s", t, x, v)

    max_speed = float(np.max(speed))
    mean_speed = float(np.mean(speed))
    logger.info("Maximum speed: %.4f m/s", max_speed)
    logger.info("Mean speed:    %.4f m/s", mean_speed)

    _plot_speed(TIME, speed)
    logger.info("Saved figure: %s", FIGURES_DIR / "task15_differentiation.png")

    payload = {
        "time": TIME,
        "position": POSITION,
        "speed": speed,
        "max_speed": max_speed,
        "mean_speed": mean_speed,
    }
    save_results("task15_numerical_differentiation", payload)
    return payload


if __name__ == "__main__":
    main()
