# Documentation Index

Everything *about* the code that isn't the code itself. The aim is to keep
**mathematics** separated from **implementation**, so a reviewer can check
the derivation independently of the Python.

| File | Purpose |
|------|---------|
| [`architecture.md`](architecture.md) | Package layout, dependency graph, design decisions. |
| [`mathematical_notes.md`](mathematical_notes.md) | Compact derivations for every numerical method used. |
| [`methodology.md`](methodology.md) | How inputs, parameters, and tolerances were chosen. |
| [`reproducibility.md`](reproducibility.md) | Step-by-step reproduction of every artefact. |
| [`tasks/`](tasks/) | One focused page per task (02 → 20). |

## Conventions

* **Math** is written in LaTeX between `$...$` (inline) or `$$...$$` (block).
* Every task page follows the same six-section template:

  1. **Concept** — one-paragraph plain-English statement.
  2. **Mathematical formulation** — variables, equation(s), assumptions.
  3. **Algorithm** — pseudocode or step list.
  4. **Inputs & parameters** — with units and provenance.
  5. **Outputs** — fields in the corresponding `results/*.json`.
  6. **Interpretation** — what a non-specialist should read from the numbers.