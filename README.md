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

![Task 02: NumPy arrays and descriptive statistics](docs/figures/task-02.svg)

<sub>Figure: conceptual illustration of numpy arrays and descriptive statistics; visual aid only, not a measured result.</sub>

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

For example:

```python
import numpy as np

temperatures_c = np.array([20, 22, 24, 23, 21], dtype=float)

mean_c = np.mean(temperatures_c)
minimum_c = np.min(temperatures_c)
maximum_c = np.max(temperatures_c)
temperatures_f = temperatures_c * 9 / 5 + 32
```

NumPy's broadcasting and array operations support concise computation, although their performance depends on the operation, array size, and memory requirements. See the [NumPy broadcasting documentation](https://numpy.org/doc/stable/user/basics.broadcasting.html).

### Interpretation and verification

The mean describes the central level of the observations, while the range describes their spread between the extremes. Neither statistic alone captures the full distribution or identifies unusual observations.

Verification should include checking the calculated mean independently and confirming that each converted temperature satisfies the conversion formula.

**Conclusion:** array computation provides an efficient foundation for processing scientific observations, provided the units, dimensions, missing values, and statistical interpretation are handled correctly.

---

## Task 03 — Vectorisation and Performance Analysis

![Task 03: Vectorisation and benchmarking](docs/figures/task-03.svg)

<sub>Figure: conceptual illustration of vectorisation and benchmarking; visual aid only, not a measured result.</sub>

### Objective

To compare explicit looping with vectorised numerical computation and understand the conditions under which vectorisation improves performance.

### Mathematical explanation

Consider the transformation

\[
y_i=2x_i+1,\qquad i=1,\ldots,n.
\]

A loop evaluates the expression for each element individually. A vectorised operation expresses the same transformation over an entire array.

For example:

```python
import numpy as np

x = np.arange(1, 6, dtype=float)
y = 2 * x + 1
```

The mathematical outputs are

\[
y=[3,5,7,9,11].
\]

The important distinction is not the mathematical result, which should be identical in this example, but the computational mechanism.

Vectorised NumPy operations frequently execute their element-wise calculations in compiled code, reducing Python interpreter overhead.

### Performance measurement

Speed-up is defined as

\[
S=\frac{t_{\text{loop}}}{t_{\text{vectorised}}},
\]

where \(t_{\text{loop}}\) and \(t_{\text{vectorised}}\) are the measured execution times.

If a loop takes \(0.50\) seconds and an equivalent vectorised calculation takes \(0.10\) seconds, the illustrative speed-up is

\[
S=\frac{0.50}{0.10}=5.
\]

This means the vectorised version is five times as fast under those hypothetical measurements. These numbers demonstrate the calculation; they are not benchmark results from the submitted repository.

### Experimental design

A fair benchmark should use identical input data, equivalent operations, comparable execution conditions, and repeated measurements. Small operations may be dominated by timing overhead, while large arrays may be limited by memory bandwidth or allocation costs.

Vectorisation can also create large temporary arrays, so a vectorised implementation is not automatically the most memory-efficient solution.

### Verification

Confirm that both implementations return equivalent arrays using a tolerance-based comparison. Measure execution times separately and record the array size, software environment, and timing method.

**Conclusion:** vectorisation is an important performance technique, but claims about speed-up must be supported by measurements rather than assumed from code style.

---

## Task 04 — Floating-Point Arithmetic and Numerical Stability

![Task 04: Floating-point stability](docs/figures/task-04.svg)

<sub>Figure: conceptual illustration of floating-point stability; visual aid only, not a measured result.</sub>

### Objective

To explain finite-precision arithmetic, rounding error, cancellation, and the effect of algebraic reformulation on numerical accuracy.

### Mathematical explanation

Computers represent many real numbers approximately using finite-precision binary floating-point arithmetic. Decimal fractions such as \(0.1\) generally have no exact finite binary representation.

Consequently, an expression such as

```python
0.1 + 0.2
```

may produce a value displayed as

```text
0.30000000000000004
```

