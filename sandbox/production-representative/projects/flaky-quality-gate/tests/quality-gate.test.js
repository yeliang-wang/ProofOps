const assert = require("assert");
const { evaluateReleaseGate } = require("../src/quality");

const metrics = process.env.OCTOPUS_REPRESENTATIVE_FAULT === "latency-regression"
  ? { maxLatencyMs: 900, errorRate: 0.001, approved: true }
  : { maxLatencyMs: 180, errorRate: 0.001, approved: true };

const result = evaluateReleaseGate(metrics);
assert.equal(result.status, "PASS");
assert.deepEqual(result.reasons, []);

console.log("quality-gate representative checks passed");
