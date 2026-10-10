# Task 04 — Floating-Point Arithmetic and Numerical Errors

**Module:** `bit2118.task04_floating_point`
**Concept:** IEEE-754 representation and stability.
**Real-world anchor:** banking, GPS, iterative solvers.

## 1. Concept
Computers store most real numbers approximately. `0.1 + 0.2 != 0.3`
because the binary representation of those decimals is not exact.

## 2. Mathematical formulation
$\text{absolute} = |\text{true} - \text{approx}|$,
$\text{relative} = \text{absolute} / |\text{true}|$.
Unstable $(\sqrt{1+x}-1)/x$ vs. stable $1/(\sqrt{1+x}+1)$ for small $x$.

## 3. Algorithm
1. Compare `0.1 + 0.2` to `0.3` exactly and with `np.isclose`.
2. Compute absolute and relative error for `sqrt(2) ≈ 1.414`.
3. Evaluate both the unstable and stable identity for
   $x \in \{10^{-4}, 10^{-8}, 10^{-12}\}$.

## 4. Inputs
| Name | Value |
|------|-------|
| `SQRT2_APPROX` | 1.414 |
| `STABILITY_X_VALUES` | $10^{-4}, 10^{-8}, 10^{-12}$ |

## 5. Outputs
`fp_demo`, `sqrt2`, `stability` (list of `{x, direct, stable, delta}`).

## 6. Interpretation
The exact equality check returns `False`; the tolerance check returns
`True`. As $x$ shrinks, `delta` grows because the unstable form loses
significance to cancellation — motivating the stable rewrite.