This is a representation effect, not evidence that ordinary arithmetic is incorrect. Python documents these limitations in its [floating-point arithmetic guide](https://docs.python.org/3/tutorial/floatingpoint.html).

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

for values where the expressions are defined.

The second form avoids subtracting two nearly equal quantities and is often more accurate for small \(x\).

### Sensitivity and stability

A problem is ill-conditioned when small changes in its input can produce large changes in its true solution. An algorithm is numerically unstable when its computational errors grow excessively during the calculation.

These are distinct concepts: a stable algorithm cannot remove the intrinsic sensitivity of an ill-conditioned problem.

### Verification

Evaluate both algebraic forms over a range of small and moderate values, comparing them with a higher-precision reference where necessary. Inspect absolute and relative error rather than relying solely on printed decimal digits.

**Conclusion:** numerical accuracy depends on the representation of numbers, the conditioning of the problem, and the stability of the chosen algorithm.

---

## Task 05 — Matrix Algebra and Geometric Transformations

![Task 05: Matrix transformations](docs/figures/task-05.svg)

<sub>Figure: conceptual illustration of matrix transformations; visual aid only, not a measured result.</sub>

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

### Verification

Test transformations on known points and confirm the determinant identities. Check the order of multiplication carefully and distinguish angles measured in degrees from those measured in radians.

**Conclusion:** matrices provide a compact, composable representation of geometric transformations and make their mathematical properties straightforward to verify.

---

## Task 06 — Solving Systems of Linear Equations

![Task 06: Linear systems](docs/figures/task-06.svg)

<sub>Figure: conceptual illustration of linear systems; visual aid only, not a measured result.</sub>

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

In matrix form,

\[
\begin{bmatrix}
2&1\\
1&-1
\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix}
=
\begin{bmatrix}5\\1\end{bmatrix}.
\]

### Numerical solution and residual

Scientific software typically uses a numerical linear solver instead of explicitly calculating \(A^{-1}\). Directly computing an inverse is generally unnecessary and can be less efficient or less numerically reliable than solving the system directly.

For an approximate solution \(\hat x\), define the residual

\[
r=b-A\hat x.
\]

A small residual indicates that the computed solution approximately satisfies the supplied equations.

However, a small residual does not guarantee a small error in \(\hat x\) when \(A\) is ill-conditioned.

### Application constraints

In resource-allocation problems, a mathematically valid solution may still be operationally invalid. For example, a solution of \(x=2.4\) machines is not feasible if machines must be counted as whole units.

Such problems may require non-negativity constraints or integer optimisation.

### Verification

Substitute the solution into the original equations, calculate the residual norm, and check the domain of the variables.

**Conclusion:** a linear solver must be assessed through equation satisfaction and application constraints, not merely successful execution.

---

## Task 07 — LU Decomposition

![Task 07: LU decomposition](docs/figures/task-07.svg)

<sub>Figure: conceptual illustration of lu decomposition; visual aid only, not a measured result.</sub>

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

### Worked example

Consider

\[
A=
\begin{bmatrix}
2&1\\
4&3
\end{bmatrix}.
\]

One LU factorisation without pivoting is

\[
L=
\begin{bmatrix}
1&0\\
2&1
\end{bmatrix},
\qquad
U=
\begin{bmatrix}
2&1\\
0&1
\end{bmatrix}.
\]

Multiplication verifies that

\[
LU=
\begin{bmatrix}
2&1\\
4&3
\end{bmatrix}=A.
\]

Suppose

\[
b=
\begin{bmatrix}5\\11\end{bmatrix}.
\]

Forward substitution gives

\[
y_1=5,\qquad 2y_1+y_2=11,
\]

so \(y_2=1\).

Backward substitution gives

\[
x_2=1,\qquad 2x_1+x_2=5,
\]

so \(x_1=2\). Therefore,

\[
x=
\begin{bmatrix}2\\1\end{bmatrix}.
\]

### Computational advantage

When several right-hand sides share the same matrix \(A\), its factorisation can be reused. This avoids repeating the more expensive factorisation stage for every new vector \(b\).

### Verification

Check that \(PA=LU\), solve each system, and evaluate its residual. Pivoting should be considered when zero or small pivots may cause numerical difficulties.

**Conclusion:** LU decomposition is particularly valuable when a fixed matrix must be used to solve multiple linear systems.

---

## Task 08 — Iterative Linear Solvers: Jacobi and Gauss–Seidel

![Task 08: Jacobi and Gauss–Seidel](docs/figures/task-08.svg)

<sub>Figure: conceptual illustration of jacobi and gauss–seidel; visual aid only, not a measured result.</sub>

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

### Worked example

Consider

\[
4x+y=9,
\]

\[
x+3y=7.
\]

Rearranging,

