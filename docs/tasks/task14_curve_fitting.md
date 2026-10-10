# Task 14 — Curve Fitting and Approximation

**Module:** `bit2118.task14_curve_fitting`
**Concept:** Least-squares parameter estimation.
**Real-world anchor:** server response time vs. concurrent users.

## 1. Concept
Curve fitting chooses model parameters that best follow observed data in
a least-squares sense.

## 2. Mathematical formulation
$\hat{\theta} = \arg\min_\theta \sum_i (y_i - f(x_i; \theta))^2$;
RMSE quantifies fit quality.

## 3. Algorithm
1. `curve_fit(model, USERS, RESPONSE_MS)`.
2. Report fitted $(a, b, c)$ and RMSE.
3. Extrapolate to 400 users.

## 4. Inputs
Users 50 → 350; responses 82 → 305 ms.

## 5. Outputs
`params`, `rmse_ms`, `predicted_400_users_ms`, `covariance`.

## 6. Interpretation
$y = a x^2 + b x + c$ captures the super-linear degradation under load.
Predicted response at 400 users is a planning input for capacity decisions.