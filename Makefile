# =============================================================================
# BIT 2118 Scientific Computing — developer ergonomics
# -----------------------------------------------------------------------------
# Usage:
#   make help      Show every target
#   make install   Editable install with dev extras
#   make run       Execute all tasks (figures + JSON)
#   make test      Run pytest with coverage
#   make lint      Ruff static checks
#   make format    Ruff auto-format
#   make clean     Remove caches and regenerable artefacts
# =============================================================================

PYTHON ?= python
PIP    ?= $(PYTHON) -m pip

.PHONY: help install run test lint format clean tree

# -----------------------------------------------------------------------------
help:
	@echo "BIT 2118 Scientific Computing — available targets"
	@echo "--------------------------------------------------"
	@echo "  install   Install package in editable mode with dev extras"
	@echo "  run       Execute every task (writes results/ and report/figures/)"
	@echo "  test      Run pytest with coverage"
	@echo "  lint      Run ruff static analysis"
	@echo "  format    Auto-format src/ and tests/ with ruff"
	@echo "  clean     Remove caches and regenerated artefacts"
	@echo "  tree      Print the repository tree"

# -----------------------------------------------------------------------------
install:
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

run:
	$(PYTHON) -m bit2118

test:
	$(PYTHON) -m pytest -v

lint:
	$(PYTHON) -m ruff check src tests

format:
	$(PYTHON) -m ruff format src tests

# -----------------------------------------------------------------------------
clean:
	rm -rf .pytest_cache .coverage htmlcov .ruff_cache .mypy_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +
	rm -f results/*.json
	rm -f report/figures/*.png
	@echo "Cleaned caches and generated artefacts."

tree:
	@find . -type f -not -path './.git/*' -not -path './.venv/*' \
		-not -path '*/__pycache__/*' | sort