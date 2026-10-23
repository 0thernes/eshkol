"""n-wire pairwise χ̂ walk (RFC-A).

Honesty: for n>2 this is a **pairwise cut over-approximation**, not a full
multipartite Schmidt tensor. Each unordered pair (i,j) stores an integer
upper bound χ̂_{i|j}. A CNOT on (i,j) sets that pair to 2. Measure on w
zeros every pair involving w (w classical/consumed). Other pairs untouched.

This can overstate entanglement (e.g. after CNOT on a computational |0⟩
control) and does **not** certify true multipartite entanglement.
"""
from __future__ import annotations
from typing import Dict, Iterable, List, Tuple, Union

Gate = Union[str, dict]
PairKey = Tuple[int, int]


def _pair(i: int, j: int) -> PairKey:
    return (i, j) if i < j else (j, i)


def init_pairs(n: int) -> Dict[PairKey, int]:
    if n < 2:
        raise ValueError("n must be >= 2")
    return {_pair(i, j): 1 for i in range(n) for j in range(i + 1, n)}


def apply_gate(pairs: Dict[PairKey, int], n: int, op: str, wires: List[int]) -> None:
    if op in ("I", "H", "X", "Y", "Z", "S", "Rx", "Ry", "Rz"):
        return
    if op == "CNOT":
        if len(wires) != 2:
            raise ValueError("CNOT needs two wires")
        a, b = wires
        if a == b or not (0 <= a < n and 0 <= b < n):
            raise ValueError("CNOT wire out of range")
        pairs[_pair(a, b)] = 2
        return
    if op == "MeasureZ":
        if len(wires) != 1:
            raise ValueError("MeasureZ needs one wire")
        w = wires[0]
        if not (0 <= w < n):
            raise ValueError("MeasureZ wire out of range")
        for (i, j) in list(pairs):
            if i == w or j == w:
                pairs[(i, j)] = 0  # 0 = classical/consumed on that cut
        return
    raise ValueError(f"unknown op: {op}")


def parse_gate(g: Gate, default_wires: List[int] | None = None) -> Tuple[str, List[int]]:
    if isinstance(g, str):
        return g, list(default_wires or [0])
    op = g["op"]
    if "wires" in g:
        return op, list(g["wires"])
    if "wire" in g:
        return op, [int(g["wire"])]
    if op == "CNOT":
        return op, [0, 1]
    return op, [0]


def run_multiwire(n: int, gates: Iterable[Gate]):
    """Yield (step, op, wires, pairs_snapshot, honesty)."""
    pairs = init_pairs(n)
    honesty = (
        "pairwise cut over-approx only; not a multipartite Schmidt certificate"
    )
    yield (0, "init", [], dict(pairs), honesty)
    for i, g in enumerate(gates, start=1):
        op, wires = parse_gate(g)
        apply_gate(pairs, n, op, wires)
        yield (i, op, wires, dict(pairs), honesty)


def format_pairs(pairs: Dict[PairKey, int]) -> str:
    parts = [f"{i}|{j}={v}" for (i, j), v in sorted(pairs.items())]
    return " ".join(parts)


def pairs_as_cuts(pairs: Dict[PairKey, int]) -> Dict[str, int]:
    return {f"{i}|{j}": v for (i, j), v in sorted(pairs.items())}


def walk_to_json(n: int, gates: Iterable[Gate]) -> dict:
    """Export χ̂ walk as JSON: steps, final cuts, honesty flags."""
    honesty_flags = [
        "pairwise_cut_overapprox",
        "not_multipartite_schmidt_certificate",
        "undirected_pairs_only",
    ]
    steps = []
    final_cuts: Dict[str, int] = {}
    for step, op, wires, pairs, honesty in run_multiwire(n, gates):
        cuts = pairs_as_cuts(pairs)
        final_cuts = cuts
        steps.append(
            {
                "step": step,
                "op": op,
                "wires": list(wires),
                "cuts": cuts,
                "honesty": honesty,
            }
        )
    return {
        "schema": "rfc-a-chi-walk-v0",
        "n": n,
        "honesty_flags": honesty_flags,
        "steps": steps,
        "final_cuts": final_cuts,
    }
