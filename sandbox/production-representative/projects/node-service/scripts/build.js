const assert = require("assert");
const fs = require("fs");
const path = require("path");

const source = fs.readFileSync(path.join(__dirname, "..", "src", "server.js"), "utf8");
assert.match(source, /createApp/);
assert.match(source, /\/health/);

console.log("node-service build contract passed");
