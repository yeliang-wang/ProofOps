# GA Release Plan

ProofOps separates Core GA from Field GA so the core governance engine can reach v1.0 without pretending to have independent external adoption.

| Phase | Goal | Exit Criteria |
| --- | --- | --- |
| P1 Beta extraction | Standalone project with one governor, plugin, presets, runner, docs, and CI. | `npm run release:check` passes. |
| P2 Core GA productization | Add reusable profile templates, evidence adapter contracts, stable reports, and clear install workflows. | `npm run release:check:core-ga` passes. |
| P3 Field validation | Run ProofOps against independent real target products. | Product-native field decisions are `GO` with `targetReached=true`. |
| P4 Field GA | Promote field validation claims. | `npm run release:check:field-ga` passes. |

Core GA can ship without independent external projects. Field GA remains blocked until real scoped field profiles produce product-native `GO` decisions.
