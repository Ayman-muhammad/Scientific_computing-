"""BIT 2118 Scientific Computing — reference package.

Each ``taskNN_*`` module is a self-contained, runnable demonstration of one
numerical concept from the module brief.  Every module:

* exposes a ``main()`` function that returns a results dictionary,
* writes its figures to ``report/figures/`` and its JSON metrics to
  ``results/`` via the helpers in :mod:`bit2118.io_utils`,
* uses deterministic random seeds so results are reproducible,
* is discoverable through :mod:`bit2118.registry` and runnable via
  ``python -m bit2118``.

Public surface
--------------
The package re-exports the small set of utilities that downstream code
(including tests) is expected to use:

* :data:`bit2118.__version__` — semantic version of the package.
* :func:`bit2118.configure_logging` / :func:`bit2118.get_logger`
  — shared logging configuration.
* :func:`bit2118.save_results` / :func:`bit2118.load_results`
  — JSON result persistence.
* :data:`bit2118.REPO_ROOT`, :data:`bit2118.RESULTS_DIR`,
  :data:`bit2118.FIGURES_DIR`, and :func:`bit2118.ensure_dirs`
  — canonical filesystem locations.
"""

from __future__ import annotations

__version__: str = "1.0.0"
__author__: str = "Ayman Muhammad"
__license__: str = "MIT"

# Re-export the utilities most callers need. Keeping the imports here means
# a caller can write ``from bit2118 import save_results`` instead of digging
# into submodules, while the submodules themselves remain independently
# importable (which the tests rely on).
from .io_utils import load_results, save_results
from .logging_config import configure_logging, get_logger
from .paths import FIGURES_DIR, REPO_ROOT, RESULTS_DIR, ensure_dirs

__all__ = [
    "FIGURES_DIR",
    "REPO_ROOT",
    "RESULTS_DIR",
    "__author__",
    "__license__",
    "__version__",
    "configure_logging",
    "ensure_dirs",
    "get_logger",
    "load_results",
    "save_results",
]
