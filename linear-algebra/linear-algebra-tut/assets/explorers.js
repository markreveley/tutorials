/* Local geometry and accessible explorers. No network, dependencies, or storage.
   LinAlgMath is exported for the Node check in scripts/check_calculators.js. */
(function (root) {
  'use strict';
  function finite(x) {
    if (!Number.isFinite(x)) throw new Error('Enter finite numeric values.');
  }
  // Projection of v onto the line through d, in 2-D. Returns coefficient, projection, residual.
  function project2d(v, d) {
    v.forEach(finite); d.forEach(finite);
    const nd = Math.hypot(d[0], d[1]);
    if (nd === 0) throw new Error('The direction must not be the zero vector.');
    const u = [d[0] / nd, d[1] / nd];
    const coef = v[0] * u[0] + v[1] * u[1];
    const proj = [coef * u[0], coef * u[1]];
    const resid = [v[0] - proj[0], v[1] - proj[1]];
    const nv = Math.hypot(v[0], v[1]);
    const cos = nv === 0 ? NaN : coef / nv;
    return {coef, proj, resid, cos, normV: nv, normD: nd, dot: v[0] * d[0] + v[1] * d[1]};
  }
  // SVD of a real 2x2 matrix [[a, b], [c, d]] by the closed form through A^T A.
  // Returns s (descending), right singular vectors v1, v2 (unit), left u1, u2 (unit), rank.
  function svd2x2(a, b, c, d) {
    [a, b, c, d].forEach(finite);
    // A^T A = [[a^2 + c^2, ab + cd], [ab + cd, b^2 + d^2]]
    const p = a * a + c * c, q = a * b + c * d, r = b * b + d * d;
    const tr = p + r, det = p * r - q * q;
    const disc = Math.sqrt(Math.max(0, tr * tr / 4 - det));
    const l1 = tr / 2 + disc, l2 = Math.max(0, tr / 2 - disc);
    const s1 = Math.sqrt(l1), s2 = Math.sqrt(l2);
    // eigenvector of A^T A for l1
    let v1;
    if (Math.abs(q) > 1e-12) v1 = [q, l1 - p];
    else v1 = p >= r ? [1, 0] : [0, 1];
    const n1 = Math.hypot(v1[0], v1[1]); v1 = [v1[0] / n1, v1[1] / n1];
    const v2 = [-v1[1], v1[0]];
    const Av = v => [a * v[0] + b * v[1], c * v[0] + d * v[1]];
    const eps = 1e-12 * Math.max(1, s1);
    let u1 = s1 > eps ? Av(v1).map(x => x / s1) : [1, 0];
    let u2 = s2 > eps ? Av(v2).map(x => x / s2) : [-u1[1], u1[0]];
    const rank = (s1 > eps ? 1 : 0) + (s2 > eps ? 1 : 0);
    return {s: [s1, s2], v1, v2, u1, u2, rank, det: a * d - b * c};
  }
  root.LinAlgMath = {project2d, svd2x2};
  if (typeof document === 'undefined') return;

  const fmt = x => (Math.abs(x) < 5e-4 ? 0 : x).toFixed(3);
  // ---------- shared plane drawing: 420x420 viewBox, 10 units across ----------
  const SIZE = 420, UNITS = 5, SCALE = SIZE / (2 * UNITS);
  const px = x => SIZE / 2 + x * SCALE, py = y => SIZE / 2 - y * SCALE;
  function grid() {
    let s = '';
    for (let i = -UNITS; i <= UNITS; i++) {
      s += `<line class="grid" x1="${px(i)}" y1="0" x2="${px(i)}" y2="${SIZE}"/><line class="grid" x1="0" y1="${py(i)}" x2="${SIZE}" y2="${py(i)}"/>`;
    }
    s += `<line class="axis" x1="0" y1="${py(0)}" x2="${SIZE}" y2="${py(0)}"/><line class="axis" x1="${px(0)}" y1="0" x2="${px(0)}" y2="${SIZE}"/>`;
    s += `<text x="${px(UNITS) - 12}" y="${py(0) - 6}">x</text><text x="${px(0) + 6}" y="14">y</text>`;
    return s;
  }
  const seg = (cls, a, b) => `<line class="${cls}" x1="${px(a[0])}" y1="${py(a[1])}" x2="${px(b[0])}" y2="${py(b[1])}"/>`;
  const handle = (name, p) => `<circle class="handle" data-handle="${name}" cx="${px(p[0])}" cy="${py(p[1])}" r="8"><title>${name}: drag me</title></circle>`;
  const label = (p, text, dx, dy) => `<text x="${px(p[0]) + dx}" y="${py(p[1]) + dy}">${text}</text>`;

  function toPlane(svg, event) {
    const rect = svg.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width * SIZE, y = (event.clientY - rect.top) / rect.height * SIZE;
    const clamp = v => Math.max(-UNITS, Math.min(UNITS, Math.round(v * 10) / 10));
    return [clamp((x - SIZE / 2) / SCALE), clamp((SIZE / 2 - y) / SCALE)];
  }
  function wireDrag(svg, onMove) {
    let active = null;
    svg.addEventListener('pointerdown', e => {
      const h = e.target.closest('[data-handle]');
      if (!h) return;
      active = h.dataset.handle; svg.setPointerCapture(e.pointerId); e.preventDefault();
    });
    svg.addEventListener('pointermove', e => { if (active) onMove(active, toPlane(svg, e)); });
    svg.addEventListener('pointerup', () => { active = null; });
    svg.addEventListener('pointercancel', () => { active = null; });
  }

  function drawProjection(svg, v, d, r) {
    const nd = r.normD, far = [d[0] / nd * 20, d[1] / nd * 20], back = [-far[0], -far[1]];
    svg.innerHTML = grid() + seg('dir', back, far) + seg('resid', r.proj, v) + seg('proj', [0, 0], r.proj) + seg('vec', [0, 0], v) +
      label(v, 'v', 8, -8) + label(d, 'd', 8, 14) + label(r.proj, 'projection', 8, 16) + handle('v', v) + handle('d', d);
    svg.setAttribute('aria-label', `Vector v at (${fmt(v[0])}, ${fmt(v[1])}), direction d at (${fmt(d[0])}, ${fmt(d[1])}). Projection coefficient ${fmt(r.coef)}, residual length ${fmt(Math.hypot(r.resid[0], r.resid[1]))}.`);
  }
  function drawSvd(svg, a, b, c, d, r) {
    let pts = '';
    for (let t = 0; t <= 64; t++) {
      const th = 2 * Math.PI * t / 64, x = Math.cos(th), y = Math.sin(th);
      pts += `${px(a * x + b * y)},${py(c * x + d * y)} `;
    }
    const s1 = r.s[0], s2 = r.s[1];
    svg.innerHTML = grid() + `<circle class="circle" cx="${px(0)}" cy="${py(0)}" r="${SCALE}"/>` + `<polygon class="ellipse" points="${pts.trim()}"/>` +
      seg('dir', [0, 0], r.v1) + seg('dir', [0, 0], r.v2) + seg('sing', [0, 0], [s1 * r.u1[0], s1 * r.u1[1]]) + seg('sing', [0, 0], [s2 * r.u2[0], s2 * r.u2[1]]) +
      label(r.v1, 'v1', 6, -6) + label(r.v2, 'v2', 6, -6) + label([s1 * r.u1[0], s1 * r.u1[1]], 'σ1 u1', 6, -6) + label([s2 * r.u2[0], s2 * r.u2[1]], 'σ2 u2', 6, 14);
    svg.setAttribute('aria-label', `Unit circle mapped by the matrix to an ellipse with semi-axes ${fmt(s1)} and ${fmt(s2)}.`);
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-calculator]').forEach(form => {
      const output = form.querySelector('output');
      const svg = form.querySelector('svg.plane');
      function value(name) {
        const raw = form.elements.namedItem(name).value.trim();
        if (!raw) throw new Error('Complete every field.');
        return Number(raw);
      }
      function set(name, x) { form.elements.namedItem(name).value = fmt(x).replace(/\.?0+$/, ''); }
      function calculate(event) {
        if (event) event.preventDefault();
        try {
          switch (form.dataset.calculator) {
            case 'projection': {
              const v = [value('vx'), value('vy')], d = [value('dx'), value('dy')];
              const r = project2d(v, d);
              output.textContent = `v·d = ${fmt(r.dot)}. |d| = ${fmt(r.normD)}. Coefficient v·d/|d| = ${fmt(r.coef)} (the signed length of the orange segment). Projection = (${fmt(r.proj[0])}, ${fmt(r.proj[1])}). Residual = (${fmt(r.resid[0])}, ${fmt(r.resid[1])}), length ${fmt(Math.hypot(r.resid[0], r.resid[1]))}, and residual·d = ${fmt(r.resid[0] * d[0] + r.resid[1] * d[1])}. cos(v, d) = ${Number.isNaN(r.cos) ? 'undefined (v is zero)' : fmt(r.cos)}.`;
              if (svg) drawProjection(svg, v, d, r);
              break;
            }
            case 'svd': {
              const a = value('a'), b = value('b'), c = value('c'), d = value('d');
              const r = svd2x2(a, b, c, d);
              output.textContent = `Singular values σ1 = ${fmt(r.s[0])}, σ2 = ${fmt(r.s[1])}; rank ${r.rank}; determinant ${fmt(r.det)} (σ1·σ2 = ${fmt(r.s[0] * r.s[1])}). Right singular vectors (input directions, dashed): v1 = (${fmt(r.v1[0])}, ${fmt(r.v1[1])}), v2 = (${fmt(r.v2[0])}, ${fmt(r.v2[1])}). Left singular vectors (output directions): u1 = (${fmt(r.u1[0])}, ${fmt(r.u1[1])}), u2 = (${fmt(r.u2[0])}, ${fmt(r.u2[1])}). The matrix sends the unit circle to the ellipse with semi-axes σ1 u1 and σ2 u2.`;
              if (svg) drawSvd(svg, a, b, c, d, r);
              break;
            }
          }
        } catch (error) {
          output.textContent = error.message;
        }
      }
      form.addEventListener('submit', calculate);
      form.addEventListener('input', calculate);
      if (svg && form.dataset.calculator === 'projection') {
        wireDrag(svg, (name, p) => { set(name + 'x', p[0]); set(name + 'y', p[1]); calculate(); });
      }
      calculate();
    });
  });
})(typeof globalThis === 'undefined' ? window : globalThis);