\[
x=\frac{9-y}{4},
\qquad
y=\frac{7-x}{3}.
\]

Starting from \(x^{(0)}=0\), \(y^{(0)}=0\), the first Jacobi iteration gives

\[
x^{(1)}=\frac94=2.25,
\qquad
y^{(1)}=\frac73\approx2.3333.
\]

The first Gauss–Seidel iteration updates \(x\) first and then uses that new value to calculate \(y\):

\[
x^{(1)}=2.25,
\]

\[
y^{(1)}=\frac{7-2.25}{3}\approx1.5833.
\]

The different second components illustrate how the methods use information differently. One iteration alone is not sufficient to establish which method converges faster for every problem.

### Convergence

Strict diagonal dominance is a useful sufficient condition for convergence of these methods in many standard settings. Convergence is not guaranteed for every matrix.

A stopping criterion can be based on

\[
\|b-Ax^{(k)}\|<\varepsilon,
\]

where \(\varepsilon\) is a chosen tolerance.

### Verification

Compare the final approximation with a direct solution, record the residual norm over iterations, and confirm that the stopping rule is satisfied.

**Conclusion:** iterative methods can be useful for large systems, but convergence and accuracy must be demonstrated rather than assumed.

---

## Task 09 — Eigenvalues, Eigenvectors, and Network Centrality

![Task 09: Eigenvalues and network centrality](docs/figures/task-09.svg)

<sub>Figure: conceptual illustration of eigenvalues and network centrality; visual aid only, not a measured result.</sub>

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

For directed networks, interpretation depends on the direction of edges and the particular centrality formulation. Eigenvector centrality should not be treated as identical to PageRank, which uses a different model and typically includes damping and transition probabilities.

### Verification

Evaluate

\[
r=Av-\lambda v
\]

and check that \(\|r\|\) is sufficiently small. Eigenvectors may be normalised to unit length or another stated convention because multiplying an eigenvector by a nonzero scalar produces another eigenvector.

**Conclusion:** eigenvalue analysis reveals structural properties of matrices and networks, but the interpretation depends on the matrix construction and model assumptions.

---

## Task 10 — Bisection and Fixed-Point Iteration

![Task 10: Bisection and fixed-point iteration](docs/figures/task-10.svg)

<sub>Figure: conceptual illustration of bisection and fixed-point iteration; visual aid only, not a measured result.</sub>

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

After \(n\) iterations, the interval width is

\[
\frac{b_0-a_0}{2^n}.
\]

Thus, bisection has a predictable error bound when its assumptions hold.

### Fixed-point iteration

A fixed-point method rewrites the equation as

\[
T=g(T)
\]

and iterates

\[
T_{n+1}=g(T_n).
\]

A common convergence condition is that \(|g'(T)|<1\) in a suitable neighbourhood of the fixed point. This is a sufficient local condition, not a universal guarantee.

### Comparison

Bisection is robust when a valid bracket is available. Fixed-point iteration may be simpler or faster for a suitable mapping, but convergence depends on the choice of \(g\) and the starting value.

### Verification

Confirm the initial sign change for bisection, calculate the final residual \(|f(T)|\), and check the stopping criterion. For fixed-point iteration, examine the change between successive iterates and whether the sequence converges.

**Conclusion:** method selection should account for convergence guarantees, available derivatives or brackets, and the required accuracy.

---

## Task 11 — Newton's Method, Secant Method, and Internal Rate of Return

![Task 11: Newton, secant and internal rate of return](docs/figures/task-11.svg)

<sub>Figure: conceptual illustration of newton, secant and internal rate of return; visual aid only, not a measured result.</sub>

### Objective

To explain derivative-based and derivative-free root-finding methods and their use in financial calculations.

### Newton's method

Newton's method updates an estimate using

\[
x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}.
\]

The formula comes from approximating \(f\) locally by its tangent line and using the tangent's intercept as the next estimate.

Newton's method can converge rapidly near a suitable simple root. However, it may fail when the derivative is zero or very small, when the starting estimate is poor, or when the iteration leaves the relevant region.

### Secant method

The secant method approximates the derivative using two previous points:

\[
x_{n+1}
=
x_n-f(x_n)
\frac{x_n-x_{n-1}}{f(x_n)-f(x_{n-1})}.
\]

It avoids calculating the analytical derivative but still depends on suitable initial estimates and function behaviour.

### Financial application: internal rate of return

