# ProofOps: Codex Integration

ProofOps installs `proofops-governor` as a project-scoped Codex agent.

Canonical source:

- `agents/proofops-governor.md`
- `manifests/agents/proofops-governor.json`
- generated TOML: `integrations/codex/agents/proofops-governor.toml`

## Goal Adapter

Codex `/goal` can own the outer objective while `proofops-governor` owns the inner maturity and release governance loop. The agent must establish:

- maturity target
- target preset or product-native target
- architecture readiness review
- target plan and confirmation
- release coverage matrix
- evidence map
- repair policy
- decision chain
- final report

Render the plan:

```bash
npm run proofops:plan -- \
  --agent proofops-governor \
  --project-id your-project \
  "Move this demo project toward beta readiness with real evidence"
```

## Install

```bash
cd /path/to/your/project
/Users/wangyejing/github/ProofOps/scripts/install.sh --tool codex --agent proofops-governor --update
```

Dry run:

```bash
/Users/wangyejing/github/ProofOps/scripts/install.sh --tool codex --agent proofops-governor --update --dry-run
```

ProofOps agents are installed under the target project's `.codex/agents/` directory. They do not replace global Codex skills.
