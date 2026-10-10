"""Registry of every task module, used by the batch runner.

Each entry maps a task identifier to its module name and a short
description. Modules are imported *lazily* by :func:`load_task` so
running a single task never pays for the imports of the other eighteen.

Adding a task
-------------
1. Append a :class:`TaskEntry` to :data:`TASKS` in the correct slot.
2. Make sure the module exposes a callable ``main()`` returning a
   mapping. That is the only interface the registry relies on.
"""

from __future__ import annotations

import importlib
import logging
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from types import ModuleType

__all__ = [
    "TASKS",
    "TaskEntry",
    "find_task",
    "iter_modules",
    "load_task",
    "run_all",
    "run_task",
]

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class TaskEntry:
    """One entry in the task registry.

    Attributes
    ----------
    id : str
        Stable identifier, e.g. ``"task07_gaussian_lu"``. Matches the
        module's filename without the ``.py`` suffix.
    module : str
        Fully-qualified module name under the package, e.g.
        ``"bit2118.task07_gaussian_lu"``.
    description : str
        One-line summary used in ``python -m bit2118 list``.
    """

    id: str
    module: str
    description: str


# -----------------------------------------------------------------------------
# Registry — order reflects the module brief (Tasks 02 → 20)
# -----------------------------------------------------------------------------
TASKS: tuple[TaskEntry, ...] = (
    TaskEntry(
        "task02_numpy_arrays",
        "bit2118.task02_numpy_arrays",
        "NumPy arrays: daily statistics and vectorised unit conversion.",
    ),
    TaskEntry(
        "task03_vectorization",
        "bit2118.task03_vectorization",
        "Vectorisation: loop vs NumPy benchmark on latency samples.",
    ),
    TaskEntry(
        "task04_floating_point",
        "bit2118.task04_floating_point",
        "Floating-point error: comparison pitfalls and stability rewrites.",
    ),
    TaskEntry(
        "task05_matrix_algebra",
        "bit2118.task05_matrix_algebra",
        "Matrix algebra: 2-D rotation and scaling transform.",
    ),
    TaskEntry(
        "task06_linear_systems",
        "bit2118.task06_linear_systems",
        "Linear systems: server resource allocation via A x = b.",
    ),
    TaskEntry(
        "task07_gaussian_lu",
        "bit2118.task07_gaussian_lu",
        "LU decomposition: factor once, solve many right-hand sides.",
    ),
    TaskEntry(
        "task08_iterative_linear",
        "bit2118.task08_iterative_linear",
        "Jacobi and Gauss-Seidel on a 1-D steady-state heat model.",
    ),
    TaskEntry(
        "task09_eigenvalues",
        "bit2118.task09_eigenvalues",
        "Eigenvalues and eigenvectors: network centrality.",
    ),
    TaskEntry(
        "task10_bisection_fixed_point",
        "bit2118.task10_bisection_fixed_point",
        "Bisection and fixed-point iteration on a heat-balance model.",
    ),
    TaskEntry(
        "task11_newton_secant",
        "bit2118.task11_newton_secant",
        "Newton-Raphson and secant methods for internal rate of return.",
    ),
    TaskEntry(
        "task12_nonlinear_equations",
        "bit2118.task12_nonlinear_equations",
        "Nonlinear systems: intersections of a circle and a parabola.",
    ),
    TaskEntry(
        "task13_interpolation",
        "bit2118.task13_interpolation",
        "Interpolation: linear vs cubic spline on hourly temperatures.",
    ),
    TaskEntry(
        "task14_curve_fitting",
        "bit2118.task14_curve_fitting",
        "Curve fitting: quadratic model of server response time.",
    ),
    TaskEntry(
        "task15_numerical_differentiation",
        "bit2118.task15_numerical_differentiation",
        "Numerical differentiation: GPS speed estimation.",
    ),
    TaskEntry(
        "task16_numerical_integration",
        "bit2118.task16_numerical_integration",
        "Numerical integration: energy from smart-meter readings.",
    ),
    TaskEntry(
        "task17_euler_ode",
        "bit2118.task17_euler_ode",
        "Euler method: Newton's law of cooling.",
    ),
    TaskEntry(
        "task18_scipy_ode",
        "bit2118.task18_scipy_ode",
        "solve_ivp: RC circuit charging.",
    ),
    TaskEntry(
        "task19_optimization",
        "bit2118.task19_optimization",
        "Constrained optimisation: cloud capacity planning.",
    ),
    TaskEntry(
        "task20_monte_carlo",
        "bit2118.task20_monte_carlo",
        "Monte Carlo: server-overload risk estimation.",
    ),
)


