import math
from expect_grad import L_alpha0, dL_alpha0, fd_dL_alpha0, gradient

def test_fd_matches_closed_form():
    for theta in (0.0, 0.3, 1.0, math.pi / 2):
        err = abs(dL_alpha0(theta) - fd_dL_alpha0(theta))
        assert err < 1e-5, (theta, err)

def test_known_values():
    assert abs(L_alpha0(0.0) - 1.0) < 1e-12
    assert abs(dL_alpha0(0.0) - 0.0) < 1e-12

def test_alpha0_ok():
    r = gradient(0.3, alpha=0.0)
    assert r["ok"] is True
    assert abs(r["dL"] - dL_alpha0(0.3)) < 1e-12

def test_refuse_alpha_nonzero():
    r = gradient(0.3, alpha=0.1)
    assert r["ok"] is False
    assert r["reason"] == "pathwise-undefined"
    assert "dL" not in r  # must not smuggle a wrong number

if __name__ == "__main__":
    test_known_values()
    test_fd_matches_closed_form()
    test_alpha0_ok()
    test_refuse_alpha_nonzero()
    print("RFC-B midcircuit_expect_oracle: PASS")
