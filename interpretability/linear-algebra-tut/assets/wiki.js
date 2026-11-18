/* linear-algebra-tut shared runtime: sidebar nav, search, prev/next, glossary tooltips.
   Pure static — no fetch(), works from file://. Data comes from nav-data.js
   and glossary-data.js, which must be included before this script. */
(function () {
  "use strict";

  // Site root relative to the current page, derived from this script's src.
  var scripts = document.getElementsByTagName("script");
  var ROOT = "";
  for (var i = 0; i < scripts.length; i++) {
    var m = (scripts[i].getAttribute("src") || "").match(/^(.*)assets\/wiki\.js$/);
    if (m) { ROOT = m[1]; break; }
  }

  var NAV = window.NAV || [];
  var GLOSSARY = window.GLOSSARY || {};

  // Flat ordered page list for prev/next and current-page detection.
  var flat = [];
  NAV.forEach(function (mod) {
    mod.pages.forEach(function (p) { flat.push(p); });
  });

  function currentPath() {
    var here = location.pathname.replace(/\\/g, "/");
    for (var i = 0; i < flat.length; i++) {
      if (here.slice(-flat[i].path.length) === flat[i].path) return flat[i].path;
    }
    if (/\/$/.test(here)) return "index.html";
    return null;
  }
  var cur = currentPath();

  /* ---------- sidebar ---------- */
  function buildSidebar(el) {
    var html = '<p class="site-title"><a href="' + ROOT + 'index.html">Linear Algebra for Interpretability</a></p>' +
      '<p class="site-sub">from activation vectors to directions you can defend</p>' +
      '<input class="search" type="search" placeholder="Search pages &amp; glossary…" aria-label="Search">' +
      '<div class="search-results" aria-live="polite" style="display:none"></div>';
    NAV.forEach(function (mod) {
      html += '<div class="nav-module"><span class="mod-label">' + mod.module + "</span>";
      mod.pages.forEach(function (p) {
        var cls = p.path === cur ? ' class="current"' : "";
        html += '<a href="' + ROOT + p.path + '"' + cls + ">" +
          (p.n ? '<span class="pgnum">' + p.n + "</span>" : "") + p.title + "</a>";
      });
      html += "</div>";
    });
    el.innerHTML = html;

    // scroll current link into view
    var curLink = el.querySelector("a.current");
    if (curLink) { curLink.setAttribute("aria-current", "page"); if (window.innerWidth > 900) el.scrollTop = Math.max(0, curLink.offsetTop - el.clientHeight / 2); }

    /* search */
    var input = el.querySelector(".search");
    var results = el.querySelector(".search-results");
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      if (!q) { results.style.display = "none"; results.innerHTML = ""; return; }
      var out = [];
      flat.forEach(function (p) {
        if ((p.title + " " + (p.kw || "")).toLowerCase().indexOf(q) !== -1) {
          out.push('<a href="' + ROOT + p.path + '">' + p.title + '<span class="kind">page</span></a>');
        }
      });
      Object.keys(GLOSSARY).forEach(function (slug) {
        var g = GLOSSARY[slug];
        var hay = (g.name + " " + (g.also || "") + " " + g.def).toLowerCase();
        if (hay.indexOf(q) !== -1) {
          out.push('<a href="' + ROOT + "glossary.html#" + slug + '">' + g.name + '<span class="kind">term</span></a>');
        }
      });
      results.innerHTML = out.length ? out.slice(0, 20).join("") : '<div class="empty">No matches.</div>';
      results.style.display = "block";
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { input.value = ""; results.style.display = "none"; }
    });
  }

  /* ---------- prev / next ---------- */
  function buildPageNav() {
    if (document.querySelector(".pagenav")) return;
    if (!cur || cur === "index.html") return;
    var idx = -1;
    for (var i = 0; i < flat.length; i++) if (flat[i].path === cur) { idx = i; break; }
    if (idx < 0) return;
    var main = document.querySelector("main.page");
    if (!main) return;
    var prev = idx > 0 ? flat[idx - 1] : null;
    var next = idx < flat.length - 1 ? flat[idx + 1] : null;
    var html = '<div class="pagenav">';
    if (prev) html += '<a class="prev" href="' + ROOT + prev.path + '"><span class="dir">&larr; Previous</span>' + prev.title + "</a>";
    if (next) html += '<a class="next" href="' + ROOT + next.path + '"><span class="dir">Next &rarr;</span>' + next.title + "</a>";
    html += "</div>";
    main.insertAdjacentHTML("beforeend", html);
  }

  /* ---------- heading anchors ---------- */
  function addAnchors() {
    document.querySelectorAll("main.page h2[id], main.page h3[id]").forEach(function (h) {
      var a = document.createElement("a");
      a.className = "anchor";
      a.href = "#" + h.id;
      a.textContent = "#";
      h.appendChild(a);
    });
  }

  /* ---------- glossary tooltips ---------- */
  var tip = null;
  var tipOwner = null;
  function showTip(el) {
    var slug = el.getAttribute("data-g");
    var g = GLOSSARY[slug];
    if (!g) return;
    hideTip();
    tip = document.createElement("div");
    tip.className = "term-tip";
    tip.id = "active-term-tip";
    tip.setAttribute("role", "tooltip");
    tipOwner = el;
    el.setAttribute("aria-describedby", tip.id);
    tip.innerHTML = '<span class="tt-name">' + g.name + "</span>" + g.short +
      ' <span>Follow the term for its full definition.</span>';
    document.body.appendChild(tip);
    var r = el.getBoundingClientRect();
    var top = r.bottom + window.scrollY + 6;
    var left = Math.min(r.left + window.scrollX, window.scrollX + document.documentElement.clientWidth - 360);
    tip.style.top = top + "px";
    tip.style.left = Math.max(8, left) + "px";
  }
  function hideTip() {
    if (tip) { tip.remove(); tip = null; }
    if (tipOwner) { tipOwner.removeAttribute("aria-describedby"); tipOwner = null; }
  }
  function wireTerms() {
    document.querySelectorAll(".term[data-g]").forEach(function (el) {
      var slug = el.getAttribute("data-g");
      if (!GLOSSARY[slug]) { el.classList.add("term-missing"); return; }
      el.setAttribute("tabindex", "0");
      el.addEventListener("mouseenter", function () { showTip(el); });
      el.addEventListener("mouseleave", hideTip);
      el.addEventListener("focus", function () { showTip(el); });
      el.addEventListener("blur", hideTip);
      el.setAttribute("href", ROOT + "glossary.html#" + slug);
    });
    // keep tooltip when hovering it? simple version: hide on scroll
    window.addEventListener("scroll", hideTip, { passive: true });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") hideTip(); });
  }

  /* ---------- glossary page render ---------- */
  function renderGlossary() {
    var host = document.querySelector("[data-glossary]");
    if (!host || host.children.length) return;
    var slugs = Object.keys(GLOSSARY).sort(function (a, b) {
      return GLOSSARY[a].name.toLowerCase().localeCompare(GLOSSARY[b].name.toLowerCase());
    });
    var byLetter = {};
    slugs.forEach(function (s) {
      var L = GLOSSARY[s].name[0].toUpperCase();
      if (!/[A-Z]/.test(L)) L = "#";
      (byLetter[L] = byLetter[L] || []).push(s);
    });
    var letters = Object.keys(byLetter).sort();
    var html = '<div class="gloss-index">' + letters.map(function (L) {
      return '<a href="#letter-' + L + '">' + L + "</a>";
    }).join("") + "</div>";
    letters.forEach(function (L) {
      html += '<div class="gloss-letter" id="letter-' + L + '">' + L + "</div>";
      byLetter[L].forEach(function (s) {
        var g = GLOSSARY[s];
        html += '<div class="gloss-entry" id="' + s + '"><h3>' + g.name + "</h3>";
        if (g.also) html += '<p class="gloss-also">Also: ' + g.also + "</p>";
        html += "<p>" + g.def + "</p>";
        if (g.see && g.see.length) {
          html += '<p class="gloss-also">See: ' + g.see.map(function (ref) {
            return GLOSSARY[ref] ? '<a href="#' + ref + '">' + GLOSSARY[ref].name + "</a>" : ref;
          }).join(", ") + "</p>";
        }
        html += "</div>";
      });
    });
    host.innerHTML = html;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var side = document.querySelector("[data-nav]");
    if (side) buildSidebar(side);
    renderGlossary();
    buildPageNav();
    addAnchors();
    wireTerms();
  });
})();
