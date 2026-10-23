"""CLI: python -m chi_bound_oracle <gates.json> [--json]

2-wire (default): uses chi_after / trace.
n-wire ("n": 3 in JSON or --n): pairwise cut over-approx via multiwire.
--json: emit machine-readable walk (steps, final_cuts, honesty_flags).
Still not wired into the typechecker.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from trace import run_trace
from multiwire import run_multiwire, format_pairs, walk_to_json


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="RFC-A χ̂ step-by-step trace (oracle only)")
    p.add_argument("gates_json", help="JSON gate list / fixture")
    p.add_argument("--chi-in", default="1,1", help="2-wire initial χ̂ (ignored if n>2)")
    p.add_argument("--n", type=int, default=None, help="override wire count")
    p.add_argument("--json", action="store_true", help="emit JSON walk export")
    args = p.parse_args(argv)

    data = json.loads(Path(args.gates_json).read_text())
    gates = data["gates"] if isinstance(data, dict) else data
    n = args.n if args.n is not None else (data.get("n") if isinstance(data, dict) else 2)
    n = int(n or 2)

    use_multi = n > 2 or (isinstance(data, dict) and "n" in data)

    if args.json:
        if use_multi:
            out = walk_to_json(n, gates)
        else:
            # 2-wire JSON via trace wrapped similarly
            a_s, b_s = args.chi_in.split(",")
            chi_in = (int(a_s), int(b_s))
            steps = []
            final = None
            for step, op, wire, chi in run_trace(gates, chi_in=chi_in):
                cuts = {"0|1": max(chi)} if step == 0 else {"0": chi[0], "1": chi[1]}
                # keep simple 2-wire representation
                entry = {
                    "step": step,
                    "op": op,
                    "wires": [] if wire is None else [wire],
                    "chi_hat": list(chi),
                }
                steps.append(entry)
                final = list(chi)
            out = {
                "schema": "rfc-a-chi-walk-v0",
                "n": 2,
                "honesty_flags": ["two_wire_chi_after", "not_in_typechecker"],
                "steps": steps,
                "final_chi_hat": final,
            }
        sys.stdout.write(json.dumps(out, indent=2, sort_keys=True) + "\n")
        return 0

    if not use_multi:
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
