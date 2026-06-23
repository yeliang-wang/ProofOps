const toolDefinition = {
  name: "collect_release_signal",
  description: "Collect a product-native release signal from a representative project.",
  inputSchema: {
    type: "object",
    required: ["projectId", "signal"],
    properties: {
      projectId: { type: "string" },
      signal: { type: "string", enum: ["evidence", "risk", "approval"] }
    }
  }
};

function collectReleaseSignal(input) {
  if (!input || !input.projectId || !input.signal) throw new Error("INVALID_INPUT");
  return { projectId: input.projectId, signal: input.signal, collected: true };
}

module.exports = { toolDefinition, collectReleaseSignal };
