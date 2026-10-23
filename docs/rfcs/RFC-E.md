# RFC-E: Self-hosting macros that invent ansatzes via Eshkol AD

**Status:** Draft — MVP scaffolding started  
**Repos:** `tsotchke/eshkol` via `0thernes/eshkol`  
**Branch:** `feat/rfc-E-ansatz-macros`  
**Related:** Frontier Idea E; moonshot F7

## 1. Problem

Variational ansatz design is human craft or external AutoML (Python). Eshkol is **homoiconic** and has **compiler-native AD**. That combination should allow macros to search a circuit AST space **at expansion/compile time**, scoring sketches with `(derivative …)` or energy oracles, and emit a concrete specialized program.

## 2. Prior art

- AutoML / NAS for quantum circuits (Python).
- Quipper-scale circuit generation without AD-in-the-macro.
- No shipping language where **compile-time macro expansion calls host AD** to invent the circuit.

## 3. Hooks

| Hook | Path |
|------|------|
| Macros | Scheme frontend / homoiconicity |
| AD | `lib/backend/autodiff_codegen.cpp` |
| VQE / H2 | `lib/agent/quantum.esk`, `examples/h2_vibrational*.esk` |
| Examples | `examples/` |

## 4. Design (MVP)

Macro `invent-ansatz` (MVP may be a **compile-time script** invoked by CI if full macro-time AD is too early):

1. Enumerate ≤16 two-qubit gate sketches from a fixed library.
2. Score each with a deterministic oracle (FD or energy at fixed θ / seeded).
3. Emit winning sketch as generated `.esk`.
4. Replay must be deterministic given seed.

True macro-time AD is the stretch; MVP proves the **search+emit** loop with a documented oracle hook shaped for AD.

## 5. MVP acceptance tests

| ID | Expect |
|----|--------|
| E1 | Search over ≤16 sketches terminates under seed |
| E2 | Emitted file typechecks / runs energy probe |
| E3 | Same seed → identical emitted AST |
| E4 | Winner beats empty/baseline sketch on oracle score |

**Scaffold:** `examples/rfc_e_ansatz_search/` script + `tests/examples/rfc_e_ansatz_seed_determinism_test.esk` (or `.sh`) red until wired.

## 6. Stretch

- Real `(derivative …)` inside expansion.
- Certificates of improvement (TYPE_FLAG_PROOF).
- Coupling to RFC-A χ constraints on sketches.

## 7. Risks

- Compile-time cost / non-reproducible macros if RNG leaks.
- Overfitting one molecule (H2).

## 8. 30 / 60 / 90

- **30d:** Enumerate+emit with classical oracle; E1/E3.
- **60d:** Hook Moonlab H2 energy; E4.
- **90d:** Macro-time AD path or documented blocker.

## 9. Open questions

1. Macro expansion vs separate `eshkol --invent-ansatz` tool for MVP?
2. Where do generated files live without dirtying the tree?