The internal rate of return is a discount rate \(r\) that satisfies

\[
\operatorname{NPV}(r)
=
\sum_{t=0}^{n}
\frac{CF_t}{(1+r)^t}=0,
\]

where \(CF_t\) denotes the cash flow at time \(t\).

Consider an investment costing 100 units initially and returning 110 units after one period:

\[
\operatorname{NPV}(r)=-100+\frac{110}{1+r}.
\]

Setting NPV equal to zero gives

\[
-100+\frac{110}{1+r}=0.
\]

Therefore,

\[
1+r=1.1
\quad\Longrightarrow\quad
\boxed{r=0.10=10\%}.
\]

This is an exact result for the illustrative one-period investment.

### Important limitation

For cash flows that change sign more than once, the NPV equation may have multiple roots or no economically meaningful root. A numerical solver's output must therefore be interpreted in the context of the cash-flow pattern.

### Verification

Substitute the estimated discount rate into the NPV equation and check that the residual is close to zero. Also verify that \(r>-1\) when the standard discounting formula requires positive \(1+r\).

**Conclusion:** Newton and secant methods are useful for nonlinear financial equations, but convergence and economic interpretation remain essential.

---

## Task 12 — Solving Nonlinear Systems

![Task 12: Nonlinear systems](docs/figures/task-12.svg)

<sub>Figure: conceptual illustration of nonlinear systems; visual aid only, not a measured result.</sub>

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

These values are rounded illustrations of the algebraic solutions.

### Numerical formulation

Define the residual vector

\[
F(x,y)=
\begin{bmatrix}
x^2+y^2-4\\
y-x^2+1
\end{bmatrix}.
\]

A numerical nonlinear solver seeks a point for which both components are approximately zero.

### Initial guesses and verification

Different initial guesses can lead a local solver to different intersections. A solver may also fail or converge to a point with an unacceptable residual.

Every candidate should be substituted into both original equations. Graphical intersection is useful for interpretation, but numerical substitution provides a stronger verification check.

**Conclusion:** nonlinear systems may have multiple valid solutions, making initial conditions and independent residual checks important.

---

## Task 13 — Interpolation and Cubic Splines

![Task 13: Interpolation and cubic splines](docs/figures/task-13.svg)

<sub>Figure: conceptual illustration of interpolation and cubic splines; visual aid only, not a measured result.</sub>

### Objective

To estimate intermediate values from known data points and compare linear interpolation with spline interpolation.

### Linear interpolation

Given two observations \((x_0,y_0)\) and \((x_1,y_1)\), linear interpolation estimates a value between the points using

\[
y(x)=y_0+
\frac{x-x_0}{x_1-x_0}(y_1-y_0).
\]

Suppose a sensor records \(10\) units at time \(0\) and \(20\) units at time \(4\). The estimated value at time \(2\) is

\[
y(2)=10+\frac{2-0}{4-0}(20-10)=15.
\]

This is an interpolation estimate, not necessarily the true physical measurement at time \(2\).

### Cubic spline interpolation

A cubic spline represents each interval using a cubic polynomial,

\[
S_i(x)=a_i+b_i(x-x_i)+c_i(x-x_i)^2+d_i(x-x_i)^3.
\]

The coefficients are chosen to satisfy interpolation conditions and suitable continuity constraints. Standard cubic splines are constructed to maintain continuity of the function and its first and second derivatives at internal knots.

Boundary conditions, such as natural or clamped conditions, affect the resulting spline.

### Comparison

Linear interpolation is simple and locally transparent. Cubic splines can produce smoother curves but may overshoot between data points, particularly when the data vary sharply.

Neither method should be assumed to recover the true underlying function without further information.

### Verification

Check that the interpolant reproduces the supplied data at every knot. Where a reference function or independent observations exist, calculate interpolation errors at additional points.

**Conclusion:** interpolation provides estimates between observations, but the method should reflect the smoothness and behaviour expected of the underlying process.

---

## Task 14 — Curve Fitting and Regression

![Task 14: Regression and curve fitting](docs/figures/task-14.svg)

<sub>Figure: conceptual illustration of regression and curve fitting; visual aid only, not a measured result.</sub>

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

Least squares chooses the coefficients that minimise this quantity.

The root-mean-square error is

\[
\operatorname{RMSE}
=
\sqrt{\frac{1}{n}
\sum_{i=1}^{n}(y_i-\hat y_i)^2}.
\]

