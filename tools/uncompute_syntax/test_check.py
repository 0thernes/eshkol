"""Round-trip syntactic uncompute tests + certificate (RFC-C MVP v0)."""
from check import check_uncompute
from certificate import issue_certificate, verify_certificate

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
    # tamper
    bad = dict(cert)
    bad["gates"] = ["H"]
    try:
        verify_certificate(bad)
        raise AssertionError("expected hash/check failure")
    except ValueError:
        pass

def test_cli_issue_and_verify(tmp_path=None):
    """Smoke: issue cert via CLI helpers, write JSON, --verify path."""
    import json, tempfile
    from pathlib import Path
    from certificate import issue_certificate, verify_certificate

    cert = issue_certificate(["H", "X"], ["X", "H"], released=True)
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "cert.json"
        path.write_text(json.dumps(cert))
        loaded = json.loads(path.read_text())
        verify_certificate(loaded)
        assert loaded["hash"] == cert["hash"]


if __name__ == "__main__":
    test_roundtrip_self_inverse_hh_ok()
    test_roundtrip_xz_ok()
    test_fail_missing_release_zero()
    test_fail_inverse_order()
    test_certificate_roundtrip()
    test_cli_issue_and_verify()
    print("RFC-C uncompute_syntax: PASS")
