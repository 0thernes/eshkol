from check import check_uncompute

def test_leak_rejected():
    try:
        check_uncompute(["H"], ["H"], released=False)
        raise AssertionError("expected reject")
    except ValueError as e:
        assert "release-zero" in str(e)

def test_matched_h_ok():
    check_uncompute(["H"], ["H"], released=True)

def test_bad_inverse_rejected():
    try:
        check_uncompute(["H"], ["X"], released=True)
        raise AssertionError("expected reject")
    except ValueError:
        pass

if __name__ == "__main__":
    test_leak_rejected()
    test_matched_h_ok()
    test_bad_inverse_rejected()
    print("RFC-C uncompute_syntax: PASS")
