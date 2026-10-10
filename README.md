# BIT 2118 — Scientific Computing
## Final Technical Submission Report

**Student:** Ayman Muhammad  
**Student ID:** BSCCS/2025/30137  
**Course:** BIT 2118 — Scientific Computing  
**Assignment:** Group Work — Tasks 02–20  
**Submission date:** 10 October 2026  
**Repository:** https://github.com/Ayman-muhammad/Scientific_computing-

---

## 1. Executive Summary

Scientific computing combines mathematics, numerical analysis, algorithms, programming, and scientific interpretation to solve problems that are difficult to handle analytically. Its purpose is not simply to produce numerical answers, but to obtain results whose accuracy, stability, limitations, and meaning can be evaluated.

This report discusses nineteen scientific-computing tasks, from Task 02 through Task 20. The topics include array processing, vectorisation, floating-point arithmetic, matrix transformations, linear systems, LU decomposition, iterative solvers, eigenvalues, nonlinear equations, interpolation, regression, numerical differentiation, numerical integration, ordinary differential equations, optimisation, and Monte Carlo simulation.

The report uses mathematical derivations, worked examples, and verification criteria to explain the principles behind each technique. Illustrative values are included where useful; they are examples for demonstrating the mathematics rather than claims about measurements from a particular software implementation.

The principal conclusion is that a numerical result should be judged by more than whether an algorithm terminates. Its residual, approximation error, convergence behaviour, assumptions, and suitability for the intended application must also be examined.

## 2. Introduction and Objectives

### 2.1 Background

Many scientific and engineering problems involve equations that cannot be solved conveniently by elementary algebra. Examples include large systems of simultaneous equations, nonlinear equilibrium models, predictions from measured data, dynamical systems, and probability estimates.

Numerical methods approximate solutions through finite computational procedures. Their advantages include scalability, flexibility, and the ability to handle complicated mathematical models. Their limitations include round-off error, truncation error, sensitivity to input data, convergence problems, and computational cost.

A scientifically sound computation therefore requires five stages:

1. Mathematical formulation.
2. Selection of an appropriate numerical method.
3. Computational implementation.
4. Verification and error analysis.
5. Interpretation within the assumptions of the model.

### 2.2 Objectives

The objectives are to:

- Explain the mathematical foundations of Tasks 02–20.
- Identify relevant variables, equations, assumptions, and algorithmic parameters.
- Demonstrate how numerical techniques are applied to practical problems.
- Explain sensitivity, convergence, accuracy, and computational efficiency.
- Identify appropriate verification methods for each task.
- Establish the importance of reproducible scientific software.

---

# 3. Task-by-Task Technical Analysis

## Task 02 — NumPy Arrays and Descriptive Statistics

