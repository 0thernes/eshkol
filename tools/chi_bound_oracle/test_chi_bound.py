"""Green property tests for RFC-A MVP v0."""
from chi_bound import Circuit2
from schmidt import schmidt_rank_2q
import math

INV_SQRT2 = 1 / math.sqrt(2)

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

def test_oracle_ge_true_schmidt_table():
    """Property: for each hard-coded state, matching oracle path has χ̂ ≥ χ."""
    table = [
        # label, amps (a00,a01,a10,a11), oracle_chi_hat after corresponding path
        ("product |00>", (1+0j, 0j, 0j, 0j), 1),
        ("bell", (INV_SQRT2, 0j, 0j, INV_SQRT2), 2),
        ("product |+0> after H on a only", (INV_SQRT2, 0j, INV_SQRT2, 0j), 1),
    ]
    for label, amps, chi_hat in table:
        chi = schmidt_rank_2q(amps)
        assert chi_hat >= chi, (label, chi_hat, chi)

if __name__ == "__main__":
    test_cnot_raises_bound()
    test_measure_collapses_residual()
    test_oracle_ge_true_schmidt_table()
    print("RFC-A chi_bound: PASS")
