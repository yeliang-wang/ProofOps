# Release Readiness

`npm run release:check` is the ProofOps public-beta release gate.

It verifies:

- package metadata and license
- beta-or-better lifecycle state
- target presets
- loop contracts
- architecture readiness contract
- production release evidence rule
- generated Codex distribution
- generated catalogs
- deterministic eval
- project-scoped install drift
- production representative sandbox
- release docs

## Platform-Wide Production Release Rule

ProofOps must not use mock, fake, stub, simulator, fixture-only, demo-only, smoke-only, or chat-only evidence as production release evidence.

## Loop Goal Window

Every maturity or release loop must define final goal, phase goals, acceptance criteria, target plan, target plan confirmation, report cadence, and final decision vocabulary before execution.

## Release Coverage Matrix Loop

Release, beta, RC, and GA loops must use a release coverage matrix with evidence map, blocker policy, repair policy, release decision, and per-phase decision chain.

## Active Workload Stability

GA loops should include active workload stability when the target product exposes enough counters or product-native release criteria. Health-only polling can prove the service did not crash, but it is not release evidence by itself.

An active stability row must:

- capture a baseline product summary,
- run a real workload command on a configured cadence,
- probe health and readiness endpoints during the window,
- prove run, code-change, and pipeline counters increased by configured thresholds,
- fail the row when there is no active workload delta.

## Core GA

`npm run release:check:core-ga` and `npm run release:check:ga` evaluate Core GA. Core GA covers the stable governance engine, reusable profile templates, evidence adapter contracts, production-representative evidence, and final reports.

## Field GA

`npm run release:check:field-ga` evaluates independent Field GA. It is expected to fail until at least two independent real target products produce product-native `GO` decisions with `targetReached=true`.
