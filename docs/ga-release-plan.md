# GA Release Plan

ProofOps is currently a beta GA-candidate project. The release plan keeps beta useful while preventing premature stable GA claims.

| Phase | Goal | Exit Criteria |
| --- | --- | --- |
| P1 Beta extraction | Standalone project with one governor, plugin, presets, runner, docs, and CI. | `npm run release:check` passes. |
| P2 Real target evidence | Run ProofOps against real agent/product projects. | Final reports show product-native decisions and evidence maps. |
| P3 RC hardening | Add compatibility notes, upgrade guidance, rollback evidence, and risk closure. | No high open risks for scoped profiles. |
| P4 Stable GA | Promote lifecycle to `production-ready`. | `npm run release:check:ga` passes. |

Stable GA is blocked until real scoped profiles produce product-native `GO` decisions.
