# Build status

Implemented in this ZIP:

- standalone ExceptionTree IC;
- immutable draft/seal rule-set lifecycle;
- root + nested exception tree;
- bounded semantic applicability consensus;
- independent validator material-status check;
- deterministic reachability/precedence/conflict/ambiguity resolver;
- definition, rule, case, assessment and resolution hashes;
- single-shot case finality;
- typed `is_outcome` / `is_allowed` consumer surface;
- replay-protected companion ExceptionGate;
- adversarial Direct Mode test suite;
- static preflight and deployment documentation.

Validation produced in this environment:

- `python scripts/preflight.py`: PASS;
- `python -m compileall -q contracts tests scripts`: PASS;
- `genvm-lint lint contracts/exceptiontree.py`: PASS (3 checks);
- `genvm-lint lint contracts/exception_gate.py`: PASS (3 checks);
- `.venv\\Scripts\\python.exe -m pytest -q`: 18 passed.

Live stable Studionet proof completed on chain `61999`: ExceptionTree deployed at
`0x59Fca84CEA0A93614Be6c11FD7F8D1F3adb8C4e6`, ExceptionGate deployed at
`0x1Ff1748b791b94b2B93D6B4F1D8a44B19CDbBBEB`, with normal five-validator
consensus. See `DEPLOYMENT.md` for the recorded hashes and outcomes.

Compatibility correction: stable GenVM 0.3.0-rc7 exposed by Direct Mode has no
`gl.emit` API. The event declarations remain as part of the contract interface,
while unsupported emission calls were removed so state transitions execute on the
stable runtime.

The packaging environment used to create this handoff did not have `gltest` installed, so Python parsing/preflight can be verified here but Direct Mode results must be produced by the implementation agent.
