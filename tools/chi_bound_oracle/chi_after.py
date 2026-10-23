"""Pure χ̂ transition table — contract a future typechecker could call.

See DESIGN.md. Not wired into Eshkol.
"""
from __future__ import annotations
from typing import Tuple

# Wire indices: 0 = control/a, 1 = target/b for two-wire ops.
ChiPair = Tuple[int, int]

OPS_1Q = frozenset({"I", "H", "X", "Y", "Z", "S", "Rx", "Ry", "Rz"})
OPS_2Q = frozenset({"CNOT"})
OPS_MEAS = frozenset({"MeasureZ"})


def chi_after(op: str, chi_in: ChiPair, wire: int = 0) -> ChiPair:
    """Return χ̂' for both wires after `op`.

    Contract (DESIGN.md recurrence, 2-wire MVP):
      I/H/X/Y/Z/S/Rx/Ry/Rz on one wire: χ̂ unchanged
      CNOT (from any χ_in): both wires ← max(χ_a, χ_b, 2) if either was product
        spanning pair — MVP: both ← 2 (sound over-approx from product; from
        already-2 stays 2)
      MeasureZ on wire w: that wire unused post-measure; residual ← 1
        (we zero the measured wire's χ̂ to 0 meaning 'classical/consumed')
    """
    a, b = chi_in
    if a < 1 or b < 1:
        # allow 0 only as post-measure marker on the measured wire
        if a < 0 or b < 0:
            raise ValueError("chi_in must be non-negative")

    if op in OPS_1Q:
        if wire not in (0, 1):
            raise ValueError("wire must be 0 or 1")
        return (a, b)

    if op in OPS_2Q:
        # Sound over-approx: after CNOT on the pair, χ̂ = 2
        return (2, 2)

    if op in OPS_MEAS:
        if wire == 0:
            return (0, 1)  # residual b separable
        if wire == 1:
            return (1, 0)
        raise ValueError("wire must be 0 or 1")

    raise ValueError(f"unknown op: {op}")
