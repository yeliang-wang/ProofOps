# ProofOps Agent Catalog

| Agent | File | Best For |
| --- | --- | --- |
| `proofops-governor` | `agents/proofops-governor.md` | Demo-to-GA maturity and release governance with target presets, architecture readiness, release coverage matrix, real evidence, repair loop, final report, and GO/NO-GO decisions. |

## Product Contracts

| Agent | Manifest |
| --- | --- |
| `proofops-governor` | `manifests/agents/proofops-governor.json` |

## Plugin

| Plugin | Manifest | Agents |
| --- | --- | --- |
| `proofops` | `plugins/proofops/plugin.json` | `proofops-governor` |

Generated catalogs live in `catalog/agents.json` and `catalog/plugins.json`.
