# BIT 2118 — Scientific Computing
## Final Technical Submission Report

**Student:** Ayman Muhammad  
**Student ID:** [Insert student ID]  
**Course:** BIT 2118 — Scientific Computing  
**Assignment:** Group Work — Tasks 02–20  
**Submission date:** [Insert submission date]  
**GitHub repository:** https://github.com/Ayman-muhammad/Scientific_computing-  
**Branch:** `main`  
**Reference commit:** `ac9d7dc`  
**Release:** `v1.0.0` — create and verify this tag before claiming it as a published release.

---

## Table of Contents

1. Executive Summary
2. Introduction and Objectives
3. Repository Architecture
4. Computational Methodology
5. Task-by-Task Technical Analysis
6. Parameter Sensitivity Analysis
7. Verification and Validation
8. Reproducibility and Execution
9. Critical Reflection and Learning Outcomes
10. Limitations and Future Improvements
11. Conclusion
12. Appendix A — Reproduction Commands
13. Appendix B — Repository File Index

---

# 1. Executive Summary

Scientific computing is not simply the act of translating mathematical formulae into Python. It is the disciplined application of numerical methods, computational algorithms, error analysis, verification, and interpretation to problems that may be difficult or impractical to solve analytically.

This project implements a structured scientific-computing package for the nineteen assignment tasks spanning Task 02 through Task 20. The work covers array computation, numerical stability, matrix algebra, linear systems, eigenvalue analysis, nonlinear root-finding, interpolation, regression, numerical calculus, ordinary differential equations, optimisation, and Monte Carlo simulation.

The implementation adopts a modular Python architecture. Each task is represented by a dedicated computational module, while shared utilities handle filesystem paths, logging, JSON persistence, and task registration. Automated tests are provided to verify important mathematical properties and numerical results.

The central engineering principle is that **a numerical answer is not trustworthy merely because a program produces it**. Its correctness must be assessed using independent references, residuals, invariants, analytical solutions, convergence behaviour, or other appropriate verification criteria.

## 1.1 Project objectives

The project is designed to:

1. Implement the numerical techniques required by the assignment.
2. Identify the mathematical inputs, parameters, assumptions, and operations for each task.
3. demonstrate parameter sensitivity by examining how numerical outputs change when inputs or algorithmic parameters change.
4. Interpret computational results using mathematical reasoning and relevant real-world contexts.
5. Organise the implementation as a maintainable and reproducible software package.
6. Support independent execution and verification through automated tests and version control.

## 1.2 Technical scope

| Area | Tasks | Principal concepts |
|---|---|---|
| Array computation | 02–03 | NumPy arrays, vectorisation, performance |
| Numerical precision | 04 | Floating-point representation, stability, error |
| Linear algebra | 05–08 | Transformations, linear systems, LU, iterative methods |
| Spectral analysis | 09 | Eigenvalues, eigenvectors, centrality |
| Nonlinear equations | 10–12 | Bisection, fixed-point, Newton, secant, systems |
| Approximation and regression | 13–14 | Interpolation, splines, least squares |
| Numerical calculus | 15–16 | Finite differences, quadrature |
| Differential equations | 17–18 | Euler integration, adaptive ODE solvers |
| Operations research and risk | 19–20 | Optimisation, Monte Carlo estimation |

The source code and supporting documentation are maintained in the public GitHub repository listed above.

**Evidence standard:** numerical values, timing measurements, test totals, coverage percentages, generated artefacts, and continuous-integration status must be confirmed by executing the current repository. The theoretical results described in this report should not be mistaken for verified runtime measurements unless the corresponding execution evidence is available.

---

# 2. Introduction and Objectives

## 2.1 Background

Scientific computing provides the computational machinery required to investigate mathematical models, approximate solutions, and interpret quantitative behaviour.

Many practical problems cannot be solved efficiently using elementary algebra alone. Examples include large linear systems, nonlinear equilibrium equations, parameter estimation, dynamical systems, and uncertainty analysis. Numerical methods address these problems by converting mathematical formulations into algorithms that can be executed, tested, and analysed.

However, numerical computation introduces its own difficulties. Finite-precision arithmetic can distort results; iterative algorithms may fail to converge; approximations introduce truncation error; and an apparently plausible output may still violate the governing equations.

Consequently, this assignment treats numerical computing as a combination of:

- Mathematical formulation.
- Algorithm selection.
- Computational implementation.
- Error and convergence analysis.
- Independent verification.
- Interpretation of results.

## 2.2 Objectives

The work follows the assignment's stated requirements through the following objectives.

**Objective A — Implementation:** develop computational modules for Tasks 02–20.

**Objective B — Parameter identification:** document the inputs, mathematical parameters, assumptions, and operations relevant to each task.

**Objective C — Sensitivity analysis:** investigate how selected inputs or numerical parameters affect accuracy, convergence, computational cost, or predicted outcomes.

**Objective D — Interpretation:** explain the meaning of numerical outputs and the information conveyed by relevant plots.

**Objective E — Application:** associate each numerical technique with a distinct illustrative real-world problem.

**Objective F — Software engineering:** organise the implementation into reusable modules with shared infrastructure.

**Objective G — Reproducibility:** maintain the source code in version control and provide a documented procedure for rerunning the computations.

---

# 3. Repository Architecture

## 3.1 Directory structure

