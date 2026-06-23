# Changelog

## 1.0.0-core-ga

- Promoted ProofOps core contracts to `production-ready`.
- Split GA into Core GA and Field GA so v1.0 can ship without pretending to have independent external product validation.
- Added Core GA and Field GA scope files.
- Added reusable profile templates for GitHub Actions beta, GitLab + Jenkins RC, and LLM agent GA workflows.
- Added evidence adapter contracts for GitHub Actions, GitLab, Jenkins, LLM provider, Playwright, and product-native release APIs.
- Added Core GA release readiness script targets.

Field GA remains blocked until at least two independent real target products produce product-native `GO` decisions with `targetReached=true`.

## 0.1.0-beta

- Extracted ProofOps as an independent beta project.
- Added `proofops-governor` as the canonical maturity and release governance agent.
- Added fallback target presets for `demo-to-alpha`, `alpha`, `beta`, `rc`, and `ga`.
- Added architecture readiness as a first-class governance phase.
- Added ProofOps release readiness and stable GA gates.
- Added generated Codex distribution and project-scoped install support.

Stable GA remains blocked until scoped real-project profiles produce product-native `GO` decisions and `npm run release:check:ga` passes.
