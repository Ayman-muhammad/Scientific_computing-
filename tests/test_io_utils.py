"""Tests for :mod:`bit2118.io_utils`.

Covers the JSON contract: automatic ``task`` and ``meta`` keys, NumPy
serialisation, atomic write, and round-trip fidelity. Uses a temporary
``RESULTS_DIR`` via monkeypatching so tests never pollute the real
``results/`` directory that ships with the repository.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from bit2118 import io_utils
from bit2118.io_utils import (
    build_meta,
    load_results,
    results_path,
    save_results,
)


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture()
def tmp_results(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect ``RESULTS_DIR`` to a per-test temporary directory.

    Patches both :mod:`bit2118.paths` and :mod:`bit2118.io_utils` names so
    that every call into the module sees the sandbox directory.
    """
    sandbox = tmp_path / "results"
    sandbox.mkdir()

    from bit2118 import paths as paths_mod

    monkeypatch.setattr(paths_mod, "RESULTS_DIR", sandbox, raising=True)
    monkeypatch.setattr(io_utils, "RESULTS_DIR", sandbox, raising=True)
    return sandbox


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_build_meta_contains_expected_keys() -> None:
    """``build_meta`` must include timestamp, version and platform."""
    meta = build_meta()
    for key in ("timestamp", "package_version", "python_version", "platform"):
        assert key in meta, f"meta is missing key {key!r}"
    assert isinstance(meta["timestamp"], str) and "T" in meta["timestamp"]


def test_build_meta_records_seed_when_supplied() -> None:
    meta = build_meta(seed=123)
    assert meta["seed"] == 123


def test_results_path_appends_json_suffix() -> None:
    assert results_path("foo").name == "foo.json"
    assert results_path("foo.json").name == "foo.json"


def test_save_and_load_round_trip(tmp_results: Path) -> None:
    """Data written by ``save_results`` must be recoverable verbatim."""
    payload = {"x": np.array([1.0, 2.0, 3.0]), "n": 3, "flag": True}
    path = save_results("round_trip", payload)

    assert path.exists()
    assert path.parent == tmp_results

    loaded = load_results("round_trip")
    assert loaded["task"] == "round_trip"
    assert loaded["n"] == 3
    assert loaded["flag"] is True
    assert loaded["x"] == [1.0, 2.0, 3.0]
    assert "meta" in loaded and "timestamp" in loaded["meta"]


def test_save_injects_meta_with_seed(tmp_results: Path) -> None:
    save_results("seeded", {"value": 1}, seed=42)
    loaded = load_results("seeded")
    assert loaded["meta"]["seed"] == 42


def test_numpy_scalars_are_serialised(tmp_results: Path) -> None:
    """NumPy scalar types must be converted to Python scalars."""
    payload = {
        "int": np.int64(7),
        "float": np.float64(3.14),
        "bool": np.bool_(True),
    }
    save_results("scalars", payload)
    on_disk = json.loads((tmp_results / "scalars.json").read_text())
    assert on_disk["int"] == 7 and isinstance(on_disk["int"], int)
    assert on_disk["float"] == 3.14 and isinstance(on_disk["float"], float)
    assert on_disk["bool"] is True


def test_unsupported_type_raises(tmp_results: Path) -> None:
    class Weird:
        pass

    with pytest.raises(TypeError):
        save_results("bad", {"x": Weird()})


def test_load_missing_file_raises(tmp_results: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_results("does_not_exist")


def test_overwrite_false_keeps_existing(tmp_results: Path) -> None:
    save_results("keep", {"version": 1})
    save_results("keep", {"version": 2}, overwrite=False)
    loaded = load_results("keep")
    assert loaded["version"] == 1


def test_results_path_rejects_path_traversal() -> None:
    with pytest.raises(ValueError):
        results_path("../outside")
    with pytest.raises(ValueError):
        results_path("nested/task")


def test_results_path_accepts_task_identifiers() -> None:
    assert results_path("task02_numpy_arrays").name == "task02_numpy_arrays.json"
    assert results_path("task02_numpy_arrays.json").name == "task02_numpy_arrays.json"


def test_non_finite_numbers_are_rejected_without_leaving_temp_files(
    tmp_results: Path,
) -> None:
    with pytest.raises(ValueError):
        save_results("invalid_numeric", {"value": float("nan")})

    assert not (tmp_results / "invalid_numeric.json").exists()
    assert list(tmp_results.glob("*.tmp")) == []
