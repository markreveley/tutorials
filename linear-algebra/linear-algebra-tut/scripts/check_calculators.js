/* Mathematical cross-checks for the browser explorers, with no DOM dependency. */
const assert = require('node:assert/strict');
require('../assets/explorers.js');
const m = globalThis.LinAlgMath;
function near(a, b, tol = 1e-9) { assert.ok(Math.abs(a - b) < tol, `${a} != ${b}`); }
// Hand-computed projections (same cases as labs/test_linalg.py).
let r = m.project2d([3, 4], [1, 0]);
near(r.coef, 3); near(r.proj[0], 3); near(r.proj[1], 0); near(r.resid[0], 0); near(r.resid[1], 4); near(r.cos, 0.6);
r = m.project2d([3, 4], [1, 1]);
near(r.coef, 7 / Math.SQRT2); near(r.proj[0], 3.5); near(r.proj[1], 3.5); near(r.resid[0], -0.5); near(r.resid[1], 0.5);
const r2 = m.project2d([3, 4], [10, 10]);
near(r.coef, r2.coef); near(r.proj[0], r2.proj[0]);
// Residual is orthogonal to d and Pythagoras holds, on a grid of cases.
for (let vx = -3; vx <= 3; vx += 1.5) for (let vy = -3; vy <= 3; vy += 1.5) for (const d of [[1, 2], [-2, 0.5], [0, 1]]) {
  const q = m.project2d([vx, vy], d);
  near(q.resid[0] * d[0] + q.resid[1] * d[1], 0, 1e-9);
  near(q.proj[0] ** 2 + q.proj[1] ** 2 + q.resid[0] ** 2 + q.resid[1] ** 2, vx * vx + vy * vy, 1e-9);
}
assert.throws(() => m.project2d([1, 1], [0, 0]));
assert.throws(() => m.project2d([NaN, 1], [1, 0]));
// SVD of known matrices.
let s = m.svd2x2(3, 0, 0, 2);               // diagonal: singular values 3 and 2
near(s.s[0], 3); near(s.s[1], 2); assert.equal(s.rank, 2); near(Math.abs(s.v1[0]), 1); near(Math.abs(s.u1[0]), 1);
s = m.svd2x2(1, 2, 2, 4);                   // rank one: rows proportional; sigma1 = sqrt(1+4+4+16) = 5
near(s.s[0], 5); near(s.s[1], 0, 1e-7); assert.equal(s.rank, 1); near(Math.abs(s.v1[0] * 2 - s.v1[1]), 0, 1e-9);
s = m.svd2x2(0, -1, 1, 0);                  // rotation: both singular values 1
near(s.s[0], 1); near(s.s[1], 1); near(s.det, 1);
s = m.svd2x2(0, 0, 0, 0);
assert.equal(s.rank, 0);
// Reconstruction A = s1 u1 v1^T + s2 u2 v2^T and orthonormality, on random matrices.
let seed = 7; const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648 - 0.5) * 6;
for (let i = 0; i < 200; i++) {
  const a = rnd(), b = rnd(), c = rnd(), d = rnd();
  const t = m.svd2x2(a, b, c, d);
  const A = [[a, b], [c, d]];
  const rec = [[0, 0], [0, 0]];
  for (const [sig, u, v] of [[t.s[0], t.u1, t.v1], [t.s[1], t.u2, t.v2]]) for (let r = 0; r < 2; r++) for (let k = 0; k < 2; k++) rec[r][k] += sig * u[r] * v[k];
  for (let r = 0; r < 2; r++) for (let k = 0; k < 2; k++) near(rec[r][k], A[r][k], 1e-8);
  near(t.v1[0] * t.v2[0] + t.v1[1] * t.v2[1], 0, 1e-9); near(t.u1[0] * t.u2[0] + t.u1[1] * t.u2[1], 0, 1e-7);
  near(Math.hypot(...t.u1), 1, 1e-9); near(Math.hypot(...t.v1), 1, 1e-9);
  assert.ok(t.s[0] >= t.s[1] && t.s[1] >= 0);
  near(t.s[0] * t.s[1], Math.abs(a * d - b * c), 1e-7);  // product of singular values is |det|
}
assert.throws(() => m.svd2x2(1, Infinity, 0, 1));
console.log('PASS: projection hand values, orthogonal residuals, Pythagoras, SVD known matrices, reconstruction, orthonormality, determinant, invalid inputs.');
