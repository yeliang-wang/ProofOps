const crypto = require("crypto");

function buildEvidence(records) {
  const normalized = records.map((record) => ({
    id: String(record.id),
    status: String(record.status),
    score: Number(record.score)
  }));
  const digest = crypto.createHash("sha256").update(JSON.stringify(normalized)).digest("hex");
  return {
    count: normalized.length,
    passed: normalized.filter((record) => record.status === "PASS").length,
    digest
  };
}

module.exports = { buildEvidence };
