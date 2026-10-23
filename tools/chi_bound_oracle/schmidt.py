"""True Schmidt rank for hard-coded 2-qubit amplitude tables (pure states)."""
from __future__ import annotations
import math

def schmidt_rank_2q(amps: tuple[complex, complex, complex, complex], tol: float = 1e-12) -> int:
    """amps = (a00, a01, a10, a11). Rank of 2x2 reshape via singular values."""
    # Reshape as matrix M[i,j] = amp(i,j); Schmidt ranks = rank(M)
    a00, a01, a10, a11 = amps
    # Singular values of [[a00,a01],[a10,a11]] via eigenvalues of M M†
    # M M† = [[|a00|^2+|a01|^2, a00*conj(a10)+a01*conj(a11)],
    #         [conj(...), |a10|^2+|a11|^2]]
    s00 = abs(a00) ** 2 + abs(a01) ** 2
    s11 = abs(a10) ** 2 + abs(a11) ** 2
    off = a00 * a10.conjugate() + a01 * a11.conjugate()
    # eigenvalues of Hermitian 2x2: (tr ± sqrt(tr^2 - 4 det))/2
    tr = s00 + s11
    det = s00 * s11 - abs(off) ** 2
    disc = max(tr * tr - 4 * det, 0.0)
    lam1 = 0.5 * (tr + math.sqrt(disc))
    lam2 = 0.5 * (tr - math.sqrt(disc))
    return int(lam1 > tol) + int(lam2 > tol)