The repository uses a `src/`-based Python package layout.

```text
BIT2118-Scientific-Computing/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── architecture.md
│   ├── mathematical_notes.md
│   ├── methodology.md
│   ├── reproducibility.md
│   ├── WORK_PLAN.md
│   └── tasks/
│       └── task02 ... task20 documentation
├── report/
│   ├── README.md
│   ├── REPORT_TEMPLATE.md
│   ├── report.md
│   └── figures/
├── results/
│   └── generated JSON results
├── src/
│   └── bit2118/
│       ├── __init__.py
│       ├── __main__.py
│       ├── io_utils.py
│       ├── logging_config.py
│       ├── paths.py
│       ├── registry.py
│       └── task02 ... task20 modules
├── tests/
│   ├── conftest.py
│   ├── test_io_utils.py
│   ├── test_paths.py
│   └── test_scientific_computing.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── Makefile
├── .gitignore
└── README.md
```

Generated result files and figures are produced by the computational pipeline when configured to do so. Their existence in the working directory must be checked after execution; the directory structure alone does not establish that every output has already been generated or committed.

## 3.2 Architectural decisions

### Separation of concerns

Each task has a dedicated module. This makes the numerical implementation easier to inspect and allows a problem to be tested independently of unrelated tasks.

The shared modules serve distinct responsibilities:

- `paths.py` centralises project and output paths.
- `logging_config.py` establishes consistent logging behaviour.
- `io_utils.py` handles result serialisation and persistence.
- `registry.py` provides task discovery and dispatch.
- `__main__.py` exposes the package's command-line entry point.

This separation reduces duplicated infrastructure and makes the relationship between mathematical algorithms and software mechanics easier to understand.

### Reproducible outputs

Where stochastic methods are used, explicit random seeds make experiments repeatable under the same software environment and random-number generation procedure.

JSON output provides a structured representation of numerical results. It supports programmatic inspection, comparison between runs, and downstream analysis.

Reproducibility also requires documenting dependency versions, input parameters, and relevant execution settings. A random seed alone does not guarantee byte-for-byte identical results across every library version, hardware platform, or floating-point implementation.

### Testable numerical interfaces

A numerical function should expose meaningful inputs and return outputs that can be checked independently. Tests should focus on mathematical properties rather than merely confirming that a function executes without raising an exception.

For example, a linear-system solver should be assessed through its residual; an eigenpair should satisfy the eigenvalue equation; and a numerical integrator should be compared against an analytical or independently computed reference when one is available.

---

# 4. Computational Methodology

## 4.1 General workflow

The project follows a consistent computational sequence.

1. **Formulate the problem.** Identify the governing equations, variables, assumptions, and expected solution.
2. **Select the method.** Choose an algorithm appropriate to the problem's structure, accuracy requirements, and computational cost.
3. **Implement the computation.** Use Python and relevant scientific libraries.
4. **Evaluate the result.** Compute relevant diagnostics such as residuals, errors, convergence histories, or feasibility checks.
5. **Interpret the output.** Relate the numerical result to the mathematical model and its illustrative application.
6. **Test and document.** Preserve the implementation, verification criteria, and reproduction procedure.

## 4.2 Mathematical verification

Four principal forms of verification are relevant throughout the assignment.

### Analytical comparison

When a closed-form solution exists, the numerical result can be compared against it.

For example, Newton's law of cooling has the analytical solution

\[
T(t)=T_{\mathrm{amb}}+
(T_0-T_{\mathrm{amb}})e^{-kt}.
\]

A numerical approximation can be assessed using

\[
E_{\mathrm{abs}}=
|T_{\mathrm{numerical}}-T_{\mathrm{exact}}|.
\]

### Residual analysis

For a linear system

\[
Ax=b,
\]

the residual is

\[
r=b-Ax.
\]

A small residual indicates that the computed vector approximately satisfies the supplied equations. It does not, by itself, guarantee a small forward error if the system is ill-conditioned.

### Invariant checking

Some mathematical properties should remain valid regardless of the particular numerical result.

Examples include

\[
Av=\lambda v
\]

for an eigenpair, and

\[
\sum_i p_i=1
\]

for a normalised probability vector.

### Convergence and feasibility

Iterative methods should be assessed for convergence and sensitivity to initial conditions or tolerances. Optimisation algorithms should be assessed against their constraints, objective function, and termination conditions.

A successful solver status is useful evidence, but it is not a substitute for checking the resulting solution.

## 4.3 Error and tolerance policy

Numerical tolerances must be selected in relation to the problem's scale, algorithm, and precision requirements.

| Problem type | Diagnostic | Interpretation |
|---|---|---|
| Linear systems | \(\|b-Ax\|\) | Equation-satisfaction error |
| Root finding | \(|f(x^\*)|\) and step size | Root residual and iteration behaviour |
| Eigenvalue computation | \(\|Av-\lambda v\|\) | Eigenpair consistency |
| ODE integration | Error against a reference | Approximation accuracy |
| Interpolation | Error at known points | Agreement with supplied data |
| Regression | RMSE and residual inspection | In-sample fit quality |
| Monte Carlo | Standard error or confidence interval | Sampling uncertainty |

A tolerance such as \(10^{-8}\) is not universally appropriate. The choice depends on scaling, conditioning, machine precision, and the consequences of error.

