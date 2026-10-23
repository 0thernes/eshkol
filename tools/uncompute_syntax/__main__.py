"""CLI: issue or verify syntactic uncompute certificates.

  python -m uncompute_syntax --forward H,X --inverse X,H --released
  python -m uncompute_syntax --forward H,X --inverse X,H --released -o cert.json
  python -m uncompute_syntax --verify cert.json

Still syntactic only. See docs/rfcs/RFC-C.md.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from certificate import issue_certificate, verify_certificate  # noqa: E402


def _split_gates(s: str):
    return [g.strip() for g in s.split(",") if g.strip()]


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="RFC-C syntactic uncompute certificate CLI")
    p.add_argument("--verify", metavar="FILE", help="verify an existing certificate JSON")
    p.add_argument("--forward", help="comma-separated forward gates, e.g. H,X")
    p.add_argument("--inverse", help="comma-separated inverse gates, e.g. X,H")
    p.add_argument("--released", action="store_true", help="ancilla release-zero'd")
    p.add_argument("-o", "--output", help="write certificate JSON to file (default stdout)")
    args = p.parse_args(argv)

    if args.verify:
        cert = json.loads(Path(args.verify).read_text())
        verify_certificate(cert)
        print("OK", cert.get("hash", "")[:16] + "…")
        return 0

    if not args.forward or not args.inverse:
        p.error("issue mode requires --forward and --inverse (or use --verify)")
    if not args.released:
        p.error("issue mode requires --released (MVP refuses missing release-zero)")

    cert = issue_certificate(_split_gates(args.forward), _split_gates(args.inverse), released=True)
    blob = json.dumps(cert, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(blob)
        print(f"wrote {args.output}")
    else:
        sys.stdout.write(blob)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
