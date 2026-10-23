# α = 0 derivative formula

State: `|ψ(θ)⟩ = R_y(θ)|0⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩`.

Z-measure: `P(1) = sin²(θ/2)`, `P(0) = cos²(θ/2)`.

With **no** feedforward (`α = 0`), post-measure ⟨Z⟩ equals the pre-measure
Born expectation:

`L(θ) = P(0)·(+1) + P(1)·(−1) = cos²(θ/2) − sin²(θ/2) = cos(θ)`.

Hence `dL/dθ = −sin(θ)`.

Finite-difference check: central difference with `ε = 1e-6` must match
within `1e-5` on the unit-test grid.
