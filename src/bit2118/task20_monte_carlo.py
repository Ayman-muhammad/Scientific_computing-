"""Task 20 — Random Numbers and Monte Carlo Methods.

Concept
-------
Monte Carlo methods estimate a quantity by repeated random sampling. For
an event with probability ``p``, the observed fraction over ``N``
independent simulations converges to ``p`` at rate
:math:`O(1/\\sqrt{N})` — regardless of the dimensionality of the problem,
which is the principal advantage over grid-based integration.

Mathematical formulation
------------------------
If demand :math:`D \\sim \\mathcal{N}(\\mu, \\sigma^2)` and capacity is a
fixed constant :math:`C`, we estimate

.. math::

    p = \\Pr(D > C)

with the unbiased estimator

.. math::

    \\hat{p}_N = \\frac{1}{N} \\sum_{i=1}^{N} \\mathbf{1}\\{D_i > C\\}

whose standard error is :math:`\\sqrt{p(1-p)/N}`.

Real-world application
----------------------
Estimate the probability that a network server becomes overloaded when
incoming demand is uncertain — a canonical reliability and capacity-
planning question.

Interpretation of the output
----------------------------
* ``overload_probability`` — estimated probability that demand exceeds
  capacity in a given interval.
* ``overload_count`` — number of simulated scenarios that exceeded
  capacity.
* The figure plots the running estimate against number of simulations on
  a log x-axis, showing the characteristic convergence toward the true
  probability.
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
# Problem constants
# -----------------------------------------------------------------------------
CAPACITY: float = 1000.0  # units of demand served per interval
MEAN_DEMAND: float = 850.0  # μ of Gaussian demand
STD_DEMAND: float = 120.0  # sigma of Gaussian demand
N_SIMULATIONS: int = 100_000
SEED: int = 42
PLOT_POINTS: int = 400  # log-spaced samples for the convergence plot


# -----------------------------------------------------------------------------
# Simulation
# -----------------------------------------------------------------------------
def simulate(n: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Draw ``n`` demand scenarios and compute the running estimate.

    Parameters
    ----------
    n : int
        Number of Monte Carlo trials.
    rng : numpy.random.Generator
        A seeded generator. Passing it in (rather than creating it
        inside) makes the function trivially testable with a fixed
        seed.

    Returns
    -------
    demand : numpy.ndarray, shape (n,)
        Sampled demand values.
    running_probability : numpy.ndarray, shape (n,)
        Running estimate ``overload_count / trials_so_far``.
    """
    demand = rng.normal(MEAN_DEMAND, STD_DEMAND, n)
    overloaded = demand > CAPACITY
    running_probability = np.cumsum(overloaded) / np.arange(1, n + 1)
    return demand, running_probability


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
def _log_spaced_indices(n: int, k: int) -> np.ndarray:
    """Indices at which to sample a running series for a log-x plot.

    Log-spaced sampling keeps the early, high-variance region legible
    without abandoning the converged tail.
    """
    idx = np.unique(np.logspace(0, np.log10(n), k).astype(int)) - 1
    return idx[idx >= 0]


def _plot_convergence(running: np.ndarray, probability: float) -> None:
    ensure_dirs()
    idx = _log_spaced_indices(running.size, PLOT_POINTS)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.semilogx(idx + 1, running[idx], color="teal", label="Running estimate")
    ax.axhline(probability, linestyle="--", color="crimson", label=f"final ≈ {probability:.4f}")
    ax.set_xlabel("Number of simulations")
    ax.set_ylabel("Estimated overload probability")
    ax.set_title("Monte Carlo estimate of server-overload risk")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "task20_monte_carlo.png", dpi=200)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Estimate server overload probability via Monte Carlo.

    Returns
    -------
    dict
        Keys: ``constants``, ``n_simulations``, ``seed``,
        ``overload_probability``, ``overload_count``, ``std_error``.
    """
    configure_logging()

    rng = np.random.default_rng(SEED)
    demand, running = simulate(N_SIMULATIONS, rng)

    overloaded = demand > CAPACITY
    probability = float(overloaded.mean())
    count = int(overloaded.sum())
    std_error = float(np.sqrt(probability * (1.0 - probability) / N_SIMULATIONS))

    logger.info(
        "Model: demand ~ N(μ=%.1f, sigma=%.1f), capacity=%.1f",
        MEAN_DEMAND,
        STD_DEMAND,
        CAPACITY,
    )
    logger.info("Simulations: %d", N_SIMULATIONS)
    logger.info("Estimated overload probability: %.4f%%", probability * 100.0)
    logger.info("Overload cases: %d / %d", count, N_SIMULATIONS)
    logger.info("Standard error: %.6f (≈%.4f%%)", std_error, std_error * 100.0)

    _plot_convergence(running, probability)
    logger.info("Saved figure: %s", FIGURES_DIR / "task20_monte_carlo.png")

    payload = {
        "constants": {
            "capacity": CAPACITY,
            "mean_demand": MEAN_DEMAND,
            "std_demand": STD_DEMAND,
        },
        "n_simulations": N_SIMULATIONS,
        "seed": SEED,
        "overload_probability": probability,
        "overload_count": count,
        "std_error": std_error,
    }
    save_results("task20_monte_carlo", payload, seed=SEED)
    return payload


if __name__ == "__main__":
    main()
