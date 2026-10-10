# Architecture

## Goals

1. **Traceability.** Every figure and every number in the report can be
   traced to a single module and a single JSON file.
2. **Isolation.** Tasks must not import each other; a change in Task 08
   cannot silently alter Task 09's output.
3. **Repeatability.** A fresh clone, one command, identical artefacts.
4. **Testability.** Each task's mathematical core is a pure function,
   verified by at least one pytest assertion.

## Layers
