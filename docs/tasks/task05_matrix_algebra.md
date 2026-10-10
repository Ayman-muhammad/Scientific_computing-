# Task 05 — Matrix Algebra and Matrix Operations

**Module:** `bit2118.task05_matrix_algebra`
**Concept:** Matrix multiplication, determinant, geometric transforms.
**Real-world anchor:** 2-D graphics pipeline.

## 1. Concept
A matrix organises values in rows and columns. `C = A @ B` combines rows
of A with columns of B. Rotation preserves distances; scaling stretches.

## 2. Mathematical formulation
$R(\theta)$ and $S = \operatorname{diag}(s_x, s_y)$; combined
$T = R S$. Row-vector application: $p' = p T^{\top}$.

## 3. Algorithm
1. Build the unit square as four row vectors.
2. Build `R(45°)` and `S(2, 1.5)`.
3. Combine to `T = R @ S`, apply to the points, compute `det(T)`.

## 4. Inputs
| Name | Value |
|------|-------|
| rotation angle | 45° |
| scale | (2.0, 1.5) |

## 5. Outputs
`points`, `rotation`, `scale`, `transformation`, `transformed`,
`determinant`.

## 6. Interpretation
`det(T) = sx · sy = 3.0`. The unit square is transformed into a rotated
rectangle; the shape's area is 3× the original.