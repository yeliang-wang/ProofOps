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

## Core GA

`npm run release:check:core-ga` and `npm run release:check:ga` evaluate Core GA. Core GA covers the stable governance engine, reusable profile templates, evidence adapter contracts, production-representative evidence, and final reports.

## Field GA

`npm run release:check:field-ga` evaluates independent Field GA. It is expected to fail until at least two independent real target products produce product-native `GO` decisions with `targetReached=true`.
