"""Task 14 — Curve Fitting and Approximation.

Concept
-------
Curve fitting chooses model parameters so a mathematical function follows
observed data as closely as possible. In least squares, the parameters
minimise the sum of squared residuals between observations and model
predictions.

Mathematical formulation
------------------------
For a model :math:`y = f(x; \\theta)` and observations
:math:`(x_i, y_i)`, least squares solves

.. math::

    \\hat{\\theta} = \\arg\\min_{\\theta} \\sum_{i=1}^{n}
        \\bigl(y_i - f(x_i; \\theta)\\bigr)^2

``scipy.optimize.curve_fit`` solves this iteratively via Levenberg-
Marquardt (or Trust Region Reflective when bounds are set). The
root-mean-square error,

.. math::

    \\text{RMSE} = \\sqrt{\\tfrac{1}{n}\\sum_{i=1}^{n}
        \\bigl(y_i - f(x_i; \\hat{\\theta})\\bigr)^2}

quantifies the average absolute error in the same units as the response.

Real-world application
----------------------
Model server response time as a function of concurrent user load. The
quadratic captures the well-known super-linear degradation once
contention kicks in.

Interpretation of the output
----------------------------
* ``params`` — fitted coefficients ``(a, b, c)`` for
  ``y = a x² + b x + c``.
* ``rmse_ms`` — root-mean-square error in milliseconds.
* ``predicted_400_users_ms`` — extrapolated response time at 400 users.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from .io_utils import save_results
from .logging_config import configure_logging, get_logger
from .paths import FIGURES_DIR, ensure_dirs

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Inputs — concurrent users vs measured response time (ms)
# -----------------------------------------------------------------------------
USERS: np.ndarray = np.array([50, 100, 150, 200, 250, 300, 350], dtype=float)
RESPONSE_MS: np.ndarray = np.array([82.0, 95.0, 115.0, 145.0, 185.0, 238.0, 305.0])

EXTRAPOLATION_X: float = 400.0


# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------
def model(x: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
    """Quadratic response-time model ``y = a x² + b x + c``."""
    return a * x**2 + b * x + c


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
def _plot_fit(
    users: np.ndarray,
    response: np.ndarray,
    a: float,
    b: float,
    c: float,
) -> None:
    ensure_dirs()
    x_plot = np.linspace(users.min(), EXTRAPOLATION_X, 300)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(users, response, color="black", label="Measurements")
    ax.plot(
        x_plot,
        model(x_plot, a, b, c),
        color="crimson",
        label=f"Fitted: y = {a:.3e}x² + {b:.3f}x + {c:.2f}",
    )
    ax.axvline(users.max(), linestyle=":", color="grey", alpha=0.6)
    ax.set_xlabel("Concurrent users")
    ax.set_ylabel("Response time (ms)")
    ax.set_title("Server response-time curve fitting")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "task14_curve_fitting.png", dpi=200)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Fit the quadratic model and report RMSE + extrapolation.

    Returns
    -------
    dict
        Keys: ``users``, ``response_ms``, ``params``, ``rmse_ms``,
        ``predicted_400_users_ms``, ``covariance``.
    """
    configure_logging()

    params, covariance = curve_fit(model, USERS, RESPONSE_MS)
    a, b, c = (float(p) for p in params)

    predicted = model(USERS, a, b, c)
    residuals = RESPONSE_MS - predicted
    rmse = float(np.sqrt(np.mean(residuals**2)))
    predicted_400 = float(model(EXTRAPOLATION_X, a, b, c))

    logger.info("Fitted model: y = %.6e x² + %.4f x + %.2f", a, b, c)
    logger.info("RMSE over training points: %.2f ms", rmse)
    logger.info("Predicted response at %.0f users: %.2f ms", EXTRAPOLATION_X, predicted_400)

    _plot_fit(USERS, RESPONSE_MS, a, b, c)
    logger.info("Saved figure: %s", FIGURES_DIR / "task14_curve_fitting.png")

    payload = {
        "users": USERS,
        "response_ms": RESPONSE_MS,
        "params": {"a": a, "b": b, "c": c},
        "rmse_ms": rmse,
        "predicted_400_users_ms": predicted_400,
        "covariance": covariance,
    }
    save_results("task14_curve_fitting", payload)
    return payload


if __name__ == "__main__":
    main()
