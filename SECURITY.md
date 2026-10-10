# Security Policy

## Supported Versions

The following versions receive security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

## Scope

This project is a **numerical-computing reference implementation**.
It has a deliberately small attack surface:

- **No network I/O.** No HTTP clients, no sockets, no remote data fetching.
- **No shell execution.** No `subprocess`, `os.system`, or `eval`/`exec`
  on user input.
- **No untrusted code paths.** All inputs are module-level constants or
  values produced internally.
- **No deserialisation of untrusted data.** Only JSON produced by the
  package itself is read.

Consequently, the classes of vulnerability normally reported for web
services (SSRF, RCE, SQLi, XSS, path traversal from user input) are not
applicable.

## Out of Scope

The following are **not** security issues for this project:

- **Numerical accuracy bugs.** These are correctness issues; please use
  the issue tracker with the `bug` label.
- **Performance regressions.** Unless they lead to denial of service on a
  documented workload.
- **Dependency CVEs** in upstream libraries (`numpy`, `scipy`,
  `matplotlib`). We track these via GitHub Dependabot but the fix belongs
  upstream.
- **Warnings or style deviations** in `ruff` output. These are quality
  signals, not security signals.

## Reporting a Vulnerability

If you believe you have found a security-relevant issue:

1. **Do not open a public issue.**
2. Email the maintainer listed in `CITATION.cff`.
3. Include:
   - A clear description of the issue.
   - A minimal reproduction (smallest script that triggers it).
   - The affected version(s), from `python -c "import bit2118; print(bit2118.__version__)"`.
   - Your Python version and OS.
4. Expect an acknowledgement within **72 hours**.
5. A fix or documented mitigation will be provided within **14 days**
   for confirmed issues.

We will credit reporters in the `CHANGELOG.md` unless anonymity is
requested.

## Preferred Languages

English.

## Attribution

This document is modelled on GitHub's recommended
[security policy template](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository).