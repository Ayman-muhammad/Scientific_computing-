"""Task 02 — NumPy Arrays and Numerical Computation.

Concept
-------
An array is an ordered collection of numbers of the same dtype. A *vector*
is a 1-D array; a *matrix* is a 2-D array. NumPy evaluates an operation
over every element in a single call, without a Python-level loop.

Mathematical formulation
------------------------
Given a vector :math:`x = [x_1, \\dots, x_n]` and a scalar transformation
:math:`f(x) = 1.8x + 32`, NumPy computes

.. math::

    f(x) = [\\,f(x_1), f(x_2), \\dots, f(x_n)\\,]

element-wise. The sample mean is
:math:`\\bar{x} = \\tfrac{1}{n}\\sum_{i=1}^{n} x_i`.

Real-world application
----------------------
A weather station records 24 hourly temperature readings. We store them as
an array, compute the daily mean, minimum and maximum, and convert the
whole array from Celsius to Fahrenheit in one vectorised expression.

Interpretation of the output
----------------------------
* ``mean_c`` — central tendency of the day's temperature.
* ``min_c`` / ``max_c`` — diurnal range extrema.
* ``fahrenheit`` — the same curve in imperial units, useful for
  downstream reporting systems that consume Fahrenheit.
"""

from __future__ import annotations

import numpy as np

from .io_utils import save_results
from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Inputs — 24 hourly temperature readings in degrees Celsius (°C)
# -----------------------------------------------------------------------------
TEMPERATURES_C: np.ndarray = np.array(
    [
        18.5,
        18.0,
        17.8,
        17.5,
        17.9,
        19.0,
        21.5,
        23.8,
        25.6,
        27.1,
        28.3,
        29.0,
        29.4,
        29.1,
        28.5,
        27.6,
        26.2,
        24.8,
        23.4,
        22.1,
        21.0,
        20.2,
        19.6,
        19.0,
    ],
    dtype=float,
)


# -----------------------------------------------------------------------------
# Pure functions
# -----------------------------------------------------------------------------
def celsius_to_fahrenheit(celsius: np.ndarray) -> np.ndarray:
    """Vectorised Celsius → Fahrenheit conversion.

    Applies :math:`F = 1.8 \\, C + 32` element-wise. Demonstrates that
    NumPy broadcasts a scalar expression across an entire array without an
    explicit ``for`` loop.

    Parameters
    ----------
    celsius : numpy.ndarray
        Temperatures in degrees Celsius. Any shape.

    Returns
    -------
    numpy.ndarray
        Temperatures in degrees Fahrenheit, same shape as ``celsius``.
    """
    return 1.8 * celsius + 32.0


def daily_statistics(celsius: np.ndarray) -> tuple[float, float, float]:
    """Return ``(mean, min, max)`` of ``celsius`` as Python floats.

    NumPy reductions return ``numpy.float64`` scalars; casting to ``float``
    keeps the JSON output clean and makes tests trivially comparable.
    """
    return float(np.mean(celsius)), float(np.min(celsius)), float(np.max(celsius))


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Compute daily statistics and vectorised unit conversion.

    Returns
    -------
    dict
        Keys: ``mean_c``, ``min_c``, ``max_c``, ``fahrenheit``,
        ``n_readings``.
    """
    configure_logging()

    mean_c, min_c, max_c = daily_statistics(TEMPERATURES_C)
    fahrenheit = celsius_to_fahrenheit(TEMPERATURES_C)

    logger.info("Readings:    %d", TEMPERATURES_C.size)
    logger.info("Daily mean:  %.2f °C", mean_c)
    logger.info("Minimum:     %.2f °C", min_c)
    logger.info("Maximum:     %.2f °C", max_c)
    logger.info("First six Fahrenheit readings: %s", np.round(fahrenheit[:6], 2))

    payload = {
        "n_readings": int(TEMPERATURES_C.size),
        "temperatures_c": TEMPERATURES_C,
        "mean_c": mean_c,
        "min_c": min_c,
        "max_c": max_c,
        "fahrenheit": fahrenheit,
    }
    save_results("task02_numpy_arrays", payload)
    return payload


if __name__ == "__main__":
    main()
