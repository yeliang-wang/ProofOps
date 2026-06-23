const assert = require("assert");
const { createApp } = require("./server");

const app = createApp({ serviceName: "representative-api", maxLatencyMs: 120 });

assert.deepEqual(app.handle("/health"), { status: 200, body: { ok: true, serviceName: "representative-api" } });
assert.equal(app.handle("/ready").body.maxLatencyMs, 120);
assert.equal(app.handle("/missing").status, 404);

console.log("node-service representative checks passed");
