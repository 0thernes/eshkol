"""Machine-readable syntactic uncompute certificates (RFC-C MVP v0)."""
from __future__ import annotations
import hashlib, json
from typing import Any, Dict, List, Set, Union
try:
    from .check import check_uncompute, collect_ancillae, Gate
except ImportError:
    from check import check_uncompute, collect_ancillae, Gate  # type: ignore


def issue_certificate(
    forward: List[Gate],
    inverse: List[Gate],
    released: Union[bool, List[str], Set[str]] = True,
) -> Dict[str, Any]:
    """Validate then return a certificate. Raises ValueError if check fails."""
    check_uncompute(forward, inverse, released=released)
    if isinstance(released, bool):
        release_zero = released
        released_labels = sorted(collect_ancillae(forward) | collect_ancillae(inverse)) if released else []
    else:
        released_labels = sorted({str(x) for x in released})
        release_zero = True
    payload = {
        "gates": list(forward),
        "inverse": list(inverse),
        "inverse_ok": True,
        "release_zero": release_zero,
        "released_ancillae": released_labels,
        "schema": "rfc-c-uncompute-syntax-v0",
    }
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["hash"] = hashlib.sha256(blob.encode()).hexdigest()
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
        # legacy unlabeled: honor boolean release_zero
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
    blob = json.dumps(body, sort_keys=True, separators=(",", ":"))
    expect = hashlib.sha256(blob.encode()).hexdigest()
    if cert.get("hash") != expect:
        raise ValueError("certificate: hash mismatch")
