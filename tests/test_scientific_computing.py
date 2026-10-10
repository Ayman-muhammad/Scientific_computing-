"""Numerical-correctness tests for every task module (02 → 20).

Each test asserts a **specific mathematical claim** about a task's
output — a closed-form value, a residual bound, an invariant, or an
order-of-magnitude property — rather than merely that the module runs.
Failures therefore point to a concrete assertion and a concrete number.
"""

from __future__ import annotations

import numpy as np
import pytest
from scipy import stats

from bit2118 import (
    task02_numpy_arrays as t02,
)
from bit2118 import (
    task03_vectorization as t03,
)
from bit2118 import (
    task04_floating_point as t04,
)
from bit2118 import (
    task05_matrix_algebra as t05,
)
from bit2118 import (
    task06_linear_systems as t06,
)
from bit2118 import (
    task07_gaussian_lu as t07,
)
from bit2118 import (
    task08_iterative_linear as t08,
)
from bit2118 import (
    task09_eigenvalues as t09,
)
from bit2118 import (
    task10_bisection_fixed_point as t10,
)
from bit2118 import (
    task11_newton_secant as t11,
)
from bit2118 import (
    task12_nonlinear_equations as t12,
)
from bit2118 import (
    task13_interpolation as t13,
)
from bit2118 import (
    task14_curve_fitting as t14,
)
from bit2118 import (
    task15_numerical_differentiation as t15,
)
from bit2118 import (
    task16_numerical_integration as t16,
)
from bit2118 import (
    task17_euler_ode as t17,
)
from bit2118 import (
    task18_scipy_ode as t18,
)
from bit2118 import (
    task19_optimization as t19,
)
from bit2118 import (
    task20_monte_carlo as t20,
)


# =============================================================================
# Task 02 — NumPy arrays
# =============================================================================
class TestTask02:
    def test_reading_count(self) -> None:
        assert t02.TEMPERATURES_C.size == 24

    def test_conversion_endpoints(self) -> None:
        f = t02.celsius_to_fahrenheit(np.array([0.0, 100.0]))
        assert np.allclose(f, [32.0, 212.0])

    def test_statistics_are_consistent(self) -> None:
        mean, lo, hi = t02.daily_statistics(t02.TEMPERATURES_C)
        assert lo <= mean <= hi
        assert np.isclose(mean, float(np.mean(t02.TEMPERATURES_C)))


# =============================================================================
# Task 03 — Vectorisation
# =============================================================================
class TestTask03:
    def test_vectorized_matches_loop(self) -> None:
        rng = np.random.default_rng(0)
        sample = rng.uniform(5.0, 250.0, 1_000)
        assert np.allclose(
            t03.vectorized_version(sample),
            np.array(t03.loop_version(sample)),
        )

    def test_samples_in_requested_range(self) -> None:
        s = t03.make_samples(500)
        assert s.size == 500
        assert s.min() >= t03.LATENCY_MIN_MS
        assert s.max() <= t03.LATENCY_MAX_MS


# =============================================================================
# Task 04 — Floating point
# =============================================================================
class TestTask04:
    def test_absolute_and_relative_error(self) -> None:
        assert np.isclose(t04.absolute_error(2.0, 1.5), 0.5)
        assert np.isclose(t04.relative_error(2.0, 1.5), 0.25)

    def test_relative_error_zero_input_raises(self) -> None:
        with pytest.raises(ZeroDivisionError):
            t04.relative_error(0.0, 0.5)

    @pytest.mark.parametrize("x", [1e-4, 1e-8, 1e-12])
    def test_stable_form_matches_unstable(self, x: float) -> None:
        assert np.isclose(
            t04.stable_sqrt_identity(x),
            t04.unstable_sqrt_identity(x),
            rtol=1e-4,
            atol=1e-12,
        )


# =============================================================================
# Task 05 — Matrix algebra
# =============================================================================
class TestTask05:
    def test_rotation_preserves_norm(self) -> None:
        p = np.array([[1.0, 0.0]])
        r = t05.rotation_matrix(np.deg2rad(30.0))
        rotated = p @ r.T
        assert np.isclose(np.linalg.norm(rotated), 1.0)

    def test_rotation_is_orthogonal(self) -> None:
        r = t05.rotation_matrix(0.7)
        assert np.allclose(r @ r.T, np.eye(2), atol=1e-12)

    def test_determinant_of_combined_transform(self) -> None:
        r = t05.rotation_matrix(0.4)
        s = t05.scaling_matrix(2.0, 1.5)
        assert np.isclose(np.linalg.det(r @ s), 2.0 * 1.5)


