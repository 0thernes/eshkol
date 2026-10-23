"""Symbolic χ̂ upper-bound tracker for a 2-wire straight-line toy language.

See docs/rfcs/RFC-A.md. Sound over-approximation only; not a type checker.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Wire:
    name: str
    chi_hat: int = 1

class Circuit2:
    def __init__(self) -> None:
        self.a = Wire("a", 1)
        self.b = Wire("b", 1)
        self._entangled_pair = False

    def local(self, which: str) -> None:
        # local unitaries do not change χ̂
        if which not in ("a", "b"):
            raise KeyError(which)

    def cnot(self) -> None:
        # After CNOT on a product pair spanning the full system, allow χ̂=2.
        self._entangled_pair = True
        self.a.chi_hat = 2
        self.b.chi_hat = 2

    def measure(self, which: str) -> int:
        # Residual partner collapses to χ̂=1 in this bipartite MVP model.
        other = self.b if which == "a" else self.a
        other.chi_hat = 1
        self._entangled_pair = False
        return 0  # outcome unused for bound tracking