![NumPy broadcasting](https://numpy.org/doc/stable/_images/broadcasting_1.png)  
<sub>Figure: NumPy broadcasting — a scalar is stretched to match the shape of a 1-D array during element-wise multiplication. Source: NumPy documentation.</sub>

### Objective

To represent numerical observations using arrays, perform element-wise operations, and calculate descriptive statistics efficiently.

### Mathematical explanation

An array is an ordered collection of numerical values. Suppose a weather station records temperatures

\[
C=[20,22,24,23,21].
\]

The arithmetic mean is

\[
\bar C=\frac{1}{n}\sum_{i=1}^{n}C_i.
\]

For these observations,

\[
\bar C=\frac{20+22+24+23+21}{5}=22^\circ C.
\]

The minimum is \(20^\circ C\), while the maximum is \(24^\circ C\). The range is

\[
R=C_{\max}-C_{\min}=24-20=4^\circ C.
\]

Temperature conversion from Celsius to Fahrenheit is given by

\[
F=\frac95C+32.
\]

For \(C=20^\circ C\),

\[
F=\frac95(20)+32=68^\circ F.
\]

The same formula can be applied to every observation in an array.

### Computational method

NumPy provides multidimensional arrays and element-wise operations. Instead of processing every value through an explicit Python loop, an array operation can transform an entire collection.

```python
"""Task 02: NumPy arrays and descriptive statistics.

Demonstrates array creation, element-wise operations, and descriptive
statistics using NumPy's vectorized API.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def compute_temperature_statistics(
    temperatures_c: NDArray[np.floating],
) -> dict[str, float | NDArray[np.floating]]:
    """Compute descriptive statistics and convert Celsius to Fahrenheit.

    Parameters
    ----------
    temperatures_c : NDArray[np.floating]
        One-dimensional array of temperatures in degrees Celsius.

    Returns
    -------
    dict[str, float | NDArray[np.floating]]
        Dictionary containing mean, minimum, maximum, range, and the
        converted Fahrenheit temperatures.
    """
    if temperatures_c.ndim != 1:
        raise ValueError("Expected a 1-D array of temperatures.")

    mean_c: float = float(np.mean(temperatures_c))
    min_c: float = float(np.min(temperatures_c))
    max_c: float = float(np.max(temperatures_c))
    range_c: float = max_c - min_c

    # Vectorized conversion: applies to every element without a Python loop.
    temperatures_f: NDArray[np.floating] = temperatures_c * 9.0 / 5.0 + 32.0

    return {
        "mean_c": mean_c,
        "min_c": min_c,
        "max_c": max_c,
        "range_c": range_c,
        "temperatures_f": temperatures_f,
    }


if __name__ == "__main__":
    observations_c = np.array([20.0, 22.0, 24.0, 23.0, 21.0])
    stats = compute_temperature_statistics(observations_c)

    print(f"Mean:  {stats['mean_c']:.1f} °C")
    print(f"Min:   {stats['min_c']:.1f} °C")
    print(f"Max:   {stats['max_c']:.1f} °C")
    print(f"Range: {stats['range_c']:.1f} °C")
    print(f"Fahrenheit: {stats['temperatures_f']}")
```

### Interpretation and verification

The mean describes the central level of the observations, while the range describes their spread between the extremes. Neither statistic alone captures the full distribution or identifies unusual observations.

Verification should include checking the calculated mean independently and confirming that each converted temperature satisfies the conversion formula.

**Conclusion:** array computation provides an efficient foundation for processing scientific observations, provided the units, dimensions, missing values, and statistical interpretation are handled correctly.

---

## Task 03 — Vectorisation and Performance Analysis

![Vectorization performance](https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Vectorization_benchmark.svg/800px-Vectorization_benchmark.svg.png)  
<sub>Figure: Illustrative speed-up from vectorized operations across array sizes. Vectorized NumPy operations frequently execute element-wise calculations in compiled code, reducing Python interpreter overhead.</sub>

### Objective

To compare explicit looping with vectorised numerical computation and understand the conditions under which vectorisation improves performance.

### Mathematical explanation

Consider the transformation

\[
y_i=2x_i+1,\qquad i=1,\ldots,n.
\]

A loop evaluates the expression for each element individually. A vectorised operation expresses the same transformation over an entire array.

### Computational method

```python
"""Task 03: Vectorisation and performance benchmarking.

Compares explicit Python loops with NumPy vectorized operations and
measures the speed-up ratio.
"""

from __future__ import annotations

import time
from typing import Callable

import numpy as np
from numpy.typing import NDArray


def apply_loop(x: NDArray[np.floating]) -> NDArray[np.floating]:
    """Apply y = 2x + 1 using an explicit Python loop."""
    y = np.empty_like(x)
    for i in range(len(x)):
        y[i] = 2.0 * x[i] + 1.0
    return y


def apply_vectorized(x: NDArray[np.floating]) -> NDArray[np.floating]:
    """Apply y = 2x + 1 using NumPy vectorization."""
    return 2.0 * x + 1.0


def benchmark(
    func: Callable[[NDArray[np.floating]], NDArray[np.floating]],
    x: NDArray[np.floating],
    repeats: int = 7,
) -> float:
    """Return the median execution time over several runs.

    Parameters
    ----------
    func : Callable
        Function to benchmark.
    x : NDArray[np.floating]
        Input array.
    repeats : int
        Number of timing repetitions.

    Returns
    -------
    float
        Median wall-clock time in seconds.
    """
    times: list[float] = []
    for _ in range(repeats):
        start = time.perf_counter()
        func(x)
        times.append(time.perf_counter() - start)
    return float(np.median(times))


if __name__ == "__main__":
    sizes = [1_000, 10_000, 100_000, 1_000_000]
    print(f"{'Size':>10}  {'Loop (s)':>10}  {'Vec (s)':>10}  {'Speed-up':>10}")
    print("-" * 46)

    for n in sizes:
        x = np.arange(1, n + 1, dtype=float)
        t_loop = benchmark(apply_loop, x)
        t_vec = benchmark(apply_vectorized, x)
        speedup = t_loop / t_vec if t_vec > 0 else float("inf")
        print(f"{n:>10}  {t_loop:>10.6f}  {t_vec:>10.6f}  {speedup:>10.2f}")
```

### Performance measurement

Speed-up is defined as

\[
S=\frac{t_{\text{loop}}}{t_{\text{vectorised}}},
\]

where \(t_{\text{loop}}\) and \(t_{\text{vectorised}}\) are the measured execution times.

### Verification

Confirm that both implementations return equivalent arrays using a tolerance-based comparison. Measure execution times separately and record the array size, software environment, and timing method.

**Conclusion:** vectorisation is an important performance technique, but claims about speed-up must be supported by measurements rather than assumed from code style.

---

## Task 04 — Floating-Point Arithmetic and Numerical Stability

![Floating point cancellation](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Loss_of_significance.svg/600px-Loss_of_significance.svg.png)  
<sub>Figure: Loss of significance in floating-point arithmetic. Subtracting two nearly equal numbers can discard significant digits (catastrophic cancellation).</sub>

### Objective

To explain finite-precision arithmetic, rounding error, cancellation, and the effect of algebraic reformulation on numerical accuracy.

### Mathematical explanation

Computers represent many real numbers approximately using finite-precision binary floating-point arithmetic. Decimal fractions such as \(0.1\) generally have no exact finite binary representation.

Two important error measures are absolute error,

\[
E_{\mathrm{abs}}=|x_{\mathrm{computed}}-x_{\mathrm{reference}}|,
\]

and relative error,

\[
E_{\mathrm{rel}}=
\frac{|x_{\mathrm{computed}}-x_{\mathrm{reference}}|}
{|x_{\mathrm{reference}}|},
\]

provided the reference value is nonzero.

### Catastrophic cancellation

Consider

\[
f(x)=\sqrt{1+x}-1.
\]

When \(x\) is very small, \(\sqrt{1+x}\) is close to \(1\). Subtracting two nearly equal floating-point numbers can discard significant digits.

Multiplying by the conjugate gives

\[
\sqrt{1+x}-1
=
\frac{(\sqrt{1+x}-1)(\sqrt{1+x}+1)}
{\sqrt{1+x}+1}.
\]

Simplifying,

\[
\boxed{
\sqrt{1+x}-1=
\frac{x}{\sqrt{1+x}+1}
}
\]

for values where the expressions are defined. The second form avoids subtracting two nearly equal quantities and is often more accurate for small \(x\).

### Computational method

```python
"""Task 04: Floating-point stability and catastrophic cancellation.

Compares two algebraically equivalent expressions for sqrt(1 + x) - 1
and demonstrates how reformulation improves numerical accuracy for small x.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def naive_expression(x: NDArray[np.floating]) -> NDArray[np.floating]:
    """Compute sqrt(1 + x) - 1 directly (susceptible to cancellation)."""
    return np.sqrt(1.0 + x) - 1.0


def stable_expression(x: NDArray[np.floating]) -> NDArray[np.floating]:
    """Compute sqrt(1 + x) - 1 using the conjugate form (cancellation-free)."""
    return x / (np.sqrt(1.0 + x) + 1.0)


def relative_error(
    computed: NDArray[np.floating],
    reference: NDArray[np.floating],
) -> NDArray[np.floating]:
    """Compute element-wise relative error, guarding against division by zero."""
    denominator = np.where(reference != 0.0, np.abs(reference), 1.0)
    return np.abs(computed - reference) / denominator


if __name__ == "__main__":
    # Small values where cancellation is most severe.
    x_values = np.array([1e-16, 1e-14, 1e-12, 1e-10, 1e-8], dtype=float)

    # High-precision reference using the stable formula in float128.
    x_ref = x_values.astype(np.longdouble)
    reference = x_ref / (np.sqrt(1.0 + x_ref) + 1.0)

    naive = naive_expression(x_values)
    stable = stable_expression(x_values)

    print(f"{'x':>10}  {'Naive rel err':>15}  {'Stable rel err':>15}")
    print("-" * 44)
    for i, xi in enumerate(x_values):
        err_naive = relative_error(naive[i], reference[i])
        err_stable = relative_error(stable[i], reference[i])
        print(f"{xi:>10.0e}  {err_naive:>15.6e}  {err_stable:>15.6e}")
```

### Sensitivity and stability

A problem is ill-conditioned when small changes in its input can produce large changes in its true solution. An algorithm is numerically unstable when its computational errors grow excessively during the calculation.

These are distinct concepts: a stable algorithm cannot remove the intrinsic sensitivity of an ill-conditioned problem.

**Conclusion:** numerical accuracy depends on the representation of numbers, the conditioning of the problem, and the stability of the chosen algorithm.

---

## Task 05 — Matrix Algebra and Geometric Transformations

![Matrix rotation](https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Euler2a.gif/400px-Euler2a.gif)  
<sub>Figure: Geometric rotation of a coordinate frame. A rotation matrix preserves area and orientation (\(\det(R) = 1\)).</sub>

### Objective

To use matrices to represent and combine geometric transformations.

### Mathematical explanation

A two-dimensional point is represented as

\[
\mathbf{x}=
\begin{bmatrix}x\\y\end{bmatrix}.
\]

A rotation through angle \(\theta\) is represented by

\[
R(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}.
\]

The transformed point is

\[
\mathbf{x}'=R(\theta)\mathbf{x}.
\]

For a \(90^\circ\) counterclockwise rotation,

\[
R(90^\circ)=
\begin{bmatrix}
0&-1\\
1&0
\end{bmatrix}.
\]

Applying it to \((2,1)\) gives

\[
\begin{bmatrix}
0&-1\\
1&0
\end{bmatrix}
\begin{bmatrix}2\\1\end{bmatrix}
=
\begin{bmatrix}-1\\2\end{bmatrix}.
\]

Thus, the point \((2,1)\) becomes \((-1,2)\).

Scaling is represented by

\[
S=
\begin{bmatrix}
s_x&0\\
0&s_y
\end{bmatrix}.
\]

If scaling is followed by rotation, the combined transformation is

\[
T=RS.
\]

The order matters because, in general,

\[
RS\ne SR.
\]

### Computational method

```python
"""Task 05: Matrix algebra and geometric transformations.

Demonstrates rotation and scaling matrices, composition order, and
determinant-based area preservation checks.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def rotation_matrix(theta_rad: float) -> NDArray[np.floating]:
    """Return a 2×2 counterclockwise rotation matrix."""
    c, s = np.cos(theta_rad), np.sin(theta_rad)
    return np.array([[c, -s], [s, c]], dtype=float)


def scaling_matrix(sx: float, sy: float) -> NDArray[np.floating]:
    """Return a 2×2 non-uniform scaling matrix."""
    return np.array([[sx, 0.0], [0.0, sy]], dtype=float)


def transform_point(
    matrix: NDArray[np.floating],
    point: NDArray[np.floating],
) -> NDArray[np.floating]:
    """Apply a linear transformation to a 2-D point."""
    return matrix @ point


if __name__ == "__main__":
    point = np.array([2.0, 1.0])

    # 90° counterclockwise rotation.
    theta = np.pi / 2.0
    R = rotation_matrix(theta)
    rotated = transform_point(R, point)
    print(f"Rotated point (90° CCW): {rotated}")  # [-1, 2]

    # Scaling: 2× in x, 3× in y.
    S = scaling_matrix(2.0, 3.0)
    scaled = transform_point(S, point)
    print(f"Scaled point (2×, 3×):    {scaled}")  # [4, 3]

    # Composition: rotation after scaling.
    T = R @ S
    composed = transform_point(T, point)
    print(f"Composed (R @ S):        {composed}")

    # Verify determinant identities.
    print(f"det(R) = {np.linalg.det(R):.6f}")  # 1.0
    print(f"det(S) = {np.linalg.det(S):.6f}")  # 6.0
    print(f"det(T) = {np.linalg.det(T):.6f}")  # 6.0
```

### Geometric properties

The determinant of the rotation matrix is

\[
\det(R)=1.
\]

This means a rotation preserves area and orientation. The scaling transformation changes area by the factor

\[
|\det(S)|=|s_xs_y|.
\]

If \(s_x=2\) and \(s_y=3\), the transformed area is six times the original area.

**Conclusion:** matrices provide a compact, composable representation of geometric transformations and make their mathematical properties straightforward to verify.

---

## Task 06 — Solving Systems of Linear Equations

### Objective

To solve simultaneous linear equations and assess whether the calculated solution satisfies the original system and any application constraints.

### Mathematical explanation

A linear system is written as

\[
Ax=b,
\]

where \(A\) is the coefficient matrix, \(x\) is the unknown vector, and \(b\) is the right-hand-side vector.

Consider

\[
2x+y=5,
\]

\[
x-y=1.
\]

Adding the equations gives

\[
3x=6\implies x=2.
\]

Substituting into \(x-y=1\),

\[
2-y=1\implies y=1.
\]

Therefore,

\[
\boxed{x=2,\quad y=1}.
\]

### Computational method

```python
"""Task 06: Solving linear systems with residual verification.

Uses NumPy's linear solver (LAPACK-backed) and checks the residual
norm alongside application-domain feasibility.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def solve_linear_system(
    A: NDArray[np.floating],
    b: NDArray[np.floating],
) -> NDArray[np.floating]:
    """Solve A x = b using a direct numerical linear solver.

    Parameters
    ----------
    A : NDArray[np.floating]
        Coefficient matrix of shape (n, n).
    b : NDArray[np.floating]
        Right-hand-side vector of shape (n,).

    Returns
    -------
    NDArray[np.floating]
        Solution vector x.
    """
    # np.linalg.solve uses LU decomposition with partial pivoting.
    # It is preferred over explicitly computing A^{-1}.
    return np.linalg.solve(A, b)


def residual_norm(
    A: NDArray[np.floating],
    x: NDArray[np.floating],
    b: NDArray[np.floating],
) -> float:
    """Return the Euclidean norm of the residual b - A x."""
    return float(np.linalg.norm(b - A @ x))


if __name__ == "__main__":
    A = np.array([[2.0, 1.0], [1.0, -1.0]])
    b = np.array([5.0, 1.0])

    x = solve_linear_system(A, b)
    print(f"Solution: x = {x}")  # [2, 1]

    r_norm = residual_norm(A, x, b)
    print(f"Residual norm: {r_norm:.2e}")

    # Application constraint check: variables must be non-negative.
    if np.any(x < 0):
        print("WARNING: solution violates non-negativity constraint.")
    else:
        print("Non-negativity constraint satisfied.")
```

### Numerical solution and residual

Scientific software typically uses a numerical linear solver instead of explicitly calculating \(A^{-1}\). Directly computing an inverse is generally unnecessary and can be less efficient or less numerically reliable than solving the system directly.

For an approximate solution \(\hat x\), define the residual

\[
r=b-A\hat x.
\]

A small residual indicates that the computed solution approximately satisfies the supplied equations.

**Conclusion:** a linear solver must be assessed through equation satisfaction and application constraints, not merely successful execution.

---

## Task 07 — LU Decomposition

![LU decomposition](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Diagonalization_as_rotation.gif/400px-Diagonalization_as_rotation.gif)  
<sub>Figure: Matrix factorization as a change of basis. LU decomposition factors \(A = LU\) into lower and upper triangular matrices, enabling efficient repeated solves.</sub>

### Objective

To explain how LU decomposition supports repeated solutions of linear systems with the same coefficient matrix.

### Mathematical explanation

LU decomposition factors a matrix into triangular matrices. With pivoting, it is commonly expressed as

\[
PA=LU,
\]

where \(P\) is a permutation matrix, \(L\) is lower triangular, and \(U\) is upper triangular.

To solve

\[
Ax=b,
\]

use the factorisation to obtain

\[
LUx=Pb.
\]

First solve

\[
Ly=Pb
\]

using forward substitution. Then solve

\[
Ux=y
\]

using backward substitution.

### Computational method

```python
"""Task 07: LU decomposition and repeated linear solves.

Demonstrates LU factorization and verifies the factorization identity
PA = LU, then solves a system using the factors.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.linalg import lu, lu_factor, lu_solve


def verify_lu_factorization(
    A: NDArray[np.floating],
) -> tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """Factorize A = P L U and return the factors.

    Parameters
    ----------
    A : NDArray[np.floating]
        Square matrix.

    Returns
    -------
    tuple[NDArray, NDArray, NDArray]
        Permutation matrix P, lower-triangular L, and upper-triangular U.
    """
    P, L, U = lu(A)
    # Verify the factorization: P @ A should equal L @ U.
    assert np.allclose(P @ A, L @ U, atol=1e-12)
    return P, L, U


if __name__ == "__main__":
    A = np.array([[2.0, 1.0], [4.0, 3.0]])
    b = np.array([5.0, 11.0])

    # Factorize and verify.
    P, L, U = verify_lu_factorization(A)
    print("L =\n", L)
    print("U =\n", U)

    # Solve using the LU factors (reusable for multiple right-hand sides).
    lu_piv = lu_factor(A)
    x = lu_solve(lu_piv, b)
    print(f"Solution: x = {x}")  # [2, 1]

    residual = np.linalg.norm(b - A @ x)
    print(f"Residual: {residual:.2e}")
```

### Computational advantage

When several right-hand sides share the same matrix \(A\), its factorisation can be reused. This avoids repeating the more expensive factorisation stage for every new vector \(b\).

**Conclusion:** LU decomposition is particularly valuable when a fixed matrix must be used to solve multiple linear systems.

---

## Task 08 — Iterative Linear Solvers: Jacobi and Gauss–Seidel

![Jacobi vs Gauss-Seidel convergence](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Jacobi_vs_Gauss-Seidel_Convergence.svg/800px-Jacobi_vs_Gauss-Seidel_Convergence.svg.png)  
<sub>Figure: Convergence comparison of Jacobi and Gauss–Seidel iterations on a diagonally dominant system. Gauss–Seidel typically converges faster because it uses updated values immediately.</sub>

### Objective

To understand iterative methods for solving large linear systems and compare their convergence behaviour.

### Mathematical explanation

For

\[
Ax=b,
\]

iterative methods generate successive approximations

\[
x^{(0)},x^{(1)},x^{(2)},\ldots
\]

until a stopping criterion is satisfied.

For a system with diagonal entries \(a_{ii}\), the Jacobi update is

\[
x_i^{(k+1)}
=
\frac{1}{a_{ii}}
\left(
b_i-\sum_{j\ne i}a_{ij}x_j^{(k)}
\right).
\]

Every component uses values from the previous iteration.

Gauss–Seidel uses newly calculated components immediately:

\[
x_i^{(k+1)}
=
\frac{1}{a_{ii}}
\left(
b_i
-\sum_{j<i}a_{ij}x_j^{(k+1)}
-\sum_{j>i}a_{ij}x_j^{(k)}
\right).
\]

### Computational method

```python
"""Task 08: Jacobi and Gauss–Seidel iterative solvers.

Implements both methods from scratch and records the residual history
to compare convergence behaviour.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class IterativeResult:
    """Container for iterative solver output."""
    solution: NDArray[np.floating]
    residual_history: list[float]
    iterations: int
    converged: bool


def jacobi_solve(
    A: NDArray[np.floating],
    b: NDArray[np.floating],
    x0: NDArray[np.floating] | None = None,
    tol: float = 1e-10,
    max_iter: int = 500,
) -> IterativeResult:
    """Solve A x = b using the Jacobi iteration method."""
    n = len(b)
    x = np.zeros(n) if x0 is None else x0.copy()
    D = np.diag(A)
    if np.any(np.abs(D) < np.finfo(float).eps):
        raise ValueError("Zero diagonal entry detected; Jacobi cannot proceed.")

    R = A - np.diag(D)  # Off-diagonal part.
    history: list[float] = []

    for k in range(max_iter):
        x_new = (b - R @ x) / D
        res = float(np.linalg.norm(b - A @ x_new))
        history.append(res)
        if res < tol:
            return IterativeResult(x_new, history, k + 1, True)
        x = x_new

    return IterativeResult(x, history, max_iter, False)


def gauss_seidel_solve(
    A: NDArray[np.floating],
    b: NDArray[np.floating],
    x0: NDArray[np.floating] | None = None,
    tol: float = 1e-10,
    max_iter: int = 500,
) -> IterativeResult:
    """Solve A x = b using the Gauss–Seidel iteration method."""
    n = len(b)
    x = np.zeros(n) if x0 is None else x0.copy()
    history: list[float] = []

    for k in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            sigma = 0.0
            for j in range(n):
                if j != i:
                    sigma += A[i, j] * x[j]  # Uses updated values immediately.
            if abs(A[i, i]) < np.finfo(float).eps:
                raise ValueError(f"Zero diagonal at row {i}.")
            x[i] = (b[i] - sigma) / A[i, i]

        res = float(np.linalg.norm(b - A @ x))
        history.append(res)
        if res < tol:
            return IterativeResult(x, history, k + 1, True)

    return IterativeResult(x, history, max_iter, False)


if __name__ == "__main__":
    A = np.array([[4.0, 1.0], [1.0, 3.0]])
    b = np.array([9.0, 7.0])

    jac = jacobi_solve(A, b)
    gs = gauss_seidel_solve(A, b)

    print(f"Jacobi:      x = {jac.solution}, iterations = {jac.iterations}")
    print(f"Gauss–Seidel: x = {gs.solution}, iterations = {gs.iterations}")
```

### Convergence

Strict diagonal dominance is a useful sufficient condition for convergence of these methods in many standard settings. Convergence is not guaranteed for every matrix.

A stopping criterion can be based on

\[
\|b-Ax^{(k)}\|<\varepsilon,
\]

where \(\varepsilon\) is a chosen tolerance.

**Conclusion:** iterative methods can be useful for large systems, but convergence and accuracy must be demonstrated rather than assumed.

---

## Task 09 — Eigenvalues, Eigenvectors, and Network Centrality

![Eigenvector centrality](https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Eigenvector_centrality.svg/500px-Eigenvector_centrality.svg.png)  
<sub>Figure: Eigenvector centrality in a network. Nodes with higher centrality scores (larger circles) are connected to other important nodes.</sub>

### Objective

To explain the eigenvalue problem and how eigenvectors can be used to assess the importance of nodes in a network.

### Mathematical explanation

An eigenvalue \(\lambda\) and nonzero eigenvector \(v\) of matrix \(A\) satisfy

\[
Av=\lambda v.
\]

The eigenvector identifies a direction that is unchanged by the transformation except for scaling by \(\lambda\).

Consider

\[
A=
\begin{bmatrix}
2&0\\
0&3
\end{bmatrix}.
\]

For

\[
v=
\begin{bmatrix}1\\0\end{bmatrix},
\]

we have

\[
Av=
\begin{bmatrix}2\\0\end{bmatrix}
=2v.
\]

Therefore, \(v\) is an eigenvector with eigenvalue \(2\). Similarly, \((0,1)^T\) has eigenvalue \(3\).

### Network centrality

In a graph, an adjacency matrix records connections between nodes. Eigenvector centrality assigns greater importance to nodes connected to other important nodes.

A simplified centrality relationship is

\[
Ac=\lambda c,
\]

where \(c\) contains the centrality scores.

### Computational method

```python
"""Task 09: Eigenvalues, eigenvectors, and network centrality.

Computes eigenvalues/eigenvectors of a symmetric matrix and derives
eigenvector centrality scores from an adjacency matrix.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def eigen_decomposition(
    A: NDArray[np.floating],
) -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    """Return eigenvalues and eigenvectors of a square matrix.

    Uses np.linalg.eigh for symmetric matrices, which guarantees real
    eigenvalues and orthonormal eigenvectors.
    """
    eigenvalues, eigenvectors = np.linalg.eigh(A)
    # Sort in descending order of eigenvalue.
    idx = np.argsort(eigenvalues)[::-1]
    return eigenvalues[idx], eigenvectors[:, idx]


def eigenvector_centrality(
    adjacency: NDArray[np.floating],
    max_iter: int = 1000,
    tol: float = 1e-12,
) -> NDArray[np.floating]:
    """Compute eigenvector centrality via power iteration.

    Parameters
    ----------
    adjacency : NDArray[np.floating]
        Symmetric adjacency matrix of the graph.
    max_iter : int
        Maximum number of power iterations.
    tol : float
        Convergence tolerance on the centrality vector.

    Returns
    -------
    NDArray[np.floating]
        Non-negative centrality vector normalized to unit Euclidean norm.
    """
    n = adjacency.shape[0]
    c = np.ones(n) / np.sqrt(n)

    for _ in range(max_iter):
        c_new = adjacency @ c
        norm = np.linalg.norm(c_new)
        if norm < np.finfo(float).eps:
            raise ValueError("Adjacency matrix has zero spectral radius.")
        c_new /= norm
        if np.linalg.norm(c_new - c) < tol:
            return c_new
        c = c_new

    return c


if __name__ == "__main__":
    # Simple diagonal matrix: eigenvalues are the diagonal entries.
    A_diag = np.diag([2.0, 3.0])
    vals, vecs = eigen_decomposition(A_diag)
    print(f"Eigenvalues: {vals}")
    print(f"First eigenvector: {vecs[:, 0]}")

    # Small example graph (undirected).
    adjacency = np.array([
        [0, 1, 0, 0],
        [1, 0, 1, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 0],
    ], dtype=float)
    centrality = eigenvector_centrality(adjacency)
    print(f"Eigenvector centrality: {centrality}")
    print(f"Highest centrality node: {np.argmax(centrality)}")
```

### Verification

Evaluate

\[
r=Av-\lambda v
\]

and check that \(\|r\|\) is sufficiently small. Eigenvectors may be normalised to unit length or another stated convention because multiplying an eigenvector by a nonzero scalar produces another eigenvector.

**Conclusion:** eigenvalue analysis reveals structural properties of matrices and networks, but the interpretation depends on the matrix construction and model assumptions.

---

## Task 10 — Bisection and Fixed-Point Iteration

![Bisection method](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Bisection_method.svg/600px-Bisection_method.svg.png)  
<sub>Figure: The bisection method iteratively narrows a bracket containing a root. The interval width halves with each iteration, giving a predictable error bound.</sub>

### Objective

To solve nonlinear equations and understand the difference between a bracketing method and an iterative fixed-point method.

### Mathematical explanation

A nonlinear root-finding problem seeks \(x^\ast\) such that

\[
f(x^\ast)=0.
\]

Consider the illustrative equilibrium equation

\[
f(T)=T-25-10e^{-T/20}.
\]

At \(T=25\),

\[
f(25)=-10e^{-1.25}<0.
\]

At \(T=35\),

\[
f(35)=10-10e^{-1.75}>0.
\]

Because the function is continuous and changes sign between \(25\) and \(35\), the intermediate value theorem guarantees at least one root in this interval.

### Bisection method

The midpoint is

\[
m=\frac{a+b}{2}.
\]

The algorithm evaluates \(f(m)\) and retains the half-interval that contains the sign change.

### Computational method

```python
"""Task 10: Bisection and fixed-point iteration for nonlinear root finding.

Implements the bisection method (bracketing) and fixed-point iteration
and compares their convergence behaviour on a cooling equilibrium model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class RootResult:
    """Container for root-finding output."""
    root: float
    iterations: int
    residual: float
    converged: bool


def bisection(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-10,
    max_iter: int = 200,
) -> RootResult:
    """Find a root of f in [a, b] using the bisection method.

    Requires f(a) and f(b) to have opposite signs.
    """
    fa, fb = f(a), f(b)
    if fa * fb >= 0:
        raise ValueError(
            f"Bisection requires a sign change: f({a})={fa:.4f}, f({b})={fb:.4f}"
        )

    for k in range(max_iter):
        m = 0.5 * (a + b)
        fm = f(m)
        if abs(fm) < tol or (b - a) / 2.0 < tol:
            return RootResult(m, k + 1, abs(fm), True)
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm

    m = 0.5 * (a + b)
    return RootResult(m, max_iter, abs(f(m)), False)


def fixed_point_iteration(
    g: Callable[[float], float],
    x0: float,
    tol: float = 1e-10,
    max_iter: int = 200,
) -> RootResult:
    """Find a fixed point of g using the iteration x_{n+1} = g(x_n)."""
    x = x0
    for k in range(max_iter):
        x_new = g(x)
        if abs(x_new - x) < tol:
            return RootResult(x_new, k + 1, abs(x_new - x), True)
        x = x_new
    return RootResult(x, max_iter, abs(x - g(x)), False)


if __name__ == "__main__":
    # Cooling equilibrium: f(T) = T - 25 - 10 exp(-T/20).
    f = lambda T: T - 25.0 - 10.0 * np.exp(-T / 20.0)

    result = bisection(f, 25.0, 35.0)
    print(f"Bisection root: T ≈ {result.root:.6f} °C")
    print(f"Iterations: {result.iterations}, residual: {result.residual:.2e}")

    # Fixed-point form: T = 25 + 10 exp(-T/20).
    g = lambda T: 25.0 + 10.0 * np.exp(-T / 20.0)
    fp_result = fixed_point_iteration(g, 30.0)
    print(f"Fixed-point root: T ≈ {fp_result.root:.6f} °C")
    print(f"Iterations: {fp_result.iterations}, residual: {fp_result.residual:.2e}")
```

### Verification

Confirm the initial sign change for bisection, calculate the final residual \(|f(T)|\), and check the stopping criterion. For fixed-point iteration, examine the change between successive iterates and whether the sequence converges.

**Conclusion:** method selection should account for convergence guarantees, available derivatives or brackets, and the required accuracy.

---

## Task 11 — Newton's Method, Secant Method, and Internal Rate of Return

### Objective

To explain derivative-based and derivative-free root-finding methods and their use in financial calculations.

### Newton's method

Newton's method updates an estimate using

\[
x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}.
\]

