"""Task 09 — Eigenvalues and Eigenvectors.

Concept
-------
For a square matrix ``A``, an eigenvector ``v`` is a non-zero vector whose
direction is unchanged by the transformation ``A``. It satisfies
``A v = λ v``, where ``λ`` is the eigenvalue. The eigenvalue tells how
much the vector is stretched, compressed or reversed.

Mathematical formulation
------------------------
The eigenvalues of :math:`A \\in \\mathbb{R}^{n \\times n}` solve the
characteristic polynomial :math:`\\det(A - \\lambda I) = 0`. For a
symmetric adjacency matrix of an undirected graph, the *dominant*
(Perron-Frobenius) eigenvalue :math:`\\lambda_{\\max}` is real, positive,
and its eigenvector can be normalised to give a centrality score
(PageRank-style).

Real-world application
----------------------
Ranking node influence in a small computer network from its connection
pattern (adjacency matrix).

Interpretation of the output
----------------------------
* ``dominant_eigenvalue`` — largest eigenvalue (spectral radius) of ``A``.
* ``centrality`` — normalised dominant eigenvector; larger = more
  structurally influential node.
* ``verification_error`` — :math:`\\|A v - \\lambda v\\|_2`; near-zero
  confirms the eigenpair.
"""

from __future__ import annotations

import numpy as np

from .io_utils import save_results
from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)


# -----------------------------------------------------------------------------
# Inputs — adjacency matrix of a 4-node undirected network (A, B, C, D)
# -----------------------------------------------------------------------------
ADJACENCY: np.ndarray = np.array(
    [
        [0.0, 1.0, 1.0, 0.0],
        [1.0, 0.0, 1.0, 1.0],
        [1.0, 1.0, 0.0, 1.0],
        [0.0, 1.0, 1.0, 0.0],
    ],
    dtype=float,
)

NODES: tuple[str, ...] = ("A", "B", "C", "D")


# -----------------------------------------------------------------------------
# Pure functions
# -----------------------------------------------------------------------------
def eigenvector_centrality(
    a: np.ndarray,
) -> tuple[float, np.ndarray, float]:
    """Return ``(dominant eigenvalue, normalised centrality, verification)``.

    Parameters
    ----------
    a : numpy.ndarray
        Real square matrix (typically symmetric).

    Returns
    -------
    dominant_value : float
        Largest real eigenvalue.
    centrality : numpy.ndarray
        ``|v| / sum(|v|)`` where ``v`` is the dominant eigenvector. The
        absolute value is taken to remove arbitrary sign; normalisation
        makes the scores interpretable as relative weights.
    verification_error : float
        :math:`\\|A v - \\lambda v\\|_2` for the *signed* eigenvector.
    """
    eigenvalues, eigenvectors = np.linalg.eig(a)
    idx = int(np.argmax(np.real(eigenvalues)))
    dominant_value = float(np.real(eigenvalues[idx]))

    v = np.real(eigenvectors[:, idx])
    v_abs = np.abs(v)
    centrality = v_abs / v_abs.sum()

    verification_error = float(np.linalg.norm(a @ v - dominant_value * v))
    return dominant_value, centrality, verification_error


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
def main() -> dict[str, object]:
    """Compute and report eigenvector-based node importance.

    Returns
    -------
    dict
        Keys: ``adjacency``, ``nodes``, ``dominant_eigenvalue``,
        ``centrality``, ``verification_error``.
    """
    configure_logging()

    dominant, centrality, verification = eigenvector_centrality(ADJACENCY)

    logger.info("Adjacency matrix:\n%s", ADJACENCY)
    logger.info("Dominant eigenvalue (spectral radius): %.6f", dominant)
    logger.info("Eigenvector-based centrality:")
    for node, score in zip(NODES, centrality, strict=False):
        logger.info("  %s → %.4f", node, score)
    logger.info("Verification ‖Av - λv‖: %.3e", verification)

    payload = {
        "adjacency": ADJACENCY,
        "nodes": list(NODES),
        "dominant_eigenvalue": dominant,
        "centrality": {node: float(score) for node, score in zip(NODES, centrality, strict=False)},
        "verification_error": verification,
    }
    save_results("task09_eigenvalues", payload)
    return payload


if __name__ == "__main__":
    main()
