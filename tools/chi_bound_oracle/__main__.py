"""CLI: python -m chi_bound_oracle <gates.json>

Reads a tiny gate list JSON and prints χ̂ step-by-step via chi_after.
Still not wired into the typechecker. See CONTRACT.md / DESIGN.md.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from trace import run_trace  # noqa: E402


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="RFC-A χ̂ step-by-step trace (oracle only)")
    p.add_argument("gates_json", help="JSON file: {\"gates\": [\"H\", {\"op\":\"CNOT\"}, ...]}")
    p.add_argument("--chi-in", default="1,1", help="initial χ̂ pair, default 1,1")
    args = p.parse_args(argv)

    a_s, b_s = args.chi_in.split(",")
    chi_in = (int(a_s), int(b_s))
    data = json.loads(Path(args.gates_json).read_text())
    gates = data["gates"] if isinstance(data, dict) else data

    print("step\top\twire\tchi_hat")
    for step, op, wire, chi in run_trace(gates, chi_in=chi_in):
        w = "-" if wire is None else str(wire)
        print(f"{step}\t{op}\t{w}\t{chi[0]},{chi[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