# =============================================================================
# Task 06 — Linear systems
# =============================================================================
class TestTask06:
    def test_solution_satisfies_system(self) -> None:
        x, residual = t06.solve_system(t06.A, t06.B)
        assert np.allclose(t06.A @ x, t06.B)
        assert np.linalg.norm(residual) < 1e-10

    def test_singular_matrix_raises(self) -> None:
        singular = np.array([[1.0, 2.0], [2.0, 4.0]])
        rhs = np.array([1.0, 2.0])
        with pytest.raises(np.linalg.LinAlgError):
            t06.solve_system(singular, rhs)


# =============================================================================
# Task 07 — LU decomposition
# =============================================================================
class TestTask07:
    def test_lu_solution_matches_direct(self) -> None:
        rows = t07.solve_all(t07.A, t07.MEASUREMENT_SETS)
        direct = np.linalg.solve(t07.A, t07.MEASUREMENT_SETS[0])
        assert np.allclose(rows[0]["solution"], direct)

    def test_every_residual_is_small(self) -> None:
        rows = t07.solve_all(t07.A, t07.MEASUREMENT_SETS)
        for row in rows:
            assert row["residual_norm"] < 1e-10

    def test_all_measurement_sets_processed(self) -> None:
        rows = t07.solve_all(t07.A, t07.MEASUREMENT_SETS)
        assert len(rows) == len(t07.MEASUREMENT_SETS)
        assert [r["set"] for r in rows] == [1, 2, 3]


# =============================================================================
# Task 08 — Iterative solvers
# =============================================================================
class TestTask08:
    def test_jacobi_and_gauss_seidel_agree_with_direct(self) -> None:
        x_j, _ = t08.jacobi(t08.A, t08.B)
        x_gs, _ = t08.gauss_seidel(t08.A, t08.B)
        x_exact = np.linalg.solve(t08.A, t08.B)
        assert np.allclose(x_j, x_exact, atol=1e-6)
        assert np.allclose(x_gs, x_exact, atol=1e-6)

    def test_gauss_seidel_converges_faster(self) -> None:
        _, err_j = t08.jacobi(t08.A, t08.B)
        _, err_gs = t08.gauss_seidel(t08.A, t08.B)
        assert len(err_gs) <= len(err_j)

    def test_errors_are_monotone_eventually(self) -> None:
        _, err_gs = t08.gauss_seidel(t08.A, t08.B)
        tail = np.asarray(err_gs[2:])
        assert np.all(np.diff(tail) <= 0.0)


# =============================================================================
# Task 09 — Eigenvalues
# =============================================================================
class TestTask09:
    def test_centrality_is_normalised(self) -> None:
        _, centrality, _ = t09.eigenvector_centrality(t09.ADJACENCY)
        assert np.isclose(centrality.sum(), 1.0)

    def test_eigenpair_verification(self) -> None:
        _, _, err = t09.eigenvector_centrality(t09.ADJACENCY)
        assert err < 1e-8

    def test_symmetric_matrix_gives_real_dominant(self) -> None:
        dominant, _, _ = t09.eigenvector_centrality(t09.ADJACENCY)
        assert np.isreal(dominant)
        assert dominant > 0


# =============================================================================
# Task 10 — Bisection & fixed point
# =============================================================================
class TestTask10:
    def test_bisection_and_fixed_point_agree(self) -> None:
        from scipy.optimize import root_scalar

        bisect = root_scalar(t10.heat_balance, bracket=[20.0, 40.0], method="bisect")
        fp, _ = t10.fixed_point_iteration(30.0)
        assert np.isclose(bisect.root, fp, atol=1e-6)

    def test_root_makes_residual_zero(self) -> None:
        from scipy.optimize import root_scalar

        bisect = root_scalar(t10.heat_balance, bracket=[20.0, 40.0], method="bisect")
        assert abs(t10.heat_balance(bisect.root)) < 1e-8

    def test_fixed_point_returns_full_history(self) -> None:
        root, history = t10.fixed_point_iteration(30.0)
        assert history[0] == 30.0
        assert history[-1] == root
        assert len(history) >= 2


