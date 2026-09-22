/* Local-only teaching controls. No requests, analytics, or external libraries. */
(function () {
  "use strict";
  function subnet(value) {
    var match = String(value).trim().match(/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\/(\d{1,2})$/);
    if (!match) throw new Error("Use four IPv4 octets and a prefix, such as 10.20.1.42/24.");
    var octets = match.slice(1, 5).map(Number), prefix = Number(match[5]);
    if (octets.some(function (n) { return n > 255; }) || prefix > 32) throw new Error("Each octet must be 0–255 and the prefix 0–32.");
    var number = octets.reduce(function (total, n) { return total * 256 + n; }, 0);
    var count = Math.pow(2, 32 - prefix), first = Math.floor(number / count) * count;
    function address(n) { return [24, 16, 8, 0].map(function (bits) { return Math.floor(n / Math.pow(2, bits)) % 256; }).join("."); }
    return { network: address(first) + "/" + prefix, first: address(first), last: address(first + count - 1), count: count };
  }
  function finite(value, name, allowZero) {
    if (String(value).trim() === "") throw new Error("Enter " + name + ".");
    var number = Number(value);
    if (!Number.isFinite(number) || (allowZero ? number < 0 : number <= 0)) throw new Error(name + " must be " + (allowZero ? "zero or greater." : "greater than zero."));
    return number;
  }
  function transfer(size, rate) { return finite(size, "Size", true) * 8 / finite(rate, "Bandwidth", false); }
  function capacity(rate, duration) { return finite(rate, "Rate", true) * finite(duration, "Mean duration", false); }
  if (typeof module !== "undefined" && module.exports) module.exports = { subnet: subnet, transfer: transfer, capacity: capacity };
  if (typeof document === "undefined") return;
  document.addEventListener("DOMContentLoaded", function () {
    function wire(selector, calculate) {
      var host = document.querySelector(selector);
      if (!host) return;
      var output = host.querySelector("[data-result]");
      function render() {
        try { output.textContent = calculate(host); output.removeAttribute("data-error"); }
        catch (error) { output.textContent = error.message; output.setAttribute("data-error", "true"); }
      }
      host.addEventListener("input", render); render();
    }
    wire("[data-subnet]", function (host) {
      var s = subnet(host.querySelector("input").value);
      return s.network + " contains " + s.first + " through " + s.last + " (" + s.count.toLocaleString() + " addresses, before reservations).";
    });
    wire("[data-transfer]", function (host) {
      var inputs = host.querySelectorAll("input"), seconds = transfer(inputs[0].value, inputs[1].value);
      return seconds.toLocaleString(undefined, { maximumFractionDigits: 4 }) + " seconds of serialization at the stated bottleneck rate. Other delays and overhead are excluded.";
    });
    wire("[data-capacity]", function (host) {
      var inputs = host.querySelectorAll("input"), count = capacity(inputs[0].value, inputs[1].value);
      return count.toLocaleString(undefined, { maximumFractionDigits: 2 }) + " attempts in flight on average at the target rate in a stable system. This is a relationship, not a guaranteed concurrency setting.";
    });
  });
})();
