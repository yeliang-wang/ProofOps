const assert = require("assert");
const { evaluateReleaseGate } = require("../src/quality");

assert.equal(evaluateReleaseGate({ maxLatencyMs: 100, errorRate: 0, approved: true }).status, "PASS");
assert.equal(evaluateReleaseGate({ maxLatencyMs: 500, errorRate: 0, approved: true }).status, "FAIL");

console.log("quality-gate build contract passed");
