"""Tests for :mod:`bit2118.paths`.

Verifies that the canonical filesystem locations resolve to *some*
absolute path, that their logical layout is preserved
(``results/`` and ``report/figures/`` are siblings of ``src/``), and
that :func:`ensure_dirs` is idempotent.
"""

from __future__ import annotations

from pathlib import Path

from bit2118 import FIGURES_DIR, REPO_ROOT, RESULTS_DIR, ensure_dirs


def test_repo_root_is_absolute() -> None:
    """The detected repository root must be absolute, not relative."""
    assert REPO_ROOT.is_absolute(), f"REPO_ROOT is not absolute: {REPO_ROOT}"


def test_expected_subdirectories_are_under_repo_root() -> None:
    """``RESULTS_DIR`` and ``FIGURES_DIR`` must live under the repo root."""
    assert RESULTS_DIR.parent == REPO_ROOT, (
        f"RESULTS_DIR {RESULTS_DIR} is not directly under REPO_ROOT {REPO_ROOT}"
    )
    assert FIGURES_DIR.parent.parent == REPO_ROOT, (
        f"FIGURES_DIR {FIGURES_DIR} is not under report/ under REPO_ROOT"
    )
    assert FIGURES_DIR.name == "figures"
    assert RESULTS_DIR.name == "results"


def test_anchor_detection() -> None:
    """The detected root must contain a ``pyproject.toml`` anchor file."""
    # If this fails, the fallback path was used (editable install broken
    # or wrong working directory).
    assert (REPO_ROOT / "pyproject.toml").is_file(), (
        f"REPO_ROOT {REPO_ROOT} does not contain pyproject.toml — anchor "
        "detection failed and the fallback (cwd) was used."
    )


def test_ensure_dirs_is_idempotent(tmp_path: Path) -> None:
    """Calling ``ensure_dirs`` twice on the same path must not raise."""
    target = tmp_path / "a" / "b" / "c"
    ensure_dirs(target)
    assert target.is_dir()
    ensure_dirs(target)  # second call must be a no-op
    assert target.is_dir()


def test_ensure_dirs_creates_default_targets() -> None:
    """Calling ``ensure_dirs()`` with no args creates the standard two."""
    ensure_dirs()
    assert RESULTS_DIR.is_dir()
    assert FIGURES_DIR.is_dir()
