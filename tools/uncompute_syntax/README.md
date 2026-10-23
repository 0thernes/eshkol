# Syntactic uncompute check (RFC-C MVP v0)

```bash
python3 test_check.py
```

## CLI

From `tools/`:

```
python -m uncompute_syntax --forward H,X --inverse X,H --released -o /tmp/cert.json
python -m uncompute_syntax --verify /tmp/cert.json
```

## Ancilla labels

Gates may be objects `{"op":"H","ancilla":"q2"}`. Every label that appears
must be listed in `released` (accept fixture) or the check rejects (leak).

## Certificate hash

`hash` = SHA-256 of canonical JSON (`sort_keys=True`, compact separators).
Key order in gate objects must not change the digest. `--verify` rejects
tampered hashes.
