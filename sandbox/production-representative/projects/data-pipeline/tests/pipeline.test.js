const assert = require("assert");
const { buildEvidence } = require("../src/pipeline");

const evidence = buildEvidence([
  { id: "run-1", status: "PASS", score: 98 },
  { id: "run-2", status: "BLOCKED", score: 0 }
]);

assert.equal(evidence.count, 2);
assert.equal(evidence.passed, 1);
assert.match(evidence.digest, /^[a-f0-9]{64}$/);

console.log("data-pipeline representative checks passed");
