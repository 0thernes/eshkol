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

def test_cli_golden_product_cnot_measure():
    """product → CNOT → χ̂=2 → MeasureZ → residual χ̂=1 (wire1)."""
    from pathlib import Path
    import json
    from trace import run_trace

    fixture = Path(__file__).resolve().parent / "fixtures" / "product_cnot_measure.json"
    data = json.loads(fixture.read_text())
    steps = list(run_trace(data["gates"], chi_in=(1, 1)))
    assert steps[0][3] == (1, 1)  # init
    assert steps[1][3] == (1, 1)  # H
    assert steps[2][3] == (2, 2)  # CNOT
    assert steps[3][3] == (0, 1)  # MeasureZ wire0
    assert list(steps[3][3]) == data["expect_final"]


def test_ghz3_pairwise_fixture():
    """3-wire GHZ-prep sketch: pairwise over-approx; (1|2) stays 1 (documented)."""
    from pathlib import Path
    import json
    from multiwire import run_multiwire, format_pairs

    fixture = Path(__file__).resolve().parent / "fixtures" / "ghz3_pairwise.json"
    data = json.loads(fixture.read_text())
    steps = list(run_multiwire(data["n"], data["gates"]))
    final = steps[-1][3]
    got = {f"{i}|{j}": v for (i, j), v in final.items()}
    assert got == data["expect_pairs_final"], (got, data["expect_pairs_final"])
    # honesty string present on every step
    assert "over-approx" in steps[-1][4]
    # CLI-ish format non-empty
    assert "0|1=2" in format_pairs(final)


def test_ghz3_walk_json_export():
    """JSON walk: steps + final_cuts + honesty_flags match golden GHZ fixture."""
    from pathlib import Path
    import json
    from multiwire import walk_to_json

    gates_fix = Path(__file__).resolve().parent / "fixtures" / "ghz3_pairwise.json"
    golden = Path(__file__).resolve().parent / "fixtures" / "ghz3_walk_export.json"
    data = json.loads(gates_fix.read_text())
    expect = json.loads(golden.read_text())
    got = walk_to_json(data["n"], data["gates"])
    assert got["schema"] == expect["schema"]
    assert got["n"] == expect["n"]
    assert got["honesty_flags"] == expect["honesty_flags"]
    assert got["final_cuts"] == expect["final_cuts"]
    assert len(got["steps"]) == 1 + len(data["gates"])  # init + gates
    assert got["steps"][-1]["cuts"] == expect["final_cuts"]
    assert "pairwise" in got["steps"][0]["honesty"]


if __name__ == "__main__":
    test_cnot_raises_bound()
    test_measure_collapses_residual()
    test_oracle_ge_true_schmidt_table()
    test_chi_after_locals_preserve()
    test_chi_after_cnot()
    test_chi_after_measure()
    test_chi_after_matches_circuit2_path()
    test_cli_golden_product_cnot_measure()
    test_ghz3_pairwise_fixture()
    test_ghz3_walk_json_export()
    print("RFC-A chi_bound: PASS")
