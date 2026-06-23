# Production Representative Sandbox

The Production Representative Sandbox gives ProofOps a local project set for release coverage matrix loops when real customer production projects are not available.

These projects are templates only until they are generated as real Git repositories, registered through the target product, validated by real commands, and connected to real SCM, CI/CD, LLM/runtime, and product-native evidence paths where applicable.

## Projects

| Project | Coverage |
| --- | --- |
| `node-service` | API service, Git, CI/CD, runtime validation |
| `web-dashboard` | UI-facing project, artifact validation, rollback |
| `mcp-tooling` | tool contract and runtime boundary validation |
| `data-pipeline` | batch/data path validation |
| `flaky-quality-gate` | failure containment and repair verification |

## Verify

```bash
npm run sandbox:verify
```

Verify generated repositories:

```bash
python3 sandbox/production-representative/scripts/verify-sandbox.py --generated --include-fault
```

## Use

`proofops-governor` can convert this project set into release coverage matrix rows. The target product must still register and verify the generated projects through its own API/data path before any row counts as release evidence.
