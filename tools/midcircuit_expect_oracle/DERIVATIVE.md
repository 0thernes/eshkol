# α = 0 derivative formulas

State: `|ψ(θ)⟩ = R_y(θ)|0⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩`.

No feedforward (`α = 0`). Post-prep Pauli expectations:

| Observable | `L(θ)` | `dL/dθ` |
|------------|--------|---------|
| `Z` | `cos(θ)` | `−sin(θ)` |
| `X` | `sin(θ)` | `cos(θ)` |

Derivation sketch:

- `⟨Z⟩ = |α₀|² − |α₁|² = cos²(θ/2) − sin²(θ/2) = cos(θ)`
- `⟨X⟩ = 2 Re(α₀* α₁) = 2 cos(θ/2)sin(θ/2) = sin(θ)`

Finite-difference check: central difference with `ε = 1e-6` must match
analytic `dL` within `1e-5` on the unit-test grid for both observables.

`α ≠ 0` (classical feedforward into a later rotation) remains **refused** —
see `REFUSE.md`.


## Step-size sensitivity (α = 0)

Central differences at two step sizes should agree when the analytic
derivative is smooth:

- `ε_a = 1e-6`, `ε_b = 1e-5`
- Require `|FD(ε_a) − FD(ε_b)| < 1e-4` on the unit-test θ grid for ⟨Z⟩
  (and typically ⟨X⟩).

Disagreement beyond that tol usually means ε is too large (truncation) or
too small (floating-point noise). This check does **not** apply when α ≠ 0
(refused).
