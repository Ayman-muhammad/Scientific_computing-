"""Task 18 — Numerical Solution of ODEs Using SciPy.

Concept
-------
More advanced ODE solvers use higher-order methods and automatically
adjust the step size to keep the local error below a tolerance. SciPy's
``solve_ivp`` integrates :math:`dy/dt = f(t, y)` over a time interval and
returns values at requested times. The default method (``RK45``) is an
explicit embedded Runge-Kutta pair that estimates the local truncation
error at each step and refines or coarsens accordingly.

Mathematical formulation
------------------------
An RC circuit's charging behaviour is governed by

.. math::

    \\frac{dV}{dt} = \\frac{V_s - V}{R C}

with initial condition :math:`V(0) = V_0`. The closed-form solution is

.. math::

    V(t) = V_s \\bigl(1 - e^{-t / (R C)}\\bigr)

which we use to validate the numerical integrator.

Real-world application
----------------------
Charging (and discharging) of a capacitor in an RC circuit — a
first-order linear dynamic that appears everywhere in electronics,
control systems and filtering.

Interpretation of the output
----------------------------
* ``v`` — numerically integrated capacitor voltage at each requested
  time.
* ``exact`` — analytical voltage for comparison.
* ``max_error`` — maximum absolute difference; with ``rtol=1e-9`` and
  ``atol=1e-11`` this should be well below 1 µV.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from .io_utils import save_results
from .logging_config import configure_logging, get_logger
from .paths import FIGURES_DIR, ensure_dirs

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Circuit parameters
# -----------------------------------------------------------------------------
VS: float = 5.0  # V    — supply voltage
R: float = 1000.0  # Ω    — resistance
C: float = 1e-3  # F    — capacitance (1 mF)
V0: float = 0.0  # V    — initial capacitor voltage

T_START: float = 0.0
T_END: float = 5.0  # s
N_EVAL: int = 200
RTOL: float = 1e-9
ATOL: float = 1e-11


# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------
def rc_circuit(t: float, v: np.ndarray) -> list[float]:
    """RC charging ODE ``dV/dt = (Vs - V) / (R C)``.

    ``solve_ivp`` requires the right-hand side to accept scalar ``t`` and
    array-like state ``y`` even for a 1-D system; returning a list keeps
    the shapes unambiguous.
    """
    return [(VS - v[0]) / (R * C)]


def exact_voltage(t: np.ndarray) -> np.ndarray:
    """Analytical RC charging curve ``V(t) = Vs (1 - e^{-t/(RC)})``."""
    return VS * (1.0 - np.exp(-t / (R * C)))


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
def _plot_rc(t: np.ndarray, v: np.ndarray, exact: np.ndarray) -> None:
    ensure_dirs()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(t, v, label="solve_ivp (RK45)")
    ax.plot(t, exact, linestyle="--", label="Exact")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Capacitor voltage (V)")
    ax.set_title("RC circuit charging")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "task18_rc_circuit.png", dpi=200)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Solve the RC charging ODE and validate against the exact curve.

    Returns
    -------
    dict
        Keys: ``parameters``, ``t``, ``v``, ``exact``, ``max_error``,
        ``success``, ``nfev``.
    """
    configure_logging()

    t_eval = np.linspace(T_START, T_END, N_EVAL)
    solution = solve_ivp(
        rc_circuit,
        (T_START, T_END),
        [V0],
        t_eval=t_eval,
        rtol=RTOL,
        atol=ATOL,
    )

    exact = exact_voltage(solution.t)
    max_error = float(np.max(np.abs(solution.y[0] - exact)))

    logger.info("Parameters: Vs=%.1f V, R=%.0f Ω, C=%.4f F, τ=%.3f s", VS, R, C, R * C)
    logger.info("Solver success: %s  (RHS evaluations=%d)", solution.success, solution.nfev)
    logger.info("V(%.1f s) = %.6f V", T_END, solution.y[0, -1])
    logger.info("Maximum |solve_ivp - exact| = %.3e V", max_error)

    _plot_rc(solution.t, solution.y[0], exact)
    logger.info("Saved figure: %s", FIGURES_DIR / "task18_rc_circuit.png")

    payload = {
        "parameters": {
            "Vs": VS,
            "R": R,
            "C": C,
            "V0": V0,
            "t_start": T_START,
            "t_end": T_END,
            "rtol": RTOL,
            "atol": ATOL,
            "tau": R * C,
        },
        "t": solution.t,
        "v": solution.y[0],
        "exact": exact,
        "max_error": max_error,
        "success": bool(solution.success),
        "nfev": int(solution.nfev),
    }
    save_results("task18_scipy_ode", payload)
    return payload


if __name__ == "__main__":
    main()
