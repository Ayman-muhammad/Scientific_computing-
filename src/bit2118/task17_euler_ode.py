"""Task 17 — Ordinary Differential Equations: Euler Method.

Concept
-------
An ODE describes how a quantity changes over time:
:math:`dy/dt = f(t, y)`. Euler's method starts from a known initial value
:math:`y_0` at :math:`t_0` and steps forward in fixed increments ``h``,
approximating the derivative by its forward difference.

Mathematical formulation
------------------------
Given :math:`y'(t) = f(t, y)` and initial condition :math:`y(t_0) = y_0`:

.. math::

    y_{n+1} = y_n + h \\, f(t_n, y_n), \\qquad t_{n+1} = t_n + h

The method is **first order**: the global error scales as
:math:`O(h)`. Halving ``h`` roughly halves the error. For Newton's law of
cooling the exact solution is available, so we can quantify the
discretisation error precisely.

Real-world application
----------------------
Newton's law of cooling: a hot object loses heat to its surroundings at
a rate proportional to the temperature difference,

.. math::

    \\frac{dT}{dt} = -k \\, (T - T_{\\text{ambient}})

Interpretation of the output
----------------------------
* ``temperature`` — simulated temperature history, one value per step.
* ``exact`` — closed-form exponential solution for validation.
* ``final_error`` — absolute difference between numerical and exact
  temperatures at the final time; a measure of accumulated truncation
  error.
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
# Physical model
# -----------------------------------------------------------------------------
T_AMBIENT: float = 25.0  # °C — room temperature
T_INITIAL: float = 90.0  # °C — initial temperature of the object
K: float = 0.12  # 1/min — cooling constant
H: float = 1.0  # min — Euler step size
END_TIME: float = 30.0  # min — simulation horizon


# -----------------------------------------------------------------------------
# Model functions
# -----------------------------------------------------------------------------
def cooling_rate(temperature: float) -> float:
    """``dT/dt = −k (T − T_ambient)``."""
    return -K * (temperature - T_AMBIENT)


def exact_solution(time: np.ndarray) -> np.ndarray:
    """Closed-form solution of the cooling ODE.

    .. math::

        T(t) = T_{\\text{ambient}} +
               (T_0 - T_{\\text{ambient}}) \\, e^{-k t}
    """
    return T_AMBIENT + (T_INITIAL - T_AMBIENT) * np.exp(-K * time)


# -----------------------------------------------------------------------------
# Euler integration
# -----------------------------------------------------------------------------
def euler_cooling() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Integrate the cooling ODE with the Euler method.

    Returns
    -------
    time : numpy.ndarray
        Equally spaced time points from 0 to ``END_TIME`` inclusive.
    temperature : numpy.ndarray
        Numerical temperature at each time point.
    exact : numpy.ndarray
        Closed-form reference temperature at each time point.
    """
    time = np.arange(0.0, END_TIME + H, H)
    temperature = np.zeros_like(time)
    temperature[0] = T_INITIAL

    # Vector operations are impossible here because each step depends on
    # the previous one — Euler is inherently sequential.
    for i in range(time.size - 1):
        temperature[i + 1] = temperature[i] + H * cooling_rate(temperature[i])

    exact = exact_solution(time)
    return time, temperature, exact


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
def _plot_cooling(time: np.ndarray, temperature: np.ndarray, exact: np.ndarray) -> None:
    ensure_dirs()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(time, temperature, marker="o", label=f"Euler (h = {H:g} min)")
    ax.plot(time, exact, linestyle="--", label="Exact solution")
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Cooling of a hot object — Euler vs exact")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "task17_euler_cooling.png", dpi=200)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Integrate the cooling ODE and compare against the exact curve.

    Returns
    -------
    dict
        Keys: ``parameters``, ``time``, ``temperature``, ``exact``,
        ``final_euler``, ``final_exact``, ``final_error``, ``max_error``.
    """
    configure_logging()

    time, temperature, exact = euler_cooling()

    final_euler = float(temperature[-1])
    final_exact = float(exact[-1])
    final_error = abs(final_euler - final_exact)
    max_error = float(np.max(np.abs(temperature - exact)))

    logger.info(
        "Parameters: T_ambient=%.1f °C, T_initial=%.1f °C, k=%.3f 1/min, h=%.2f min",
        T_AMBIENT,
        T_INITIAL,
        K,
        H,
    )
    logger.info("Euler temperature after %.0f min: %.4f °C", END_TIME, final_euler)
    logger.info("Exact temperature after %.0f min: %.4f °C", END_TIME, final_exact)
    logger.info("Final absolute error:              %.4f °C", final_error)
    logger.info("Maximum absolute error:            %.4f °C", max_error)

    _plot_cooling(time, temperature, exact)
    logger.info("Saved figure: %s", FIGURES_DIR / "task17_euler_cooling.png")

    payload = {
        "parameters": {
            "T_ambient": T_AMBIENT,
            "T_initial": T_INITIAL,
            "k": K,
            "h": H,
            "end_time": END_TIME,
        },
        "time": time,
        "temperature": temperature,
        "exact": exact,
        "final_euler": final_euler,
        "final_exact": final_exact,
        "final_error": final_error,
        "max_error": max_error,
    }
    save_results("task17_euler_ode", payload)
    return payload


if __name__ == "__main__":
    main()
