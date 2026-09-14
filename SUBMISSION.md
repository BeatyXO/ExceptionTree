# Submission draft

## Title

ExceptionTree — Consensus-Backed Rule Applicability With Deterministic Exception Precedence

## Short description

ExceptionTree is a reusable GenLayer Intelligent Contract primitive for policies whose general rules are modified by nested exceptions. Validators independently classify only whether each immutable clause applies to supplied case facts. The contract—not the LLM—then deterministically resolves ancestor reachability, specificity depth, explicit priority, contradictory ties and ambiguity. Sealed rule sets produce immutable definition hashes; cases pin those definitions and become single-shot immutable resolutions. A companion ExceptionGate demonstrates typed IC-to-IC consumption with definition/case pinning and action replay protection.

## Why GenLayer

Natural-language clause applicability cannot generally be reduced to byte-level deterministic logic, while allowing an LLM to choose the entire final outcome creates an opaque `AI decides X` design. ExceptionTree uses GenLayer only for the semantic layer and keeps the policy engine itself deterministic.
