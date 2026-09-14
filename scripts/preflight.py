from __future__ import annotations

import ast
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = [ROOT / "contracts" / "exceptiontree.py", ROOT / "contracts" / "exception_gate.py"]
PIN = "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6"

errors: list[str] = []
for path in CONTRACTS:
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")
        continue
    source = path.read_text(encoding="utf-8")
    try:
        ast.parse(source)
    except SyntaxError as exc:
        errors.append(f"syntax error in {path.name}: {exc}")
    if PIN not in source:
        errors.append(f"unexpected py-genlayer dependency pin in {path.name}")

core = CONTRACTS[0].read_text(encoding="utf-8") if CONTRACTS[0].exists() else ""
for marker in [
    "run_nondet_unsafe",
    "CLASSIFY APPLICABILITY",
    "deterministic_resolve",
    "create_ruleset",
    "add_exception",
    "seal_ruleset",
    "submit_case",
    "resolve_case",
    "definition_hash",
    "resolution_hash",
    "is_outcome",
]:
    if marker not in core:
        errors.append(f"core contract missing required marker: {marker}")

if (ROOT / "frontend").exists():
    errors.append("frontend directory present; ExceptionTree is a standalone Intelligent Contract primitive")

for forbidden in ["subprocess", "import os", "import sys"]:
    if forbidden in core:
        errors.append(f"forbidden/suspicious contract import marker: {forbidden}")

final_mode = "--final" in sys.argv
if final_mode:
    deployment = (ROOT / "DEPLOYMENT.md").read_text(encoding="utf-8") if (ROOT / "DEPLOYMENT.md").exists() else ""
    for placeholder in ["FINAL_EXCEPTIONTREE_ADDRESS", "FINAL_EXCEPTION_GATE_ADDRESS"]:
        if placeholder in deployment:
            errors.append(f"final preflight still contains deployment placeholder: {placeholder}")

if errors:
    print("PREFLIGHT FAIL")
    for error in errors:
        print(" -", error)
    sys.exit(1)

print("PREFLIGHT PASS")
print(" - contract Python parses")
print(" - dependency pins present")
print(" - consensus + deterministic resolver markers present")
print(" - typed consumer/replay protection present")
print(" - no frontend directory")
if final_mode:
    print(" - deployment placeholders removed")
print("Next: run pytest and GenVM lint in a GenLayer development environment.")
