"""Machine-readable syntactic uncompute certificates (RFC-C MVP v0).

Hash is SHA-256 over **canonical JSON** (sorted keys, compact separators,
UTF-8). Key insertion order in Python dicts must not affect the digest.
"""
from __future__ import annotations
import hashlib, json
from typing import Any, Dict, List, Set, Union
try:
    from .check import check_uncompute, collect_ancillae, Gate
except ImportError:
    from check import check_uncompute, collect_ancillae, Gate  # type: ignore


def canonical_dumps(obj: Any) -> str:
    """Deterministic JSON: sorted keys at every level, no spaces."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def issue_certificate(
    forward: List[Gate],
    inverse: List[Gate],
    released: Union[bool, List[str], Set[str]] = True,
) -> Dict[str, Any]:
    """Validate then return a certificate. Raises ValueError if check fails."""
    check_uncompute(forward, inverse, released=released)
    if isinstance(released, bool):
        release_zero = released
        released_labels = (
            sorted(collect_ancillae(forward) | collect_ancillae(inverse))
            if released
            else []
        )
    else:
        released_labels = sorted({str(x) for x in released})
        release_zero = True
    # Build body with stable field set; gates may be str or dict
    payload = {
        "gates": list(forward),
        "inverse": list(inverse),
        "inverse_ok": True,
        "release_zero": release_zero,
        "released_ancillae": released_labels,
        "schema": "rfc-c-uncompute-syntax-v0",
    }
    payload["hash"] = hashlib.sha256(canonical_dumps(payload).encode("utf-8")).hexdigest()
    return payload


def verify_certificate(cert: Dict[str, Any]) -> None:
    """Re-check syntactic obligations and hash. Raises ValueError on failure."""
    forward = cert["gates"]
    inverse = cert["inverse"]
    if not cert.get("inverse_ok"):
        raise ValueError("certificate: inverse_ok is false")
    labeled = collect_ancillae(forward) | collect_ancillae(inverse)
    labels = cert.get("released_ancillae")
    if labeled:
        released: Union[bool, List[str]] = list(labels or [])
    else:
        released = bool(cert.get("release_zero", False))
    check_uncompute(forward, inverse, released=released)
    body = {
        "gates": list(forward),
        "inverse": list(inverse),
        "inverse_ok": True,
        "release_zero": bool(cert.get("release_zero", True)),
        "released_ancillae": list(cert.get("released_ancillae", [])),
        "schema": cert.get("schema", "rfc-c-uncompute-syntax-v0"),
    }
    expect = hashlib.sha256(canonical_dumps(body).encode("utf-8")).hexdigest()
    if cert.get("hash") != expect:
        raise ValueError("certificate: hash mismatch")
