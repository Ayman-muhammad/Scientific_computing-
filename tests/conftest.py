"""Shared pytest fixtures and configuration.

Fixtures here are minimal by design: most tests build their own inputs
explicitly so failures point to a specific claim rather than to
background state. The exception is :func:`rng`, which standardises the
seeded generator used by any stochastic test.
"""

from __future__ import annotations

from collections.abc import Iterator

import numpy as np
import pytest


@pytest.fixture()
def rng() -> Iterator[np.random.Generator]:
    """A fresh, deterministically-seeded NumPy generator per test.

    Using a fixture (rather than a module-level constant) guarantees
    that no test can influence another via shared RNG state, which
    would otherwise make failures order-dependent.
    """
    yield np.random.default_rng(20250101)


@pytest.fixture(scope="session", autouse=True)
def _silence_matplotlib() -> None:
    """Force the non-interactive Agg backend for the entire test session.

    Some task modules call ``matplotlib.use("Agg")`` at import time, but
    matplotlib's backend cannot be switched after pyplot has loaded a
    different one. Setting ``MPLBACKEND`` here — before any task module
    is imported — avoids the warning entirely and is a hard requirement
    on headless CI runners.
    """
    import os

    os.environ.setdefault("MPLBACKEND", "Agg")
