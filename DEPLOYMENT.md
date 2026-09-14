# Deployment evidence

Target: stable Studionet only.

- network alias: `studionet`
- chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- explorer: `https://explorer-studio.genlayer.com`

The effective network was inspected with `genlayer network info` before each write
sequence and reported `studionet`, chain ID `61999`, RPC
`https://studio.genlayer.com/api`. All normal consensus writes below used the
five-validator stable network path.

## Finalized deployment

ExceptionTree address: `0x59Fca84CEA0A93614Be6c11FD7F8D1F3adb8C4e6`

ExceptionTree deployment tx: `0x5e6e46c36c996854be83736ad69411762eac2cb15a3cf2bdf36f6423e1cb6eb6`

ExceptionGate address: `0x1Ff1748b791b94b2B93D6B4F1D8a44B19CDbBBEB`

ExceptionGate deployment tx: `0xa2bab6ecbf73d800b54d51370740477d9484cfc8b1a3d43d5c0a1018821551b4`

Final source commit: `85c1d94c73797bc8c386accd49b5071006444e3b`

## Live proof

Refund ruleset ID: `1`

Refund definition hash: `cf9f8793de666b5cf2a26d42e0cbaf2b9613ae25f3a9afcb3ee226e2ee557b91`

| Case | Case hash | Outcome | Winning rule | Resolution hash |
|---:|---|---|---:|---|
| 1 | `8980fa2a3cf5b190dcf6b7e3d6e658ac245aa9aea79efb2ac3fe89da7692843a` | ALLOW | 1 | `8284bbc3d7aac83f8869a043596348a642991ab8800baa3ae7077b98a3cb9293` |
| 2 | `b9b943207afd86e74cecb0e5f18f54274f8c3bdacbb7bd62049977e9f459df93` | AMBIGUOUS | 0 | `19f619a8a37eac25234e1e92168ef8fd57e79e24e31bf173e86a33e0a7c8837a` |
| 3 | `cfa033efb44079648f2f01cdcb4883608a5fe39a9dea8bceb37486464b6e33df` | ALLOW | 3 | `2401be2b5d57d031741a6c19911367f0a02d5c2cfc734bb4596651d3522cf4ae` |
| 4 | `97ce120cf5bbb6d8d9d8f80b09e2039670be905fe30c61f56091806ed92d4547` | DENY | 4 | `bec1711f2a74dbc5b8d665a49ce4a7cc43b171143bec276961ecf46e8e8fd05b` |
| 5 | `eec8aaf28b0e6ec29290c1ea923b5e6c3111d357a5eb64d3961417fbfea9e06c` | AMBIGUOUS | 0 | `b969cdc028b25e4e78ed4dd984a72c2c4abfa6f16449fec5fb159a2a9457dfac` |
| 7 | `9cc6d9a036b457cb7aa7cc9e633ff4a63b43b70c19a349934a524d07ed719171` | DENY | 2 | `94ed6ec1d6e881acf708d93a8af60e022c702235227ee0049dfa8008cea64ebb` |

Case 7 submission transaction: `0xfe32c5b27bb39aa62b4f1a8f09dfcbc3809663bc24322d21e0bb04bc0546ed72`.
The stable CLI output for the case 7 resolution exposed the finalized contract
state and resolution hash but did not expose a transaction ID in the captured
output; no replacement or duplicate transaction was sent solely to manufacture
an ID.

Contradiction ruleset ID: `2`; definition hash:
`5b56baa9ce088076b48783479df5cb2dc48bfe9c76a29003e030a71b291346d3`.
Contradiction case ID: `6`; case hash:
`bf860e41035aaa2fadfea6001a9dcabc676ab590188bc9c25145d750543583a3`;
outcome `CONFLICT`; resolution hash:
`f78b4cc8aaea034a0dcc7d3cfe3dd70d5903e4bd78759b3c56b168247eafb311`.

ExceptionGate execution ID `1` succeeded for case `1` with action hash
`aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`.
The stored execution was read back from the gate and pinned both the definition
and case hashes. Wrong definition, wrong case, case 2 (non-ALLOW), and replay of
the successful action were each rejected with:
`ExceptionTree does not establish ALLOW for the pinned case and ruleset` for the
first three; the replay transaction returned `rollback` with
`action replay rejected`.

Case 1 was then read back and confirmed resolved; a second resolution attempt was
rejected by the contract's `case already resolved` guard (`rollback`,
`EXPECTED: case already resolved`).

The original CLI output for the successful gate execution and the first negative
gate checks did not retain their transaction IDs. Their finalized contract state
and rejection payloads were verified live; no transaction IDs are invented here.

Commands used included `genlayer network info`, `genlayer deploy --contract ...`,
`genlayer write ...`, and `genlayer call ...`, all through the stable CLI with
normal consensus and no leader-only flag.
