# χ̂ bound oracle — design note (RFC-A MVP v0)

**Status: not yet in the Eshkol typechecker.** This directory is a standalone
symbolic oracle used to nail the recurrence before any compiler work.

## Definition

For a pure bipartite state `|ψ⟩ ∈ ℂ^{d_A} ⊗ ℂ^{d_B}`, the Schmidt rank
`χ(ψ)` is `rank(ρ_A)` where `ρ_A = Tr_B(|ψ⟩⟨ψ|)`.

The oracle tracks an integer upper bound `χ̂` with `χ̂ ≥ χ(ψ)` under a
2-wire straight-line fragment.

## Recurrence (2 wires)

| Step | Update |
|------|--------|
| `alloc` / product init | `χ̂ ← 1` on each wire |
| local unitary on one wire | `χ̂` unchanged |
| `CNOT` spanning the pair (from product) | `χ̂ ← 2` on both wires |
| Z-measure one wire | residual wire: `χ̂ ← 1` |

Soundness caveat: after `CNOT`, `χ̂ = 2` even when the concrete state happens
to remain product (e.g. control in `|0⟩`). That is an intentional over-approx.

## Worked examples

1. **Product.** `alloc a,b` → `χ̂(a)=χ̂(b)=1`. True Schmidt rank of `|00⟩` is 1.
2. **Bell.** `H a; CNOT(a,b)` → oracle `χ̂=2`. True Schmidt rank of
   `(|00⟩+|11⟩)/√2` is 2.
3. **Measure-collapse.** From Bell, `measure a` → residual `χ̂(b)=1`.
   Post-measure residual is a computational-basis state (rank 1).

## Out of scope here

Typechecker integration, multipartite cuts, mixed states, Moonlab certificates.
