function evaluateReleaseGate(metrics) {
  const maxLatencyMs = Number(metrics.maxLatencyMs);
  const errorRate = Number(metrics.errorRate);
  const approved = Boolean(metrics.approved);
  return {
    status: maxLatencyMs <= 300 && errorRate <= 0.01 && approved ? "PASS" : "FAIL",
    reasons: [
      maxLatencyMs > 300 ? "latency" : "",
      errorRate > 0.01 ? "error-rate" : "",
      !approved ? "approval" : ""
    ].filter(Boolean)
  };
}

module.exports = { evaluateReleaseGate };
