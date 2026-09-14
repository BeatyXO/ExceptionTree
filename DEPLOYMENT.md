# Deployment evidence

Target: stable Studionet only.

- network alias: `studionet`
- chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- explorer: `https://explorer-studio.genlayer.com`

The stable client command documented in the handoff (`genlayer network info`) is not
installed in this environment, and no signing credentials were supplied. No live
Studionet write was attempted. Consequently there are no hosted addresses,
transactions, or lifecycle hashes to report.

The required network remains stable Studionet (`studionet`, chain ID `61999`,
RPC `https://studio.genlayer.com/api`). Any future write must inspect the effective
network first and confirm chain ID 61999.

## Hosted proof status

Not produced in this environment: deployments, sealed ruleset, case resolutions,
ExceptionGate execution, negative consumer calls, and replay evidence.