RMSE measures the typical scale of the residuals in the units of the response variable. It should not be interpreted independently of the scale and variability of the data.

### Illustrative application

Suppose a server's measured response time rises as the number of simultaneous users increases. A quadratic curve may describe the observed pattern over a limited range.

However, a good fit to the observed data does not prove that response time will continue following the same quadratic pattern at much larger user counts. The system may enter a new regime because of saturation, queueing, caching, or other effects.

### Residual analysis

Residuals are

\[
e_i=y_i-\hat y_i.
\]

Residual plots can reveal systematic patterns, unequal variance, or influential observations that a single error statistic may conceal.

### Verification

Calculate the residuals and RMSE independently, inspect the fitted curve, and evaluate predictions on held-out data when available. Model complexity should be justified rather than increased solely to reduce training error.

**Conclusion:** regression quantifies relationships in observed data, but model adequacy and predictive reliability require additional evidence.

---

## Task 15 — Numerical Differentiation

![Task 15: Numerical differentiation](docs/figures/task-15.svg)

<sub>Figure: conceptual illustration of numerical differentiation; visual aid only, not a measured result.</sub>

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

Under suitable smoothness assumptions, its truncation error is \(O(h^2)\), making it more accurate than the forward difference for sufficiently small steps when other errors are controlled.

### Worked example

Let

\[
f(x)=x^2.
\]

Its exact derivative is

\[
f'(x)=2x.
\]

At \(x=3\), the exact derivative is \(6\).

Using the forward difference with \(h=0.1\),

\[
\frac{f(3.1)-f(3)}{0.1}
=
\frac{9.61-9}{0.1}=6.1.
\]

Using the central difference,

\[
\frac{f(3.1)-f(2.9)}{0.2}
=
\frac{9.61-8.41}{0.2}=6.
\]

For this quadratic example, the central-difference result is exact apart from floating-point effects.

### Application: GPS speed estimation

If positions \(s(t)\) are sampled over time, velocity can be estimated by

\[
v(t)\approx\frac{s(t+h)-s(t)}{h}.
\]

Differentiation amplifies measurement noise. A smaller step is therefore not always better when the input consists of noisy measurements.

### Verification

Test both methods against a function with a known derivative. Check units, boundary handling, and the effect of varying \(h\).

**Conclusion:** numerical differentiation is useful for estimating rates of change, but its accuracy depends on both the numerical formula and the quality of the sampled data.

---

## Task 16 — Numerical Integration and Energy Estimation

![Task 16: Numerical integration](docs/figures/task-16.svg)

<sub>Figure: conceptual illustration of numerical integration; visual aid only, not a measured result.</sub>

### Objective

To approximate definite integrals from sampled data and explain how integration supports cumulative-quantity estimation.

### Mathematical explanation

The definite integral

\[
I=\int_a^b f(x)\,dx
\]

represents accumulated quantity over an interval. When an analytical antiderivative is unavailable or the data are discrete, numerical quadrature can approximate the integral.

### Trapezoidal rule

For observations \(f_i=f(x_i)\), the composite trapezoidal rule is

\[
I\approx
\sum_{i=0}^{n-1}
\frac{x_{i+1}-x_i}{2}(f_i+f_{i+1}).
\]

Each interval is approximated by a trapezoid whose parallel sides have heights \(f_i\) and \(f_{i+1}\).

### Worked example

Estimate

\[
\int_0^2 x^2\,dx
\]

using two equal subintervals of width \(1\).

The observations are

\[
f(0)=0,\quad f(1)=1,\quad f(2)=4.
\]

Therefore,

\[
I\approx
\frac{1}{2}(0+1)+
\frac{1}{2}(1+4).
\]

Thus,

\[
I\approx0.5+2.5=3.
\]

The exact integral is

\[
\int_0^2 x^2\,dx
=\left[\frac{x^3}{3}\right]_0^2
=\frac83\approx2.6667.
\]

The absolute error of the trapezoidal approximation is approximately

\[
|3-2.6667|=0.3333.
\]

This demonstrates that a valid numerical procedure can still introduce approximation error.

### Application: electrical energy

If electrical power is \(P(t)\), energy consumption is

\[
E=\int_{t_0}^{t_1}P(t)\,dt.
\]

When power is measured in kilowatts and time in hours, energy is measured in kilowatt-hours.

### Verification

Compare the quadrature result with an analytical integral when possible. Increase sampling resolution and check whether the approximation converges toward the reference value.

