You are taking over a substantially implemented GenLayer Intelligent Contract repository named ExceptionTree.

Do not return only a plan, checklist, commentary, review, or mockup. Inspect the entire unzipped repository first, then finish it to a reviewer-ready state in the existing folder and push the completed work to:

https://github.com/BeatyXO/ExceptionTree.git

The GitHub repository was created for this codebase and is currently intended to receive it. Preserve the product architecture unless an actual GenLayer runtime, linter, Direct Mode, or live Studionet failure proves a concrete change is necessary.

PRODUCT BOUNDARY

ExceptionTree is a standalone reusable Intelligent Contract primitive, not a full application.

There must be no frontend.

The primitive resolves natural-language rules containing nested exceptions without allowing the LLM to choose the final policy outcome.

The design boundary is non-negotiable:

- rulesets begin as creator-controlled drafts and become immutable when sealed;
- a sealed definition has root rules and nested exception nodes;
- every node has an immutable natural-language condition, ALLOW/DENY effect, explicit priority, parent binding, deterministic depth, and rule hash;
- GenLayer consensus classifies only whether each node's OWN condition is APPLIES, DOES_NOT_APPLY, or AMBIGUOUS for the supplied case facts;
- validators must independently re-evaluate the same immutable rule nodes and case facts rather than trusting a leader summary;
- the LLM must never choose ALLOW, DENY, CONFLICT, the winning rule, exception precedence, or the final outcome;
- ancestor reachability, specificity, priority, contradictory ties, relevant ambiguity and final outcome remain deterministic contract logic;
- deeper reachable clauses outrank shallower clauses;
- at equal depth, higher priority outranks lower priority;
- equal-ranked opposite effects produce CONFLICT rather than arbitrary insertion-order resolution;
- ambiguous paths must fail safely when they could change the effective outcome;
- malformed or incomplete semantic output must never silently become ALLOW;
- cases pin the sealed definition_hash and the normalized case produces a case_hash;
- resolution is single-shot: a resolved case cannot be re-adjudicated later and unexpectedly invalidate consumers;
- is_outcome / is_allowed are the reusable typed consumer surface;
- ExceptionGate proves another Intelligent Contract can consume a pinned ALLOW result and reject action replay.

Do not collapse this into a generic “AI decides whether a policy allows X” contract. The core contribution is semantic clause applicability plus deterministic exception precedence.

Also preserve the explicit non-goal: ExceptionTree does not prove whether supplied case facts are externally true. Evidence/oracle/attestation contracts can provide facts. ExceptionTree resolves those supplied facts against a sealed rule hierarchy.

NON-NEGOTIABLE NETWORK

Use stable Studionet only for final hosted proof:

- network alias: studionet
- chain ID: 61999
- RPC: https://studio.genlayer.com/api
- explorer: https://explorer-studio.genlayer.com

Do not switch the project to studio-dev / chain 61997 just because newer release-candidate tooling is available.

Before every live deploy or write workflow, run the effective network inspection and confirm chain ID 61999. Never rely only on an assumed alias.

REQUIRED WORK

1. Read README.md, AGENT_HANDOFF.md, BUILD_STATUS.md, SUBMISSION.md, DEPLOYMENT.md, every file under docs/, proof/, both contracts, every test, gltest.config.yaml, requirements-test.txt, pyproject.toml and every script before editing.

2. Run immediately:

   python scripts/preflight.py

3. Create/use an isolated Python 3.12+ environment, install the repository test tooling from requirements-test.txt, and run Python compilation, GenVM lint, and all Direct Mode tests.

4. Fix actual failures completely. Do not weaken assertions, remove adversarial cases, bypass validators, mark failures xfail, or convert substantive tests into static string checks merely to make the suite green.

