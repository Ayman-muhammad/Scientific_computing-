# Mathematical Notes

Compact derivations for every numerical method used in the package. Each
section corresponds to one task module.

## Task 02 — Array statistics
$$
\bar{x} = \tfrac{1}{n}\sum_{i=1}^{n} x_i
\qquad
F = 1.8\,C + 32
$$

## Task 03 — Vectorisation
Element-wise: $y_i = (x_i / 1000)^2$. Same operation, applied in C
without a Python loop.

## Task 04 — Floating-point error
$$
\text{absolute} = |\text{true} - \text{approx}|
\qquad
\text{relative} = \frac{|\text{true} - \text{approx}|}{|\text{true}|}
$$
Unstable identity: $(\sqrt{1+x}-1)/x$. Stable: $1/(\sqrt{1+x}+1)$.

## Task 05 — Matrix algebra
$$
R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}
\qquad
S = \operatorname{diag}(s_x, s_y)
$$
Combined: $T = R S$. Applied to row vectors: $p' = p T^{\top}$.

## Task 06 — Linear systems
Solve $A x = b$ via LU with partial pivoting (`dgesv`). Residual
$\|b - A x\|_2 \approx 0$ when $A$ is well conditioned.

## Task 07 — LU decomposition
$P A = L U$. Per right-hand side: forward-substitute $L y = P b$, then
back-substitute $U x = y$. Cost: $O(n^3)$ once, $O(n^2)$ per solve.

## Task 08 — Jacobi & Gauss-Seidel
Write $A = D + R$ with $D = \operatorname{diag}(A)$.

* Jacobi: $x^{(k+1)} = D^{-1}(b - R x^{(k)})$
* Gauss-Seidel: $x_i^{(k+1)} = \bigl(b_i - \sum_{j<i} A_{ij} x_j^{(k+1)} - \sum_{j>i} A_{ij} x_j^{(k)}\bigr)/A_{ii}$

Both converge if $A$ is strictly diagonally dominant.

## Task 09 — Eigenvalues
Solve $\det(A - \lambda I) = 0$. For symmetric $A$ the dominant
(Perron-Frobenius) eigenpair gives a centrality vector.

## Task 10 — Bisection & fixed point
Bisection: interval $\|b - a\| / 2^k$ after $k$ steps. Fixed-point
$x_{n+1} = g(x_n)$ converges if $|g'(r)| < 1$ near the root $r$.

## Task 11 — Newton & secant
Newton: $x_{n+1} = x_n - f(x_n) / f'(x_n)$ — quadratic near simple roots.
Secant: $x_{n+1} = x_n - f(x_n) (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))$.

## Task 12 — Nonlinear systems
Solve $F(z) = 0$ with $F: \mathbb{R}^n \to \mathbb{R}^n$ via Powell's
hybrid method (Newton + trust-region).

## Task 13 — Interpolation
Linear: $S(x) = y_i + \frac{y_{i+1} - y_i}{x_{i+1} - x_i}(x - x_i)$.
Cubic spline: piecewise cubics with $C^0$, $C^1$, $C^2$ continuity.

## Task 14 — Least squares
$$
\hat{\theta} = \arg\min_\theta \sum_i (y_i - f(x_i; \theta))^2
$$
RMSE: $\sqrt{\tfrac{1}{n}\sum_i (y_i - f(x_i; \hat{\theta}))^2}$.

## Task 15 — Numerical differentiation
$$
f'(x_i) \approx \frac{f(x_{i+1}) - f(x_i)}{h}
\quad\text{or}\quad
f'(x_i) \approx \frac{f(x_{i+1}) - f(x_{i-1})}{2h}
$$

## Task 16 — Numerical integration
$$
\int_a^b f \approx \frac{h}{2}\bigl(f_0 + 2\sum_{i=1}^{n-1} f_i + f_n\bigr)
\quad\text{(trapezoidal)}
$$
Simpson: $\frac{h}{3}(f_0 + 4\sum_\text{odd} + 2\sum_\text{even, interior} + f_n)$.

## Task 17 — Euler method
$y_{n+1} = y_n + h f(t_n, y_n)$. First order: global error $O(h)$.

## Task 18 — solve_ivp
RK45 embedded pair. Local error estimates from the difference between
order-4 and order-5 solutions drive adaptive step-size control.

## Task 19 — Optimisation
SLSQP on $\min f(z)$ s.t. $g(z) \ge 0$, $a \le z \le b$.

## Task 20 — Monte Carlo
$$
\hat{p}_N = \frac{1}{N}\sum_{i=1}^N \mathbf{1}\{D_i > C\}
\qquad
\text{SE}(\hat{p}_N) = \sqrt{\frac{p(1-p)}{N}}
$$