The formula comes from approximating \(f\) locally by its tangent line and using the tangent's intercept as the next estimate.

### Secant method

The secant method approximates the derivative using two previous points:

\[
x_{n+1}
=
x_n-f(x_n)
\frac{x_n-x_{n-1}}{f(x_n)-f(x_{n-1})}.
\]

### Financial application: internal rate of return

The internal rate of return is a discount rate \(r\) that satisfies

\[
\operatorname{NPV}(r)
=
\sum_{t=0}^{n}
\frac{CF_t}{(1+r)^t}=0,
\]

where \(CF_t\) denotes the cash flow at time \(t\).

### Computational method

```python
"""Task 11: Newton and secant methods for root finding.

Implements both methods and applies them to an IRR calculation.
"""

from __future__ import annotations

from typing import Callable

import numpy as np


def newton_method(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    tol: float = 1e-12,
    max_iter: int = 100,
) -> float:
    """Find a root using Newton–Raphson iteration."""
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        dfx = df(x)
        if abs(dfx) < np.finfo(float).eps:
            raise ZeroDivisionError(f"Derivative vanished at x = {x}.")
        x -= fx / dfx
    raise RuntimeError("Newton method did not converge within max_iter.")


def secant_method(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tol: float = 1e-12,
    max_iter: int = 100,
) -> float:
    """Find a root using the secant method (derivative-free)."""
    for _ in range(max_iter):
        f0, f1 = f(x0), f(x1)
        if abs(f1) < tol:
            return x1
        if abs(f1 - f0) < np.finfo(float).eps:
            raise ZeroDivisionError("Secant denominator vanished.")
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, x1 = x1, x2
    raise RuntimeError("Secant method did not converge within max_iter.")


def npv(
    rate: float,
    cash_flows: list[float],
) -> float:
    """Compute net present value for a series of cash flows."""
    return sum(
        cf / (1.0 + rate) ** t for t, cf in enumerate(cash_flows)
    )


if __name__ == "__main__":
    # One-period investment: cost 100, return 110.
    cash_flows = [-100.0, 110.0]

    f = lambda r: npv(r, cash_flows)
    df = lambda r: -110.0 / (1.0 + r) ** 2  # Analytical derivative.

    r_newton = newton_method(f, df, 0.05)
    r_secant = secant_method(f, 0.05, 0.15)

    print(f"IRR (Newton): r = {r_newton:.6f} = {r_newton * 100:.2f}%")
    print(f"IRR (Secant): r = {r_secant:.6f} = {r_secant * 100:.2f}%")
    print(f"NPV at Newton root: {f(r_newton):.2e}")
```

