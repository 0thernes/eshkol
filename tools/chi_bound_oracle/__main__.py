"""CLI: python -m chi_bound_oracle <gates.json>

2-wire (default): uses chi_after / trace.
n-wire (\"n\": 3 in JSON or --n): pairwise cut over-approx via multiwire.
Still not wired into the typechecker.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from trace import run_trace
from multiwire import run_multiwire, format_pairs


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="RFC-A χ̂ step-by-step trace (oracle only)")
    p.add_argument("gates_json", help="JSON gate list / fixture")
    p.add_argument("--chi-in", default="1,1", help="2-wire initial χ̂ (ignored if n>2)")
    p.add_argument("--n", type=int, default=None, help="override wire count")
    args = p.parse_args(argv)

    data = json.loads(Path(args.gates_json).read_text())
    gates = data["gates"] if isinstance(data, dict) else data
    n = args.n if args.n is not None else (data.get("n") if isinstance(data, dict) else 2)
    n = int(n or 2)

    if n == 2 and "n" not in (data if isinstance(data, dict) else {}):
        a_s, b_s = args.chi_in.split(",")
        chi_in = (int(a_s), int(b_s))
        print("step\top\twire\tchi_hat")
        for step, op, wire, chi in run_trace(gates, chi_in=chi_in):
            w = "-" if wire is None else str(wire)
            print(f"{step}\t{op}\t{w}\t{chi[0]},{chi[1]}")
        return 0

    print("# honesty: pairwise cut over-approx only; not a multipartite Schmidt certificate")
    print("step\top\twires\tpairs")
    for step, op, wires, pairs, _h in run_multiwire(n, gates):
        w = "-" if not wires else ",".join(str(x) for x in wires)
        print(f"{step}\t{op}\t{w}\t{format_pairs(pairs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
