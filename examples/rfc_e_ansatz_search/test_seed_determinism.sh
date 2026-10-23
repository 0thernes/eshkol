#!/usr/bin/env bash
# RFC-E E3: same seed → identical emitted AST
set -euo pipefail
DIR=$(cd "$(dirname "$0")" && pwd)
python3 "$DIR/invent_ansatz.py" --seed 7 --out /tmp/rfc_e_a.esk
python3 "$DIR/invent_ansatz.py" --seed 7 --out /tmp/rfc_e_b.esk
diff -u /tmp/rfc_e_a.esk /tmp/rfc_e_b.esk
echo "RFC-E E3 PASS: deterministic emit"
