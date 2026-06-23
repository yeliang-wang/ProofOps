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

## Stable GA

`npm run release:check:ga` evaluates stable GA. In beta, it is expected to fail until scoped final reports are product-native `GO` and targetReached=true.
