"""Command-line entry point for the BIT 2118 package.

Usage
-----
::

    python -m bit2118                  # run every task (default)
    python -m bit2118 list             # list every registered task
    python -m bit2118 run              # same as no subcommand
    python -m bit2118 run task07       # run one task (prefix match)
    python -m bit2118 run task07 task11 task14   # run several
    python -m bit2118 run --fail-fast  # abort on first error

Exit codes
----------
0
    Every requested task succeeded.
1
    At least one task failed, or an invalid argument was supplied.
"""

from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Sequence

from . import __version__
from .logging_config import configure_logging
from .registry import TASKS, find_task, run_all

logger = logging.getLogger("bit2118.cli")


# -----------------------------------------------------------------------------
# Parser
# -----------------------------------------------------------------------------
def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bit2118",
        description=(
            "BIT 2118 Scientific Computing — batch runner. "
            "Executes every task module and writes figures + JSON results."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  python -m bit2118                 run every task\n"
            "  python -m bit2118 list            list registered tasks\n"
            "  python -m bit2118 run task07      run one task (prefix match)\n"
            "  python -m bit2118 run --fail-fast abort on first error\n"
        ),
    )
    parser.add_argument("--version", action="version", version=f"bit2118 {__version__}")

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List every registered task.")

    run_p = sub.add_parser("run", help="Run one or more tasks (default: all).")
    run_p.add_argument(
        "tasks",
        nargs="*",
        help="Task identifiers, prefixes or substrings. Omit to run all.",
    )
    run_p.add_argument(
        "--fail-fast",
        action="store_true",
        help="Abort on the first failing task.",
    )
    run_p.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable DEBUG-level logging.",
    )

    return parser


# -----------------------------------------------------------------------------
# Commands
# -----------------------------------------------------------------------------
def _cmd_list() -> int:
    """Print every registered task in a fixed-width table."""
    width = max(len(t.id) for t in TASKS)
    print(f"{'TASK'.ljust(width)}  DESCRIPTION")
    print(f"{'-' * width}  {'-' * 60}")
    for task in TASKS:
        print(f"{task.id.ljust(width)}  {task.description}")
    return 0


def _cmd_run(task_queries: Sequence[str], *, fail_fast: bool, verbose: bool) -> int:
    """Run the selected tasks and return a process exit code."""
    configure_logging(logging.DEBUG if verbose else logging.INFO)

    # Resolve any user-supplied queries up front so a typo fails fast
    # before we start executing tasks.
    resolved_ids: list[str] | None
    if task_queries:
        try:
            resolved_ids = [find_task(q).id for q in task_queries]
        except LookupError as exc:
            logger.error("%s", exc)
            return 1
    else:
        resolved_ids = None

    logger.info(
        "Running %d task(s) from %s",
        len(resolved_ids) if resolved_ids else len(TASKS),
        "selection" if resolved_ids else "registry",
    )

    summary = run_all(only=resolved_ids, fail_fast=fail_fast)

    # Compact end-of-run report.
    succeeded = [k for k, v in summary.items() if not isinstance(v, BaseException)]
    failed = [(k, v) for k, v in summary.items() if isinstance(v, BaseException)]

    print()
    print(f"{'=' * 68}")
    print(f"  {len(succeeded)} succeeded · {len(failed)} failed")
    print(f"{'=' * 68}")
    if failed:
        for tid, exc in failed:
            print(f"  ✘ {tid}: {exc}")
        return 1
    return 0


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main(argv: Sequence[str] | None = None) -> int:
    """Parse ``argv`` (defaults to :data:`sys.argv`) and dispatch.

    Returns
    -------
    int
        Process exit code.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "list":
        return _cmd_list()

    if args.command in (None, "run"):
        # Support both `python -m bit2118` and `python -m bit2118 run ...`.
        task_queries = getattr(args, "tasks", []) or []
        fail_fast = bool(getattr(args, "fail_fast", False))
        verbose = bool(getattr(args, "verbose", False))
        return _cmd_run(task_queries, fail_fast=fail_fast, verbose=verbose)

    parser.print_help()
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)
