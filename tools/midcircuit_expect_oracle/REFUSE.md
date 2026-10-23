# When the expectation gradient is undefined (MVP)

## In scope (α = 0)

Circuit: `R_y(θ)|0⟩`, Z-measure, no feedforward rotation (`α = 0`).
Then `L(θ) = E[⟨Z⟩] = cos(θ)` and `dL/dθ = -sin(θ)` (closed form).

## Refuse path (α ≠ 0)

With feedforward `R_x(α)` applied when the outcome is 1, the post-measure
state depends on a discrete sample. A **pathwise** (sample-path) derivative
through the projective collapse is not defined in the usual calculus sense.

This oracle therefore **refuses** to return a numeric `dL/dθ` when `α ≠ 0`.
It returns a structured result `{ ok: false, reason: "pathwise-undefined", ... }`
instead of a silently wrong float.

Expectation-level estimators (score-function / Born-rule Jacobian) for `α ≠ 0`
are future work — not implemented here.
