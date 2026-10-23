"""Green property tests for RFC-A MVP v0."""
from chi_bound import Circuit2

def test_cnot_raises_bound():
    c = Circuit2()
    assert c.a.chi_hat == 1 and c.b.chi_hat == 1
    c.local("a")
    c.cnot()
    assert c.a.chi_hat == 2 and c.b.chi_hat == 2

def test_measure_collapses_residual():
    c = Circuit2()
    c.cnot()
    c.measure("a")
    assert c.b.chi_hat == 1

if __name__ == "__main__":
    test_cnot_raises_bound()
    test_measure_collapses_residual()
    print("RFC-A chi_bound: PASS")
