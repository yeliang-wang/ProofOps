# Stable GA Criteria

ProofOps reaches stable GA only when release governance itself is backed by repeatable real-project evidence.

## Scope

The first GA scope is:

- `proofops-governor`
- `proofops` plugin
- target preset contracts
- project profile runner
- release coverage matrix workflow
- architecture readiness phase
- final report artifacts
- Codex and Claude Code install flows

## Required Evidence

| Gate | Requirement |
| --- | --- |
| Lifecycle | Scoped agent and plugin are `production-ready`. |
| Target presets | `demo-to-alpha`, `alpha`, `beta`, `rc`, and `ga` presets are versioned and validated. |
| Architecture readiness | Demo-to-production and beta-to-GA loops include an architecture readiness result. |
| Real profiles | Scoped project profiles run through the release coverage matrix runner. |
| Product-native decisions | GA-scoped real target projects produce product-native `GO` decisions. |
| External boundaries | LLM, SCM, CI/CD, product API, rollback, approval, and evidence boundaries are real where required. |
| Reports | Final reports include coverage matrix, evidence map, repair policy, release decision, and final target summary. |
| Distribution | Release includes changelog, support matrix, install/upgrade notes, and compatibility notes. |

## Promotion Rule

ProofOps can move from `beta` to `production-ready` only after:

1. `npm run release:check` passes.
2. `npm run release:check:ga` passes.
3. Scoped final reports are `GO` with `targetReached=true`.
4. At least two real target projects and one production-representative profile exercise the core workflow.
5. Release notes identify any remaining non-GA scope.

Do not mark ProofOps stable GA from local validation, prompt quality, smoke checks, or chat-only summaries.