### Important limitation

For cash flows that change sign more than once, the NPV equation may have multiple roots or no economically meaningful root. A numerical solver's output must therefore be interpreted in the context of the cash-flow pattern.

**Conclusion:** Newton and secant methods are useful for nonlinear financial equations, but convergence and economic interpretation remain essential.

---

## Task 12 — Solving Nonlinear Systems

### Objective

To solve systems involving nonlinear equations and understand multiple solutions and initial-guess sensitivity.

### Mathematical model

Consider the system

\[
x^2+y^2=4,
\]

\[
y=x^2-1.
\]

The first equation represents a circle of radius \(2\) centred at the origin. The second represents a parabola.

Substitute \(y=x^2-1\) into the circle equation:

\[
x^2+(x^2-1)^2=4.
\]

Expanding,

\[
x^4-x^2-3=0.
\]

Let \(z=x^2\). Then

\[
z^2-z-3=0.
\]

Applying the quadratic formula,

\[
z=\frac{1\pm\sqrt{13}}{2}.
\]

Since \(z=x^2\geq0\), only

\[
x^2=\frac{1+\sqrt{13}}{2}
\]

is admissible. Hence,

\[
x=\pm\sqrt{\frac{1+\sqrt{13}}{2}}.
\]

For both candidates,

\[
y=x^2-1=\frac{\sqrt{13}-1}{2}.
\]

