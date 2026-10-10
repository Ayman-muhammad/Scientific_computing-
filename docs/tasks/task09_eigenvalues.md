# Task 09 — Eigenvalues and Eigenvectors

**Module:** `bit2118.task09_eigenvalues`
**Concept:** $A v = \lambda v$.
**Real-world anchor:** network centrality.

## 1. Concept
An eigenvector's direction is unchanged by $A$; the eigenvalue is the
stretch factor. The dominant eigenvector of an adjacency matrix provides
a PageRank-style importance score.

## 2. Mathematical formulation
$\det(A - \lambda I) = 0$ gives eigenvalues.
Normalised dominant eigenvector gives centrality.

## 3. Algorithm
1. Form the 4×4 symmetric adjacency matrix.
2. `np.linalg.eig` → eigenvalues, eigenvectors.
3. Pick the largest real eigenvalue; normalise its eigenvector to sum 1.
4. Verify $\|A v - \lambda v\|_2$.

## 4. Inputs
4-node undirected network (A, B, C, D).

## 5. Outputs
`dominant_eigenvalue`, `centrality` (per node), `verification_error`.

## 6. Interpretation
Node C has the highest centrality because it connects to every other
node. Verification error is below $10^{-15}$, confirming the eigenpair.