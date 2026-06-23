const assert = require("assert");
const fs = require("fs");
const path = require("path");
const { releaseSummary } = require("../src/app");

const html = fs.readFileSync(path.join(__dirname, "..", "src", "index.html"), "utf8");
assert.match(html, /data-testid="release-dashboard"/);
assert.match(html, /approve-release/);
assert.deepEqual(releaseSummary([{ status: "ready" }, { status: "blocked" }]), { total: 2, ready: 1, blocked: 1 });

console.log("web-dashboard representative checks passed");
