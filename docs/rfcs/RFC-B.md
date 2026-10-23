# RFC-B: AD through mid-circuit measurement and classical feedforward

**Status:** Draft — MVP scaffolding started  
**Repos:** `tsotchke/eshkol` via `0thernes/eshkol`  
**Branch:** `feat/rfc-B-ad-midcircuit`  
**Related:** Frontier Idea B; moonshot F2

## 1. Problem

`(derivative …)` in Eshkol is a compiler primitive (`lib/backend/autodiff_codegen.cpp`) but **stops making sense** at projective measurement: collapse is discontinuous / stochastic. PennyLane and JAX users hit the same wall. Mid-circuit measure + classical feedforward into later gates is exactly where adaptive algorithms live — and where gradients are least defined.

## 2. Prior art

- Parameter-shift / adjoint methods for unitary circuits (Schuld et al.; PennyLane).
- Score-function / REINFORCE estimators for discrete stochastic nodes.
- Pathwise gradients invalid through nondifferentiable sample ops unless reparameterized.
- No shipping **language** that types “this measure node admits estimator E” vs “refuse pathwise”.

## 3. Hooks

| Hook | Path |
|------|------|
| AD engine | `lib/backend/autodiff_codegen.cpp`, `docs/design/AD_TAYLOR_TOWER.md` |
| Measure | `moonlab/src/quantum/measurement.h` (`measurement_single_qubit(..., random_value)`) |
| FFI | `lib/agent/quantum.esk` `measure` |
| Seeded randomness | CQM `src/math/rng.ts` pattern; Moonlab takes explicit `random_value` — perfect for replay |
| AD tests | `tests/ad/*` |

## 4. Design (MVP)

Define two AD modes through `measure`:

1. **Expectation-AD (default):** differentiate `E[f(b, θ)]` where `b ~ Bern(p(θ))` via score-function or analytic Born-rule Jacobian when available.
2. **Pathwise-AD:** **rejected** by the type/AD checker for projective measure unless an explicit `@reparam` form exists.

Feedforward: classical `Bit` used as `if` into `Rx(θ)` must appear in the reverse-mode tape as a stochastic node with declared estimator.

## 5. MVP acceptance tests

| ID | Expect |
|----|--------|
| B1 | Program: prepare Ry(θ)\|0⟩, measure, if 1 then Rx(α) else I, return ⟨Z⟩; `(derivative … θ)` defined |
| B2 | Grad matches seeded FD over many shots within tol |
| B3 | Requesting pathwise AD through measure → compile or runtime typed diagnostic |
| B4 | Fixed `random_value` sequence → deterministic replay |

**Scaffold:** `tests/ad/rfc_b_midcircuit_measure_gradient_test.esk` (red) + harness note.

## 6. Stretch

- Nested AD through two measure points.
- Entangled mid-circuit measure.
- Integration with RFC-A χ collapse.

## 7. Risks

- Silent wrong gradients worse than none.
- Variance explosion of score-function estimators.
- Mixing dual-number forward mode with stochastic nodes incorrectly.

## 8. 30 / 60 / 90

- **30d:** Spec + FD oracle harness + B3 refuse path.
- **60d:** B1/B2 green on 1-qubit toy.
- **90d:** Nested case; docs in AD_TAYLOR_TOWER.md.

## 9. Open questions

1. Forward-mode duals vs reverse tape for score-function?
2. Shot budget in the type of `Estimator`?
3. Shared seeded RNG API across Eshkol/Moonlab?
