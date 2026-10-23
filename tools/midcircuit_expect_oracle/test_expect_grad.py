import math
from expect_grad import L_alpha0, dL_alpha0, fd_dL_alpha0, gradient

def test_fd_matches_closed_form_tight():
    """α=0: analytic dL/dθ = -sin(θ) vs central FD (ε=1e-6), tol 1e-5."""
    for theta in (0.0, 0.3, 1.0, math.pi / 2, 2.0):
        analytic = dL_alpha0(theta)
        fd = fd_dL_alpha0(theta, eps=1e-6)
        err = abs(analytic - fd)
        assert err < 1e-5, (theta, analytic, fd, err)
        # also matches -sin(θ) exactly
        assert abs(analytic - (-math.sin(theta))) < 1e-15

def test_known_values():
    assert abs(L_alpha0(0.0) - 1.0) < 1e-12
    assert abs(dL_alpha0(0.0) - 0.0) < 1e-12
    assert abs(L_alpha0(math.pi / 2) - 0.0) < 1e-12

def test_alpha0_ok():
    r = gradient(0.3, alpha=0.0)
    assert r["ok"] is True
    assert abs(r["dL"] - dL_alpha0(0.3)) < 1e-12

def test_refuse_alpha_nonzero():
    r = gradient(0.3, alpha=0.1)
    assert r["ok"] is False
    assert r["reason"] == "pathwise-undefined"
    assert "dL" not in r

if __name__ == "__main__":
    test_known_values()
    test_fd_matches_closed_form_tight()
    test_alpha0_ok()
    test_refuse_alpha_nonzero()
    print("RFC-B midcircuit_expect_oracle: PASS")