Numerically, the intersections are approximately

\[
(x,y)\approx(1.517,1.303)
\]

and

\[
(x,y)\approx(-1.517,1.303).
\]

### Computational method

```python
"""Task 12: Solving nonlinear systems.

Uses scipy.optimize.fsolve to find intersections of a circle and a
parabola, demonstrating multiple solutions and initial-guess sensitivity.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import fsolve


def nonlinear_system(
    variables: NDArray[np.floating],
) -> tuple[float, float]:
    """Residual vector for the circle–parabola intersection problem.

    Equations:
        x^2 + y^2 - 4 = 0
        y - x^2 + 1 = 0
    """
    x, y = variables
    return (x**2 + y**2 - 4.0, y - x**2 + 1.0)


def find_all_intersections() -> list[NDArray[np.floating]]:
    """Locate both intersection points using distinct initial guesses."""
    guesses = [
        np.array([2.0, 2.0]),   # Upper-right quadrant.
        np.array([-2.0, 2.0]),  # Upper-left quadrant.
    ]
    solutions: list[NDArray[np.floating]] = []

    for guess in guesses:
        sol, info, ier, msg = fsolve(nonlinear_system, guess, full_output=True)
        if ier != 1:
            raise RuntimeError(f"Solver failed: {msg}")
        residual = np.linalg.norm(nonlinear_system(sol))
        print(f"Guess {guess} -> solution {sol}, residual {residual:.2e}")
        solutions.append(sol)

    return solutions


if __name__ == "__main__":
    solutions = find_all_intersections()
    print(f"\nNumber of intersections found: {len(solutions)}")
```

### Initial guesses and verification

Different initial guesses can lead a local solver to different intersections. A solver may also fail or converge to a point with an unacceptable residual.

Every candidate should be substituted into both original equations. Graphical intersection is useful for interpretation, but numerical substitution provides a stronger verification check.

**Conclusion:** nonlinear systems may have multiple valid solutions, making initial conditions and independent residual checks important.

---

## Task 13 — Interpolation and Cubic Splines

### Objective

To estimate intermediate values from known data points and compare linear interpolation with spline interpolation.

### Linear interpolation

Given two observations \((x_0,y_0)\) and \((x_1,y_1)\), linear interpolation estimates a value between the points using

\[
y(x)=y_0+
\frac{x-x_0}{x_1-x_0}(y_1-y_0).
\]

### Cubic spline interpolation

A cubic spline represents each interval using a cubic polynomial,

\[
S_i(x)=a_i+b_i(x-x_i)+c_i(x-x_i)^2+d_i(x-x_i)^3.
\]

### Computational method

```python
"""Task 13: Interpolation and cubic splines.

Compares linear interpolation with cubic spline interpolation on a
small set of sensor measurements.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.interpolate import CubicSpline, interp1d


def linear_interpolate(
    x_data: NDArray[np.floating],
    y_data: NDArray[np.floating],
    x_query: NDArray[np.floating],
) -> NDArray[np.floating]:
    """Perform piecewise linear interpolation."""
    interpolator = interp1d(x_data, y_data, kind="linear")
    return interpolator(x_query)


def cubic_spline_interpolate(
    x_data: NDArray[np.floating],
    y_data: NDArray[np.floating],
    x_query: NDArray[np.floating],
) -> NDArray[np.floating]:
    """Perform cubic spline interpolation with natural boundary conditions."""
    spline = CubicSpline(x_data, y_data, bc_type="natural")
    return spline(x_query)


if __name__ == "__main__":
    # Sensor data: time (s) vs. measurement (units).
    time = np.array([0.0, 4.0, 8.0, 12.0])
    measurement = np.array([10.0, 20.0, 15.0, 25.0])

    query_time = np.array([2.0, 6.0, 10.0])

    linear = linear_interpolate(time, measurement, query_time)
    spline = cubic_spline_interpolate(time, measurement, query_time)

    print(f"Query times: {query_time}")
    print(f"Linear:      {linear}")
    print(f"Spline:      {spline}")

    # Verify interpolation at knots.
    at_knots = cubic_spline_interpolate(time, measurement, time)
    assert np.allclose(at_knots, measurement), "Spline must reproduce data at knots."
    print("Spline reproduces data at knots: OK")
```

### Comparison

Linear interpolation is simple and locally transparent. Cubic splines can produce smoother curves but may overshoot between data points, particularly when the data vary sharply.

**Conclusion:** interpolation provides estimates between observations, but the method should reflect the smoothness and behaviour expected of the underlying process.

---

## Task 14 — Curve Fitting and Regression

### Objective

To estimate model parameters from observed data and evaluate the quality and limitations of the fitted model.

### Mathematical explanation

Regression estimates a relationship between explanatory variables and an observed response. For a quadratic model,

\[
\hat y=ax^2+bx+c,
\]

the coefficients \(a\), \(b\), and \(c\) are often estimated by least squares.

For observations \((x_i,y_i)\), the sum of squared errors is

\[
\operatorname{SSE}
=
\sum_{i=1}^{n}(y_i-\hat y_i)^2.
\]

The root-mean-square error is

\[
\operatorname{RMSE}
=
\sqrt{\frac{1}{n}
\sum_{i=1}^{n}(y_i-\hat y_i)^2}.
\]

### Computational method

```python
"""Task 14: Curve fitting and regression.

Fits a quadratic polynomial to synthetic server response-time data
using least squares and evaluates residuals and RMSE.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def fit_polynomial(
    x: NDArray[np.floating],
    y: NDArray[np.floating],
    degree: int = 2,
) -> NDArray[np.floating]:
    """Fit a polynomial of the given degree using least squares.

    Returns the coefficient vector in descending order of power.
    """
    return np.polyfit(x, y, deg=degree)


def compute_rmse(
    y_true: NDArray[np.floating],
    y_pred: NDArray[np.floating],
) -> float:
    """Return the root-mean-square error between true and predicted values."""
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


if __name__ == "__main__":
    # Synthetic data: response time vs. concurrent users.
    users = np.array([10, 20, 30, 40, 50, 60, 70], dtype=float)
    response_time = np.array([15, 22, 32, 48, 70, 98, 135], dtype=float)

    coefficients = fit_polynomial(users, response_time, degree=2)
    fitted = np.polyval(coefficients, users)
    residuals = response_time - fitted

    rmse = compute_rmse(response_time, fitted)

    print(f"Quadratic coefficients (a, b, c): {coefficients}")
    print(f"RMSE: {rmse:.4f}")
    print(f"Residuals: {residuals}")
```

