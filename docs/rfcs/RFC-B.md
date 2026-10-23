# RFC-B (MVP v0): Gradients of expectations through mid-circuit measure (classical oracle)

**Status:** Proposal — discussion / design artifact  
**Target repo:** `tsotchke/eshkol`  
**Branch:** `feat/rfc-B-ad-midcircuit`  
**Effort estimate:** Days for the oracle; weeks for a language-level estimator behind a flag

## Intent

Clarify **what is mathematically defined** when differentiating through mid-circuit measurement, and ship a **classical 1-qubit oracle** that matches finite differences. This does **not** claim Eshkol `(derivative …)` already works through `measure`.

## Precise math (MVP)

Circuit:

1. Prepare `|ψ(θ)⟩ = R_y(θ)|0⟩` (real amplitudes: `cos(θ/2)|0⟩ + sin(θ/2)|1⟩`).
2. Measure in Z basis → bit `b ~ Bern(p)` with `p = sin²(θ/2)`.
3. If `b = 1`, apply `R_x(α)`; else identity. (Feedforward; for the MVP loss we use a simple post-measure observable.)

**MVP loss (expectation only):** `L(θ) = E[⟨Z⟩ after feedforward]`.

For the special case `α = 0` (no feedforward rotation), `L(θ) = 1 - 2p = cos(θ)`, so `dL/dθ = -sin(θ)`.

**Defined:** derivatives of **expectations** `d/dθ E[f(b,θ)]` (score-function or closed form when available).  
**Undefined / refused in MVP:** pathwise (sample-path) derivatives through projective collapse.

## Non-goals

- No change to `autodiff_codegen.cpp` in this MVP.
- No claim of parity with PennyLane or nested AD through multiple measures.
- No entangled mid-circuit measure.

## Smallest mergeable artifact

1. This RFC.
2. `tools/midcircuit_expect_oracle/` — pure Python: closed-form `L`, `dL/dθ`, and FD check (green).
3. Later: document a refuse-path if `(derivative …)` meets `measure` (compiler PR, separate).

## Acceptance

| ID | Criterion |
|----|-----------|
| B0 | `|dL_closed - dL_FD| < 1e-5` on a fixed θ grid (`α=0`) |
| B1 | README states pathwise AD is out of scope |

## Open questions

1. Which estimator to prototype first in-compiler (score-function vs analytic Born)?
2. Seeded `random_value` API alignment with Moonlab?
