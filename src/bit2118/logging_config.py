"""Shared logging configuration used by every task module.

Design notes
------------
* **Idempotent.** ``configure_logging`` can safely be called multiple
  times (each ``main()`` calls it). Repeated calls with ``force=False``
  are no-ops once the root logger already has a handler.
* **Console by default.** The format is compact and timestamped so
  terminal output reads like a run log. An optional file handler can be
  attached for reproducing a session.
* **Library-safe.** Importing this module has *no* side effects — it
  only touches the root logger when :func:`configure_logging` is called.

Usage
-----
Each task module does::

    from bit2118.logging_config import configure_logging, get_logger
    logger = get_logger(__name__)

    def main() -> dict:
        configure_logging()
        logger.info("starting task ...")

:func:`get_logger` returns the standard :class:`logging.Logger`; calling
it does not configure anything, so importing a task module never mutates
global logging state.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

__all__ = ["DEFAULT_DATEFMT", "DEFAULT_FORMAT", "configure_logging", "get_logger"]


DEFAULT_FORMAT: str = "%(asctime)s | %(levelname)-7s | %(name)-32s | %(message)s"
"""Default log record format.

The ``%(name)-32s`` field keeps alignment readable when several modules
emit into the same stream — handy when running ``python -m bit2118``.
"""

DEFAULT_DATEFMT: str = "%H:%M:%S"
"""Timestamp format used with :data:`DEFAULT_FORMAT`."""


def configure_logging(
    level: int = logging.INFO,
    *,
    log_file: str | Path | None = None,
    force: bool = False,
) -> logging.Logger:
    """Configure the root logger with a console handler and optional file.

    Parameters
    ----------
    level : int, optional
        Logging level applied to the root logger (default: ``logging.INFO``).
    log_file : str or pathlib.Path, optional
        If provided, a :class:`logging.FileHandler` is attached writing to
        this path with the same format as the console. Parent directories
        are created automatically.
    force : bool, optional
        When ``True``, remove existing root handlers before configuring.
        Useful in notebooks or tests where a handler may already be
        attached. When ``False`` (default), a second call is a no-op if
        the root logger is already configured.

    Returns
    -------
    logging.Logger
        The root logger, for chaining or direct use.

    Notes
    -----
    Attaching handlers is the only side effect. The function never lowers
    an already-configured level unless ``force=True``.
    """
    root = logging.getLogger()

    already_configured = bool(root.handlers) and not force
    if already_configured:
        # Respect the caller's level request even on a no-op path so
        # `configure_logging(DEBUG)` after an INFO call behaves sensibly.
        if level < root.level or root.level == logging.NOTSET:
            root.setLevel(level)
        return root

    if force:
        for handler in list(root.handlers):
            root.removeHandler(handler)
            handler.close()

    root.setLevel(level)

    formatter = logging.Formatter(fmt=DEFAULT_FORMAT, datefmt=DEFAULT_DATEFMT)

    console = logging.StreamHandler(stream=sys.stdout)
    console.setFormatter(formatter)
    root.addHandler(console)

    if log_file is not None:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(path, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    # Silence noisy third-party loggers below WARNING so our own output
    # stays legible when batch-running every task.
    for noisy in ("matplotlib", "PIL", "scipy", "numpy"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    return root


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger with the given name.

    A thin wrapper around :func:`logging.getLogger` used so that every
    task module obtains its logger the same way. It performs no
    configuration; call :func:`configure_logging` from ``main()`` for
    that.
    """
    return logging.getLogger(name)