For floating-point comparisons, tolerance-based checks such as `numpy.isclose` are generally more appropriate than exact equality when comparing computed real numbers.

---

# 5. Task-by-Task Technical Analysis

Each task is discussed in terms of its mathematical concept, computational approach, illustrative inputs, interpretation, and verification criteria.

Numerical values in the examples below describe the intended experimental cases. Confirm them against the actual generated outputs before treating them as measured findings.

## Task 02 — NumPy Arrays

**Concept:** array construction, element-wise operations, and descriptive statistics.

**Application:** hourly weather-station measurements.

Given an array of temperatures

\[
C=[C_1,C_2,\ldots,C_n],
\]

the arithmetic mean is

\[
\bar C=\frac{1}{n}\sum_{i=1}^{n}C_i.
\]

Conversion from Celsius to Fahrenheit follows

\[
F_i=\frac95C_i+32.
\]

NumPy applies this transformation element-wise without requiring an explicit Python loop.

**Interpretation:** vectorised expressions make numerical operations concise and efficient. The mean, minimum, and maximum provide a basic summary of the observed temperature profile.

**Verification:** compare the array statistics against independently calculated values and confirm that each Fahrenheit value satisfies the conversion equation.

## Task 03 — Vectorisation and Performance

**Concept:** replacing repeated Python-level operations with array-oriented computation.

**Application:** network-latency analysis using a large sample of synthetic observations.

A loop-based implementation and a NumPy implementation should produce equivalent results when they apply the same mathematical operation to the same data.

Performance can be assessed using elapsed times:

\[
S=\frac{t_{\mathrm{loop}}}{t_{\mathrm{vectorised}}},
\]

where \(S\) is the measured speed-up.

**Interpretation:** vectorisation can reduce interpreter overhead and exploit optimised array operations. The magnitude of the benefit depends on data size, memory access, the operation performed, and the hardware.

**Verification:** compare the output arrays within an appropriate tolerance. Measure both implementations under comparable conditions; do not present a single timing result as a universal performance guarantee.

## Task 04 — Floating-Point Arithmetic

**Concept:** finite-precision representation, rounding error, and numerical stability.

**Application:** financial calculations, GPS computations, and iterative numerical algorithms.

Most decimal fractions cannot be represented exactly in binary floating-point. Consequently, an expression such as

```python
0.1 + 0.2
```

may produce

```text
0.30000000000000004
```

rather than an exact decimal representation of \(0.3\).

A second issue is cancellation. For small \(x\), the expression

\[
\sqrt{1+x}-1
\]

subtracts two nearly equal quantities. Rationalisation gives

\[
\sqrt{1+x}-1
=\frac{x}{\sqrt{1+x}+1}.
\]

For sufficiently small \(x\), the rationalised form can preserve more significant information.

**Interpretation:** algebraic equivalence does not imply equal numerical behaviour. A stable algorithm accounts for finite precision rather than treating real-number arithmetic as exact.

**Verification:** compare both expressions against a higher-precision reference over a range of \(x\) values. Measure absolute and relative errors, and avoid interpreting exact equality as the sole correctness criterion.

## Task 05 — Matrix Algebra and Geometric Transformations

**Concept:** matrix multiplication, determinants, rotation, and scaling.

**Application:** a two-dimensional graphics transformation.

A rotation through angle \(\theta\) is represented by

\[
R(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}.
\]

A scaling transformation is

\[
S=
\begin{bmatrix}
s_x&0\\
0&s_y
\end{bmatrix}.
\]

For a scaling followed by a rotation, the composite transformation is

\[
T=RS.
\]

The determinant of the scaling matrix is

\[
\det(S)=s_xs_y,
\]

while \(\det(R)=1\). Thus, rotation preserves area, whereas scaling changes area by the factor \(|s_xs_y|\).

**Interpretation:** matrix composition allows several geometric operations to be expressed as a single transformation.

**Verification:** test the determinant identities and compare transformed coordinates against direct calculations. The order of matrix multiplication must be stated because matrix multiplication is generally noncommutative.

## Task 06 — Solving Linear Systems

**Concept:** solving simultaneous linear equations.

**Application:** allocating two types of servers under CPU and memory constraints.

Suppose the numbers of Type A and Type B servers are \(x_1\) and \(x_2\). If their resource totals are represented by a matrix \(A\) and vector \(b\), the system is

\[
Ax=b.
\]

A numerical solver computes an approximate solution \(x\).

The result should be checked using

\[
r=b-Ax.
\]

**Interpretation:** the solution describes a resource allocation consistent with the equations, provided the solution is feasible for the intended application. A mathematically valid fractional solution may not be operationally valid if the variables represent indivisible servers.

**Verification:** calculate the residual and check the original equations. If the application requires integer counts, explicitly check integrality and non-negativity.

## Task 07 — LU Decomposition

**Concept:** matrix factorisation and repeated solution of linear systems.

For a suitable square matrix, LU decomposition expresses

\[
PA=LU,
\]

where \(P\) is a permutation matrix, \(L\) is lower triangular, and \(U\) is upper triangular.

To solve \(Ax=b\), first solve

\[
Ly=Pb,
\]

then solve

\[
Ux=y.
\]

When several right-hand sides share the same matrix, the factorisation can be reused rather than recomputed for every solve.

**Interpretation:** the main advantage is computational efficiency when the coefficient matrix remains unchanged.

