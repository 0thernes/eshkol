"""Syntactic uncomputation check for straight-line ancilla fragments.

Accepts matched self-inverse pairs + release-zero; rejects leaks.
Not a semantic |0⟩ proof under entanglement. See docs/rfcs/RFC-C.md.
"""
from __future__ import annotations
from typing import List

# MVP gate set: self-inverse gates only (H,X,Y,Z). Extend later with dagger table.
SELF_INVERSE = {"H", "X", "Y", "Z"}

def check_uncompute(forward: List[str], inverse: List[str], released: bool) -> None:
    if not released:
        raise ValueError("uncompute: ancilla not release-zero'd")
    if len(forward) != len(inverse):
        raise ValueError("uncompute: inverse length mismatch")
    for g, ig in zip(reversed(forward), inverse):
        if g not in SELF_INVERSE or ig != g:
            raise ValueError(f"uncompute: expected self-inverse dagger of {g}, got {ig}")
