const assert = require("assert");
const fs = require("fs");
const path = require("path");

const html = fs.readFileSync(path.join(__dirname, "..", "src", "index.html"), "utf8");
assert.match(html, /<!doctype html>/i);
assert.match(html, /Release Operations/);

console.log("web-dashboard build contract passed");