**Verification:** compare the computed solutions with a trusted direct solver and evaluate residuals for every right-hand side. Pivoting and matrix conditioning should be considered when interpreting accuracy.

## Task 08 — Iterative Linear Solvers

**Concept:** Jacobi and Gauss–Seidel iteration.

**Application:** steady-state heat conduction along a one-dimensional material.

A discretised heat-conduction problem can be expressed as a linear system

\[
Ax=b.
\]

Jacobi iteration updates each component using values from the previous iteration. Gauss–Seidel uses newly computed values immediately within the current sweep.

Both methods require suitable convergence conditions. Strict diagonal dominance is a useful sufficient condition in many cases, but convergence must not be assumed for every arbitrary matrix.

**Interpretation:** iterative methods can be attractive for large sparse systems. Gauss–Seidel may converge in fewer iterations than Jacobi for a particular problem, but this is not a universal rule.

**Verification:** record the residual or iteration error, check the stopping criterion, and compare the result with a direct solution. A convergence plot should show how the selected error measure changes across iterations.

## Task 09 — Eigenvalues and Eigenvectors

**Concept:** spectral properties of matrices.

An eigenvalue \(\lambda\) and corresponding nonzero eigenvector \(v\) satisfy

\[
Av=\lambda v.
\]

For an adjacency matrix describing a network, the dominant eigenvector can be used to define eigenvector centrality, subject to the assumptions of the chosen centrality model.

A normalised non-negative centrality vector can be scaled so that

\[
\sum_i c_i=1.
\]

**Interpretation:** a node may be considered important when it is connected to other important nodes. This differs from simply counting the number of direct connections.

**Verification:** calculate the eigenpair residual and check the normalisation. The interpretation of the dominant eigenvector depends on the graph structure and assumptions; the method should not be described as universally equivalent to PageRank.

## Task 10 — Bisection and Fixed-Point Iteration

**Concept:** solving a nonlinear scalar equation.

For the illustrative equilibrium model

\[
f(T)=T-25-10e^{-T/20},
\]

the objective is to find \(T^\*\) such that

\[
f(T^\*)=0.
\]

Bisection begins with an interval whose endpoint values have opposite signs. Each iteration halves the interval while retaining a bracket containing a root.

Fixed-point iteration instead uses

\[
T_{n+1}=g(T_n).
\]

A fixed point is locally attractive under suitable conditions, such as \(|g'(T^\*)|<1\).

**Interpretation:** bisection offers robust bracketing when the sign-change condition is satisfied. Fixed-point iteration can be simpler but depends on the mapping and its convergence behaviour.

**Verification:** compare the computed roots and evaluate the residuals. Confirm the initial interval satisfies the required sign-change condition.

## Task 11 — Newton and Secant Methods

**Concept:** derivative-based and derivative-free root-finding.

For an objective \(f(x)\), Newton's method uses

\[
x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}.
\]

The secant method estimates the derivative using two previous approximations:

\[
x_{n+1}=x_n-
f(x_n)\frac{x_n-x_{n-1}}
{f(x_n)-f(x_{n-1})}.
\]

An illustrative financial application is the internal rate of return. The rate \(r\) is found by solving

\[
\operatorname{NPV}(r)=
\sum_{t=0}^{n}\frac{CF_t}{(1+r)^t}=0,
\]

subject to the validity of the cash-flow model and rate domain.

**Interpretation:** Newton's method can converge rapidly near a suitable root but is sensitive to initial guesses and derivative behaviour. The secant method avoids explicitly calculating the derivative but is not guaranteed to converge in every case.

**Verification:** evaluate the objective at the estimated root, inspect iteration termination, and check whether multiple economically meaningful roots may exist.

## Task 12 — Nonlinear Systems

**Concept:** solving multiple nonlinear equations simultaneously.

Consider the system

\[
x^2+y^2=4,
\]

\[
y=x^2-1.
\]

The first equation describes a circle and the second a parabola. Their intersection points satisfy both equations simultaneously.

A numerical method may use a vector-valued residual function

\[
F(x,y)=
\begin{bmatrix}
x^2+y^2-4\\
y-x^2+1
\end{bmatrix}.
\]

The objective is to find a point where \(F(x,y)\) is approximately the zero vector.

**Interpretation:** nonlinear systems can have multiple solutions. A solver's output may depend on its initial guess, and a single successful run does not establish that all roots have been found.

**Verification:** substitute every candidate solution into both equations and inspect the residual vector. Use multiple initial guesses when investigating multiple intersections.

## Task 13 — Interpolation

**Concept:** estimating values between observed data points.

Linear interpolation between \((x_0,y_0)\) and \((x_1,y_1)\) is

\[
y(x)=y_0+
\frac{x-x_0}{x_1-x_0}(y_1-y_0).
\]

Cubic splines use piecewise cubic polynomials with continuity constraints to construct a smoother interpolant.

**Application:** estimating temperatures at more frequent intervals from hourly measurements.

**Interpretation:** a spline may provide a smoother representation than linear interpolation, but smoothness alone does not guarantee greater accuracy. The suitability of an interpolant depends on the data and the underlying process.

**Verification:** confirm that the interpolant reproduces the supplied data at the interpolation knots and compare predictions against held-out observations or a known reference where available.

## Task 14 — Curve Fitting

**Concept:** estimating model parameters from observed data.