### Residual analysis

Residuals are

\[
e_i=y_i-\hat y_i.
\]

Residual plots can reveal systematic patterns, unequal variance, or influential observations that a single error statistic may conceal.

**Conclusion:** regression quantifies relationships in observed data, but model adequacy and predictive reliability require additional evidence.

---

## Task 15 — Numerical Differentiation

### Objective

To approximate derivatives from sampled values and understand how step size and measurement noise affect derivative estimates.

### Forward difference

The forward-difference approximation is

\[
f'(x)\approx\frac{f(x+h)-f(x)}{h}.
\]

Under standard smoothness assumptions, its truncation error is \(O(h)\).

### Central difference

The central-difference approximation is

\[
f'(x)\approx\frac{f(x+h)-f(x-h)}{2h}.
\]

Under suitable smoothness assumptions, its truncation error is \(O(h^2)\).

### Computational method

```python
"""Task 15: Numerical differentiation.

Compares forward and central finite-difference approximations against
an analytical derivative for f(x) = x^2.
"""

from __future__ import annotations

from typing import Callable


def forward_difference(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-5,
) -> float:
    """Approximate f'(x) using the forward-difference formula."""
    return (f(x + h) - f(x)) / h


def central_difference(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-5,
) -> float:
    """Approximate f'(x) using the central-difference formula."""
    return (f(x + h) - f(x - h)) / (2.0 * h)


if __name__ == "__main__":
    f = lambda x: x**2
    exact_derivative = lambda x: 2.0 * x

    x0 = 3.0
    exact = exact_derivative(x0)

    print(f"{'h':>10}  {'Forward err':>12}  {'Central err':>12}")
    print("-" * 38)

    for h in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
        fwd = forward_difference(f, x0, h)
        ctr = central_difference(f, x0, h)
        print(
            f"{h:>10.1e}  {abs(fwd - exact):>12.2e}  {abs(ctr - exact):>12.2e}"
        )
```

### Application: GPS speed estimation

If positions \(s(t)\) are sampled over time, velocity can be estimated by

\[
v(t)\approx\frac{s(t+h)-s(t)}{h}.
\]

Differentiation amplifies measurement noise. A smaller step is therefore not always better when the input consists of noisy measurements.

**Conclusion:** numerical differentiation is useful for estimating rates of change, but its accuracy depends on both the numerical formula and the quality of the sampled data.

---

## Task 16 — Numerical Integration and Energy Estimation

### Objective

To approximate definite integrals from sampled data and explain how integration supports cumulative-quantity estimation.

### Mathematical explanation

The definite integral

\[
I=\int_a^b f(x)\,dx
\]

represents accumulated quantity over an interval.

### Trapezoidal rule

For observations \(f_i=f(x_i)\), the composite trapezoidal rule is

\[
I\approx
\sum_{i=0}^{n-1}
\frac{x_{i+1}-x_i}{2}(f_i+f_{i+1}).
\]

### Computational method

```python
"""Task 16: Numerical integration using the trapezoidal rule.

Approximates the integral of f(x) = x^2 on [0, 2] and compares with
the exact value.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import trapezoid


def trapezoidal_integration(
    x: NDArray[np.floating],
    y: NDArray[np.floating],
) -> float:
    """Composite trapezoidal rule for non-uniformly spaced samples."""
    return float(trapezoid(y, x))


if __name__ == "__main__":
    # Two subintervals of width 1 on [0, 2].
    x = np.array([0.0, 1.0, 2.0])
    y = x**2  # f(x) = x^2.

    approx = trapezoidal_integration(x, y)
    exact = 8.0 / 3.0  # ∫₀² x² dx = 8/3.

    print(f"Trapezoidal approximation: {approx:.6f}")
    print(f"Exact integral:           {exact:.6f}")
    print(f"Absolute error:           {abs(approx - exact):.6f}")

    # Convergence check: refine the mesh.
    for n in [2, 4, 8, 16, 32]:
        x_fine = np.linspace(0.0, 2.0, n + 1)
        y_fine = x_fine**2
        approx_fine = trapezoidal_integration(x_fine, y_fine)
        print(f"n = {n:>3}: error = {abs(approx_fine - exact):.6e}")
```

### Verification

Compare the quadrature result with an analytical integral when possible. Increase sampling resolution and check whether the approximation converges toward the reference value.

**Conclusion:** numerical integration estimates accumulated quantities, but sampling resolution and the behaviour of the integrand determine its accuracy.

---

## Task 17 — Euler's Method and Newton's Law of Cooling

### Objective

To solve an initial-value ordinary differential equation numerically and examine the relationship between step size, stability, and accuracy.

### Mathematical model

Newton's law of cooling is

\[
\frac{dT}{dt}=-k(T-T_{\mathrm{amb}}),
\]

with initial condition

\[
T(0)=T_0.
\]

The analytical solution is

\[
T(t)=T_{\mathrm{amb}}+
(T_0-T_{\mathrm{amb}})e^{-kt}.
\]

### Euler's method

Euler's method approximates the derivative over a small time interval \(h\):

\[
\boxed{
T_{n+1}
=
T_n-hk(T_n-T_{\mathrm{amb}})
}
\]

### Computational method

```python
"""Task 17: Euler's method for Newton's law of cooling.

Integrates the cooling ODE with Euler's method and compares against
the analytical solution for varying step sizes.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def euler_cooling(
    T0: float,
    T_amb: float,
    k: float,
    h: float,
    t_end: float,
) -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    """Integrate the cooling ODE with Euler's method.

    Returns
    -------
    tuple[NDArray, NDArray]
        Time array and temperature array.
    """
    n_steps = int(np.ceil(t_end / h))
    t = np.linspace(0.0, n_steps * h, n_steps + 1)
    T = np.empty_like(t)
    T[0] = T0

    for i in range(n_steps):
        dT = -k * (T[i] - T_amb)
        T[i + 1] = T[i] + h * dT

    return t, T


def analytical_cooling(
    T0: float,
    T_amb: float,
    k: float,
    t: NDArray[np.floating],
) -> NDArray[np.floating]:
    """Exact solution of Newton's law of cooling."""
    return T_amb + (T0 - T_amb) * np.exp(-k * t)


if __name__ == "__main__":
    T0, T_amb, k = 100.0, 20.0, 0.1

    print(f"{'h':>8}  {'T(1) Euler':>12}  {'T(1) Exact':>12}  {'Error':>10}")
    print("-" * 48)

    for h in [1.0, 0.5, 0.25, 0.1, 0.05]:
        t, T_euler = euler_cooling(T0, T_amb, k, h, t_end=1.0)
        T_exact = analytical_cooling(T0, T_amb, k, np.array([1.0]))[0]
        T_euler_at_1 = T_euler[-1]
        print(
            f"{h:>8.2f}  {T_euler_at_1:>12.4f}  {T_exact:>12.4f}  "
            f"{abs(T_euler_at_1 - T_exact):>10.4f}"
        )

    # Stability check: u_{n+1} = (1 - kh) u_n.
    print("\nStability condition: |1 - kh| < 1")
    for h in [1.0, 5.0, 10.0, 20.0]:
        amplification = abs(1.0 - k * h)
        status = "stable" if amplification < 1.0 else "UNSTABLE"
        print(f"  h = {h:>5.1f}, |1 - kh| = {amplification:.4f} -> {status}")
```

### Step size and stability

For a sufficiently smooth problem, Euler's method generally has first-order global error over a fixed interval in its stable regime. Halving \(h\) should reduce the leading global error by approximately a factor of two when the method is operating in its asymptotic convergence regime.

**Conclusion:** Euler's method illustrates the fundamentals of time integration, but its simplicity must be balanced against step-size restrictions and approximation error.

---

## Task 18 — SciPy ODE Integration and RC Circuit Charging

### Objective

To explain how an adaptive ODE solver can numerically integrate a physical model and compare its result with an analytical solution.

### Mathematical model

For a series RC circuit with constant supply voltage \(V_s\), resistance \(R\), capacitance \(C\), and capacitor voltage \(V_C(t)\),

\[
\frac{dV_C}{dt}
=
\frac{V_s-V_C}{RC}.
\]

For an initially uncharged capacitor,

\[
V_C(0)=0.
\]

The analytical solution is

\[
\boxed{
V_C(t)=V_s(1-e^{-t/(RC)})
}
\]

The product

\[
\tau=RC
\]

is the circuit's time constant.

### Computational method

