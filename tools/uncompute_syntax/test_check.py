"""Round-trip syntactic uncompute tests + certificate + ancilla labels (RFC-C)."""
from pathlib import Path
import json
from check import check_uncompute
from certificate import issue_certificate, verify_certificate

FIX = Path(__file__).resolve().parent / "fixtures"


def test_roundtrip_self_inverse_hh_ok():
    check_uncompute(["H", "H"], ["H", "H"], released=True)


def test_roundtrip_xz_ok():
    check_uncompute(["X", "Z"], ["Z", "X"], released=True)


def test_fail_missing_release_zero():
    try:
        check_uncompute(["H"], ["H"], released=False)
        raise AssertionError("expected reject")
    except ValueError as e:
        assert "release-zero" in str(e)


def test_fail_inverse_order():
    try:
        check_uncompute(["X", "Z"], ["X", "Z"], released=True)
        raise AssertionError("expected reject")
    except ValueError:
        pass


def test_certificate_roundtrip():
    cert = issue_certificate(["H", "X"], ["X", "H"], released=True)
    assert cert["inverse_ok"] is True
    assert cert["release_zero"] is True
    assert len(cert["hash"]) == 64
    verify_certificate(cert)
    bad = dict(cert)
    bad["gates"] = ["H"]
    try:
        verify_certificate(bad)
        raise AssertionError("expected hash/check failure")
    except ValueError:
        pass


def test_cli_issue_and_verify():
    import tempfile
    cert = issue_certificate(["H", "X"], ["X", "H"], released=True)
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "cert.json"
        path.write_text(json.dumps(cert))
        loaded = json.loads(path.read_text())
        verify_certificate(loaded)
        assert loaded["hash"] == cert["hash"]


def test_ancilla_accept_fixture():
    data = json.loads((FIX / "ancilla_accept.json").read_text())
    check_uncompute(data["forward"], data["inverse"], released=data["released"])
    cert = issue_certificate(data["forward"], data["inverse"], released=data["released"])
    assert "q2" in cert["released_ancillae"]
    verify_certificate(cert)


def test_ancilla_reject_leak_fixture():
    data = json.loads((FIX / "ancilla_reject_leak.json").read_text())
    try:
        check_uncompute(data["forward"], data["inverse"], released=data["released"])
        raise AssertionError("expected reject")
    except ValueError as e:
        assert "release-zero" in str(e)
        assert "q2" in str(e)


def test_hash_stable_across_key_order():
    """Canonical JSON: different dict key insertion orders → same hash."""
    from certificate import issue_certificate, canonical_dumps
    import hashlib

    # same logical gates, different key order in dict literals
    f1 = [{"op": "H", "ancilla": "q2"}, {"ancilla": "q2", "op": "X"}]
    f2 = [{"ancilla": "q2", "op": "H"}, {"op": "X", "ancilla": "q2"}]
    inv1 = [{"op": "X", "ancilla": "q2"}, {"ancilla": "q2", "op": "H"}]
    inv2 = [{"ancilla": "q2", "op": "X"}, {"op": "H", "ancilla": "q2"}]
    c1 = issue_certificate(f1, inv1, released=["q2"])
    c2 = issue_certificate(f2, inv2, released=["q2"])
    assert c1["hash"] == c2["hash"]
    # canonical_dumps itself ignores key order
    assert canonical_dumps({"b": 1, "a": 2}) == canonical_dumps({"a": 2, "b": 1})


def test_verify_fails_on_tampered_hash():
    from certificate import issue_certificate, verify_certificate
    cert = issue_certificate(["H"], ["H"], released=True)
    bad = dict(cert)
    bad["hash"] = "0" * 64
    try:
        verify_certificate(bad)
        raise AssertionError("expected hash mismatch")
    except ValueError as e:
        assert "hash mismatch" in str(e)


if __name__ == "__main__":
    test_roundtrip_self_inverse_hh_ok()
    test_roundtrip_xz_ok()
    test_fail_missing_release_zero()
    test_fail_inverse_order()
    test_certificate_roundtrip()
    test_cli_issue_and_verify()
    test_ancilla_accept_fixture()
    test_ancilla_reject_leak_fixture()
    test_hash_stable_across_key_order()
    test_verify_fails_on_tampered_hash()
    print("RFC-C uncompute_syntax: PASS")
