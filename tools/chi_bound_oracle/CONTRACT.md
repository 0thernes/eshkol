# `chi_after` contract (RFC-A)

Pure function: `chi_after(op, chi_in, wire=0) -> chi_out`.

| `op` | Effect on `(χ̂_a, χ̂_b)` |
|------|-------------------------|
| `I`,`H`,`X`,`Y`,`Z`,`S`,`Rx`,`Ry`,`Rz` | unchanged |
| `CNOT` | `(2, 2)` |
| `MeasureZ` on wire 0 | `(0, 1)` |
| `MeasureZ` on wire 1 | `(1, 0)` |

`0` on a wire after measure means “classical / consumed,” not Schmidt rank 0.

**Not wired into the typechecker.** This table is the proposed analysis API.