# =============================================================================
# Task 11 — Newton & secant
# =============================================================================
class TestTask11:
    def test_npv_analytic_at_known_rate(self) -> None:
        assert np.isclose(t11.npv(0.0), sum(t11.CASH_FLOWS))

    def test_newton_converges_to_zero_npv(self) -> None:
        from scipy.optimize import root_scalar

        sol = root_scalar(t11.npv, fprime=t11.d_npv, x0=0.10, method="newton")
        assert abs(t11.npv(sol.root)) < 1e-9
        assert 0.0 < sol.root < 1.0

    def test_secant_agrees_with_newton(self) -> None:
        from scipy.optimize import root_scalar

        newton = root_scalar(t11.npv, fprime=t11.d_npv, x0=0.10, method="newton")
        secant = root_scalar(t11.npv, x0=0.05, x1=0.20, method="secant")
        assert np.isclose(newton.root, secant.root, atol=1e-9)


# =============================================================================
# Task 12 — Nonlinear systems
# =============================================================================
class TestTask12:
    def test_all_roots_satisfy_both_equations(self) -> None:
        rows = t12.find_intersections()
        for row in rows:
            for residual in row["residuals"]:
                assert abs(residual) < 1e-8

    def test_solver_reports_success(self) -> None:
        for row in t12.find_intersections():
            assert row["converged"] is True

    def test_two_distinct_intersections(self) -> None:
        rows = t12.find_intersections()
        sols = np.array([row["solution"] for row in rows])
        assert sols.shape == (2, 2)
        assert np.isclose(sols[0, 0], -sols[1, 0], atol=1e-6)


# =============================================================================
# Task 13 — Interpolation
# =============================================================================
class TestTask13:
    def test_interpolators_match_at_knots(self) -> None:
        linear, cubic = t13.build_interpolators(t13.HOURS, t13.TEMPERATURE)
        assert np.allclose(linear(t13.HOURS), t13.TEMPERATURE)
        assert np.allclose(cubic(t13.HOURS), t13.TEMPERATURE)

    def test_estimates_at_midpoint_are_plausible(self) -> None:
        linear, cubic = t13.build_interpolators(t13.HOURS, t13.TEMPERATURE)
        assert 22.0 <= float(linear(10.5)) <= 24.0
        assert 22.0 <= float(cubic(10.5)) <= 24.0

    def test_grid_includes_endpoints(self) -> None:
        grid = t13.build_dense_grid(0.0, 1.0, 0.1)
        assert grid[0] == pytest.approx(0.0)
        assert grid[-1] == pytest.approx(1.0)


# =============================================================================
# Task 14 — Curve fitting
# =============================================================================
class TestTask14:
    def test_model_evaluates_elementwise(self) -> None:
        y = t14.model(np.array([0.0, 1.0, 2.0]), 1.0, 2.0, 3.0)
        assert np.allclose(y, [3.0, 6.0, 11.0])

    def test_fit_achieves_low_rmse(self) -> None:
        from scipy.optimize import curve_fit

        params, _ = curve_fit(t14.model, t14.USERS, t14.RESPONSE_MS)
        predicted = t14.model(t14.USERS, *params)
        rmse = float(np.sqrt(np.mean((t14.RESPONSE_MS - predicted) ** 2)))
        assert rmse < 10.0

    def test_fitted_quadratic_is_convex(self) -> None:
        from scipy.optimize import curve_fit

        params, _ = curve_fit(t14.model, t14.USERS, t14.RESPONSE_MS)
        assert params[0] > 0.0


# =============================================================================
# Task 15 — Numerical differentiation
# =============================================================================
class TestTask15:
    def test_speed_matches_known_linear_case(self) -> None:
        t = np.array([0.0, 1.0, 2.0, 3.0])
        x = np.array([0.0, 5.0, 10.0, 15.0])
        v = t15.numerical_speed(t, x)
        assert np.allclose(v, 5.0)

    def test_speed_nonnegative_for_monotone_position(self) -> None:
        v = t15.numerical_speed(t15.TIME, t15.POSITION)
        assert np.all(v >= 0.0)

    def test_shape_mismatch_raises(self) -> None:
        with pytest.raises(ValueError):
            t15.numerical_speed(np.array([0.0, 1.0]), np.array([0.0, 1.0, 2.0]))


