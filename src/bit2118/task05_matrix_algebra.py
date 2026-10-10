"""Task 05 — Matrix Algebra and Matrix Operations.

Concept
-------
Matrices organise values in rows and columns. ``C = A @ B`` combines rows
of ``A`` with columns of ``B`` (inner-product rule). The determinant
indicates whether a square matrix is invertible; the inverse satisfies
:math:`A A^{-1} = I`.

Mathematical formulation
------------------------
A 2-D rotation by angle :math:`\\theta` is

.. math::

    R(\\theta) = \\begin{bmatrix} \\cos\\theta & -\\sin\\theta \\\\
                                  \\sin\\theta &  \\cos\\theta \\end{bmatrix}

A non-uniform scaling by :math:`(s_x, s_y)` is
:math:`S = \\mathrm{diag}(s_x, s_y)`. The combined transform is
:math:`T = R S`, applied to row-vector points via :math:`p' = p\\,T^{\\!\\top}`.

Real-world application
----------------------
Rotating and scaling 2-D coordinates in a graphics pipeline using a single
combined transformation matrix.
"""

from __future__ import annotations

import numpy as np

from .io_utils import save_results
from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
# Unit square: rows are [x, y] coordinates in counter-clockwise order.
POINTS: np.ndarray = np.array(
    [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]],
    dtype=float,
)
ROTATION_DEG: float = 45.0
SCALE_X: float = 2.0
SCALE_Y: float = 1.5


# -----------------------------------------------------------------------------
# Pure functions
# -----------------------------------------------------------------------------
def rotation_matrix(angle_rad: float) -> np.ndarray:
    """Return the 2×2 rotation matrix for ``angle_rad`` radians."""
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    return np.array([[c, -s], [s, c]], dtype=float)


def scaling_matrix(sx: float, sy: float) -> np.ndarray:
    """Return the 2×2 axis-aligned scaling matrix."""
    return np.array([[sx, 0.0], [0.0, sy]], dtype=float)


def apply_transform(points: np.ndarray, transform: np.ndarray) -> np.ndarray:
    """Apply ``transform`` to row-vector ``points`` via ``p @ Tᵀ``."""
    return points @ transform.T


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Rotate 45° then scale (2×, 1.5×) a unit square.

    Returns
    -------
    dict
        Keys: ``points``, ``rotation``, ``scale``, ``transformation``,
        ``transformed``, ``determinant``.
    """
    configure_logging()

    angle = np.deg2rad(ROTATION_DEG)
    rotation = rotation_matrix(angle)
    scale = scaling_matrix(SCALE_X, SCALE_Y)
    transformation = rotation @ scale

    transformed = apply_transform(POINTS, transformation)
    determinant = float(np.linalg.det(transformation))

    logger.info("Original points:\n%s", POINTS)
    logger.info("Rotation matrix (%.1f°):\n%s", ROTATION_DEG, np.round(rotation, 4))
    logger.info("Scaling matrix:\n%s", scale)
    logger.info("Combined transformation:\n%s", np.round(transformation, 4))
    logger.info("Transformed points:\n%s", np.round(transformed, 4))
    logger.info("Determinant: %.6f (= sx·sy = %.2f)", determinant, SCALE_X * SCALE_Y)

    payload = {
        "points": POINTS,
        "rotation_deg": ROTATION_DEG,
        "rotation": rotation,
        "scale": scale,
        "transformation": transformation,
        "transformed": transformed,
        "determinant": determinant,
    }
    save_results("task05_matrix_algebra", payload)
    return payload


if __name__ == "__main__":
    main()
