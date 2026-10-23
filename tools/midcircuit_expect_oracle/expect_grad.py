"""Closed-form E[⟨Z⟩] for Ry(θ)|0⟩ measure with optional feedforward α.

α=0: L=cos(θ), dL=-sin(θ).
α≠0: refuse numeric pathwise gradient (structured undefined).
See REFUSE.md and docs/rfcs/RFC-B.md.
"""
from __future__ import annotations
import math
from typing import TypedDict, Union

class GradOk(TypedDict):
    ok: bool  # True
    theta: float
    alpha: float
    L: float
    dL: float

class GradUndefined(TypedDict):
    ok: bool  # False
    theta: float
    alpha: float
    reason: str
    detail: str

GradResult = Union[GradOk, GradUndefined]

def L_alpha0(theta: float) -> float:
    return math.cos(theta)

def dL_alpha0(theta: float) -> float:
    return -math.sin(theta)

def fd_dL_alpha0(theta: float, eps: float = 1e-6) -> float:
    return (L_alpha0(theta + eps) - L_alpha0(theta - eps)) / (2 * eps)

def gradient(theta: float, alpha: float = 0.0) -> GradResult:
    """Return closed-form grad when α=0; structured refuse when α≠0."""
    if abs(alpha) > 0.0:
        return {
            "ok": False,
            "theta": theta,
            "alpha": alpha,
            "reason": "pathwise-undefined",
            "detail": (
                "Numeric dL/dθ refused for α≠0: pathwise derivative through "
                "projective collapse is undefined in this MVP. Use α=0 or a "
                "future expectation-level estimator."
            ),
        }
    return {
        "ok": True,
        "theta": theta,
        "alpha": 0.0,
        "L": L_alpha0(theta),
        "dL": dL_alpha0(theta),
    }
