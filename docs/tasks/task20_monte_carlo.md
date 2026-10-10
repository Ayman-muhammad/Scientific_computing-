# Task 20 — Random Numbers and Monte Carlo Methods

**Module:** `bit2118.task20_monte_carlo`
**Concept:** Estimate probabilities by repeated sampling.
**Real-world anchor:** server overload risk under uncertain demand.

## 1. Concept
Monte Carlo estimates $\Pr(D > C)$ by simulating many demand scenarios.
Error scales as $O(1/\sqrt{N})$.

## 2. Mathematical formulation
$\hat{p}_N = \frac{1}{N}\sum \mathbf{1}\{D_i > C\}$;
$\text{SE} = \sqrt{p(1-p)/N}$.

## 3. Algorithm
1. Draw $N = 100{,}000$ demand samples from $N(850, 120^2)$.
2. Count scenarios exceeding 1000.
3. Track running estimate for the convergence plot.

## 4. Inputs
| Name | Value |
|------|-------|
| capacity | 1000 |
| μ | 850 |
| σ | 120 |
| N | 100,000 |
| seed | 42 |

## 5. Outputs
`overload_probability`, `overload_count`, `std_error`.

## 6. Interpretation
Estimated probability ≈ 10.5 %, matching the analytic Gaussian tail
$1 - \Phi((1000 - 850)/120)$. The convergence plot on a log x-axis
demonstrates the characteristic $O(1/\sqrt{N})$ decay.