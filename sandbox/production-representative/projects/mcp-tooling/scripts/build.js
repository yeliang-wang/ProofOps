const assert = require("assert");
const { toolDefinition } = require("../src/tool");

assert.equal(toolDefinition.inputSchema.type, "object");
assert.ok(toolDefinition.description.length > 20);

console.log("mcp-tooling build contract passed");