For a quadratic model,

\[
y=ax^2+bx+c,
\]

the coefficients are estimated by minimising the sum of squared residuals:

\[
\operatorname{SSE}=
\sum_{i=1}^{n}
(y_i-\hat y_i)^2.
\]

Root-mean-square error is defined as

\[
\operatorname{RMSE}=
\sqrt{\frac1n
\sum_{i=1}^{n}(y_i-\hat y_i)^2}.
\]

**Application:** modelling server response time as a function of concurrent users.

**Interpretation:** a quadratic term can represent nonlinear growth in response time, but the fitted curve should not be extrapolated beyond the observed range without justification.

**Verification:** calculate residuals and RMSE, inspect the fit graph, and compare model predictions against independent data when possible. A low training error alone does not establish predictive reliability.

## Task 15 — Numerical Differentiation

**Concept:** approximating derivatives from discrete observations.

For a sufficiently smooth function, the forward-difference approximation is

\[
f'(x)\approx\frac{f(x+h)-f(x)}{h}.
\]

The central-difference approximation is

\[
f'(x)\approx\frac{f(x+h)-f(x-h)}{2h}.
\]

For smooth functions, the forward difference has first-order truncation error, while the central difference has second-order truncation error under standard assumptions.

**Application:** estimating speed from GPS position samples.

**Interpretation:** central differences often provide better accuracy at interior points, but they require observations on both sides of the target point. Measurement noise and the choice of step size affect the derivative estimate.

**Verification:** test against a known function with an analytical derivative and inspect units, boundary treatment, and noise sensitivity.

## Task 16 — Numerical Integration

**Concept:** approximating definite integrals from sampled values.

The trapezoidal rule approximates an integral using trapezoids:

\[
\int_a^b f(x)\,dx
\approx
\sum_{i=0}^{n-1}
\frac{x_{i+1}-x_i}{2}
(f_i+f_{i+1}).
\]

Simpson's rule uses quadratic approximations and has different accuracy conditions, including restrictions on the number and arrangement of sample intervals for its standard composite form.

**Application:** calculating energy consumption from power measurements.

Since power is energy per unit time,

\[
E=\int_{t_0}^{t_1}P(t)\,dt.
\]

For power in kilowatts and time in hours, the resulting energy is measured in kilowatt-hours.

**Interpretation:** numerical integration converts a sampled rate into an accumulated quantity. Agreement between two rules can be informative but does not, by itself, prove that either result is accurate.

**Verification:** compare against an analytical integral for a known function and ensure the units and sampling intervals are handled correctly.

## Task 17 — Euler's Method

**Concept:** numerical integration of ordinary differential equations.

For the initial-value problem

\[
\frac{dT}{dt}=-k(T-T_{\mathrm{amb}}),
\qquad T(0)=T_0,
\]

explicit Euler integration gives

\[
T_{n+1}=T_n-hk(T_n-T_{\mathrm{amb}}),
\]

where \(h\) is the time step.

The exact solution is

\[
T(t)=T_{\mathrm{amb}}+
(T_0-T_{\mathrm{amb}})e^{-kt}.
\]

**Interpretation:** Euler's method is easy to implement and useful for understanding numerical time stepping. Its global error is generally first-order in \(h\) for sufficiently smooth problems over a fixed interval, provided the method remains stable.

**Verification:** compare numerical temperatures against the analytical solution at matching time points. Repeat with smaller step sizes and measure the error rather than assuming it will halve exactly in every finite computation.

## Task 18 — SciPy ODE Integration

**Concept:** numerical solution of an initial-value problem using an adaptive solver.

For an RC charging circuit, the capacitor voltage may be modelled as

\[
\frac{dV_C}{dt}
=\frac{V_s-V_C}{RC}.
\]

For constant supply voltage and zero initial capacitor voltage, the analytical solution is

\[
V_C(t)=V_s(1-e^{-t/(RC)}).
\]

An adaptive solver such as SciPy's `solve_ivp` adjusts its integration steps according to the selected method and error tolerances.

**Interpretation:** adaptive integration can allocate smaller steps where needed and larger steps where the solution is smooth. Accuracy and computational cost depend on the system, solver, and tolerances.

**Verification:** compare the numerical solution with the analytical curve, inspect the solver status, and evaluate the maximum absolute error over a defined set of comparison points.

## Task 19 — Optimisation

**Concept:** minimising a cost function subject to constraints.

A generic optimisation problem is

\[
\min_x c^\mathsf{T}x
\]

subject to

\[
Ax\ge b,\qquad x\ge0.
\]

If the decision variables represent indivisible resources, integer constraints may be required.

**Application:** selecting server capacity under a minimum service-capacity requirement.

A continuous relaxation permits fractional decisions. An integer formulation restricts selected variables to integer values.

**Interpretation:** the continuous solution may provide a lower bound on the minimum cost of the corresponding integer minimisation problem when the relaxation is valid. The two solutions need not be close in every instance.

**Verification:** evaluate the objective, check all constraints, and confirm the variable domains. For integer optimisation, explicitly test integrality and report solver termination status.

## Task 20 — Monte Carlo Simulation

**Concept:** estimating probabilities through random sampling.

Suppose simulated demand \(D\) follows a normal model,

\[
D\sim\mathcal N(\mu,\sigma^2),
\]

and overload occurs when \(D>C\), where \(C\) is system capacity.

