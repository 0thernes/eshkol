"""Closed-form E[⟨Z⟩] and d/dθ for Ry(θ)|0⟩ measure with α=0 feedforward.

L(θ) = cos(θ), L'(θ) = -sin(θ). Pathwise AD through collapse is out of scope.
See docs/rfcs/RFC-B.md.
"""
from __future__ import annotations
import math

def L(theta: float) -> float:
    return math.cos(theta)

def dL(theta: float) -> float:
    return -math.sin(theta)

def fd_dL(theta: float, eps: float = 1e-6) -> float:
    return (L(theta + eps) - L(theta - eps)) / (2 * eps)