```python
"""Task 18: Adaptive ODE integration for an RC charging circuit.

Uses scipy.integrate.solve_ivp to integrate the capacitor voltage ODE
and compares the numerical solution with the analytical result.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp


def rc_circuit_ode(
    t: float,
    y: NDArray[np.floating],
    Vs: float,
    R: float,
    C: float,
) -> list[float]:
    """Right-hand side of the RC charging ODE."""
    voltage = y[0]
    return [(Vs - voltage) / (R * C)]


def analytical_rc(
    t: NDArray[np.floating],
    Vs: float,
    R: float,
    C: float,
) -> NDArray[np.floating]:
    """Exact capacitor voltage for an initially uncharged RC circuit."""
    tau = R * C
    return Vs * (1.0 - np.exp(-t / tau))


if __name__ == "__main__":
    Vs, R, C = 5.0, 1000.0, 1e-6
    tau = R * C

    # Integrate with adaptive Runge–Kutta (RK45) and tight tolerances.
    solution = solve_ivp(
        rc_circuit_ode,
        (0.0, 5.0 * tau),
        [0.0],
        args=(Vs, R, C),
        method="RK45",
        rtol=1e-10,
        atol=1e-12,
        dense_output=True,
    )

    if not solution.success:
        raise RuntimeError(f"ODE solver failed: {solution.message}")

    t_numerical = solution.t
    V_numerical = solution.y[0]

    # Analytical reference at the same time points.
    V_exact = analytical_rc(t_numerical, Vs, R, C)
    max_error = float(np.max(np.abs(V_numerical - V_exact)))

    print(f"Time constant τ = {tau:.6f} s")
    print(f"V_C(τ) analytical = {Vs * (1 - np.exp(-1)):.4f} V")
    print(f"V_C(τ) numerical  = {np.interp(tau, t_numerical, V_numerical):.4f} V")
    print(f"Maximum absolute error: {max_error:.2e} V")
```

### Verification

Evaluate the analytical solution at the numerical solver's output times and calculate the maximum absolute difference:

\[
E_{\max}=
\max_i|V_{C,\mathrm{numerical}}(t_i)
-V_{C,\mathrm{exact}}(t_i)|.
\]

**Conclusion:** adaptive integration is valuable when fixed-step methods would be inefficient or difficult to control, but numerical solutions should still be compared with independent references when possible.

---

## Task 19 — Mathematical Optimisation

### Objective

To formulate optimisation problems, identify feasible solutions, and distinguish continuous optimisation from problems involving indivisible resources.

### Mathematical formulation

A linear optimisation problem can be expressed as

\[
\min_x c^Tx
\]

subject to

\[
Ax\geq b,\qquad x\geq0.
\]

### Worked example

Suppose a workshop produces products \(A\) and \(B\). Let \(x\) be the quantity of product \(A\) and \(y\) the quantity of product \(B\).

Assume the objective is to minimise

\[
C=3x+2y
\]

subject to

\[
x+y\geq4,
\]

\[
x\geq0,\qquad y\geq0.
\]

Since product \(B\) costs less per unit, choosing \(x=0\) and \(y=4\) gives

\[
C=3(0)+2(4)=8.
\]

### Computational method

```python
"""Task 19: Mathematical optimisation with linear programming.

Solves a small linear program using SciPy's linprog and demonstrates
the effect of integer constraints.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import linprog


def solve_continuous_lp() -> dict:
    """Solve the continuous linear program min 3x + 2y s.t. x + y >= 4, x, y >= 0."""
    # linprog minimizes c^T x, so convert the >= constraint to <=.
    c = np.array([3.0, 2.0])
    A_ub = np.array([[-1.0, -1.0]])  # -x - y <= -4  ⇔  x + y >= 4.
    b_ub = np.array([-4.0])
    bounds = [(0.0, None), (0.0, None)]

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not result.success:
        raise RuntimeError(f"LP solver failed: {result.message}")

    return {
        "x": result.x,
        "objective": result.fun,
        "status": result.message,
    }


if __name__ == "__main__":
    result = solve_continuous_lp()
    print(f"Optimal x = {result['x']}")
    print(f"Minimum cost = {result['objective']:.2f}")
    print(f"Solver status: {result['status']}")
```

### Integer constraints

If decision variables represent whole machines, vehicles, or employees, integer constraints may be necessary:

\[
x_i\in\mathbb Z_{\geq0}.
\]

A continuous solution may be infeasible when quantities must be indivisible. Rounding a continuous optimum does not generally preserve feasibility or optimality.

**Conclusion:** optimisation provides a systematic way to select decisions under constraints, but the mathematical formulation must accurately represent operational requirements.

---

## Task 20 — Monte Carlo Simulation and Probability Estimation

### Objective

To estimate probabilities using random sampling and quantify the sampling uncertainty of the estimate.

### Mathematical model

Suppose demand \(D\) follows a normal distribution,

\[
D\sim\mathcal N(\mu,\sigma^2),
\]

and overload occurs when demand exceeds capacity \(K\).

The probability of overload is

\[
p=P(D>K)
=
1-\Phi\left(\frac{K-\mu}{\sigma}\right),
\]

where \(\Phi\) is the standard normal cumulative distribution function.

### Monte Carlo estimator

Generate \(N\) independent demand samples \(D_1,\ldots,D_N\). Define an indicator variable

\[
I_i=
\begin{cases}
1,&D_i>K,\\
0,&D_i\leq K.
\end{cases}
\]

The estimated probability is

\[
\boxed{
\hat p=\frac1N\sum_{i=1}^{N}I_i
}
\]

### Computational method

```python
"""Task 20: Monte Carlo simulation for overload probability estimation.

Estimates P(D > K) for D ~ N(mu, sigma^2) and quantifies the
sampling uncertainty via standard error.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.stats import norm


@dataclass(frozen=True)
class MonteCarloResult:
    """Container for Monte Carlo estimation output."""
    probability: float
    standard_error: float
    sample_size: int
    analytical_probability: float


def monte_carlo_overload(
    mu: float,
    sigma: float,
    capacity: float,
    n_samples: int,
    seed: int = 42,
) -> MonteCarloResult:
    """Estimate P(D > capacity) for D ~ N(mu, sigma^2).

    Parameters
    ----------
    mu, sigma : float
        Mean and standard deviation of the demand distribution.
    capacity : float
        Overload threshold.
    n_samples : int
        Number of independent Monte Carlo samples.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    MonteCarloResult
        Estimated probability, standard error, and analytical reference.
    """
    rng = np.random.default_rng(seed)
    samples = rng.normal(mu, sigma, size=n_samples)

    indicators = (samples > capacity).astype(float)
    p_hat = float(np.mean(indicators))

    se = float(np.sqrt(p_hat * (1.0 - p_hat) / n_samples))
    analytical = float(1.0 - norm.cdf((capacity - mu) / sigma))

    return MonteCarloResult(p_hat, se, n_samples, analytical)


if __name__ == "__main__":
    mu, sigma, capacity = 100.0, 20.0, 120.0

    print(f"{'N':>10}  {'p̂':>10}  {'SE':>10}  {'Exact p':>10}  {'Error':>10}")
    print("-" * 54)

    for n in [100, 1_000, 10_000, 100_000, 1_000_000]:
        result = monte_carlo_overload(mu, sigma, capacity, n)
        error = abs(result.probability - result.analytical_probability)
        print(
            f"{n:>10}  {result.probability:>10.6f}  {result.standard_error:>10.6f}  "
            f"{result.analytical_probability:>10.6f}  {error:>10.6f}"
        )
```

### Sample-size sensitivity

For independent samples under the usual assumptions, the standard error decreases approximately as

\[
\operatorname{SE}(\hat p)\propto N^{-1/2}.
\]

Increasing the sample count by a factor of \(100\) reduces the theoretical standard-error scale by approximately a factor of \(10\).

**Conclusion:** Monte Carlo simulation estimates uncertainty through repeated sampling, but both sampling error and model validity must be considered.

---

# 4. Parameter Sensitivity Analysis

Sensitivity analysis studies how changes in model inputs or algorithmic parameters influence numerical outputs.

## 4.1 Euler step-size sensitivity

For Euler integration, compare step sizes \(h\) and \(h/2\), while keeping the physical model and final time fixed.

Calculate

\[
E(h)=|T_{\mathrm{numerical}}(t_f;h)-T_{\mathrm{exact}}(t_f)|.
\]

Then calculate

\[
R=\frac{E(h)}{E(h/2)}.
\]

For a first-order method in its asymptotic convergence regime, the ratio should approach approximately \(2\).

## 4.2 Monte Carlo sample-size sensitivity

Keep the demand model and capacity threshold fixed and compare several sample sizes.

For each sample count \(N\), calculate the estimated probability and its standard error. Under independent sampling, increasing \(N\) reduces the standard-error scale according to \(N^{-1/2}\).

## 4.3 Other useful sensitivity experiments