A Monte Carlo estimator is

\[
\hat p=\frac1N
\sum_{i=1}^{N}\mathbf1(D_i>C),
\]

where \(\mathbf1\) is the indicator function.

For the normal model, the analytical comparison is

\[
p=P(D>C)=
1-\Phi\left(\frac{C-\mu}{\sigma}\right),
\]

where \(\Phi\) is the standard normal cumulative distribution function.

For independent Bernoulli indicators, the approximate standard error of the estimated probability is

\[
\operatorname{SE}(\hat p)
\approx
\sqrt{\frac{\hat p(1-\hat p)}{N}}.
\]

**Interpretation:** Monte Carlo estimation is particularly useful for complicated or high-dimensional probability models. Its sampling uncertainty decreases at a rate proportional to \(N^{-1/2}\), so reducing the error by a factor of ten typically requires about one hundred times as many samples under comparable conditions.

**Verification:** compare the estimate with the analytical probability, calculate a sampling-uncertainty measure, and confirm that the random seed is recorded. A single estimate should not be presented as the exact underlying probability.

---

# 6. Parameter Sensitivity Analysis

Sensitivity analysis examines how a computational result responds to changes in inputs, assumptions, or algorithmic parameters. It distinguishes a numerical method's behaviour from the particular example used to demonstrate it.

Two representative experiments illustrate the approach.

## 6.1 Task 17 — Euler step-size sensitivity

Consider Euler integration of Newton's law of cooling.

The primary numerical parameter is the time step \(h\). For a fixed final time, reducing \(h\) increases the number of steps but generally reduces the global discretisation error for a sufficiently smooth problem in the stable operating regime.

A controlled experiment should:

1. Select a fixed initial temperature, ambient temperature, cooling constant, and final time.
2. Compute the analytical solution at the final time.
3. Run Euler integration using step sizes \(h\) and \(h/2\).
4. Calculate the absolute error for each run.
5. Compare error reduction with the expected first-order convergence behaviour.

The error ratio can be estimated as

\[
R=\frac{E(h)}{E(h/2)}.
\]

For a method operating in its first-order convergence regime, \(R\) is expected to approach approximately \(2\) as the step size becomes sufficiently small.

**Engineering implication:** improving accuracy requires additional computational steps. The correct step size is a trade-off between computational cost and acceptable error.

## 6.2 Task 20 — Monte Carlo sample-size sensitivity

The primary parameter is the sample count \(N\).

Run the same demand model with a small sample count and a substantially larger sample count while keeping the model assumptions and capacity threshold unchanged.

For example, compare \(N=1{,}000\) with \(N=100{,}000\).

The estimated probability may vary between runs because it is a random-sampling estimator. Increasing \(N\) generally reduces its standard error according to

\[
\operatorname{SE}(\hat p)\propto N^{-1/2}.
\]

Increasing the sample count by a factor of one hundred therefore reduces the theoretical standard-error scale by a factor of approximately ten, provided the other assumptions remain unchanged.

**Engineering implication:** sample-size selection should be guided by the required precision, not merely by the desire to generate a large dataset.

## 6.3 Sensitivity reporting for the remaining tasks

For each remaining task, sensitivity analysis should identify a parameter that materially influences the computation.

| Task | Example parameter | Quantity to examine |
|---|---|---|
| 02 | Input observations | Mean, range, and transformed values |
| 03 | Array length | Runtime and speed-up |
| 04 | Magnitude of \(x\) | Floating-point error |
| 05 | Rotation angle or scale | Transformed coordinates and determinant |
| 06 | Resource totals | Solution and residual |
| 07 | Number of right-hand sides | Repeated-solve cost |
| 08 | Stopping tolerance | Iterations and final residual |
| 09 | Graph structure | Eigenvector centrality |
| 10 | Initial bracket | Root enclosure and iteration count |
| 11 | Initial guesses | Convergence and root residual |
| 12 | Initial estimates | Which intersection is found |
| 13 | Interpolation method | Estimated intermediate values |
| 14 | Model degree or data range | Fit quality and extrapolation |
| 15 | Difference step \(h\) | Derivative error |
| 16 | Sampling resolution | Integral approximation error |
| 18 | Solver tolerances | Accuracy and function evaluations |
| 19 | Capacity requirement | Feasibility and minimum cost |

These are proposed experimental dimensions. A claim that every task has been experimentally varied should be made only after the corresponding runs and outputs have been recorded.

---

# 7. Verification and Validation

## 7.1 Verification strategy

Verification asks whether the implementation correctly performs the intended numerical computation. Validation asks whether the mathematical model and its assumptions adequately represent the problem being investigated.

These are related but distinct questions.

For example, a Monte Carlo program may correctly estimate the overload probability of a normal distribution while the assumed normal demand model remains inappropriate for the real system. Likewise, a regression algorithm may correctly minimise squared error without establishing that its fitted model predicts future observations reliably.

## 7.2 Verification matrix

