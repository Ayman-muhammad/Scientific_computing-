# Reproducibility

Follow these steps on a clean machine to reproduce every artefact.

## 1. Environment

```bash
python -m venv .venv
source .venv/bin/activate         # Windows MINGW: source .venv/Scripts/activate
pip install -e ".[dev]"