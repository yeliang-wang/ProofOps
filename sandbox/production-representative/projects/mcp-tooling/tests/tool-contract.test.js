const assert = require("assert");
const { toolDefinition, collectReleaseSignal } = require("../src/tool");

assert.equal(toolDefinition.name, "collect_release_signal");
assert.deepEqual(toolDefinition.inputSchema.required, ["projectId", "signal"]);
assert.deepEqual(collectReleaseSignal({ projectId: "mcp-tooling", signal: "evidence" }), {
  projectId: "mcp-tooling",
  signal: "evidence",
  collected: true
});
assert.throws(() => collectReleaseSignal({ projectId: "mcp-tooling" }), /INVALID_INPUT/);

console.log("mcp-tooling representative checks passed");
