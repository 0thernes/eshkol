# RFC-A (MVP v0): Symbolic Schmidt-rank upper bounds (design + oracle)

**Status:** Proposal — discussion / design artifact  
**Target repo:** `tsotchke/eshkol` (reference branch on `0thernes/eshkol`)  
**Branch:** `feat/rfc-A-entanglement-linear`  
**Effort estimate:** 1–2 weeks for a first checker hook; this MVP is docs + a standalone oracle (days)

## Intent (one sentence)

Record a **sound over-approximation** of bipartite Schmidt-rank upper bounds (`χ`) for a tiny gate language, as a stepping stone toward optional type refinements — **not** a claim that Eshkol already tracks entanglement in the type checker.

## Precise definition (MVP)

For a pure bipartite state `|ψ⟩ ∈ ℂ² ⊗ ℂ²` (extend componentwise later), the **Schmidt rank** `χ(ψ)` is the rank of the reduced density matrix `ρ_A = Tr_B(|ψ⟩⟨ψ|)`.

We track only an **integer upper bound** `χ̂ ≥ χ(ψ)` under these rules (straight-line, pure, two wires):

| Op | Rule |
|----|------|
| `alloc` / `|0⟩` | `χ̂ := 1` |
| local unitary on one wire (`H`,`X`,`Y`,`Z`,`R_x/y/z`) | `χ̂` unchanged |
| `CNOT` (control, target) when both wires start with `χ̂=1` and are the full system | `χ̂ := 2` (Bell-capable; sound over-approx even if state remains product for some inputs) |
| computational-basis `measure` on one wire of a 2-wire system | residual wire: `χ̂ := 1` |

These rules are **sound but coarse**: they never under-report entanglement after CNOT; they may over-report.

## Non-goals (explicit)

- No dependent/`Qubit[χ≤k]` syntax in the compiler in this MVP.
- No multipartite cuts, mixed states, approximate entanglement, or runtime Moonlab certificates.
- No claim that this “beats” Q#/Silq or closes BI-3.
- No changes to `quantum.esk` FFI typing.

## Smallest mergeable artifact

1. This RFC under `docs/rfcs/` (or an Issue body).
2. A **standalone** Python oracle + tests (`tools/chi_bound_oracle/`) that encode the table above and pass on Bell + measure.
3. Optional later PR: plumb `χ̂` as a side map in the type checker behind a flag — **separate** review.

## Acceptance (MVP v0)

| ID | Criterion |
|----|-----------|
| A0 | Oracle: two alloc → CNOT → `χ̂ == 2` |
| A1 | Oracle: after measure one wire → residual `χ̂ == 1` |
| A2 | Doc lists non-goals and soundness caveat |

## Risks

Maintainers may prefer this stay an Issue until a flagged checker hook exists. That is fine.

## Open questions for maintainers

1. Prefer Issue-only vs a docs-only PR?
2. Should `χ̂` live next to `LinearContext` or as a separate analysis pass?
