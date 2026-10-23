"""Step-by-step χ̂ traces using chi_after (RFC-A)."""
from __future__ import annotations
from typing import Iterable, List, Tuple, Union
from chi_after import chi_after

Gate = Union[str, dict]
ChiPair = Tuple[int, int]


def run_trace(gates: Iterable[Gate], chi_in: ChiPair = (1, 1)):
    chi: ChiPair = (int(chi_in[0]), int(chi_in[1]))
    yield (0, "init", None, chi)
    for i, g in enumerate(gates, start=1):
        if isinstance(g, str):
            op, wire = g, 0
        else:
            op = g["op"]
            wire = int(g.get("wire", 0))
        chi = chi_after(op, chi, wire=wire)
        yield (i, op, wire, chi)