**Conclusion:** numerical integration estimates accumulated quantities, but sampling resolution and the behaviour of the integrand determine its accuracy.

---

## Task 17 — Euler's Method and Newton's Law of Cooling

![Task 17: Euler method and Newton cooling](docs/figures/task-17.svg)

<sub>Figure: conceptual illustration of euler method and newton cooling; visual aid only, not a measured result.</sub>

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

Here \(T(t)\) is the object's temperature, \(T_{\mathrm{amb}}\) is the ambient temperature, and \(k>0\) is the cooling constant.

The analytical solution is

\[
T(t)=T_{\mathrm{amb}}+
(T_0-T_{\mathrm{amb}})e^{-kt}.
\]

### Euler's method

Euler's method approximates the derivative over a small time interval \(h\):

\[
\frac{T_{n+1}-T_n}{h}
\approx-k(T_n-T_{\mathrm{amb}}).
\]

Rearranging,

\[
\boxed{
T_{n+1}
=
T_n-hk(T_n-T_{\mathrm{amb}})
}
\]

This update calculates the next temperature using the current temperature and its estimated rate of change.

### Worked example

Let

\[
T_0=100^\circ C,\quad
T_{\mathrm{amb}}=20^\circ C,\quad
k=0.1,\quad h=1.
\]

Then

\[
T_1=100-1(0.1)(100-20)=92^\circ C.
\]

The analytical solution at \(t=1\) is

\[
T(1)=20+80e^{-0.1}
\approx92.39^\circ C.
\]

The Euler approximation is approximately \(92^\circ C\), giving an absolute error of about \(0.39^\circ C\). The values are rounded for presentation.

### Step size and stability

For a sufficiently smooth problem, Euler's method generally has first-order global error over a fixed interval in its stable regime. Halving \(h\) should reduce the leading global error by approximately a factor of two when the method is operating in its asymptotic convergence regime.

For the cooling equation, the error dynamics are particularly transparent. Defining \(u_n=T_n-T_{\mathrm{amb}}\),

\[
u_{n+1}=(1-kh)u_n.
\]

The numerical solution decays without alternating sign when \(0\leq kh\leq1\), and its linear stability condition is \(|1-kh|<1\).

### Verification

Compare the numerical temperatures with the exact solution at identical times. Repeat the computation with smaller time steps and calculate the error ratio.

**Conclusion:** Euler's method illustrates the fundamentals of time integration, but its simplicity must be balanced against step-size restrictions and approximation error.

---

## Task 18 — SciPy ODE Integration and RC Circuit Charging

![Task 18: Adaptive ODE integration and RC circuit](docs/figures/task-18.svg)

<sub>Figure: conceptual illustration of adaptive ode integration and rc circuit; visual aid only, not a measured result.</sub>

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

is the circuit's time constant. At \(t=\tau\),

\[
V_C(\tau)=V_s(1-e^{-1})
\approx0.6321V_s.
\]

Thus, after one time constant, the capacitor reaches approximately \(63.2\%\) of the final voltage.

### Numerical integration

SciPy's `solve_ivp` solves initial-value problems of the form

\[
\frac{dy}{dt}=f(t,y),\qquad y(t_0)=y_0.
\]

It supports several numerical integration methods, including adaptive Runge–Kutta methods. The solver adjusts its step sizes according to its error-control procedure and specified tolerances. See the [SciPy `solve_ivp` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html).

A typical implementation is:

```python
import numpy as np
from scipy.integrate import solve_ivp

Vs = 5.0
R = 1000.0
C = 1e-6

def circuit_rhs(t, y):
    voltage = y[0]
    return [(Vs - voltage) / (R * C)]

solution = solve_ivp(
    circuit_rhs,
    (0.0, 0.01),
    [0.0],
    rtol=1e-8,
    atol=1e-10
)
```

The code illustrates the model setup. Its numerical accuracy should be assessed by examining the returned solution rather than assumed from the chosen tolerance alone.

### Verification

Evaluate the analytical solution at the numerical solver's output times and calculate the maximum absolute difference:

\[
E_{\max}=
\max_i|V_{C,\mathrm{numerical}}(t_i)
-V_{C,\mathrm{exact}}(t_i)|.
\]

Also check solver success, units, initial conditions, and the chosen tolerances.