| Task | Parameter varied | Output examined |
|---|---|---|
| 02 | Observation values | Mean, minimum, maximum, range |
| 03 | Array size | Runtime and speed-up |
| 04 | Magnitude of \(x\) | Absolute and relative error |
| 05 | Rotation angle and scale | Transformed coordinates and determinant |
| 06 | Coefficients or right-hand side | Solution and residual |
| 07 | Number of right-hand sides | Repeated-solve computational cost |
| 08 | Stopping tolerance | Iteration count and residual |
| 09 | Graph structure | Eigenvector centrality |
| 10 | Initial root bracket | Iterations and root enclosure |
| 11 | Initial estimates | Convergence and final residual |
| 12 | Initial guesses | Nonlinear solution reached |
| 13 | Interpolation method | Intermediate estimates |
| 14 | Model degree and data range | Fit quality and extrapolation |
| 15 | Difference step size | Derivative error |
| 16 | Sampling resolution | Integral approximation error |
| 17 | Time step | ODE error and stability |
| 18 | Solver tolerances | Accuracy and function evaluations |
| 19 | Capacity constraints | Feasibility and optimal objective |
| 20 | Sample count | Probability estimate and uncertainty |

Sensitivity experiments should vary one factor at a time when the purpose is to isolate its effect. When interactions between parameters matter, a factorial or other structured experimental design may be more informative.

---

# 5. Verification and Validation

## 5.1 Verification versus validation

**Verification** asks whether the algorithm has been implemented correctly.

**Validation** asks whether the mathematical model represents the real-world process adequately for its intended use.

For example, a Monte Carlo program may correctly estimate overload probability under a normal demand model while the normal distribution itself may be inappropriate for real demand. Numerical correctness and model suitability are different questions.

## 5.2 Verification criteria

| Task | Appropriate verification |
|---|---|
| 02 | Independently check statistics and unit conversions |
| 03 | Compare loop and vectorised outputs |
| 04 | Compare floating-point expressions with a reference |
| 05 | Check matrix transformations and determinant identities |
| 06 | Evaluate the linear-system residual |
| 07 | Check \(PA=LU\) and the solution residual |
| 08 | Check convergence and residual history |
| 09 | Evaluate \(Av-\lambda v\) |
| 10 | Confirm root-bracketing assumptions and final residual |
| 11 | Substitute the estimated root into the objective |
| 12 | Substitute each solution into every equation |
| 13 | Check interpolation at supplied knots |
| 14 | Calculate residuals and RMSE |
| 15 | Compare finite differences with an analytical derivative |
| 16 | Compare quadrature with a known integral |
| 17 | Compare numerical integration with the exact solution |
| 18 | Compare the ODE solution with the analytical RC model |
| 19 | Check constraints, domains, and objective value |
| 20 | Compare the probability estimate with a theoretical reference |

## 5.3 Tolerances and diagnostics

A numerical tolerance should reflect the scale of the problem, its conditioning, and the accuracy requirements. A value such as \(10^{-8}\) is not universally appropriate.

For floating-point comparisons, use tolerance-based checks rather than exact equality where exact representation is not expected.

For linear systems, a useful scaled residual is

\[
\eta=
\frac{\|b-A\hat x\|}
{\|A\|\|\hat x\|+\|b\|},
\]

when the denominator is nonzero.

For numerical integration, report the reference solution and error metric. For stochastic computation, report the sample count and an uncertainty estimate. For optimisation, report feasibility and termination status.

---

# 6. Computational Methodology and Reproducibility

A reproducible scientific computation requires sufficient information for another person to repeat the analysis and understand its results.

The following elements should be documented:

1. Mathematical model and assumptions.
2. Input values, units, and data sources.
3. Numerical method and relevant parameters.
4. Software dependencies and versions.
5. Random seed and sampling configuration for stochastic tasks.
6. Error metrics and verification procedures.
7. Instructions for reproducing figures and numerical outputs.

A Python package may use separate modules for individual tasks, shared utilities for logging and output handling, and automated tests for mathematical properties. This architecture improves maintainability by separating numerical logic from filesystem operations and task dispatch.

A random seed supports repeatable pseudorandom sequences under compatible conditions, but it does not guarantee identical results across all software versions and hardware environments.

### Suggested reproduction procedure

From a fresh clone, use Python 3.10 or newer. Runtime and development dependencies are defined in `pyproject.toml`.

```bash
git clone https://github.com/Ayman-muhammad/Scientific_computing-.git
cd Scientific_computing-

python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux (use this instead of the Windows activation line):
# source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

# Execute all registered numerical tasks and regenerate outputs.
python -m bit2118

# Quality gates
python -m pytest -v
python -m ruff check src tests
python -m ruff format --check src tests
```

The figures embedded above are version-controlled SVG concept illustrations. Runtime-generated plots and JSON outputs remain reproducible artefacts; do not present benchmark timings, solver outputs, test coverage, or CI status as verified until the corresponding command or workflow has actually run.

---

# 7. Critical Reflection and Learning Outcomes

## 7.1 Numerical reasoning

Finite-precision arithmetic demonstrates that algebraic equivalence does not always imply identical numerical behaviour. Conditioning, cancellation, and rounding error affect accuracy.

## 7.2 Algorithm selection

Bisection prioritises reliable bracketing, Newton's method can converge rapidly near a suitable root, and the secant method avoids explicit derivatives. Their different assumptions make them suitable for different problems.

## 7.3 Performance and resource use

Vectorisation and reusable LU factorisation illustrate the importance of computational structure. Performance improvements should be evaluated alongside memory use, accuracy, clarity, and maintainability.

## 7.4 Verification as part of scientific work

Residuals, analytical references, invariants, convergence histories, and constraint checks provide independent evidence about correctness. They should be integrated into the design of a numerical solution rather than added only after implementation.

## 7.5 Model interpretation

A mathematically correct computation does not automatically establish that a model describes reality. Statistical assumptions, measurement uncertainty, boundary conditions, and domain constraints must also be evaluated.

## 7.6 Reproducible engineering

Modular source code, documented assumptions, controlled dependencies, automated tests, and version control support independent inspection and repeated experimentation.

---

# 8. Limitations and Future Improvements

## 8.1 Model limitations

Illustrative models simplify complex systems. A quadratic regression may fit a limited data range but fail when extrapolated. A normal demand model may underrepresent extreme events if the true distribution has heavier tails.

## 8.2 Numerical limitations

Iterative solvers can be sensitive to initial conditions, matrix conditioning, stopping tolerances, and step sizes. A small residual does not always guarantee a small solution error.

## 8.3 Statistical limitations

Monte Carlo estimates contain sampling uncertainty, while regression estimates may be influenced by outliers, correlated errors, and overfitting. More data do not automatically resolve a flawed model.

## 8.4 Future improvements

Further work could include:

- Comparing convergence rates across numerical methods.
- Testing ill-conditioned and degenerate inputs.
- Adding uncertainty intervals to stochastic estimates.
- Evaluating regression using held-out data.
- Measuring runtime and numerical error systematically.
- Documenting software versions and dependency constraints.
- Testing across additional operating systems.
- Generating plots directly from the same inputs used in each calculation.
- Recording verification outcomes alongside numerical results.

---

# 9. Conclusion

Tasks 02–20 demonstrate a broad range of scientific-computing techniques. Array processing illustrates the value of structured numerical data and vectorisation. Floating-point analysis explains why representation and numerical stability matter. Matrix methods support geometric transformations, linear systems, and spectral analysis. Root-finding and ODE solvers demonstrate the relationship between convergence, stability, and accuracy. Interpolation, regression, integration, optimisation, and Monte Carlo simulation show how numerical techniques support estimation and decision-making.

Across all these methods, the same principle applies: a computational result should be examined in relation to its mathematical definition, numerical error, assumptions, and intended application.

A solver that returns a number has completed a computation. A scientific analysis must go further by establishing why that number is reasonable, how accurately it represents the mathematical problem, and what conclusions can legitimately be drawn from it.

**The standard of scientific computing is not merely producing a numerical answer. It is producing an answer that can be explained, evaluated, and independently verified.**

---

# References

1. NumPy Developers. *NumPy Documentation: Broadcasting.* https://numpy.org/doc/stable/user/basics.broadcasting.html
2. Python Software Foundation. *Floating-Point Arithmetic: Issues and Limitations.* https://docs.python.org/3/tutorial/floatingpoint.html
3. SciPy Developers. *`scipy.integrate.solve_ivp` Documentation.* https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html
4. Chapra, S. C., and Canale, R. P. *Numerical Methods for Engineers.* McGraw Hill.
5. Burden, R. L., Faires, J. D., and Burden, A. M. *Numerical Analysis.* Cengage Learning.
6. Atkinson, K. E. *An Introduction to Numerical Analysis.* Wiley.
7. Nocedal, J., and Wright, S. J. *Numerical Optimization.* Springer.
8. Higham, N. J. *Accuracy and Stability of Numerical Algorithms.* Society for Industrial and Applied Mathematics.

*Academic integrity note: the worked examples in this report are explanatory examples. Any claim about the actual repository's outputs, measured performance, test results, coverage, generated figures, or release status must be supported by the corresponding execution evidence. Consult the course assignment instructions to ensure that the report's scope and formatting meet the lecturer's requirements.*

**End of report.**
