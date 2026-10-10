"""Task 03 — Mathematical Functions and Vectorization.

Concept
-------
Vectorisation applies an operation to an entire array at once. For example
``sin²(x) + cos²(x) == 1`` element-wise for every element of ``x``, with no
Python-level loop.

Mathematical formulation
------------------------
Given a vector of samples :math:`x` and a scalar transformation
:math:`y_i = (x_i / 1000)^2`, NumPy evaluates

.. math::

    y = (x / 1000)^2

in C, using SIMD instructions where available. The same expression applied
by a Python ``for`` loop runs one scalar operation per iteration.

Real-world application
----------------------
A network-monitoring system receives latency measurements in milliseconds.
This task compares a Python loop with NumPy vectorisation. The speed-up is
measured on the current machine; no fixed performance ratio is assumed.

Interpretation of the output
----------------------------
* ``loop_time_s`` — wall-clock time of the pure-Python implementation.
* ``vector_time_s`` — wall-clock time of the NumPy implementation.
* ``speedup`` — ratio ``loop_time / vector_time``; higher is better.
"""

from __future__ import annotations

import timeit
from statistics import median

import numpy as np

from .io_utils import save_results
from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
N_SAMPLES: int = 1_000_000
SEED: int = 42
LATENCY_MIN_MS: float = 5.0
LATENCY_MAX_MS: float = 250.0
BENCHMARK_REPEATS: int = 3


# -----------------------------------------------------------------------------
# Pure functions
# -----------------------------------------------------------------------------
def loop_version(latency_ms: np.ndarray) -> list[float]:
    """Baseline: pure-Python loop over the samples.

    Parameters
    ----------
    latency_ms : numpy.ndarray
        Latency samples in milliseconds.

    Returns
    -------
    list of float
        ``(latency_ms / 1000)²`` computed element by element.
    """
    squared: list[float] = []
    for value in latency_ms:
        seconds = value / 1000.0
        squared.append(seconds**2)
    return squared


def vectorized_version(latency_ms: np.ndarray) -> np.ndarray:
    """Vectorised: single expression, no Python-level loop.

    Parameters
    ----------
    latency_ms : numpy.ndarray
        Latency samples in milliseconds.

    Returns
    -------
    numpy.ndarray
        ``(latency_ms / 1000)²`` computed in C across the whole array.
    """
    seconds = latency_ms / 1000.0
    return seconds**2


def make_samples(n: int, *, seed: int = SEED) -> np.ndarray:
    """Generate ``n`` synthetic latency samples in milliseconds.

    Uses ``default_rng`` (the modern generator) so results are fully
    independent of the legacy global random state.
    """
    rng = np.random.default_rng(seed)
    return rng.uniform(LATENCY_MIN_MS, LATENCY_MAX_MS, n)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Benchmark the loop vs the vectorised implementation.

    Returns
    -------
    dict
        Keys: ``n_samples``, ``loop_time_s``, ``vector_time_s``,
        ``speedup``, ``first_five`` (first five squared values).
    """
    configure_logging()

    latency_ms = make_samples(N_SAMPLES)

    # Warm up both implementations on the same representative sample.
    # Correctness is checked separately from timing so the benchmark cannot
    # silently report a speed-up for mathematically different outputs.
    warmup = latency_ms[: min(10_000, latency_ms.size)]
    loop_version(warmup)
    vectorized_version(warmup)
    if not np.allclose(
        np.asarray(loop_version(warmup)),
        vectorized_version(warmup),
        rtol=1e-12,
        atol=1e-15,
    ):
        raise RuntimeError("Loop and vectorised implementations produced different results.")

    # Repeat both implementations equally and report the median to reduce
    # sensitivity to a single noisy timing sample.
    loop_times = timeit.repeat(
        lambda: loop_version(latency_ms),
        repeat=BENCHMARK_REPEATS,
        number=1,
    )
    vector_times = timeit.repeat(
        lambda: vectorized_version(latency_ms),
        repeat=BENCHMARK_REPEATS,
        number=1,
    )
    loop_time = median(loop_times)
    vector_time = median(vector_times)
    if vector_time <= 0.0:
        raise RuntimeError("Vectorised benchmark duration must be positive.")
    speedup = loop_time / vector_time

    result = vectorized_version(latency_ms)

    logger.info("Samples:          %d", N_SAMPLES)
    logger.info("Loop time:        %.4f s", loop_time)
    logger.info("Vectorised time:  %.4f s", vector_time)
    logger.info("Speed-up:         %.1fx", speedup)
    logger.info("First five squared latencies: %s", result[:5])

    payload = {
        "n_samples": N_SAMPLES,
        "loop_time_s": loop_time,
        "vector_time_s": vector_time,
        "speedup": speedup,
        "first_five": result[:5],
    }
    save_results("task03_vectorization", payload, seed=SEED)
    return payload


if __name__ == "__main__":
    main()
