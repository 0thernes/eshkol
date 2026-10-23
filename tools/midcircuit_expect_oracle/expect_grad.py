"""Closed-form E[⟨O⟩] for Ry(θ)|0⟩ with optional feedforward α.

α=0, O∈{Z,X}: analytic L and dL/dθ.
α≠0: refuse numeric pathwise gradient (structured undefined).
See REFUSE.md, DERIVATIVE.md, docs/rfcs/RFC-B.md.
"""
from __future__ import annotations
import math
from typing import Literal, TypedDict, Union

Obs = Literal["Z", "X"]

class GradOk(TypedDict):
    ok: bool  # True
    theta: float
    alpha: float
    obs: str
    L: float
    dL: float

class GradUndefined(TypedDict):
    ok: bool  # False
    theta: float
    alpha: float
    obs: str
    reason: str
    detail: str

GradResult = Union[GradOk, GradUndefined]


def L_alpha0(theta: float, obs: Obs = "Z") -> float:
    """Born expectation of Pauli obs on Ry(θ)|0⟩ (no feedforward)."""
    if obs == "Z":
        # ⟨Z⟩ = cos²(θ/2) − sin²(θ/2) = cos(θ)
        return math.cos(theta)
    if obs == "X":
        # ⟨X⟩ = 2 cos(θ/2)sin(θ/2) = sin(θ)
        return math.sin(theta)
    raise ValueError(f"unsupported obs: {obs}")


def dL_alpha0(theta: float, obs: Obs = "Z") -> float:
    if obs == "Z":
        return -math.sin(theta)
    if obs == "X":
        return math.cos(theta)
    raise ValueError(f"unsupported obs: {obs}")


def fd_dL_alpha0(theta: float, obs: Obs = "Z", eps: float = 1e-6) -> float:
    return (L_alpha0(theta + eps, obs) - L_alpha0(theta - eps, obs)) / (2 * eps)


def gradient(theta: float, alpha: float = 0.0, obs: Obs = "Z") -> GradResult:
    """Return closed-form grad when α=0; structured refuse when α≠0."""
    if obs not in ("Z", "X"):
        raise ValueError(f"unsupported obs: {obs}")
    if abs(alpha) > 0.0:
        return {
            "ok": False,
            "theta": theta,
            "alpha": alpha,
            "obs": obs,
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
        "obs": obs,
        "L": L_alpha0(theta, obs),
        "dL": dL_alpha0(theta, obs),
    }


def fd_sensitivity_alpha0(
    theta: float,
    obs: Obs = "Z",
    eps_a: float = 1e-6,
    eps_b: float = 1e-5,
) -> tuple[float, float, float]:
    """Return (fd_a, fd_b, abs_diff) for two step sizes. α=0 only."""
    a = fd_dL_alpha0(theta, obs, eps=eps_a)
    b = fd_dL_alpha0(theta, obs, eps=eps_b)
    return a, b, abs(a - b)
