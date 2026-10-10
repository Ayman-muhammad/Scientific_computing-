"""Task 10 — Root Finding: Bisection and Fixed-Point Methods.

Concept
-------
A root of ``f(x)`` is a value ``r`` with ``f(r) = 0``. Bisection starts
with an interval ``[a, b]`` where ``f(a)`` and ``f(b)`` have opposite
signs, and repeatedly halves the interval, keeping the half that still
contains a sign change. Fixed-point iteration rewrites ``f(x) = 0`` as
``x = g(x)`` and repeatedly evaluates ``x_{n+1} = g(x_n)``.

Mathematical formulation
------------------------
* Bisection error after ``k`` steps: :math:`|b - a| / 2^k` — always
  converges, but only linearly.
* Fixed-point iteration converges when :math:`|g'(r)| < 1` in a
  neighbourhood of the root :math:`r`.

Real-world application
----------------------
Find the equilibrium temperature at which a nonlinear heat-balance
equation vanishes: heat gain equals heat loss.

Interpretation of the output
----------------------------
* ``bisection.root`` — bracketed root, °C.
* ``fixed_point.root`` — same root via fixed-point iteration.
* ``fixed_point.iterations`` — number of iterations to reach tolerance.
* The figure shows ``f(T)`` with the root marked.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import root_scalar

from .io_utils import save_results
from .logging_config import configure_logging, get_logger
from .paths import FIGURES_DIR, ensure_dirs

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
BRACKET: tuple[float, float] = (20.0, 40.0)
XTOL: float = 1e-10
FP_INITIAL_GUESS: float = 30.0
FP_MAX_ITER: int = 200


# -----------------------------------------------------------------------------
# Model functions
# -----------------------------------------------------------------------------
def heat_balance(t: float) -> float:
    """Nonlinear heat-balance function ``f(T) = T - 25 - 10·e^(-T/20)``.

    ``f(T) = 0`` means heat gain equals heat loss. The bracket
    ``[20, 40]`` contains exactly one sign change.
    """
    return t - 25.0 - 10.0 * np.exp(-t / 20.0)


def g_fixed_point(t: float) -> float:
    """Fixed-point form ``T = 25 + 10·e^(-T/20)`` derived from f(T)=0."""
    return 25.0 + 10.0 * np.exp(-t / 20.0)


# -----------------------------------------------------------------------------
# Solvers
# -----------------------------------------------------------------------------
def fixed_point_iteration(
    x0: float,
    *,
    tol: float = XTOL,
    max_iter: int = FP_MAX_ITER,
) -> tuple[float, list[float]]:
    """Iterate ``x_{n+1} = g(x_n)`` until ``|Δx| < tol``.

    Returns
    -------
    root : float
        Final iterate.
    history : list of float
        Sequence including the initial guess; length is
        ``iterations + 1``.
    """
    history: list[float] = [x0]
    x = x0
    for _ in range(max_iter):
        x_new = g_fixed_point(x)
        history.append(x_new)
        if abs(x_new - x) < tol:
            return x_new, history
        x = x_new
    return x, history


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
def _plot_equilibrium(root: float) -> None:
    """Plot f(T) over the bracket with the root marked."""
    ensure_dirs()
    temps = np.linspace(20.0, 40.0, 400)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(temps, heat_balance(temps), label="f(T) = T - 25 - 10·e^(-T/20)")
    ax.axhline(0.0, linewidth=0.8, color="k")
    ax.axvline(root, linestyle="--", color="crimson", label=f"root ≈ {root:.4f} °C")
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Heat-balance function f(T)")
    ax.set_title("Equilibrium temperature")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "task10_equilibrium.png", dpi=200)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Locate the equilibrium temperature by both methods.

    Returns
    -------
    dict
        Keys: ``bisection``, ``fixed_point``.
    """
    configure_logging()

    bisect = root_scalar(heat_balance, bracket=list(BRACKET), method="bisect", xtol=XTOL)
    fp_root, fp_history = fixed_point_iteration(FP_INITIAL_GUESS)

    logger.info("Bisection root:   %.6f °C  (iters=%d)", bisect.root, bisect.iterations)
    logger.info("Fixed-point root: %.6f °C  (iters=%d)", fp_root, len(fp_history) - 1)
    logger.info("Difference:       %.3e °C", abs(bisect.root - fp_root))

    _plot_equilibrium(float(bisect.root))
    logger.info("Saved figure: %s", FIGURES_DIR / "task10_equilibrium.png")

    payload = {
        "bisection": {
            "root": float(bisect.root),
            "iterations": int(bisect.iterations),
            "bracket": list(BRACKET),
        },
        "fixed_point": {
            "root": fp_root,
            "iterations": len(fp_history) - 1,
            "history": fp_history,
        },
    }
    save_results("task10_bisection_fixed_point", payload)
    return payload


if __name__ == "__main__":
    main()
