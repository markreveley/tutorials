/* Mathematical cross-checks for the browser controls, with no DOM dependency. */
const assert = require('node:assert/strict');
require('../assets/explorers.js');
const m=globalThis.StatsMath;
function near(a,b,tol=1e-10) { assert.ok(Math.abs(a-b)<tol, `${a} != ${b}`); }
let r=m.wilson(50,100); near(r.low,.4038315303659956); near(r.high,.5961684696340044);
for (const n of [1,10,100]) {
  for (let x=0;x<=n;x++) {
    const a=m.wilson(x,n), b=m.wilson(n-x,n);
    assert.ok(0<=a.low && a.low<=a.p && a.p<=a.high && a.high<=1);
    near(a.low,1-b.high); near(a.high,1-b.low);
  }
}
assert.equal(m.power(.5,3),2181);
r=m.reliability(.8,3); near(r.any,.992); near(r.all,.512);
assert.equal(m.reliability(0,10).any,0);
assert.equal(m.reliability(1,10).all,1);
for (const bad of [()=>m.wilson(11,10),()=>m.wilson(1,0),()=>m.wilson(NaN,10),
                  ()=>m.power(.5,0),()=>m.reliability(1.1,3),()=>m.reliability(.8,1.5)]) {
  assert.throws(bad);
}
console.log('PASS: browser calculator boundaries, binomial symmetry, reference values, planning, reliability, and invalid inputs.');