# -----------------------------------------------------------------------------
# Lookup helpers
# -----------------------------------------------------------------------------
def find_task(query: str) -> TaskEntry:
    """Return the unique registry entry matching ``query``.

    Matching rules, in order of precedence:

    1. **Exact identifier** — ``"task07_gaussian_lu"``.
    2. **Prefix** — ``"task07"`` matches the same entry.
    3. **Substring** — ``"gaussian"`` matches the same entry.

    Parameters
    ----------
    query : str
        Identifier, prefix or substring. Case-insensitive.

    Returns
    -------
    TaskEntry

    Raises
    ------
    LookupError
        If no entry matches, or if the substring form is ambiguous.
    """
    needle = query.strip().lower()
    if not needle:
        raise LookupError("Empty task query.")

    # 1. Exact id.
    for entry in TASKS:
        if entry.id.lower() == needle:
            return entry

    # 2. Prefix.
    prefix_hits = [e for e in TASKS if e.id.lower().startswith(needle)]
    if len(prefix_hits) == 1:
        return prefix_hits[0]

    # 3. Substring.
    sub_hits = [e for e in TASKS if needle in e.id.lower()]
    if len(sub_hits) == 1:
        return sub_hits[0]
    if len(sub_hits) > 1:
        options = ", ".join(e.id for e in sub_hits)
        raise LookupError(f"Ambiguous task query {query!r}. Candidates: {options}")

    raise LookupError(f"No task matches {query!r}. Run `python -m bit2118 list` to see options.")


def iter_modules(entries: Iterable[TaskEntry] | None = None) -> Iterable[TaskEntry]:
    """Yield registry entries (defaults to the full registry)."""
    yield from (entries if entries is not None else TASKS)


# -----------------------------------------------------------------------------
# Execution helpers
# -----------------------------------------------------------------------------
def load_task(entry: TaskEntry) -> ModuleType:
    """Import and return the module referenced by ``entry``.

    The import happens exactly once per process — subsequent calls
    return the cached module from :data:`sys.modules`.
    """
    module = importlib.import_module(entry.module)
    return module


def _resolve_main(module: ModuleType) -> Callable[[], Mapping[str, object]]:
    """Return the module's ``main`` callable, or raise a clear error."""
    main = getattr(module, "main", None)
    if not callable(main):
        raise AttributeError(f"Module {module.__name__!r} does not expose a callable main().")
    return main


def run_task(entry: TaskEntry) -> Mapping[str, object]:
    """Import ``entry``, call its ``main()``, and return the results."""
    logger.info("▶ %s — %s", entry.id, entry.description)
    module = load_task(entry)
    main = _resolve_main(module)
    result = main()
    if not isinstance(result, Mapping):
        raise TypeError(
            f"{entry.module}.main() must return a mapping, got {type(result).__name__}."
        )
    logger.info("✔ %s done", entry.id)
    return result


def run_all(
    *,
    only: Iterable[str] | None = None,
    fail_fast: bool = False,
) -> dict[str, Mapping[str, object] | BaseException]:
    """Run every task (or a subset) and return a status map.

    Parameters
    ----------
    only : iterable of str, optional
        Task identifiers to run. If omitted, every task runs in registry
        order.
    fail_fast : bool, optional
        When ``True``, the first exception aborts the batch. Otherwise
        failures are recorded and the run continues.

    Returns
    -------
    dict
        Maps task id → the mapping returned by ``main()``, or the
        exception instance if the task failed.
    """
    entries: list[TaskEntry]
    entries = list(TASKS) if only is None else [find_task(q) for q in only]

    summary: dict[str, Mapping[str, object] | BaseException] = {}
    for entry in entries:
        try:
            summary[entry.id] = run_task(entry)
        except BaseException as exc:
            logger.error("✘ %s failed: %s", entry.id, exc)
            summary[entry.id] = exc
            if fail_fast:
                raise
    return summary
