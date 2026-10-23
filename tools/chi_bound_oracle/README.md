# χ̂ bound oracle (RFC-A MVP v0)

Standalone symbolic upper bounds for a 2-wire toy circuit.
Not wired into the Eshkol type checker.

```bash
python3 test_chi_bound.py
```

## CLI

From `tools/`:

```
python -m chi_bound_oracle chi_bound_oracle/fixtures/product_cnot_measure.json
```

Prints a step table of χ̂. Not a typechecker.