5. Review contracts/exceptiontree.py for current stable GenLayer SDK/runtime compatibility, especially:

   - persisted storage types and dataclass storage compatibility;
   - DynArray / TreeMap behavior;
   - public method annotations and return types;
   - event definitions and emission;
   - cross-contract interface compatibility;
   - deterministic code outside nondeterministic blocks;
   - LLM calls occurring only inside the nondeterministic leader/validator path;
   - bounded input sizes;
   - canonicalization of malformed model output;
   - prompt-injection resistance for untrusted rule/case text;
   - rule-tree acyclicity by construction;
   - parent reachability semantics;
   - depth/priority precedence semantics;
   - equal-rank contradiction handling;
   - ambiguity propagation;
   - hash construction and consumer pinning;
   - resolved-case finality.

6. Keep the stable py-genlayer dependency pin already present unless stable Studionet itself proves that it cannot run. Do not migrate to release-candidate Studio tooling merely for convenience.

7. Preserve a substantive leader/validator design. The leader may return a canonical applicability vector, but each validator must independently classify the same stored rules against the same case facts and reject a materially different status vector. Validators must not simply validate JSON shape or trust leader reasoning text.

8. Preserve the semantic boundary: the model may classify APPLIES / DOES_NOT_APPLY / AMBIGUOUS for each clause only. The final rule/exception outcome must be computed by deterministic_resolve or an equivalent deterministic implementation.

9. Audit deterministic_resolve against the documented invariants. At minimum verify:

   - child cannot be definitely reachable when any ancestor does not apply;
   - nested exceptions can override their ancestors only when the full path applies;
   - deeper rules beat shallower rules;
   - higher priority beats lower priority at equal depth;
   - equal depth + equal priority + opposite effects => CONFLICT;
   - same-rank same-effect overlap remains deterministic;
   - a relevant ambiguous path that could change the winner => AMBIGUOUS;
   - ambiguity that cannot change the final effect does not needlessly poison a stable outcome;
   - no applicable rule uses the sealed default effect unless relevant ambiguity could change it.

10. Preserve immutable sealing. After seal_ruleset succeeds, no method may alter the rules, hierarchy, effects, conditions, priorities, scope, default effect, rule hashes or definition hash.

11. Preserve single-shot resolution. Arbitrary callers must not be able to re-run semantic adjudication on an already resolved case and thereby create a new result or new consumer binding.

12. Review contracts/exception_gate.py and ensure it performs a real typed IC-to-IC read of ExceptionTree's pinned outcome. The gate must require the expected definition hash and exact case hash, require ALLOW, and reject replay of an already-used 64-hex action_hash.

13. Expand adversarial Direct Mode coverage wherever a reviewer would reasonably expect it. In addition to the supplied tests, consider missing cases around:

   - unauthorized draft mutation;
   - maximum depth / maximum rule count;
   - malformed, reordered, missing or duplicate model assessments;
   - leader/validator disagreement;
   - parent false / child true attempts;
   - contradictory roots;
   - contradictory sibling exceptions;
   - explicit priority ordering;
   - ambiguity on an ancestor with deeper possible descendants;
   - default-effect behavior;
   - definition-hash mismatch;
   - case-hash mismatch;
   - second resolution attempt;
   - action replay;
   - non-ALLOW gate attempt;
   - wrong ExceptionTree address/interface behavior where practical.

14. If a supplied implementation detail is incompatible with current stable GenVM, make the smallest architecture-preserving correction and document why. Do not rewrite the primitive into a different product.

15. Do not invent deployment proof, contract addresses, transaction hashes, test counts, lint results, finalization status, validator consensus evidence, or GitHub commit SHAs.

GITHUB

The target repository is:

BeatyXO/ExceptionTree
https://github.com/BeatyXO/ExceptionTree.git

The repository was initially empty. Work in the provided unzipped folder.

- Initialize/configure git if necessary.
- Use main as the intended primary branch unless the remote proves otherwise.
- Confirm the remote before pushing.
- Do not push secrets, private keys, .env files, virtual environments, caches, build artifacts or unrelated local files.
- Commit the substantive implementation and tests.
- Push the finished code to the target repository.
- After pushing, inspect the actual remote repository and confirm the expected files and final commit are present.

