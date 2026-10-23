# RFC-A: Entanglement-indexed dependent linear types

**Status:** Draft — MVP scaffolding started  
**Repos:** `tsotchke/eshkol` (work via `0thernes/eshkol` fork)  
**Branch:** `feat/rfc-A-entanglement-linear`  
**Authors:** Alex Donahue / Grok Bot collaborator  
**Related:** Page audit §25 Frontier Ideas A; moonshots F1

## 1. Problem

Eshkol already enforces **no-cloning** via `Qubit` + `TYPE_FLAG_LINEAR` (`inc/eshkol/types/hott_types.h`). That rejects `(cons q q)` but says nothing about **entanglement topology**. After a Bell prep, both qubits are entangled; a type that still looks like an independent `Qubit` cannot express “this wire is correlated with that one” or “Schmidt rank across cut C is ≤ k”.

Resource-theory and entanglement theory treat Schmidt rank, entanglement of formation, and cut entanglement as first-class quantities. Languages (Q#, Silq, Quipper) do not track them in the type system of a shipping compiler.

## 2. Prior art

- Linear / affine quantum types: Selinger & Valiron, Green et al.; Silq (qfree/const); Q# qubit ownership.
- Dependent / refinement types for resources: academic (Proto-Quipper variants, QWIRE) — not gradual + AD + AOT LLVM.
- Moonlab already **computes** bipartite measures (`moonlab/src/quantum/entanglement.h`: Schmidt, concurrence, EoF).
- Nobody ships **compile-time χ / cut bounds refined by CNOT and measure** in a gradual industrial language.

## 3. Hooks in this tree

| Hook | Path |
|------|------|
| Linear `Qubit` | `inc/eshkol/types/hott_types.h` (`TypeId Qubit`, `TYPE_FLAG_LINEAR`) |
| Linear analysis | `lib/types/type_checker.cpp` (`LinearContext`), `lib/types/linear_check_bridge.cpp` |
| Regression bed | `tests/typesystem/qubit_*.esk` (37 fixtures) |
| Runtime measures | `moonlab/src/quantum/entanglement.h` / `.c` |
| FFI surface today | `lib/agent/quantum.esk` (still i64 handles — out of MVP scope but future consumer) |

## 4. Type / IR design (MVP)

Introduce a **refinement** (initially phantom / proof-erased):

```text
Qubit                    ; existing
Qubit[χ≤k]               ; upper bound on Schmidt rank vs a named cut (MVP: implicit bipartition tag)
```

Rules (MVP, pure bipartition, compile-time symbolic only):

1. Fresh `alloc` → `Qubit[χ≤1]` (product / separable w.r.t. empty cut).
2. `cnot : (Qubit[χ≤a], Qubit[χ≤b]) → (Qubit[χ≤a+b], Qubit[χ≤a+b])` (sound over-approx).
3. Local Pauli/H/phase preserve χ.
4. `measure : Qubit[χ≤k] → Bit` and residual partner collapses to `Qubit[χ≤1]` when k was raised only by that pair (MVP: tagged pair id).
5. Reject ops annotated `@product-only` when χ>1.

`TYPE_FLAG_PROOF` carries χ; erased at runtime for MVP (no runtime tax). Later: optional runtime assert vs Moonlab Schmidt.

## 5. MVP acceptance tests

| ID | Expect |
|----|--------|
| A1 | Bell-prep program types both outputs as χ≥2 (or χ≤2 with lower bound ghost) |
| A2 | Applying `@product-only` local op to χ≥2 **fails compile** |
| A3 | After measure on one Bell half, partner types as χ≤1 |
| A4 | Existing `qubit_no_cloning_test.esk` still fails for clone |
| A5 | Doc: χ is an **upper bound**; mixed/approximate states out of scope |

**Scaffold:** red tests under `tests/typesystem/rfc_a_*.esk` encoding A2/A3; stub `docs/rfcs/RFC-A.md` in-tree copy optional.

## 6. Stretch goals

- Multipartite cuts; automatic χ inference for Clifford fragments (ties RFC-V).
- Runtime χ certificates via `entanglement.h`.
- Wire into typed `agent.quantum` once linear Qubit FFI exists.

## 7. Risks

- Undecidability / gradual holes (BI-3 laundering still open).
- False confidence if χ is only a coarse upper bound.
- Annotation burden vs inference.

## 8. 30 / 60 / 90 day plan

- **30d:** Phantom syntax + A2 red→green on one Bell pattern; design doc frozen.
- **60d:** Measure collapse rule A3; CNOT refinement; 10 fixtures.
- **90d:** Optional runtime check vs Moonlab Schmidt on CI; ADR.

## 9. Open questions

1. Syntax: `Qubit[χ≤2]` vs `(Qubit χ 2)` vs ghost parameter?
2. Cut naming: implicit pair-id vs explicit `Cut` type?
3. Interaction with BI-3 — must BI-3 land first?

## 10. Draft GitHub issue body

See branch `feat/rfc-A-entanglement-linear` and `/workspace/cqm-audit/rfcs/RFC-A.md`.
