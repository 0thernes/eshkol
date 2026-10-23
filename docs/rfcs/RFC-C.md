# RFC-C (MVP v0): Syntactic uncomputation check (ancilla liveness)

**Status:** Proposal — discussion / design artifact  
**Target repo:** `tsotchke/eshkol`  
**Branch:** `feat/rfc-C-proven-uncompute`  
**Effort estimate:** Days for the syntactic checker; weeks for a macro + LinearContext hook

## Intent

Define an achievable meaning of “proven uncompute” for MVP: **syntactic inverse of a straight-line gate list on a declared ancilla**, plus a liveness check that the ancilla is restored — **not** a quantum Hoare logic or Silq-complete automatic uncomputation.

## Precise meaning of “proven” here

Given:

- declared ancilla wire `a`
- forward fragment `F = g₁;…;gₙ` acting on `a` (and possibly others)
- user-supplied inverse fragment `F†` (or auto-derived as reverse gate order with dagger for the MVP gate set)

The checker accepts iff:

1. Every gate in `F†` is the dagger of the corresponding gate in reversed `F` (syntactic), and
2. After `F; F†`, the **ancilla use-count / ownership** model marks `a` as returned to the pool (MVP: explicit `release-zero a` sentinel required), and
3. If `a` is still live with no `release-zero`, the check **rejects**.

This is a **syntactic + ownership** obligation. It does **not** prove the residual state is `|0⟩` under arbitrary entanglement with other wires; that is a stretch goal (needs a stronger semantics).

## Non-goals

- Full automatic synthesis of inverses for arbitrary programs.
- Loops, measurement inside uncompute, or gradual-typing escapes.
- Claiming equivalence to Silq.

## Smallest mergeable artifact

1. This RFC.
2. `tools/uncompute_syntax/` — Python checker + green tests (leak rejects; matched inverse accepts).
3. Later: Scheme macro `with-uncompute` calling the same rules inside LinearContext.

## Acceptance

| ID | Criterion |
|----|-----------|
| C0 | Leak (forward without inverse/`release-zero`) → reject |
| C1 | `H a; H a; release-zero a` → accept (H is self-inverse) |
| C2 | Doc states limits (no semantic `|0⟩` proof under entanglement) |

## Open questions

1. Gate set for auto-dagger in v0 (`H,X,Y,Z,S,CNOT,…`)?
2. Must BI-3 land before trusting cross-helper uncompute?
