const assert = require("assert");
const { buildEvidence } = require("../src/pipeline");

assert.equal(typeof buildEvidence([]).digest, "string");

console.log("data-pipeline build contract passed");
