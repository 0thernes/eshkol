"""Syntactic uncomputation check for straight-line ancilla fragments.

Accepts matched self-inverse pairs + release-zero; rejects leaks.
Supports optional ancilla labels on gates; every labeled ancilla must appear
in the released set. Not a semantic |0⟩ proof under entanglement.
See docs/rfcs/RFC-C.md.
"""
from __future__ import annotations
from typing import Any, Dict, Iterable, List, Optional, Set, Union

SELF_INVERSE = {"H", "X", "Y", "Z"}

Gate = Union[str, Dict[str, Any]]


def _op(g: Gate) -> str:
    return g if isinstance(g, str) else str(g["op"])


def _ancilla(g: Gate) -> Optional[str]:
    if isinstance(g, str):
        return None
    a = g.get("ancilla")
    return str(a) if a is not None else None


def collect_ancillae(gates: Iterable[Gate]) -> Set[str]:
    out: Set[str] = set()
    for g in gates:
        a = _ancilla(g)
        if a:
            out.add(a)
    return out


def check_uncompute(
    forward: List[Gate],
    inverse: List[Gate],
    released: Union[bool, List[str], Set[str]] = True,
) -> None:
    """Validate inverse order + release-zero.

    `released`:
      - bool True/False (legacy): all-or-nothing release flag
      - list/set of ancilla labels that were release-zero'd
        If forward/inverse mention ancilla labels, each must be in this set.
        If no labels appear, a non-empty released set OR True is required
        only when labels exist; unlabeled legacy form still needs bool True
        or a non-empty list treated as success for the anonymous ancilla.
    """
    # Normalize release
    labeled = collect_ancillae(forward) | collect_ancillae(inverse)

    if isinstance(released, bool):
        if not released:
            raise ValueError("uncompute: ancilla not release-zero'd")
        if labeled:
            # bool True with labels is accepted as "all released"
            pass
    else:
        rel_set = {str(x) for x in released}
        if labeled:
            missing = labeled - rel_set
            if missing:
                raise ValueError(
                    f"uncompute: ancilla not release-zero'd: {sorted(missing)}"
                )
        else:
            # unlabeled legacy path: empty released list means not released
            if len(rel_set) == 0:
                raise ValueError("uncompute: ancilla not release-zero'd")

    if len(forward) != len(inverse):
        raise ValueError("uncompute: inverse length mismatch")
    for g, ig in zip(reversed(forward), inverse):
        og, oig = _op(g), _op(ig)
        if og not in SELF_INVERSE or oig != og:
            raise ValueError(f"uncompute: expected self-inverse dagger of {og}, got {oig}")
        # if both have ancilla labels, they must match on the paired inverse slot
        ag, aig = _ancilla(g), _ancilla(ig)
        if ag is not None and aig is not None and ag != aig:
            raise ValueError(f"uncompute: ancilla label mismatch {ag} vs {aig}")