| Task | Verification criterion |
|---|---|
| 02 | Statistics agree with independently computed array values |
| 03 | Loop and vectorised outputs agree within tolerance |
| 04 | Floating-point behaviour agrees with expected representation and error analysis |
| 05 | Transformation and determinant identities hold |
| 06 | Linear-system residual is acceptably small |
| 07 | LU solutions agree with an independent direct solver |
| 08 | Iterative results satisfy the system and stopping criterion |
| 09 | Eigenpair residual is small and centrality normalisation is valid |
| 10 | Root residuals are small and bracketing assumptions hold |
| 11 | Root residual and iteration termination are checked |
| 12 | Each nonlinear solution satisfies every equation |
| 13 | Interpolants reproduce the data at the knots |
| 14 | Residuals and RMSE are computed correctly |
| 15 | Finite differences agree with an analytical derivative in a known test case |
| 16 | Quadrature agrees with a known integral in a controlled test |
| 17 | Euler solution is compared with the exact cooling curve |
| 18 | Numerical ODE solution is compared with the analytical RC solution |
| 19 | Objective, constraints, and variable domains are checked |
| 20 | Monte Carlo estimate is compared with an analytical probability |

The tolerance used for each criterion must be documented alongside the test. A threshold should be chosen based on the mathematical problem and numerical method rather than selected after seeing the result.

## 7.3 Automated testing

The project includes a pytest suite covering utility functionality and scientific-computing tasks.

A complete verification run should include:

```bash
pytest -v
```

Where coverage reporting is configured:

```bash
pytest --cov=bit2118 --cov-report=term-missing
```

Linting can be checked using:

```bash
ruff check src tests
```

The final report should record the actual test summary and coverage output from the current codebase. It should not substitute an expected number of passing tests for the test runner's measured output.

## 7.4 Continuous integration

The repository contains a GitHub Actions workflow at `.github/workflows/ci.yml`.

The workflow should be inspected and executed to establish which Python versions, dependency configurations, lint rules, and tests are actually covered.

A workflow file is evidence that automation has been configured; a successful run is the evidence that the configured checks passed.

---

# 8. Reproducibility and Execution

Reproducibility allows another person to recreate the computational results using the same source code, inputs, dependencies, and relevant execution settings.

## 8.1 Environment setup

The following commands illustrate a Windows Git Bash setup.

```bash
git clone https://github.com/Ayman-muhammad/Scientific_computing-.git
cd Scientific_computing-

python -m venv .venv
source .venv/Scripts/activate

python -m pip install --upgrade pip
pip install -e ".[dev]"
```

The editable installation command assumes that `pyproject.toml` defines the relevant package and development dependencies. If the project's optional dependency group has a different name, use the group actually configured in that file.

If editable installation is not configured, install the documented dependencies and follow the import instructions in the repository README.

## 8.2 Execute the computational pipeline

If the package entry point is configured to run all registered tasks:

```bash
python -m bit2118
```

The command should be checked against `src/bit2118/__main__.py` and the task registry to confirm its actual behaviour.

If configured as described, execution will run the registered computations and write the supported results to the designated output locations.

Then run the tests:

```bash
pytest -v
ruff check src tests
```

## 8.3 Inspect generated artefacts

After execution, inspect the result directories:

```bash
find results -maxdepth 1 -type f
find report/figures -maxdepth 1 -type f
```

Confirm the actual number and names of generated JSON files and figures. Some generated outputs may be excluded from Git by `.gitignore` because they can be reproduced from the source code.

## 8.4 Reproducibility limitations

Reproducibility has several levels:

- **Procedural reproducibility:** another user can follow the same documented steps.
- **Numerical reproducibility:** results agree within a defined tolerance.
- **Bitwise reproducibility:** output bytes are identical.

Bitwise reproducibility is stricter than numerical reproducibility. Timestamps, dependency changes, floating-point behaviour, library versions, and output ordering can cause files to differ even when the scientific conclusions are equivalent.

For stochastic tasks, record the seed and the relevant generator configuration. For performance measurements, record the machine, Python version, library versions, and measurement procedure.

---

# 9. Critical Reflection and Learning Outcomes

## 9.1 Numerical reasoning

One of the most important lessons from scientific computing is that a mathematical expression and its implementation are not automatically equivalent in finite-precision arithmetic.

Floating-point representation, conditioning, cancellation, and truncation error all influence computational accuracy. Choosing an algorithm therefore requires more than identifying a formula that is correct over the real numbers.

A reliable implementation must also consider how the computation behaves under finite precision.

## 9.2 Algorithm selection

The root-finding tasks illustrate that numerical algorithms have different strengths.

Bisection prioritises robust bracketing. Newton's method can converge rapidly when its assumptions are favourable. The secant method avoids explicit derivative evaluation but remains sensitive to the problem and starting estimates.

No single method is optimal for every nonlinear equation. Algorithm selection depends on the available information, convergence requirements, and acceptable failure modes.

## 9.3 Computational efficiency

Vectorisation and reusable matrix factorisation demonstrate that performance improvements often come from selecting the right computational structure rather than merely writing more code.

The relevant question is not simply whether an implementation is fast. It is whether it achieves an appropriate balance between speed, memory usage, accuracy, clarity, and maintainability.

## 9.4 Verification as part of implementation

A numerical algorithm should be designed with verification in mind.

Residuals, analytical references, invariants, convergence diagnostics, and constraint checks provide independent evidence about correctness. They also make debugging more systematic because they identify which mathematical property has failed.

Testing should therefore be treated as part of the scientific method, not as a final administrative step.

## 9.5 Reproducible software engineering

The `src/` package layout, shared utilities, documentation, version control, and automated tests establish a foundation for maintainable scientific software.

