"""Green property tests for RFC-A MVP v0."""
from chi_bound import Circuit2
from chi_after import chi_after
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
    table = [
        ("product |00>", (1+0j, 0j, 0j, 0j), 1),
        ("bell", (INV_SQRT2, 0j, 0j, INV_SQRT2), 2),
        ("product |+0> after H on a only", (INV_SQRT2, 0j, INV_SQRT2, 0j), 1),
    ]
    for label, amps, chi_hat in table:
        chi = schmidt_rank_2q(amps)
        assert chi_hat >= chi, (label, chi_hat, chi)

def test_chi_after_locals_preserve():
    assert chi_after("H", (1, 1), wire=0) == (1, 1)
    assert chi_after("X", (2, 2), wire=1) == (2, 2)

def test_chi_after_cnot():
    assert chi_after("CNOT", (1, 1)) == (2, 2)
    assert chi_after("CNOT", (2, 2)) == (2, 2)

def test_chi_after_measure():
    assert chi_after("MeasureZ", (2, 2), wire=0) == (0, 1)
    assert chi_after("MeasureZ", (2, 2), wire=1) == (1, 0)

def test_chi_after_matches_circuit2_path():
    # alloc product -> H -> CNOT -> MeasureZ(a)
    s = (1, 1)
    s = chi_after("H", s, 0)
    s = chi_after("CNOT", s)
    assert s == (2, 2)
    s = chi_after("MeasureZ", s, 0)
    assert s == (0, 1)

if __name__ == "__main__":
    test_cnot_raises_bound()
    test_measure_collapses_residual()
    test_oracle_ge_true_schmidt_table()
    test_chi_after_locals_preserve()
    test_chi_after_cnot()
    test_chi_after_measure()
    test_chi_after_matches_circuit2_path()
    print("RFC-A chi_bound: PASS")
