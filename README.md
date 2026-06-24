# ProofOps

ProofOps is an evidence-first maturity and release governance project for AI agent products and engineering automation systems.

It helps a project move from demo, alpha, beta, or RC toward production-ready GA by turning the target into a reviewable plan, architecture readiness review, release coverage matrix, real-boundary evidence loop, productized repair cycle, final report, and explicit `GO`, `CONDITIONAL-GO`, `NO-GO`, or `BLOCKED` decision.

ProofOps is not a general agent framework like LangGraph, CrewAI, or AutoGen. It is the governance layer above agent runtimes, coding agents, CI/CD, SCM, LLM providers, and product APIs.

## Status

ProofOps is currently `1.0.0 Core GA`.

Core GA means the ProofOps governance engine, agent/plugin contracts, target presets, generated Codex distribution, release coverage runner, production-representative sandbox, reusable profile templates, evidence adapter contracts, release readiness gates, and CI workflow are stable and repeatably validated.

Core GA does not claim independent field validation. Field GA remains a separate milestone that requires at least two independent real target products to produce product-native `GO` decisions with `targetReached=true`.

## Core Agent

| Agent | Purpose |
| --- | --- |
| `proofops-governor` | Evidence-first maturity and release governance from demo/alpha/beta/RC targets to GA decisions. |

The canonical source is `agents/proofops-governor.md`. The generated Codex distribution is `integrations/codex/agents/proofops-governor.toml`.

## What ProofOps Does

ProofOps drives this lifecycle:

```text
discover
  -> maturity assessment
  -> architecture review
  -> target preset selection
  -> target plan confirmation
  -> readiness
  -> cleanup
  -> non-mock precheck
  -> evidence loop
  -> productized repair
  -> rollback and release evidence
  -> final report
  -> GO / CONDITIONAL-GO / NO-GO / BLOCKED
```

It refuses production claims backed only by mock, fake, stub, simulator, fixture-only, demo-only, smoke-only, or chat-only evidence.

For GA targets, ProofOps also distinguishes active stability from empty soak. Health-only polling can prove connectivity, but it cannot prove GA stability by itself. A GA active workload stability row must run a real workload while the target product stays healthy and product counters such as runs, code changes, and pipelines advance by configured thresholds.

## Target Presets

ProofOps includes fallback target presets under `targets/`:

| Target | Use When |
| --- | --- |
| `demo-to-alpha` | A demo needs to become a repeatable engineering prototype. |
| `alpha` | A project needs internal trial readiness. |
| `beta` | A project needs real-project validation and public-beta evidence. |
| `rc` | A project needs release-candidate hardening. |
| `ga` | A project needs production-ready GA proof. |

Product-native targets always win over presets. Presets only create the initial target plan when the product has no release target API or explicit target contract.

## Architecture Readiness

Every demo-to-production or beta-to-GA loop includes an architecture readiness phase. It checks whether the architecture can support the selected target, including runtime boundaries, adapters, state, resume, rollback, observability, evidence storage, release decisions, and productized repair paths.

## Install

Install dependencies:

```bash
npm ci
```

Validate the project:

```bash
npm run validate
npm run check
npm run generate -- --check
npm run eval
npm run release:check
```

Core GA gate:

```bash
npm run release:check:core-ga
npm run release:check:ga
```

Field GA gate:

```bash
npm run release:check:field-ga
```

Field GA is expected to fail until independent real-project evidence is available.

## Codex Usage

Render a target plan:

```bash
npm run proofops:plan -- \
  --agent proofops-governor \
  --project-id your-project \
  "Move this demo project toward beta readiness with real evidence"
```

Install the generated Codex agent into a target project:

```bash
/Users/wangyejing/github/ProofOps/scripts/install.sh --tool codex --agent proofops-governor --update
```

## Project Profiles

Release coverage profiles live under `project-profiles/examples/`. A profile defines services, boundaries, target plan, matrix steps, final report paths, and release decision behavior.

Run a profile once:

```bash
npm run release:runner -- --profile project-profiles/examples/proofops.public-beta.json --once
```

Reusable profile templates live under `project-profiles/templates/`, and evidence adapter contracts live under `adapters/`.

GA-oriented profiles can include an `active-stability` matrix step. The runner records a baseline summary, executes the configured workload on a cadence, probes health/readiness endpoints, then compares final counters to the configured activity thresholds. If the service stays healthy but no real workload delta appears, the row fails as release evidence instead of becoming an empty soak pass.

```bash
npm run proofops:install -- --help
python3 scripts/proofops-control.py profile-templates
python3 scripts/proofops-control.py adapters
python3 scripts/proofops-control.py init-profile \
  --template github-actions-beta \
  --project-id your-project \
  --output project-profiles/examples/your-project.beta.json \
  --dry-run
```

## Release Gates

`npm run release:check` is the public baseline gate. It checks package metadata, lifecycle state, target presets, loop contracts, generated distributions, deterministic eval, project-scoped install drift, release docs, support docs, and profile readiness.

`npm run release:check:ga` is the Core GA gate. It requires scoped agents and plugins to be `production-ready`, reusable profile templates and evidence adapters to be present, and scoped Core GA project profile final reports to be `GO` with `targetReached=true`.

`npm run release:check:field-ga` is the independent field validation gate. It requires at least two independent real target products with product-native `GO` decisions. Production-representative sandbox evidence does not count as field evidence.

Health-only soak, copied logs, or chat summaries do not satisfy GA active stability. The target product should either expose product-native release decisions that include active stability criteria or be governed by a ProofOps profile with an `active-stability` row backed by real workload deltas.

## Boundary

ProofOps does not replace:

- agent runtimes
- coding agents
- SCM providers
- CI/CD systems
- LLM providers
- product-owned GA definitions

ProofOps governs whether the target product has enough real evidence to advance to the requested maturity target.
