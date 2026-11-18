/* Local arithmetic and accessible calculators. No network, dependencies, or storage. */
(function (root) {
  'use strict';
  const Z95 = 1.959963984540054;
  const Z80 = 0.8416212335729143;
  function finite(x) {
    if (!Number.isFinite(x)) throw new Error('Enter finite numeric values.');
  }
  function integer(x, low, high) {
    finite(x);
    if (!Number.isInteger(x) || x < low || x > high) throw new Error(`Enter a whole number from ${low} to ${high}.`);
  }
  function wilson(passes, trials) {
    integer(trials, 1, 1e9); integer(passes, 0, trials);
    const p = passes / trials, z2 = Z95 * Z95, d = 1 + z2 / trials;
    const center = (p + z2 / (2 * trials)) / d;
    const half = Z95 * Math.sqrt(p * (1 - p) / trials + z2 / (4 * trials * trials)) / d;
    return {p, low: passes === 0 ? 0 : Math.max(0, center - half), high: passes === trials ? 1 : Math.min(1, center + half)};
  }
  function power(sd, deltaPoints) {
    finite(sd); finite(deltaPoints);
    if (sd <= 0 || sd > 2 || deltaPoints < .001 || deltaPoints > 100) throw new Error('Use SD in (0, 2] and an effect from 0.001 to 100 percentage points.');
    return Math.ceil(((Z95 + Z80) * sd / (deltaPoints / 100)) ** 2);
  }
  function reliability(p, k) {
    finite(p); integer(k, 1, 10000);
    if (p < 0 || p > 1) throw new Error('Probability must lie between zero and one.');
    return {any: p === 1 ? 1 : -Math.expm1(k * Math.log1p(-p)), all: p ** k};
  }
  root.StatsMath = {wilson, power, reliability};
  if (typeof document === 'undefined') return;
  const percent = x => (100*x).toFixed(2) + '%';
  function plot(svg, result) {
    const x = p => 30 + 500*p;
    svg.setAttribute('aria-label', `Observed rate ${percent(result.p)}. 95% Wilson interval ${percent(result.low)} to ${percent(result.high)} on a 0 to 100 percent scale.`);
    svg.innerHTML = '<line class="axis" x1="30" y1="52" x2="530" y2="52"/>' +
      [0,.25,.5,.75,1].map(p => `<line class="axis" x1="${x(p)}" x2="${x(p)}" y1="48" y2="58"/><text x="${x(p)}" y="80" text-anchor="middle">${p*100}%</text>`).join('') +
      `<line class="interval" x1="${x(result.low)}" x2="${x(result.high)}" y1="30" y2="30"/><circle class="point" cx="${x(result.p)}" cy="30" r="7"/>`;
  }
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-calculator]').forEach(form => {
      const output = form.querySelector('output');
      function value(name) {
        const raw = form.elements.namedItem(name).value.trim();
        if (!raw) throw new Error('Complete every field.');
        return Number(raw);
      }
      function calculate(event) {
        if (event) event.preventDefault();
        try {
          switch (form.dataset.calculator) {
            case 'wilson': {
              const r = wilson(value('passes'), value('trials'));
              output.textContent = `Observed rate: ${percent(r.p)}. 95% Wilson interval: ${percent(r.low)} to ${percent(r.high)}. Width: ${(100*(r.high-r.low)).toFixed(2)} percentage points.`;
              const svg = form.querySelector('svg'); svg.style.display = ''; plot(svg, r); break;
            }
            case 'power':
              output.textContent = `${power(value('sd'), value('delta')).toLocaleString()} independent pairs, approximately. Revisit the assumptions before treating this as an experiment budget.`; break;
            case 'reliability': {
              const r = reliability(value('p'), value('k'));
              output.textContent = `At least one success: ${percent(r.any)}. Every attempt succeeds: ${percent(r.all)}.`; break;
            }
          }
        } catch (error) {
          output.textContent = error.message;
          const svg = form.querySelector('svg'); if (svg) svg.style.display = 'none';
        }
      }
      form.addEventListener('submit', calculate);
      form.addEventListener('input', calculate);
      calculate();
    });
  });
})(typeof globalThis === 'undefined' ? window : globalThis);
