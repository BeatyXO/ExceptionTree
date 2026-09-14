# ExceptionTree

ExceptionTree is a standalone reusable GenLayer Intelligent Contract primitive for resolving natural-language rules with nested exceptions without delegating the final outcome to an LLM.

The semantic consensus job is deliberately narrow: validators independently classify whether each sealed rule node's **own condition** applies to supplied case facts as `APPLIES`, `DOES_NOT_APPLY`, or `AMBIGUOUS`. The final result is then computed deterministically from the immutable rule tree.

## Why it exists

Real policies often look like this:

- purchases within 30 days are refundable;
- **except** perishable goods;
- **except** materially defective perishables;
- **except** defects reported too late.

A generic `AI decides whether the refund is allowed` contract gives the model too much authority. ExceptionTree instead makes applicability semantic and precedence mechanical.

## Deterministic protocol

A sealed rule set contains root rules and nested exceptions. Each node has:

- immutable natural-language condition;
- `ALLOW` or `DENY` effect;
- explicit integer priority;
- parent binding and deterministic depth;
- immutable `rule_hash`.

A rule is **definitely reachable** only if its own status is `APPLIES` and every ancestor is definitely reachable. A rule is **possibly reachable** while no node on its path is `DOES_NOT_APPLY`.

Resolution then follows protocol rules, not model preference:

1. deeper reachable rules outrank shallower ones;
2. at equal depth, higher priority outranks lower priority;
3. equal-ranked opposite effects produce `CONFLICT` rather than an arbitrary tie-break;
4. an ambiguous path produces `AMBIGUOUS` only when it could change the effective outcome;
5. if no rule definitely applies, the sealed default effect is used unless a relevant ambiguous path could change it.

## Product boundary

ExceptionTree is a reusable Intelligent Contract primitive, **not a frontend or full application**. It does not verify whether the supplied case facts are true in the real world. It resolves those supplied facts against a sealed semantic rule hierarchy. Evidence/oracle systems can provide the facts; ExceptionTree provides rule/exception precedence.

## Main API

```text
create_ruleset(title, scope, default_effect)
add_root_rule(ruleset_id, label, condition_text, effect, priority)
add_exception(parent_rule_id, label, condition_text, effect, priority)
seal_ruleset(ruleset_id) -> definition_hash
submit_case(ruleset_id, case_text, expected_definition_hash)
resolve_case(case_id)

get_ruleset(...)
get_rule(...)
get_case(...)
is_outcome(case_id, expected_definition_hash, expected_case_hash, required_outcome)
is_allowed(case_id, expected_definition_hash, expected_case_hash)
```

## Consumer proof

`contracts/exception_gate.py` is a second Intelligent Contract that demonstrates typed IC-to-IC reuse. It consumes only a pinned `ALLOW` resolution and rejects replay of the same `action_hash`.

## Security properties

- rule sets are creator-controlled only while `DRAFT`;
- sealing freezes the rule definition and generates a `definition_hash`;
- cases must pin that exact hash;
- resolved cases are single-shot and cannot be re-adjudicated;
- validators independently re-run semantic applicability classification;
- malformed model output canonicalizes toward ambiguity, never a silent allow;
- equal-ranked contradictory rules surface `CONFLICT`;
- relevant semantic uncertainty surfaces `AMBIGUOUS`;
- consumer reads pin both ruleset definition and exact case hash;
- example consumer actions are replay-protected.

## Development target

Stable GenLayer Studionet only for final hosted proof:

- alias: `studionet`
- chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- explorer: `https://explorer-studio.genlayer.com`

Run `genlayer network info` before every deploy/write workflow and confirm chain ID `61999`.

## Local checks

```bash
python scripts/preflight.py
python -m compileall -q contracts tests scripts
pytest -q
```

The ZIP intentionally does **not** contain invented deployment addresses, transaction hashes, live test results, or CI claims. Those belong in `DEPLOYMENT.md` only after they are actually produced.
