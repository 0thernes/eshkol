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
