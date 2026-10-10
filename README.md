from pathlib import Path
import pypandoc

markdown = r"""# BIT 2118 — Scientific Computing
## Final Technical Submission Report

**Student:** Ayman Muhammad  
**Student ID:** BSCCS/2025/30137  
**Course:** BIT 2118 — Scientific Computing  
**Assignment:** Group Work — Tasks 02–20  
**Submission date:** 10 October 2026  
**GitHub repository:** https://github.com/Ayman-muhammad/Scientific_computing-  
**Branch:** `main`  
**Reference commit:** `ac9d7dc`  
**Release:** `v1.0.0` — create and verify this tag before describing it as a published release.

![Scientific computing: numerical analysis and data visualisation](https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=1600&q=85)

*Cover image: abstract mathematical visualisation. This is an illustrative image, not evidence of the project's numerical results.*

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
14. Appendix C — Figure Register

---

# 1. Executive Summary

Scientific computing is not simply the translation of mathematical formulae into Python. It is the disciplined application of numerical methods, computational algorithms, error analysis, verification, and interpretation to problems that may be difficult or impractical to solve analytically.

This project is organised around nineteen assignment tasks, spanning Task 02 through Task 20. The intended technical scope includes array computation, numerical stability, matrix algebra, linear systems, eigenvalue analysis, nonlinear root-finding, interpolation, regression, numerical calculus, ordinary differential equations, optimisation, and Monte Carlo simulation.

The implementation uses a modular Python architecture. Each task is represented by a dedicated computational module, while shared utilities handle filesystem paths, logging, JSON persistence, and task registration. Automated tests are intended to verify important mathematical properties and numerical results.

The central engineering principle is that **a numerical answer is not trustworthy merely because a program produces it**. Its correctness must be assessed using independent references, residuals, invariants, analytical solutions, convergence behaviour, or other appropriate verification criteria.

> **Evidence standard:** numerical values, timing measurements, test totals, coverage percentages, generated artefacts, and continuous-integration status must be confirmed by executing the current repository. The presence of a figure path in this report does not prove that the figure has been generated. The plots embedded below are expected output paths and must be checked against the files actually produced by the code.

## 1.1 Project objectives

The project aims to:

1. Implement the numerical techniques required by the assignment.
2. Identify the mathematical inputs, parameters, assumptions, and operations for each task.
3. Demonstrate parameter sensitivity by examining how numerical outputs change when inputs or algorithmic parameters change.
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
| Nonlinear equations | 10–12 | Bisection, fixed-point, Newton, secant, nonlinear systems |
| Approximation and regression | 13–14 | Interpolation, splines, least squares |
| Numerical calculus | 15–16 | Finite differences, quadrature |
| Differential equations | 17–18 | Euler integration, adaptive ODE solvers |
| Operations research and risk | 19–20 | Optimisation, Monte Carlo estimation |

The source code and supporting documentation are maintained in the public GitHub repository listed above.

---

# 2. Introduction and Objectives

## 2.1 Background

Scientific computing provides the computational machinery required to investigate mathematical models, approximate solutions, and interpret quantitative behaviour.

Many practical problems cannot be solved efficiently using elementary algebra alone. Examples include large linear systems, nonlinear equilibrium equations, parameter estimation, dynamical systems, and uncertainty analysis. Numerical methods address these problems by converting mathematical formulations into algorithms that can be executed, tested, and analysed.

However, numerical computation introduces its own difficulties. Finite-precision arithmetic can distort results; iterative algorithms may fail to converge; approximations introduce truncation error; and an apparently plausible output may still violate the governing equations.

Consequently, this assignment treats numerical computing as a combination of mathematical formulation, algorithm selection, computational implementation, error and convergence analysis, independent verification, and interpretation of results.

## 2.2 Objectives

**Objective A — Implementation:** develop computational modules for Tasks 02–20.

**Objective B — Parameter identification:** document the inputs, mathematical parameters, assumptions, and operations relevant to each task.

**Objective C — Sensitivity analysis:** investigate how selected inputs or numerical parameters affect accuracy, convergence, computational cost, or predicted outcomes.

**Objective D — Interpretation:** explain the meaning of numerical outputs and the information conveyed by relevant plots.

**Objective E — Application:** associate each numerical technique with an illustrative real-world problem.

**Objective F — Software engineering:** organise the implementation into reusable modules with shared infrastructure.

**Objective G — Reproducibility:** maintain the source code in version control and provide a documented procedure for rerunning the computations.

---

# 3. Repository Architecture

## 3.1 Directory structure

The repository uses a `src/`-based Python package layout.

```text
Scientific_computing-/
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

1. **Formulate the problem.** Identify the governing equations, variables, assumptions, and expected solution.
2. **Select the method.** Choose an algorithm appropriate to the problem's structure, accuracy requirements, and computational cost.
3. **Implement the computation.** Use Python and relevant scientific libraries.
4. **Evaluate the result.** Compute diagnostics such as residuals, errors, convergence histories, or feasibility checks.
5. **Interpret the output.** Relate the numerical result to the mathematical model and its illustrative application.
6. **Test and document.** Preserve the implementation, verification criteria, and reproduction procedure.

## 4.2 Mathematical verification

### Analytical comparison

When a closed-form solution exists, the numerical result can be compared against it. Newton's law of cooling, for example, has the analytical solution

\[
T(t)=T_{\mathrm{amb}}+(T_0-T_{\mathrm{amb}})e^{-kt}.
\]

A numerical approximation can be assessed using

\[
E_{\mathrm{abs}}=|T_{\mathrm{numerical}}-T_{\mathrm{exact}}|.
\]

### Residual analysis

For a linear system \(Ax=b\), the residual is

\[
r=b-Ax.
\]

A small residual indicates that the computed vector approximately satisfies the supplied equations. It does not, by itself, guarantee a small forward error if the system is ill-conditioned.

### Invariant checking

Mathematical properties provide independent checks. An eigenpair should satisfy

\[
Av=\lambda v,
\]

and a normalised probability vector should satisfy

\[
\sum_i p_i=1.
\]

### Convergence and feasibility

Iterative methods should be assessed for convergence and sensitivity to initial conditions or tolerances. Optimisation algorithms should be assessed against their constraints, objective function, and termination conditions.

A successful solver status is useful evidence, but it is not a substitute for checking the resulting solution.

## 4.3 Error and tolerance policy

| Problem type | Diagnostic | Interpretation |
|---|---|---|
| Linear systems | \(\|b-Ax\|\) | Equation-satisfaction error |
| Root finding | \(|f(x^\*)|\) and step size | Root residual and iteration behaviour |
| Eigenvalue computation | \(\|Av-\lambda v\|\) | Eigenpair consistency |
| ODE integration | Error against a reference | Approximation accuracy |
| Interpolation | Error at known points | Agreement with supplied data |
| Regression | RMSE and residual inspection | In-sample fit quality |
| Monte Carlo | Standard error or confidence interval | Sampling uncertainty |

A tolerance such as \(10^{-8}\) is not universally appropriate. The choice depends on scaling, conditioning, machine precision, and the consequences of error. For floating-point comparisons, tolerance-based checks such as `numpy.isclose` are generally more appropriate than exact equality.

---

# 5. Task-by-Task Technical Analysis

Each task is discussed in terms of its mathematical concept, computational approach, illustrative inputs, interpretation, and verification criteria. Numerical outputs must be checked against the actual generated results before being described as measured findings.

## Task 02 — NumPy Arrays

**Concept:** array construction, element-wise operations, and descriptive statistics.  
**Application:** hourly weather-station measurements.

Given temperatures \(C=[C_1,C_2,\ldots,C_n]\), the mean is

\[
\bar C=\frac{1}{n}\sum_{i=1}^{n}C_i.
\]

Conversion to Fahrenheit is

\[
F_i=\frac95C_i+32.
\]

NumPy applies this transformation element-wise without requiring an explicit Python loop. The mean, minimum, and maximum provide a basic summary of the temperature profile.

**Verification:** compare the array statistics against independently calculated values and confirm that each Fahrenheit value satisfies the conversion equation.

![Task 02 — weather observations and descriptive statistics](figures/task02_weather_statistics.png)

*Figure 1. Weather observations and descriptive statistics. Generate this figure from the same data used by Task 02; label the time axis and temperature units.*

## Task 03 — Vectorisation and Performance

**Concept:** replacing repeated Python-level operations with array-oriented computation.  
**Application:** network-latency analysis using synthetic observations.

Performance can be assessed using

\[
S=\frac{t_{\mathrm{loop}}}{t_{\mathrm{vectorised}}},
\]

where \(S\) is the measured speed-up. Vectorisation can reduce interpreter overhead, but the benefit depends on data size, memory access, operation, and hardware.

**Verification:** compare output arrays within an appropriate tolerance and measure both implementations under comparable conditions.

![Task 03 — loop and vectorised execution times](figures/task03_vectorization_benchmark.png)

*Figure 2. Runtime comparison between loop-based and vectorised computation. Report the measurement procedure, array size, and execution environment.*

## Task 04 — Floating-Point Arithmetic

**Concept:** finite-precision representation, rounding error, and numerical stability.

An expression such as `0.1 + 0.2` may produce `0.30000000000000004` because most decimal fractions cannot be represented exactly in binary floating-point.

For small \(x\), the expression

\[
\sqrt{1+x}-1
\]

may suffer cancellation. Rationalisation gives

\[
\sqrt{1+x}-1=\frac{x}{\sqrt{1+x}+1}.
\]

**Verification:** compare both expressions against a higher-precision reference over a range of \(x\) values and measure absolute and relative errors.

![Task 04 — floating-point cancellation and numerical error](figures/task04_floating_point_error.png)

*Figure 3. Numerical error across input magnitudes. State the reference computation and error metric used.*

## Task 05 — Matrix Algebra and Geometric Transformations

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
S=\begin{bmatrix}s_x&0\\0&s_y\end{bmatrix}.
\]

For scaling followed by rotation, the composite transformation is \(T=RS\). Since \(\det(R)=1\), rotation preserves area, whereas scaling changes area by \(|s_xs_y|\).

**Verification:** test determinant identities and compare transformed coordinates against direct calculations. State the order of matrix multiplication because matrix multiplication is generally noncommutative.

![Task 05 — original and transformed coordinates](figures/task05_matrix_transformations.png)

*Figure 4. Original geometry and its transformed coordinates. Label the original and transformed shapes and state the rotation angle and scaling factors.*

## Task 06 — Solving Linear Systems

For a system \(Ax=b\), a numerical solver computes an approximate solution \(x\). The residual is

\[
r=b-Ax.
\]

A solution is operationally valid only if it also satisfies application constraints. For example, fractional server counts are not valid if the variables represent indivisible machines.

**Verification:** calculate the residual and check the original equations, non-negativity, and integrality where required.

![Task 06 — resource allocation solution](figures/task06_linear_system.png)

*Figure 5. Resource-allocation inputs and computed solution. Include the equations or resource constraints used in the calculation.*

## Task 07 — LU Decomposition

For a suitable square matrix, LU decomposition expresses

\[
PA=LU,
\]

where \(P\) is a permutation matrix, \(L\) is lower triangular, and \(U\) is upper triangular. Reusing the factorisation is efficient when several right-hand sides share the same coefficient matrix.

**Verification:** compare solutions against a trusted direct solver and evaluate residuals for every right-hand side. Consider pivoting and matrix conditioning when interpreting accuracy.

![Task 07 — repeated linear-system solves](figures/task07_lu_reuse.png)

*Figure 6. Solutions obtained using a reused LU factorisation. Use measured results from the implementation; do not imply a speed-up unless it was benchmarked.*

## Task 08 — Iterative Linear Solvers

A discretised heat-conduction problem can be expressed as \(Ax=b\). Jacobi iteration uses values from the previous iteration; Gauss–Seidel uses newly computed values immediately within the current sweep.

Strict diagonal dominance is a useful sufficient convergence condition in many cases, but convergence must not be assumed for every matrix. Gauss–Seidel may converge in fewer iterations for a particular problem, but this is not universal.

**Verification:** record the residual or iteration error, check the stopping criterion, and compare against a direct solution.

![Task 08 — Jacobi and Gauss–Seidel convergence](figures/task08_iterative_convergence.png)

*Figure 7. Convergence history for Jacobi and Gauss–Seidel. The vertical axis must specify the residual norm or error measure.*

## Task 09 — Eigenvalues and Eigenvectors

An eigenvalue \(\lambda\) and corresponding nonzero eigenvector \(v\) satisfy

\[
Av=\lambda v.
\]

For an adjacency matrix, the dominant eigenvector can be used to define eigenvector centrality, subject to the assumptions of the selected centrality model.

**Verification:** calculate the eigenpair residual and check centrality normalisation. The dominant eigenvector should not be described as universally equivalent to PageRank.

![Task 09 — network and eigenvector centrality](figures/task09_network_centrality.png)

*Figure 8. Network structure with node sizes or labels derived from computed centrality values.*

## Task 10 — Bisection and Fixed-Point Iteration

For the illustrative equilibrium model

\[
f(T)=T-25-10e^{-T/20},
\]

the objective is to find \(T^\*\) such that \(f(T^\*)=0\). Bisection retains a root-containing bracket when endpoint values have opposite signs. Fixed-point iteration uses \(T_{n+1}=g(T_n)\) and depends on the mapping's convergence behaviour.

**Verification:** evaluate the residuals and confirm that the initial interval satisfies the sign-change condition.

![Task 10 — nonlinear function and computed root](figures/task10_root_finding.png)

*Figure 9. Function curve with the estimated root and search interval marked.*

## Task 11 — Newton and Secant Methods

Newton's method uses

\[
x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}.
\]

The secant method estimates the derivative from two previous approximations. An internal rate of return is a root of

\[
\operatorname{NPV}(r)=\sum_{t=0}^{n}\frac{CF_t}{(1+r)^t}=0.
\]

Newton's method can converge rapidly near a suitable root but is sensitive to initial guesses and derivative behaviour. The secant method avoids explicit derivative calculation but is not guaranteed to converge in every case.

**Verification:** evaluate the objective at the estimated root and consider whether multiple economically meaningful roots exist.

![Task 11 — NPV against discount rate](figures/task11_irr_npv.png)

*Figure 10. Net present value against discount rate. Mark the estimated root and report the cash-flow assumptions.*

## Task 12 — Nonlinear Systems

Consider

\[
x^2+y^2=4,\qquad y=x^2-1.
\]

The equations describe a circle and a parabola. A vector-valued residual is

\[
F(x,y)=
\begin{bmatrix}
x^2+y^2-4\\
y-x^2+1
\end{bmatrix}.
\]

Nonlinear systems may have multiple solutions, and the solver's output can depend on its initial estimate.

**Verification:** substitute every candidate solution into both equations and inspect the residual vector.

![Task 12 — circle and parabola intersections](figures/task12_nonlinear_intersections.png)

*Figure 11. Circle and parabola with candidate intersection points. Check every candidate against both equations.*

## Task 13 — Interpolation

Linear interpolation between \((x_0,y_0)\) and \((x_1,y_1)\) is

\[
y(x)=y_0+\frac{x-x_0}{x_1-x_0}(y_1-y_0).
\]

Cubic splines use piecewise cubic polynomials with continuity constraints. Smoothness does not guarantee greater accuracy; the suitability of an interpolant depends on the data and underlying process.

**Verification:** confirm that the interpolant reproduces supplied data at the knots and compare against a known reference or held-out observations when available.

![Task 13 — samples and interpolation curves](figures/task13_interpolation.png)

*Figure 12. Observed samples and interpolated values. Distinguish measured points from estimated values.*

## Task 14 — Curve Fitting

For a quadratic model \(y=ax^2+bx+c\), coefficients can be estimated by minimising

\[
\operatorname{SSE}=\sum_{i=1}^{n}(y_i-\hat y_i)^2.
\]

The root-mean-square error is

\[
\operatorname{RMSE}=\sqrt{\frac1n\sum_{i=1}^{n}(y_i-\hat y_i)^2}.
\]

A quadratic model may describe response-time growth over a limited range, but extrapolation requires justification.

**Verification:** calculate residuals and RMSE, inspect the fit graph, and compare predictions against independent data where possible.

![Task 14 — measured response times and fitted curve](figures/task14_regression.png)

*Figure 13. Observed server response times and the fitted model. State the RMSE and distinguish observations from predictions.*

## Task 15 — Numerical Differentiation

The forward-difference approximation is

\[
f'(x)\approx\frac{f(x+h)-f(x)}{h},
\]

and the central-difference approximation is

\[
f'(x)\approx\frac{f(x+h)-f(x-h)}{2h}.
\]

For smooth functions, the forward difference has first-order truncation error and the central difference has second-order truncation error under standard assumptions.

**Application:** estimating speed from GPS position samples. Measurement noise, boundary treatment, and step size affect the derivative estimate.

**Verification:** test against a known function with an analytical derivative and inspect units and noise sensitivity.

![Task 15 — GPS position and estimated speed](figures/task15_gps_speed.png)

*Figure 14. Position samples and estimated speed. Label distance and time units.*

## Task 16 — Numerical Integration

The trapezoidal rule approximates

\[
\int_a^b f(x)\,dx
\approx\sum_{i=0}^{n-1}\frac{x_{i+1}-x_i}{2}(f_i+f_{i+1}).
\]

For power \(P(t)\), energy is

\[
E=\int_{t_0}^{t_1}P(t)\,dt.
\]

When power is measured in kilowatts and time in hours, energy is measured in kilowatt-hours. Agreement between two quadrature rules is informative but does not by itself prove accuracy.

**Verification:** compare against a known integral and ensure units and sampling intervals are handled correctly.

![Task 16 — power observations and integrated energy](figures/task16_energy_integration.png)

*Figure 15. Power over time; the area under the curve represents estimated energy consumption.*

## Task 17 — Euler's Method

For Newton's law of cooling,

\[
\frac{dT}{dt}=-k(T-T_{\mathrm{amb}}),\qquad T(0)=T_0,
\]

explicit Euler integration gives

\[
T_{n+1}=T_n-hk(T_n-T_{\mathrm{amb}}).
\]

The exact solution is

\[
T(t)=T_{\mathrm{amb}}+(T_0-T_{\mathrm{amb}})e^{-kt}.
\]

Euler's method is simple and useful for understanding time stepping. Its global error is generally first-order in \(h\) for sufficiently smooth problems over a fixed interval, provided the method remains stable.

**Verification:** compare numerical temperatures against the analytical solution at matching time points and repeat with smaller step sizes.

![Task 17 — Euler approximation and exact cooling solution](figures/task17_newton_cooling.png)

*Figure 16. Euler approximations compared with the analytical cooling solution.*

## Task 18 — SciPy ODE Integration

For an RC charging circuit,

\[
\frac{dV_C}{dt}=\frac{V_s-V_C}{RC}.
\]

For constant supply voltage and zero initial capacitor voltage,

\[
V_C(t)=V_s(1-e^{-t/(RC)}).
\]

An adaptive solver such as SciPy's `solve_ivp` adjusts integration steps according to the selected method and error tolerances.

**Verification:** compare the numerical solution with the analytical curve, inspect solver status, and evaluate maximum absolute error at defined comparison points.

![Task 18 — numerical and analytical RC charging curves](figures/task18_rc_charging.png)

*Figure 17. Capacitor voltage during RC charging. Include the solver method and tolerances in the caption or surrounding text.*

## Task 19 — Optimisation

A generic optimisation problem is

\[
\min_x c^\mathsf{T}x
\quad\text{subject to}\quad Ax\ge b,\quad x\ge0.
\]

If decision variables represent indivisible resources, integer constraints may be required. A continuous relaxation may provide a lower bound on the corresponding integer minimisation problem when the relaxation is valid.

**Verification:** evaluate the objective, check all constraints, confirm variable domains, and report solver termination status.

![Task 19 — feasible capacity and cost comparison](figures/task19_capacity_optimisation.png)

*Figure 18. Feasible resource allocations and their costs. Highlight the selected solution and capacity requirement.*

## Task 20 — Monte Carlo Simulation

Suppose demand follows \(D\sim\mathcal N(\mu,\sigma^2)\), and overload occurs when \(D>C\). The Monte Carlo estimator is

\[
\hat p=\frac1N\sum_{i=1}^{N}\mathbf1(D_i>C).
\]

For the normal model, the analytical comparison is

\[
p=P(D>C)=1-\Phi\left(\frac{C-\mu}{\sigma}\right).
\]

The approximate standard error is

\[
\operatorname{SE}(\hat p)\approx
\sqrt{\frac{\hat p(1-\hat p)}{N}}.
\]

Sampling uncertainty decreases at a rate proportional to \(N^{-1/2}\). Reducing the error scale by a factor of ten typically requires about one hundred times as many independent samples under comparable conditions.

**Verification:** compare the estimate with the analytical probability, calculate a sampling-uncertainty measure, and record the random seed.

![Task 20 — demand distribution and overload threshold](figures/task20_monte_carlo.png)

*Figure 19. Simulated demand distribution with the overload threshold marked. Report the estimated probability and its uncertainty.*

---

# 6. Parameter Sensitivity Analysis

Sensitivity analysis examines how a computational result responds to changes in inputs, assumptions, or algorithmic parameters.

## 6.1 Task 17 — Euler step-size sensitivity

For a fixed final time, reducing the time step \(h\) increases the number of steps but generally reduces global discretisation error for a sufficiently smooth problem in the stable regime.

A controlled experiment should:

1. Fix initial temperature, ambient temperature, cooling constant, and final time.
2. Compute the analytical solution at the final time.
3. Run Euler integration using \(h\) and \(h/2\).
4. Calculate absolute error for each run.
5. Compare the error ratio

\[
R=\frac{E(h)}{E(h/2)}.
\]

For a method operating in its first-order convergence regime, \(R\) is expected to approach approximately \(2\) as the step size becomes sufficiently small.

![Task 17 — Euler error against step size](figures/task17_step_size_sensitivity.png)

*Figure 20. Absolute Euler error for multiple step sizes. A log–log plot can help assess the observed convergence order.*

## 6.2 Task 20 — Monte Carlo sample-size sensitivity

Keep the demand model and capacity threshold fixed while changing the sample count, for example from \(N=1{,}000\) to \(N=100{,}000\). Increasing \(N\) generally reduces the standard error according to

\[
\operatorname{SE}(\hat p)\propto N^{-1/2}.
\]

A hundredfold increase in sample count therefore reduces the theoretical standard-error scale by approximately a factor of ten, provided the assumptions remain unchanged.

![Task 20 — Monte Carlo estimate against sample size](figures/task20_sample_size_sensitivity.png)

*Figure 21. Estimated overload probability and an uncertainty interval as sample size increases.*

## 6.3 Sensitivity dimensions for the remaining tasks

| Task | Example parameter | Quantity to examine |
|---|---|---|
| 02 | Input observations | Mean, range, transformed values |
| 03 | Array length | Runtime and speed-up |
| 04 | Magnitude of \(x\) | Floating-point error |
| 05 | Rotation angle or scale | Coordinates and determinant |
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

These are proposed experimental dimensions. Claim that a task has been experimentally varied only after the corresponding runs and outputs have been recorded.

---

# 7. Verification and Validation

## 7.1 Verification strategy

Verification asks whether the implementation correctly performs the intended numerical computation. Validation asks whether the mathematical model and its assumptions adequately represent the problem being investigated.

A Monte Carlo program may correctly estimate the overload probability of a normal distribution while the normal demand model remains inappropriate for a real system. Likewise, a regression algorithm may correctly minimise squared error without establishing that its fitted model predicts future observations reliably.

## 7.2 Verification matrix

| Task | Verification criterion |
|---|---|
| 02 | Statistics agree with independently computed values |
| 03 | Loop and vectorised outputs agree within tolerance |
| 04 | Floating-point behaviour agrees with expected error analysis |
| 05 | Transformation and determinant identities hold |
| 06 | Linear-system residual is acceptably small |
| 07 | LU solutions agree with an independent direct solver |
| 08 | Iterative results satisfy the system and stopping criterion |
| 09 | Eigenpair residual is small and normalisation is valid |
| 10 | Root residuals are small and bracketing assumptions hold |
| 11 | Root residual and iteration termination are checked |
| 12 | Each nonlinear solution satisfies every equation |
| 13 | Interpolants reproduce the data at the knots |
| 14 | Residuals and RMSE are computed correctly |
| 15 | Finite differences agree with an analytical derivative in a known case |
| 16 | Quadrature agrees with a known integral in a controlled test |
| 17 | Euler solution is compared with the exact cooling curve |
| 18 | ODE solution is compared with the analytical RC solution |
| 19 | Objective, constraints, and variable domains are checked |
| 20 | Monte Carlo estimate is compared with an analytical probability |

## 7.3 Automated testing

Run the test suite:

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

Record the actual test summary and coverage output from the current codebase. Do not substitute an expected number of passing tests for the test runner's measured output.

## 7.4 Continuous integration

The repository contains a GitHub Actions workflow at `.github/workflows/ci.yml`. Inspect the workflow to establish which Python versions, dependency configurations, lint rules, and tests it covers.

A workflow file is evidence that automation has been configured; a successful run is evidence that the configured checks passed.

---

# 8. Reproducibility and Execution

Reproducibility allows another person to recreate computational results using the same source code, inputs, dependencies, and relevant execution settings.

## 8.1 Environment setup

The following commands illustrate a Windows Git Bash setup:

```bash
git clone https://github.com/Ayman-muhammad/Scientific_computing-.git
cd Scientific_computing-

python -m venv .venv
source .venv/Scripts/activate

python -m pip install --upgrade pip
pip install -e ".[dev]"
```

The editable installation command assumes that `pyproject.toml` defines the package and a development dependency group named `dev`. If the actual configuration differs, use the installation instructions in `README.md` and `pyproject.toml`.

## 8.2 Execute the computational pipeline

If the package entry point is configured to run all registered tasks:

```bash
python -m bit2118
```

Check `src/bit2118/__main__.py` and the task registry to confirm the command's actual behaviour.

Then run:

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

Confirm the actual number and names of generated JSON files and figures. Some generated outputs may be excluded from Git by `.gitignore` because they can be reproduced from source code.

## 8.4 Reproducibility limitations

- **Procedural reproducibility:** another user can follow the documented steps.
- **Numerical reproducibility:** results agree within a defined tolerance.
- **Bitwise reproducibility:** output bytes are identical.

Bitwise reproducibility is stricter than numerical reproducibility. Timestamps, dependency changes, floating-point behaviour, library versions, and output ordering can cause files to differ even when scientific conclusions are equivalent.

For stochastic tasks, record the seed and generator configuration. For performance measurements, record the machine, Python version, library versions, and measurement procedure.

---

# 9. Critical Reflection and Learning Outcomes

## 9.1 Numerical reasoning

A mathematical expression and its implementation are not automatically equivalent in finite-precision arithmetic. Floating-point representation, conditioning, cancellation, and truncation error all influence computational accuracy. Algorithm selection therefore requires consideration of both mathematical validity and numerical behaviour.

## 9.2 Algorithm selection

Bisection prioritises robust bracketing. Newton's method can converge rapidly when its assumptions are favourable. The secant method avoids explicit derivative evaluation but remains sensitive to the problem and starting estimates.

No single method is optimal for every nonlinear equation. Selection depends on available information, convergence requirements, and acceptable failure modes.

## 9.3 Computational efficiency

Vectorisation and reusable matrix factorisation demonstrate that performance improvements often come from selecting the right computational structure rather than merely writing more code.

The relevant question is not simply whether an implementation is fast. It is whether it balances speed, memory use, accuracy, clarity, and maintainability.

## 9.4 Verification as part of implementation

Residuals, analytical references, invariants, convergence diagnostics, and constraint checks provide independent evidence about correctness. Testing should be treated as part of the scientific method, not as a final administrative step.

## 9.5 Reproducible software engineering

The `src/` package layout, shared utilities, documentation, version control, and automated tests establish a foundation for maintainable scientific software. A well-structured repository enables reviewers to inspect methods and independently reproduce experiments.

---

# 10. Limitations and Future Improvements

## 10.1 Model limitations

Illustrative applications simplify complex systems. A quadratic response-time model may describe a limited observed range but fail under substantially different workloads. A normal demand distribution may underestimate risk if actual demand has heavy tails.

Model assumptions must be assessed separately from numerical correctness.

## 10.2 Numerical limitations

Iterative methods may depend on initial estimates, matrix conditioning, step sizes, or stopping tolerances. Small residuals do not always imply small solution errors, particularly for ill-conditioned problems.

## 10.3 Statistical limitations

Monte Carlo estimates have sampling uncertainty. Regression estimates may be affected by outliers, correlated errors, and extrapolation. A single simulation or training-error statistic is insufficient to establish general predictive performance.

## 10.4 Future development

1. Add convergence-rate experiments for iterative solvers.
2. Expand tests to cover ill-conditioned and degenerate inputs.
3. Add uncertainty intervals to Monte Carlo estimates.
4. Evaluate fitted models using held-out data.
5. Record execution time and numerical error systematically.
6. Pin or lock dependencies for more controlled environments.
7. Extend continuous integration to additional operating systems where practical.
8. Improve reporting so generated figures, numerical summaries, and test results can be reproduced consistently.

---

# 11. Conclusion

This assignment brings together nineteen scientific-computing tasks covering a broad range of numerical techniques. The central challenge is not merely implementing algorithms, but understanding their assumptions, evaluating their numerical behaviour, and determining whether their outputs are trustworthy.

Array computation demonstrates the value of vectorised operations. Floating-point analysis shows why finite precision matters. Linear algebra and spectral methods reveal the importance of residuals and invariants. Root-finding and differential-equation solvers illustrate the relationship between convergence, stability, and accuracy. Interpolation, regression, optimisation, and Monte Carlo simulation demonstrate how numerical methods support approximation and decision-making.

The modular package structure provides a foundation for maintaining implementations and reproducing experiments. Tests, documentation, and version-controlled source code support independent review.

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

## Evidence to record

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
| `report/figures/` | Generated figures referenced by this report |
| `results/` | Generated numerical results |
| `.github/workflows/ci.yml` | Continuous-integration workflow |

---

# Appendix C — Figure Register

The following figure files are referenced in this report. These names are a reporting convention; the actual figure-generation code must save the files to the corresponding paths or the Markdown references must be updated.

| Figure | Expected file |
|---|---|
| 1 | `report/figures/task02_weather_statistics.png` |
| 2 | `report/figures/task03_vectorization_benchmark.png` |
| 3 | `report/figures/task04_floating_point_error.png` |
| 4 | `report/figures/task05_matrix_transformations.png` |
| 5 | `report/figures/task06_linear_system.png` |
| 6 | `report/figures/task07_lu_reuse.png` |
| 7 | `report/figures/task08_iterative_convergence.png` |
| 8 | `report/figures/task09_network_centrality.png` |
| 9 | `report/figures/task10_root_finding.png` |
| 10 | `report/figures/task11_irr_npv.png` |
| 11 | `report/figures/task12_nonlinear_intersections.png` |
| 12 | `report/figures/task13_interpolation.png` |
| 13 | `report/figures/task14_regression.png` |
| 14 | `report/figures/task15_gps_speed.png` |
| 15 | `report/figures/task16_energy_integration.png` |
| 16 | `report/figures/task17_newton_cooling.png` |
| 17 | `report/figures/task18_rc_charging.png` |
| 18 | `report/figures/task19_capacity_optimisation.png` |
| 19 | `report/figures/task20_monte_carlo.png` |
| 20 | `report/figures/task17_step_size_sensitivity.png` |
| 21 | `report/figures/task20_sample_size_sensitivity.png` |

**Figure integrity rule:** do not create artificial plots merely to satisfy this list. Generate each figure from the corresponding task implementation and actual input data. If a task does not yet produce a figure, implement and verify that output or remove the corresponding image reference before submission.

---

**End of Final Submission Report**

**Submission repository:** https://github.com/Ayman-muhammad/Scientific_computing-

**Student:** Ayman Muhammad  
**Course:** BIT 2118 — Scientific Computing  
**Submission date:** 10 October 2026
"""

output_path = Path("/mnt/data/FINAL_SUBMISSION.md")
pypandoc.convert_text(
    markdown,
    to="md",
    format="md",
    outputfile=str(output_path),
    extra_args=["--standalone"],
)
print(f"Created: {output_path}")
print(f"Markdown characters: {len(markdown):,}")
print(f"Embedded task/sensitivity figures: {markdown.count('![')}")