# =============================================================================
# Task 16 — Numerical integration
# =============================================================================
class TestTask16:
    def test_constant_power_matches_analytic(self) -> None:
        time = np.array([0.0, 1.0, 2.0, 3.0])
        power = np.full_like(time, 2.0)
        trap = float(np.trapezoid(power, time))
        sim = float(__import__("scipy.integrate", fromlist=["simpson"]).simpson(power, x=time))
        assert np.isclose(trap, 6.0)
        assert np.isclose(sim, 6.0)

    def test_two_rules_agree_on_smooth_data(self) -> None:
        trap = float(np.trapezoid(t16.POWER_KW, t16.TIME_HOURS))
        from scipy.integrate import simpson

        sim = float(simpson(t16.POWER_KW, x=t16.TIME_HOURS))
        assert abs(sim - trap) / abs(trap) < 0.10


# =============================================================================
# Task 17 — Euler method
# =============================================================================
class TestTask17:
    def test_euler_matches_exact_at_t0(self) -> None:
        _time, temperature, exact = t17.euler_cooling()
        assert np.isclose(temperature[0], t17.T_INITIAL)
        assert np.isclose(exact[0], t17.T_INITIAL)

    def test_temperature_decreases_monotonically(self) -> None:
        _, temperature, _ = t17.euler_cooling()
        assert np.all(np.diff(temperature) <= 0.0)

    def test_first_order_global_error_is_oom_0_1(self) -> None:
        _, temperature, exact = t17.euler_cooling()
        final_error = abs(temperature[-1] - exact[-1])
        assert 0.0 < final_error < 1.0


# =============================================================================
# Task 18 — solve_ivp
# =============================================================================
class TestTask18:
    def test_solver_succeeds(self) -> None:
        from scipy.integrate import solve_ivp

        sol = solve_ivp(t18.rc_circuit, (0.0, 1.0), [0.0], t_eval=[0.0, 0.5, 1.0])
        assert sol.success

    def test_steady_state_matches_source(self) -> None:
        from scipy.integrate import solve_ivp

        # At t = 5.0 s (5 time constants), RC charging reaches V(t) = Vs * (1 - e^-5) ≈ 4.9663 V
        sol = solve_ivp(t18.rc_circuit, (0.0, 5.0), [0.0], t_eval=[5.0])
        assert np.isclose(sol.y[0, -1], t18.VS, atol=0.05)

    def test_exact_solution_formula(self) -> None:
        t = np.array([0.0, 1.0, 5.0])
        v = t18.exact_voltage(t)
        assert np.isclose(v[0], 0.0)
        assert v[-1] < t18.VS


# =============================================================================
# Task 19 — Optimisation
# =============================================================================
class TestTask19:
    def test_capacity_constraint_sign(self) -> None:
        assert t19.capacity_constraint(np.array([0.0, 0.0])) < 0.0
        assert np.isclose(t19.capacity_constraint(np.array([10.0, 0.0])), 0.0)

    def test_continuous_solution_meets_capacity(self) -> None:
        sol = t19.solve_continuous()
        assert sol["success"] is True
        assert sol["capacity"] >= t19.REQUIRED_CAPACITY - 1e-6

    def test_integer_solution_is_feasible(self) -> None:
        sol = t19.solve_integer()
        assert sol["capacity"] >= t19.REQUIRED_CAPACITY

    def test_integer_cost_is_at_least_continuous_cost(self) -> None:
        cont = t19.solve_continuous()
        ints = t19.solve_integer()
        assert ints["cost"] + 1e-9 >= cont["cost"]


# =============================================================================
# Task 20 — Monte Carlo
# =============================================================================
class TestTask20:
    def test_estimate_matches_theoretical_gaussian_tail(self) -> None:
        z = (t20.CAPACITY - t20.MEAN_DEMAND) / t20.STD_DEMAND
        theoretical = 1.0 - stats.norm.cdf(z)

        rng = np.random.default_rng(t20.SEED)
        demand, _ = t20.simulate(200_000, rng)
        mc = float((demand > t20.CAPACITY).mean())

        assert abs(mc - theoretical) < 0.005

    def test_running_probability_bounded(self) -> None:
        rng = np.random.default_rng(0)
        _, running = t20.simulate(1_000, rng)
        assert np.all((running >= 0.0) & (running <= 1.0))

    def test_seed_reproducibility(self) -> None:
        rng_a = np.random.default_rng(7)
        rng_b = np.random.default_rng(7)
        d_a, _ = t20.simulate(500, rng_a)
        d_b, _ = t20.simulate(500, rng_b)
        assert np.array_equal(d_a, d_b)