A well-structured repository helps separate implementation details from scientific reasoning. It also enables other students, instructors, or reviewers to inspect the methods and independently reproduce the results.

---

# 10. Limitations and Future Improvements

A technically credible report should acknowledge what the current methods do not establish.

## 10.1 Model limitations

Illustrative real-world applications simplify complex systems. A quadratic response-time model, for example, may describe a limited observed range but fail under substantially different workloads. A normal demand distribution may underestimate risk if the actual demand distribution has heavy tails.

Model assumptions must be assessed separately from the numerical correctness of the implementation.

## 10.2 Numerical limitations

Iterative methods may depend on initial estimates, matrix conditioning, step sizes, or stopping tolerances. Small residuals do not always imply small solution errors, particularly for ill-conditioned problems.

Numerical diagnostics should therefore be interpreted in context.

## 10.3 Statistical limitations

Monte Carlo estimates have sampling uncertainty. Regression estimates may be affected by outliers, correlated errors, and extrapolation. A single simulation or training-error statistic is insufficient to establish general predictive performance.

Confidence intervals, residual analysis, sensitivity studies, and independent observations can provide stronger evidence.

## 10.4 Future development

Potential extensions include:

1. Add convergence-rate experiments for the iterative solvers.
2. Expand tests to cover ill-conditioned and degenerate inputs.
3. Add uncertainty intervals to Monte Carlo estimates.
4. Evaluate fitted models using held-out data.
5. Record execution time and numerical error systematically.
6. Pin or lock dependencies for more controlled environments.
7. Extend continuous integration to additional operating systems where practical.
8. Improve the reporting pipeline so that generated figures, numerical summaries, and test results can be reproduced consistently.

These improvements would deepen the project's analytical strength and make its numerical conclusions easier to evaluate independently.

---

# 11. Conclusion

This assignment brings together nineteen scientific-computing tasks covering a broad range of numerical techniques. The central challenge is not merely implementing algorithms, but understanding their assumptions, evaluating their numerical behaviour, and determining whether their outputs are trustworthy.

Array computation demonstrates the value of vectorised operations. Floating-point analysis shows why finite precision matters. Linear algebra and spectral methods reveal the importance of residuals and invariants. Root-finding and differential-equation solvers illustrate the relationship between convergence, stability, and accuracy. Interpolation, regression, optimisation, and Monte Carlo simulation demonstrate how numerical methods support approximation and decision-making.

The modular package structure provides a foundation for maintaining the implementations and reproducing the experiments. Its tests, documentation, and version-controlled source code support independent review.

The ultimate standard of scientific computing is not whether a program produces a number. It is whether the number can be explained, verified, and interpreted within the assumptions of the model.

That principle governs the work presented in this report.

---

# Appendix A — Reproduction Commands

From a fresh Windows Git Bash session:

```bash
git clone https://github.com/Ayman-muhammad/Scientific_computing-.git
cd Scientific_computing-

python -m venv .venv
source .venv/Scripts/activate

python -m pip install --upgrade pip
pip install -e ".[dev]"

python -m bit2118
pytest -v
ruff check src tests
```

These commands assume the corresponding package entry point, optional dependencies, and CLI configuration are present. If a command differs from the repository's actual configuration, follow the instructions in `README.md` and `pyproject.toml`.

## Expected evidence to record

After executing the commands, complete the following using actual output:

| Check | Recorded result |
|---|---|
| Python version | [Insert actual version] |
| Package installation | [Pass/fail] |
| Computational pipeline | [Actual success/failure summary] |
| Generated JSON files | [Actual count] |
| Generated figures | [Actual count] |
| Pytest | [Actual passed/failed/skipped counts] |
| Coverage | [Actual percentage, if measured] |
| Ruff | [Actual result] |
| GitHub Actions | [Actual workflow status and run] |

Do not replace these fields with anticipated results.

---

# Appendix B — Repository File Index

| Path | Purpose |
|---|---|
| `README.md` | Project overview and entry-point documentation |
| `pyproject.toml` | Package metadata, dependencies, and tool configuration |
| `requirements.txt` | Runtime dependencies |
| `requirements-dev.txt` | Development dependencies |
| `Makefile` | Common development commands |
| `src/bit2118/` | Numerical task implementations and shared utilities |
| `src/bit2118/__main__.py` | Package execution entry point |
| `src/bit2118/registry.py` | Task registration and dispatch |
| `src/bit2118/io_utils.py` | Result input/output utilities |
| `tests/` | Automated test suite |
| `tests/test_scientific_computing.py` | Scientific-computing verification tests |
| `docs/architecture.md` | Architectural rationale |
| `docs/mathematical_notes.md` | Mathematical derivations and notes |
| `docs/methodology.md` | Methodology and computational assumptions |
| `docs/reproducibility.md` | Reproduction guidance |
| `docs/tasks/` | Task-specific technical documentation |
| `report/report.md` | Supporting technical report |
| `report/figures/` | Location for generated figures |
| `results/` | Location for generated numerical results |
| `.github/workflows/ci.yml` | Continuous-integration workflow |

---

**End of Final Submission Report**

**Submission repository:** https://github.com/Ayman-muhammad/Scientific_computing-

**Student:** Ayman Muhammad  
**Course:** BIT 2118 — Scientific Computing  
**Submission date:** [Insert submission date]
