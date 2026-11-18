"use strict";
const assert = require("node:assert/strict");
const { subnet, transfer, capacity } = require("../assets/explorers.js");
assert.deepEqual(subnet("10.20.1.42/24"), { network: "10.20.1.0/24", first: "10.20.1.0", last: "10.20.1.255", count: 256 });
assert.deepEqual(subnet("255.255.255.255/0"), { network: "0.0.0.0/0", first: "0.0.0.0", last: "255.255.255.255", count: 4294967296 });
assert.deepEqual(subnet("255.255.255.255/32"), { network: "255.255.255.255/32", first: "255.255.255.255", last: "255.255.255.255", count: 1 });
assert.equal(subnet("192.168.1.5/31").first, "192.168.1.4");
for (const input of ["999.1.1.1/24", "1.2.3.4/33", "1.2.3/24", "", "1.2.3.4/-1"]) assert.throws(() => subnet(input));
assert.equal(transfer(100, 100), 8);
assert.equal(transfer(0, 100), 0);
assert.equal(capacity(20, 3), 60);
assert.equal(capacity(0, 3), 0);
for (const bad of ["", -1, Infinity, "abc"]) {
  assert.throws(() => transfer(bad, 100));
  assert.throws(() => capacity(bad, 3));
}
assert.throws(() => transfer(100, 0));
assert.throws(() => capacity(20, 0));
console.log("PASS: subnet boundaries /0–/32, address normalization, units, capacity examples, and invalid inputs.");
