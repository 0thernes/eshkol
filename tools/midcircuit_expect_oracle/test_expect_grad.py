import math
from expect_grad import L_alpha0, dL_alpha0, fd_dL_alpha0, gradient

def test_fd_matches_closed_form_Z():
    """α=0, ⟨Z⟩: analytic dL/dθ = -sin(θ) vs central FD."""
    for theta in (0.0, 0.3, 1.0, math.pi / 2, 2.0):
        analytic = dL_alpha0(theta, "Z")
        fd = fd_dL_alpha0(theta, "Z", eps=1e-6)
        assert abs(analytic - fd) < 1e-5, (theta, analytic, fd)
        assert abs(analytic - (-math.sin(theta))) < 1e-15

def test_fd_matches_closed_form_X():
    """α=0, ⟨X⟩: analytic dL/dθ = cos(θ) vs central FD."""
    for theta in (0.0, 0.3, 1.0, math.pi / 2, 2.0):
        analytic = dL_alpha0(theta, "X")
        fd = fd_dL_alpha0(theta, "X", eps=1e-6)
        assert abs(analytic - fd) < 1e-5, (theta, analytic, fd)
        assert abs(analytic - math.cos(theta)) < 1e-15
        assert abs(L_alpha0(theta, "X") - math.sin(theta)) < 1e-15

def test_known_values():
    assert abs(L_alpha0(0.0, "Z") - 1.0) < 1e-12
    assert abs(dL_alpha0(0.0, "Z") - 0.0) < 1e-12
    assert abs(L_alpha0(math.pi / 2, "Z") - 0.0) < 1e-12
    assert abs(L_alpha0(0.0, "X") - 0.0) < 1e-12
    assert abs(L_alpha0(math.pi / 2, "X") - 1.0) < 1e-12
    assert abs(dL_alpha0(0.0, "X") - 1.0) < 1e-12

def test_alpha0_ok_both_obs():
    for obs in ("Z", "X"):
        r = gradient(0.3, alpha=0.0, obs=obs)
        assert r["ok"] is True
        assert r["obs"] == obs
        assert abs(r["dL"] - dL_alpha0(0.3, obs)) < 1e-12

def test_refuse_alpha_nonzero_both_obs():
    for obs in ("Z", "X"):
        r = gradient(0.3, alpha=0.1, obs=obs)
        assert r["ok"] is False
        assert r["reason"] == "pathwise-undefined"
        assert "dL" not in r

if __name__ == "__main__":
    test_known_values()
    test_fd_matches_closed_form_Z()
    test_fd_matches_closed_form_X()
    test_alpha0_ok_both_obs()
    test_refuse_alpha_nonzero_both_obs()
    print("RFC-B midcircuit_expect_oracle: PASS")
