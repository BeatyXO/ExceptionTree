# Protocol invariants

1. A sealed rule set never mutates.
2. Every exception points to an older existing rule in the same rule set; cycles are impossible by construction.
3. Every node has exactly one immutable effect: `ALLOW` or `DENY`.
4. The LLM never chooses final outcome or precedence.
5. A child cannot become definitely reachable unless its entire ancestor path is definitely reachable.
6. `DOES_NOT_APPLY` blocks every descendant path regardless of a descendant's standalone semantic classification.
7. Equal-ranked opposite effects never resolve through arbitrary ID ordering; they produce `CONFLICT`.
8. Relevant ambiguity cannot silently become a decisive outcome.
9. Malformed/incomplete semantic output degrades to `AMBIGUOUS`, not `ALLOW`.
10. Case submission pins the exact sealed `definition_hash`.
11. Consumer assertions pin both `definition_hash` and `case_hash`.
12. A resolved case cannot be re-resolved and therefore cannot invalidate downstream consumers through no-op adjudication.
