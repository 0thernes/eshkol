# RFC-C: Type-checker-proven uncomputation synthesis

**Status:** Draft — MVP scaffolding started  
**Repos:** `tsotchke/eshkol` via `0thernes/eshkol`  
**Branch:** `feat/rfc-C-proven-uncompute`  
**Related:** Frontier Idea C; moonshot F3

## 1. Problem

Uncomputation (restore ancillas to \|0⟩) is either manual (Q# `Adjoint`) or academic sugar (Silq). Eshkol has the ingredients for **proof-obligated** uncomputation: linear use analysis + `TYPE_FLAG_PROOF` + macros — but no `with-uncompute` that the checker verifies.

## 2. Prior art

- Silq automatic uncomputation; Q# adjoint functors; reversible computing (Bennett).
- Proof-carrying / refinement approaches rare in QC langs.

## 3. Hooks

| Hook | Path |
|------|------|
| Linear analysis | `lib/types/type_checker.cpp` `LinearContext` |
| Proof flag | `TYPE_FLAG_PROOF` in `hott_types.h` |
| VM parity bridge | `lib/types/linear_check_bridge.cpp` |
| Macros | Scheme frontend |
| Fixtures | `tests/typesystem/qubit_*` |

## 4. Design (MVP)

```scheme
(with-uncompute ((a : Qubit (alloc)))
  ;; body may use a
  ;; checker requires a consumed by an inverse path returning |0⟩
  ...)
```

MVP: **verify** user-supplied inverse (not full synthesis). Synthesis is stretch.

Rules:

1. Ancilla live at end of block without uncompute → **compile fail**.
2. Explicit `(uncompute-adjoint body-fragment)` must type as returning ancilla to zero state (ghost `Zero` refinement).
3. Emit `TYPE_FLAG_PROOF` certificate erased at runtime.

## 5. MVP acceptance tests

| ID | Expect |
|----|--------|
| C1 | Leaky ancilla `with-uncompute` **fails compile** |
| C2 | Textbook ancilla-AND / compute-uncompute pattern **succeeds** |
| C3 | Existing no-cloning fixtures unchanged |
| C4 | Certificate artifact (sidecar or comment) present in compile log under flag |

**Scaffold:** `tests/typesystem/rfc_c_uncompute_leak_fail_test.esk` (EXPECT-COMPILE: fail) + `rfc_c_uncompute_ok_test.esk` (red until macro exists).

## 6. Stretch

- Synthesize inverse for straight-line unitary blocks.
- Interaction with RFC-A χ.
- Mid-circuit measure inside uncompute = reject.

## 7. Risks

- Incompleteness mistaken for unsoundness.
- Macro hygiene / scope bugs creating false greens.

## 8. 30 / 60 / 90

- **30d:** Surface macro + C1 green (fail correctly).
- **60d:** C2 green for one textbook pattern.
- **90d:** Mini synthesis for Clifford+T fragment.

## 9. Open questions

1. Is `Zero` a refinement of `Qubit` or a separate type?
2. Must BI-3 land before trusting uncompute across helpers?
