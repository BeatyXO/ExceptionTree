# Architecture

## Separation of responsibilities

ExceptionTree deliberately splits semantic judgment from protocol resolution.

### GenLayer consensus decides

For each immutable rule node, validators independently classify only the node's own condition against the submitted case facts:

- `APPLIES`
- `DOES_NOT_APPLY`
- `AMBIGUOUS`

The leader returns a canonical applicability vector. Validators independently run the same bounded classification and reject a materially different vector.

### Deterministic code decides

The contract computes ancestor reachability, exception depth, priority, contradictory ties, relevant ambiguity, final outcome, winning rule, hashes, and consumer assertions.

The model never outputs `ALLOW`, `DENY`, `CONFLICT`, a winning rule ID, or an override decision.

## Rule-tree model

Every root is depth 0. Each exception references an already-existing parent in the same rule set, so cycles cannot be created. Child depth is parent depth + 1 and is bounded.

The hierarchy is therefore immutable and acyclic by construction.

## Precedence

For definitely reachable nodes, rank is `(depth, priority)` and higher is stronger.

- deeper beats shallower;
- same depth + higher priority beats lower priority;
- same depth + same priority + opposite effects => `CONFLICT`;
- same depth + same priority + same effect => deterministic lowest rule ID is recorded as the representative winner.

## Ambiguity

The resolver tracks both definite and possible reachability. A path containing `AMBIGUOUS` remains possible until a `DOES_NOT_APPLY` ancestor blocks it.

A relevant ambiguous path taints a result only if its rank can tie/outrank the definitive winner and its effect could change the result. This avoids both false certainty and indiscriminate ambiguity poisoning.

## Hash binding

`definition_hash` commits to title, scope, default effect and the ordered list of rule hashes. Each rule hash commits to parent, kind, effect, priority, depth, label and condition.

`case_hash` commits to the normalized supplied case facts.

`assessment_hash` commits to ordered rule IDs and consensus-backed applicability statuses.

`resolution_hash` commits to definition hash, case hash, assessment hash, outcome and winning rule ID.
