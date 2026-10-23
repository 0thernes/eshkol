"""Round-trip syntactic uncompute tests (RFC-C MVP v0)."""
from check import check_uncompute

def test_roundtrip_self_inverse_hh_ok():
    # H; H is self-inverse; reverse dagger list is H; H
    forward = ["H", "H"]
    inverse = ["H", "H"]  # reverse order, each self-inverse
    check_uncompute(forward, inverse, released=True)

def test_roundtrip_xz_ok():
    forward = ["X", "Z"]
    inverse = ["Z", "X"]
    check_uncompute(forward, inverse, released=True)

def test_fail_missing_release_zero():
    try:
        check_uncompute(["H"], ["H"], released=False)
        raise AssertionError("expected reject")
    except ValueError as e:
        assert "release-zero" in str(e)

def test_fail_inverse_order():
    try:
        # wrong order: should be Z then X for forward X;Z
        check_uncompute(["X", "Z"], ["X", "Z"], released=True)
        raise AssertionError("expected reject")
    except ValueError:
        pass

if __name__ == "__main__":
    test_roundtrip_self_inverse_hh_ok()
    test_roundtrip_xz_ok()
    test_fail_missing_release_zero()
    test_fail_inverse_order()
    print("RFC-C uncompute_syntax: PASS")
