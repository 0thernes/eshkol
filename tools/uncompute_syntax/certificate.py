"""Machine-readable syntactic uncompute certificates (RFC-C MVP v0)."""
from __future__ import annotations
import hashlib, json
from typing import Any, Dict, List
try:
    from .check import check_uncompute
except ImportError:
    from check import check_uncompute

def issue_certificate(forward: List[str], inverse: List[str], released: bool) -> Dict[str, Any]:
    """Validate then return a certificate. Raises ValueError if check fails."""
    check_uncompute(forward, inverse, released=released)
    payload = {
        "gates": list(forward),
        "inverse": list(inverse),
        "inverse_ok": True,
        "release_zero": bool(released),
        "schema": "rfc-c-uncompute-syntax-v0",
    }
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["hash"] = hashlib.sha256(blob.encode()).hexdigest()
    return payload

def verify_certificate(cert: Dict[str, Any]) -> None:
    """Re-check syntactic obligations and hash. Raises ValueError on failure."""
    forward = cert["gates"]
    inverse = cert["inverse"]
    released = cert["release_zero"]
    if not cert.get("inverse_ok"):
        raise ValueError("certificate: inverse_ok is false")
    check_uncompute(forward, inverse, released=released)
    # recompute hash over fields excluding hash
    body = {
        "gates": list(forward),
        "inverse": list(inverse),
        "inverse_ok": True,
        "release_zero": bool(released),
        "schema": cert.get("schema", "rfc-c-uncompute-syntax-v0"),
    }
    blob = json.dumps(body, sort_keys=True, separators=(",", ":"))
    expect = hashlib.sha256(blob.encode()).hexdigest()
    if cert.get("hash") != expect:
        raise ValueError("certificate: hash mismatch")
