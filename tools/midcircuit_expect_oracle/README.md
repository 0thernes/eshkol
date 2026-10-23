# Mid-circuit expectation oracle (RFC-B MVP v0)

Closed-form `E[⟨O⟩]` for `Ry(θ)|0⟩` with optional classical feedforward `α`.

- `α = 0`, `O ∈ {Z, X}`: analytic `L` and `dL/dθ` (see `DERIVATIVE.md`)
- `α ≠ 0`: structured refuse (`pathwise-undefined`) — see `REFUSE.md`

## What this is not

- **Not** Eshkol language-level AD through measure.
- **Not** an unbiased estimator for feedforward / collapse branches.
- **Not** a claim that pathwise derivatives exist when `α ≠ 0`.
- **Not** wired into Moonlab or `autodiff_codegen.cpp`.
- Finite-difference checks here only validate the **α = 0 closed form**.

## Report export

```python
from report import build_report
build_report(thetas=[0.0, 0.3], alphas=[0.0, 0.1], obs="Z")
```

Each row: `{theta, alpha, obs, ok, dL|reason}`. For later language-AD comparison.