LIVE STUDIONET PROOF

Only after Direct Mode tests and GenVM lint are green, run a real lifecycle on stable Studionet, chain 61999, with normal consensus. Do not use leader-only mode as the final proof.

The live proof should demonstrate at least:

A. ExceptionTree deployment finalizes successfully on chain 61999.

B. Create and seal a concrete nested refund ruleset similar to:

   1. purchase is within 30 days => ALLOW
   2. exception: item is perishable => DENY
   3. nested exception: perishable item is materially defective => ALLOW
   4. nested exception: defect was reported more than 48 hours after discovery => DENY

C. The sealed ruleset exposes a real non-empty 64-hex definition_hash.

D. Resolve enough independent cases to prove deterministic hierarchy behavior:

   - within 30 days + non-perishable => ALLOW from root;
   - within 30 days + perishable => DENY from exception;
   - perishable + defective + timely report => ALLOW from nested exception;
   - perishable + defective + late report => DENY from deeper exception.

E. Prove ambiguity behavior with a case where a potentially applicable exception is materially unclear and could change the root outcome. The result must be AMBIGUOUS, not a guessed allow/deny.

F. Prove contradiction behavior with an intentionally separate sealed ruleset containing equal-ranked applicable opposite-effect rules. The result must be CONFLICT.

G. Prove a resolved case cannot be resolved again.

H. Deploy ExceptionGate using the finalized ExceptionTree address.

I. Demonstrate a correctly pinned ALLOW case and unique action_hash succeeds through ExceptionGate.

J. Demonstrate at least these consumer failures with real evidence:

   - wrong definition hash rejected;
   - wrong case hash rejected;
   - a DENY / AMBIGUOUS / CONFLICT case cannot pass the gate;
   - replay of the successful action_hash is rejected.

If the currently installed stable client/CLI requires explicit fee estimation or updated stable transaction submission syntax, use the supported stable Studionet path. Do not change networks as a workaround.

FINAL DOCUMENTATION

Update DEPLOYMENT.md and BUILD_STATUS.md only with evidence actually produced.

DEPLOYMENT.md should contain, where applicable:

- finalized ExceptionTree address;
- finalized ExceptionTree deployment transaction;
- finalized ExceptionGate address;
- finalized ExceptionGate deployment transaction;
- final source commit SHA;
- sealed refund ruleset ID and definition hash;
- relevant case IDs, case hashes and resolution hashes;
- transaction evidence for semantic case resolution;
- ALLOW / DENY / AMBIGUOUS / CONFLICT proof;
- successful gate execution evidence;
- rejected wrong-definition, wrong-case, non-ALLOW and replay evidence;
- exact commands used;
- real Direct Mode test results;
- real GenVM lint results.

If stable tooling makes any command in the current documentation inaccurate, correct the documentation to the command that actually worked.

FINAL GATES

Before the final push, all applicable gates must be satisfied:

- python scripts/preflight.py --final passes;
- Python compilation passes;
- GenVM lint passes for both contracts;
- all Direct Mode tests pass;
- the live stable-Studionet lifecycle above passes;
- no secrets/private keys/.env/virtual environments/caches/build artifacts are tracked;
- no frontend exists;
- every final network reference remains stable Studionet / chain 61999;
- no deployment placeholder remains in the finalized deployment evidence;
- inspect git diff;
- inspect git status;
- inspect tracked files;
- inspect the final remote GitHub repository after push.

Do not claim completion until all applicable checks actually pass and the remote repository contains the final committed code.

At the end, report exactly:

1. what you changed;
2. the final architecture if any compatibility correction was necessary;
3. real preflight / compile / lint / Direct Mode results;
4. live ExceptionTree and ExceptionGate addresses;
5. real deployment and lifecycle transaction evidence;
6. sealed ruleset definition hash and key case/resolution hashes;
7. gate success and negative/replay proof;
8. final 40-character Git commit SHA;
9. confirmation that the remote repository was inspected after push;
10. any genuine limitation that still remains.
