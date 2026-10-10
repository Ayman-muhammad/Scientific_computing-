"""Helpers for persisting task results as JSON.

Result contract
---------------
Every task writes exactly one file to :data:`bit2118.paths.RESULTS_DIR`,
named ``<task_module>.json``. The file always contains at least::

    {
      "task": "task07_gaussian_lu",
      "meta": {
        "timestamp": "2025-01-01T12:00:00Z",
        "package_version": "1.0.0",
        "python_version": "3.11.5",
        "platform": "Linux-6.5.0-x86_64",
        "seed": 42
      },
      ... task-specific keys ...
    }

The ``meta`` block is injected automatically unless the caller supplies
one; the ``task`` key is derived from the ``name`` argument. Callers
should not have to think about any of this — they simply pass their
results dictionary.
"""

from __future__ import annotations

import json
import logging
import os
import platform
import re
import sys
import tempfile
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from .paths import RESULTS_DIR, ensure_dirs

__all__ = [
    "build_meta",
    "load_results",
    "results_path",
    "save_results",
]

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# JSON encoding
# -----------------------------------------------------------------------------
def _json_default(obj: Any) -> Any:
    """Serialise NumPy and common non-JSON Python types.

    Supports:

    * ``numpy.ndarray``           → list
    * ``numpy.generic`` (scalars) → Python scalar via ``.item()``
    * ``pathlib.Path``            → str
    * ``datetime`` / ``date``     → ISO-8601 string
    * ``set`` / ``frozenset``     → sorted list (deterministic order)
    * ``tuple``                   → list

    Anything else raises :class:`TypeError` so unsupported types fail
    loudly rather than being silently dropped.
    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, (datetime,)):
        return obj.astimezone(timezone.utc).isoformat()
    if isinstance(obj, (set, frozenset)):
        return sorted(obj, key=repr)
    if isinstance(obj, tuple):
        return list(obj)
    raise TypeError(f"Object of type {type(obj).__name__!r} is not JSON serialisable")


# -----------------------------------------------------------------------------
# Metadata
# -----------------------------------------------------------------------------
def build_meta(*, seed: int | None = None) -> dict[str, Any]:
    """Return a fresh metadata dictionary for a results file.

    Parameters
    ----------
    seed : int, optional
        If the task used a random seed, pass it here so the exact
        numerical output can be reproduced.

    Returns
    -------
    dict
        Keys: ``timestamp``, ``package_version``, ``python_version``,
        ``platform``, and (if provided) ``seed``.
    """
    # Local import avoids a circular dependency with __init__.
    from . import __version__

    meta: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "package_version": __version__,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
    }
    if seed is not None:
        meta["seed"] = int(seed)
    return meta


# -----------------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------------
def results_path(name: str) -> Path:
    """Return ``RESULTS_DIR/<name>.json``.

    ``name`` may be a bare task name (``"task07_gaussian_lu"``) or a path
    fragment. The ``.json`` suffix is appended automatically if absent.
    """
    if not isinstance(name, str):
        raise TypeError("Result name must be a string.")

    stem = name[:-5] if name.endswith(".json") else name
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", stem):
        raise ValueError(
            "Result name must contain only letters, digits, underscores, and hyphens; "
            "path separators and traversal components are not allowed."
        )
    return RESULTS_DIR / f"{stem}.json"


def save_results(
    name: str,
    payload: Mapping[str, Any],
    *,
    seed: int | None = None,
    overwrite: bool = True,
) -> Path:
    """Persist ``payload`` to ``results/<name>.json`` and return the path.

    Parameters
    ----------
    name : str
        Task identifier, e.g. ``"task07_gaussian_lu"``.
    payload : Mapping[str, Any]
        The task's result dictionary. May contain NumPy arrays and
        scalars; both are JSON-serialised transparently.
    seed : int, optional
        The random seed used by the task, recorded under ``meta.seed``.
    overwrite : bool, optional
        When ``False`` and the target file already exists, the write is
        skipped and a warning is logged. Default is ``True``.

    Returns
    -------
    pathlib.Path
        The path written.

    Raises
    ------
    TypeError
        If ``payload`` contains a value that cannot be JSON-serialised.
    """
    ensure_dirs()
    out = results_path(name)

    if out.exists() and not overwrite:
        logger.warning("Not overwriting existing result file: %s", out)
        return out

    record: dict[str, Any] = dict(payload)
    record.setdefault("task", name)
    record.setdefault("meta", build_meta(seed=seed))

    # Use a unique temporary file in the destination directory so concurrent
    # task runs cannot overwrite one another's temporary output. os.replace()
    # is atomic on the same filesystem and prevents partial JSON from being read.
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=out.parent,
            prefix=f".{out.name}.",
            suffix=".tmp",
            delete=False,
        ) as fh:
            temporary_path = Path(fh.name)
            json.dump(
                record,
                fh,
                indent=2,
                sort_keys=False,
                default=_json_default,
                allow_nan=False,
            )
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())

        os.replace(temporary_path, out)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    logger.debug("Wrote result file: %s", out)
    return out


def load_results(name: str) -> dict[str, Any]:
    """Load and return the JSON record for ``name``.

    Parameters
    ----------
    name : str
        Task identifier; ``.json`` is appended if absent.

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    FileNotFoundError
        If ``results/<name>.json`` does not exist.
    """
    path = results_path(name)
    if not path.exists():
        raise FileNotFoundError(f"No results file at {path}. Run `python -m bit2118.{name}` first.")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)
