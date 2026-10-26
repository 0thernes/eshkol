# 0thernes Eshkol development fork

This is the development fork at [0thernes/eshkol](https://github.com/0thernes/eshkol),
derived from [tsotchke/eshkol](https://github.com/tsotchke/eshkol).
The upstream MIT license and copyright notice are preserved in [LICENSE](LICENSE).

The primary branch is `master`. Local development uses `origin` for this fork
and `upstream` for the original repository. Changes developed for this version
are committed locally and pushed to the fork. An upstream contribution is a
separate action; existing upstream pull requests remain available for review.

## Initial fork baseline

The integration starts from upstream commit
`341ac812ed600fd9d27c28e9509d66ab71363947` (`v1.3.6-evolve`) and includes:

| Area | Included changes | Upstream review |
|---|---|---|
| Windows native runtime | JIT worker initialization, unwind table lifetime, saved-stack continuation restoration, optional-runtime exports and valid VM test registration | [#869](https://github.com/tsotchke/eshkol/pull/869) |
| Numerical differentiation | Cross-entropy reverse tape connectivity and tensor cotangents, with explicit refusals for unsupported loss derivatives | [#871](https://github.com/tsotchke/eshkol/pull/871) |
| Quantum interoperability | Validated static circuits, a 25-gate OpenQASM 3 export subset, logical resource counts and independent oracle tests | [#872](https://github.com/tsotchke/eshkol/pull/872) |
| Website and documentation | Correct setup commands and numerical/memory claims, with the matching compiled site artifact | [#870](https://github.com/tsotchke/eshkol/pull/870) |

The compiler integration at `2de351cbf49c2851e904e87937e4e10e87b53780`
passed 14 focused CTest cases on Windows x64 with LLVM/ClangCL 21.1.8 in a CPU
configuration. The independent quantum oracle checked 134 exports, including
100 generated circuits and every supported gate kind. Its compiler executable
SHA256 was `0fcf6b75f025a32a8465f42a6e92e6da6b7241277b0b74961262767bdc92cd44`.
The fork setup adds documentation and workflow changes to that integration;
these historical measurements are not a new full release qualification.

Use the checked-in test drivers and documentation to reproduce the relevant
claims in a supported native build:

```sh
ctest --test-dir build --output-on-failure -R 'windows_jit_regressions|jit_parallel_init_test|jit_windows_x64_unwind_test|windows_x64_continuation_restore_test|cross_entropy_gradient_|tensor_backward_dual_impl_gradcheck|qllm_bridge_gradcheck|quantum_circuit_export_'
```

The Windows-specific cases require Windows x64. The independent quantum
oracle is opt-in and requires its documented Python packages. See the
[circuit reference](docs/reference/stdlib/quantum_circuit.md),
[loss differentiation contract](docs/reference/tensors/loss-autodiff.md), and
[Windows regression notes](tests/toolchain/native_jit_regressions/README.md).

The full release matrix, CUDA qualification, Windows ARM64, CET-specific
continuation policies, full VM parity and ICC readiness remain separate work.
This fork has not demonstrated physical QPU execution or quantum advantage.

## Research and development program

The [25-system comparison and 100-target roadmap](docs/reports/quantum-2026-10-25/quantum-landscape.md)
includes acceptance criteria, sources and dependencies, with
[CSV](docs/reports/quantum-2026-10-25/quantum-targets.csv) and
[JSON](docs/reports/quantum-2026-10-25/quantum-landscape.json) versions.
It distinguishes foundations, parity work, advanced capabilities and open
research. The targets are not all implemented, and no universal performance
ranking is claimed.

## Fork website and automation

The inherited website still references the upstream project and its
`eshkol.ai` domain. Site validation remains active, but the Pages publishing
steps run only in the upstream repository. Publishing this fork's own website
requires a deliberate domain/URL configuration change.

The API documentation workflow uses the standard GitHub Actions bot identity
for its generated commits. It does not attribute automated fork updates to the
upstream author. The existing identity checks and the MIT attribution remain
in place.