**Conclusion:** adaptive integration is valuable when fixed-step methods would be inefficient or difficult to control, but numerical solutions should still be compared with independent references when possible.

---

## Task 19 — Mathematical Optimisation

![Task 19: Mathematical optimisation](docs/figures/task-19.svg)

<sub>Figure: conceptual illustration of mathematical optimisation; visual aid only, not a measured result.</sub>

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

Here:

- \(x\) is the decision-variable vector.
- \(c\) contains the objective coefficients.
- \(A\) describes the constraints.
- \(b\) specifies the required resource levels.

The feasible region contains every decision vector satisfying the constraints.

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

For any feasible non-negative \(x,y\),

\[
3x+2y\geq2x+2y
=2(x+y)\geq8.
\]

Therefore, the solution \((x,y)=(0,4)\) is optimal for this illustrative model, with minimum cost \(8\).

### Integer constraints

If decision variables represent whole machines, vehicles, or employees, integer constraints may be necessary:

\[
x_i\in\mathbb Z_{\geq0}.
\]

A continuous solution may be infeasible when quantities must be indivisible. Rounding a continuous optimum does not generally preserve feasibility or optimality.

### Verification

Evaluate the objective function at the proposed solution, check every constraint, and confirm the required variable domains. Solver termination status should be reported together with the actual feasibility checks.

**Conclusion:** optimisation provides a systematic way to select decisions under constraints, but the mathematical formulation must accurately represent operational requirements.

---

## Task 20 — Monte Carlo Simulation and Probability Estimation

![Task 20: Monte Carlo simulation](docs/figures/task-20.svg)

<sub>Figure: conceptual illustration of monte carlo simulation; visual aid only, not a measured result.</sub>

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

This is the fraction of simulated observations that exceed the capacity threshold.

### Worked example

Suppose a simulation produces \(120\) overload events from \(1{,}000\) independent samples.

The estimated probability is

\[
\hat p=\frac{120}{1000}=0.12.
\]

The estimated overload probability is therefore \(12\%\).

An approximate Monte Carlo standard error is

\[
\operatorname{SE}(\hat p)
\approx
\sqrt{\frac{\hat p(1-\hat p)}{N}}.
\]

Substituting,

\[
\operatorname{SE}(\hat p)
\approx
\sqrt{\frac{0.12(0.88)}{1000}}
\approx0.0103.
\]

The estimated standard error is approximately \(1.03\) percentage points. This calculation describes a hypothetical sample; it is not a result from the submitted program.

### Sample-size sensitivity

For independent samples under the usual assumptions, the standard error decreases approximately as

\[
\operatorname{SE}(\hat p)\propto N^{-1/2}.
\]

Increasing the sample count by a factor of \(100\) reduces the theoretical standard-error scale by approximately a factor of \(10\).

Monte Carlo simulation is especially useful when the probability of interest cannot be computed conveniently through direct integration or analytical methods.

### Verification and limitations

Compare the simulated estimate with the analytical probability when the distribution is known. Record the random seed and sample count, and report a confidence interval or standard-error estimate.

The quality of the estimate depends on the sampling assumptions and the model. A large sample does not correct an inappropriate probability distribution, biased sampling, or incorrect simulation logic.

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

For a first-order method in its asymptotic convergence regime, the ratio should approach approximately \(2\). This is a theoretical expectation, not a guaranteed result for every pair of step sizes.

The experiment demonstrates the trade-off between computational effort and approximation error: halving the step size approximately doubles the number of steps over a fixed interval.

## 4.2 Monte Carlo sample-size sensitivity

Keep the demand model and capacity threshold fixed and compare several sample sizes.

For each sample count \(N\), calculate the estimated probability and its standard error. Under independent sampling, increasing \(N\) reduces the standard-error scale according to \(N^{-1/2}\).

Different random samples may produce different estimates even when the seed and model are controlled. The purpose of the experiment is to examine the relationship between sampling effort and uncertainty, not to assume that every estimate improves monotonically.

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

when the denominator is nonzero. This helps interpret residuals relative to the scale of the problem.

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

Likewise, a workflow configuration file demonstrates that automated checks have been configured; only the corresponding execution record can establish whether those checks passed.

### Suggested reproduction procedure

From a fresh clone, use Python 3.10 or newer. Runtime and development dependencies are defined in `pyproject.toml`.

```bash
git clone https://github.com/Ayman-muhammad/Scientific_computing-.git
cd Scientific_computing-

python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
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
