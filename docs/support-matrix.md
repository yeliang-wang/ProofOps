# Support Matrix

| Area | Core GA Support |
| --- | --- |
| Codex project-scoped agents | Supported through generated TOML installation. |
| Claude Code agents | Supported through Markdown agent installation. |
| Target presets | Supported for `demo-to-alpha`, `alpha`, `beta`, `rc`, and `ga`. |
| Architecture readiness | Supported as a built-in review phase. |
| Release coverage profiles | Supported through `scripts/release-coverage-matrix-runner.mjs`. |
| Production representative sandbox | Supported for local representative project validation. |
| Profile templates | Supported for GitHub Actions beta, GitLab + Jenkins RC, and LLM agent GA starting points. |
| Evidence adapter contracts | Supported for GitHub Actions, GitLab, Jenkins, LLM provider, Playwright, and product release API evidence. |
| Core GA claims | Supported when `release:check:core-ga` passes. |
| Field GA claims | Not supported until `release:check:field-ga` passes with two independent real target products. |

ProofOps does not provide hosted runtime infrastructure, CI/CD hosting, SCM hosting, LLM hosting, or product-owned GA definitions.
