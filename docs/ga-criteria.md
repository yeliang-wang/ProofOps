# GA Criteria

ProofOps uses two GA levels:

- `Core GA`: the ProofOps governance engine is stable, installable, documented, and backed by repeatable self-evidence plus production-representative evidence.
- `Field GA`: ProofOps has independent real target-product evidence from at least two external products.

## Scope

The Core GA scope is:

- `proofops-governor`
- `proofops` plugin
- target preset contracts
- project profile runner
- reusable profile templates
- evidence adapter contracts
- release coverage matrix workflow
- architecture readiness phase
- final report artifacts
- Codex and Claude Code install flows

## Required Evidence

| Gate | Core GA Requirement |
| --- | --- |
| Lifecycle | Scoped agent and plugin are `production-ready`. |
| Target presets | `demo-to-alpha`, `alpha`, `beta`, `rc`, and `ga` presets are versioned and validated. |
| Architecture readiness | Demo-to-production and beta-to-GA loops include an architecture readiness result. |
| Core profiles | ProofOps self-evidence and production-representative profiles run through the release coverage matrix runner. |
| Profile templates | At least three reusable templates cover beta, RC, and GA-style projects. |
| Evidence adapters | Adapter contracts cover SCM, CI/CD, LLM, E2E, and product-native release APIs. |
| Active stability | GA profiles and adapters distinguish active workload stability from health-only or empty soak. |
| Reports | Final reports include coverage matrix, evidence map, repair policy, release decision, and final target summary. |
| Distribution | Release includes changelog, support matrix, install/upgrade notes, and compatibility notes. |

## Core GA Promotion Rule

ProofOps can mark its core components `production-ready` only after:

1. `npm run release:check` passes.
2. `npm run release:check:core-ga` passes.
3. Scoped Core GA final reports are `GO` with `targetReached=true`.
4. Profile templates and adapter contracts are validated.
5. Active stability contracts reject health-only soak as GA evidence.
6. Release notes explicitly state that independent Field GA remains separate.

## Field GA Promotion Rule

ProofOps reaches Field GA only after:

1. `npm run release:check:field-ga` passes.
2. At least two independent real target products produce product-native `GO` decisions with `targetReached=true`.
3. Required LLM, SCM, CI/CD, product API, rollback, observability, and audit boundaries are real where applicable.

Do not claim Field GA from local validation, production-representative sandbox evidence, prompt quality, smoke checks, or chat-only summaries.

## Active Stability Rule

GA stability proof must be load-bearing. A service that only responds to health checks during a timer window has not proven GA stability. ProofOps accepts active stability evidence only when a real workload runs during the window and product counters prove activity, such as run count, code-change count, and pipeline count deltas.

If the target product exposes a product-native release decision, that decision remains authoritative. ProofOps can still run an `active-stability` matrix row for products that expose summary counters and workload commands, but it must not convert empty soak into `GO`.
