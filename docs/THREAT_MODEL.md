# Threat model

## Malicious case/rule text

Rule conditions and case facts are treated as untrusted data. The prompt explicitly forbids following embedded instructions, while deterministic input checks reject common control-like injection markers.

## Forged leader result

A leader cannot simply claim a convenient applicability vector. Validators independently re-classify the same immutable rules and case and compare the material status vector.

## Model formatting failure

Malformed, missing, reordered or duplicated assessments canonicalize to all-`AMBIGUOUS`. This cannot silently create permission.

## Contradictory policy

Overlapping equal-precedence rules with opposite effects produce `CONFLICT`, making authoring defects visible rather than silently favoring insertion order.

## Ambiguous exception

An unresolved exception capable of changing the winning effect yields `AMBIGUOUS`. An ambiguity that cannot change the effect may be recorded without needlessly changing a stable result.

## Post-seal mutation

Only the creator may edit a draft. Once sealed, all rule mutation paths reject.

## Consumer replay

The example `ExceptionGate` requires exact case/definition pins and permanently records used action hashes.

## Non-goal

ExceptionTree does not prove that case facts are externally true. A caller may feed facts from another IC, oracle, attestation system, evidence primitive or manually supplied data. ExceptionTree's job is semantic applicability plus deterministic rule/exception precedence.
