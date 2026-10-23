import math
from expect_grad import L, dL, fd_dL

def test_fd_matches_closed_form():
    for theta in (0.0, 0.3, 1.0, math.pi / 2):
        err = abs(dL(theta) - fd_dL(theta))
        assert err < 1e-5, (theta, err)

def test_known_values():
    assert abs(L(0.0) - 1.0) < 1e-12
    assert abs(dL(0.0) - 0.0) < 1e-12

if __name__ == "__main__":
    test_known_values()
    test_fd_matches_closed_form()
    print("RFC-B midcircuit_expect_oracle: PASS")
