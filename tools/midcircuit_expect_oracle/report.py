"""Tiny JSON report grid for α=0 / α≠0 cases (RFC-B).

Useful later for comparing language-level AD against this oracle.
"""
from __future__ import annotations
import json
from typing import Any, Dict, List, Sequence
from expect_grad import gradient


def build_report(
    thetas: Sequence[float],
    alphas: Sequence[float],
    obs: str = "Z",
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for theta in thetas:
        for alpha in alphas:
            r = gradient(float(theta), float(alpha), obs=obs)  # type: ignore[arg-type]
            row: Dict[str, Any] = {
                "theta": float(theta),
                "alpha": float(alpha),
                "obs": obs,
                "ok": bool(r["ok"]),
            }
            if r["ok"]:
                row["dL"] = float(r["dL"])
                row["L"] = float(r["L"])
            else:
                row["reason"] = r["reason"]
            rows.append(row)
    return {
        "schema": "rfc-b-midcircuit-expect-report-v0",
        "obs": obs,
        "rows": rows,
    }


def report_json(
    thetas: Sequence[float],
    alphas: Sequence[float],
    obs: str = "Z",
) -> str:
    return json.dumps(build_report(thetas, alphas, obs), indent=2, sort_keys=True)
