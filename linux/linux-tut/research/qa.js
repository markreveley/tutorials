#!/usr/bin/env node
/* linux-tut QA: nav paths exist, every page is in nav, internal hrefs + anchors resolve,
   data-g slugs exist, template invariants hold, <pre> blocks have no raw '<' that isn't a tag
   we allow, cite links have title+http href, srcbox/lab/evals present on course pages.
   Usage: node research/qa.js  (from the site root or anywhere) */
const fs = require("fs"), path = require("path");
const root = path.join(__dirname, "..");
global.window = {};
require(path.join(root, "assets/nav-data.js"));
try { require(path.join(root, "assets/glossary-data.js")); } catch (e) { window.GLOSSARY = {}; console.log("WARN no glossary-data.js yet"); }
const NAV = window.NAV, G = window.GLOSSARY;
const navPaths = NAV.flatMap(m => m.pages.map(p => p.path));
let problems = 0;
const bad = (f, msg) => { problems++; console.log(`${f}: ${msg}`); };

for (const p of navPaths) if (!fs.existsSync(path.join(root, p))) bad(p, "in nav but missing on disk");
const onDisk = ["index.html", "glossary.html", "bibliography.html"].filter(f => fs.existsSync(path.join(root, f)))
  .concat(...["pages", "appendices"].map(d => fs.readdirSync(path.join(root, d)).filter(f => f.endsWith(".html")).map(f => `${d}/${f}`)));
for (const f of onDisk) if (!navPaths.includes(f)) bad(f, "on disk but not in nav");

const ids = {};
const read = f => fs.readFileSync(path.join(root, f), "utf8");
for (const f of onDisk) ids[f] = new Set([...read(f).matchAll(/\sid="([^"]+)"/g)].map(m => m[1]));

for (const f of onDisk) {
  const html = read(f), dir = path.dirname(f), isCourse = dir === "pages", deep = dir !== ".";
  const pre = deep ? "../" : "";
  for (const need of [`href="${pre}assets/style.css"`, `src="${pre}assets/nav-data.js"`, `src="${pre}assets/glossary-data.js"`, `src="${pre}assets/wiki.js"`,
    'class="sidebar" data-nav', '<main class="page">', 'class="kicker"', "<h1", 'class="lede"', "· Linux for Evals Engineers</title>"])
    if (!html.includes(need) && !(f === "index.html" && need.includes("</title>"))) bad(f, `template: missing ${need}`);
  if ((html.match(/<h1/g) || []).length !== 1) bad(f, "must have exactly one h1");
  for (const m of html.matchAll(/<h[23](?![^>]*\sid=)[^>]*>/g)) if (f !== "index.html") bad(f, `heading without id: ${m[0]}`);  // index modcards use bare h3
  const seen = new Set();
  for (const m of html.matchAll(/\sid="([^"]+)"/g)) { if (seen.has(m[1])) bad(f, `duplicate id ${m[1]}`); seen.add(m[1]); }
  if (isCourse) {
    for (const cls of ["srcbox", "lab", "evals", "check"]) if (!html.includes(`class="${cls}"`)) bad(f, `course page lacks .${cls}`);
    if (!/class="(pitfall|warn)"/.test(html)) bad(f, "course page lacks pitfall/warn");
  }
  // hrefs
  for (const m of html.matchAll(/<a\s[^>]*href="([^"]+)"[^>]*>/g)) {
    const href = m[1], tag = m[0];
    if (/^(https?:|mailto:)/.test(href)) { if (/class="cite"/.test(tag) && !/title="/.test(tag)) bad(f, `cite without title: ${href}`); continue; }
    if (/class="cite"/.test(tag)) bad(f, `cite with non-http href: ${href}`);
    const [p, frag] = href.split("#");
    const target = p ? path.normalize(path.join(dir, p)) : f;
    if (target.startsWith("..")) {                   // sibling course link
      if (!fs.existsSync(path.join(root, target))) bad(f, `broken external-relative link ${href}`);
      continue;
    }
    if (!fs.existsSync(path.join(root, target))) { bad(f, `broken link ${href}`); continue; }
    if (frag && target === "glossary.html") { if (!G[frag] && !/^letter-/.test(frag)) bad(f, `glossary anchor unknown: ${frag}`); }
    else if (frag && ids[target] && !ids[target].has(frag)) bad(f, `broken anchor ${href}`);
  }
  // glossary slugs
  const marked = {};
  for (const m of html.matchAll(/data-g="([^"]+)"/g)) { if (!G[m[1]]) bad(f, `unknown glossary slug ${m[1]}`); marked[m[1]] = (marked[m[1]] || 0) + 1; }
  for (const [s, n] of Object.entries(marked)) if (n > 1) bad(f, `term ${s} marked ${n}x (first mention only)`);
  // pre blocks: only span/a/strong/em/code/mark tags allowed; anything else with '<' is an escaping bug
  for (const m of html.matchAll(/<pre[^>]*>([\s\S]*?)<\/pre>/g)) {
    const inner = m[1].replace(/<\/?(span|a|strong|em|code|mark|b|i)(\s[^>]*)?>/g, "");
    const lt = inner.match(/<[^\n]{0,40}/);
    if (lt) bad(f, `unescaped '<' inside <pre>: ${JSON.stringify(lt[0])}`);
    const amp = inner.match(/&(?!(amp|lt|gt|quot|apos|nbsp|hellip|mdash|ndash|larr|rarr|#\d+|#x[0-9a-fA-F]+);)[^\n]{0,20}/);
    if (amp) bad(f, `unescaped '&' inside <pre>: ${JSON.stringify(amp[0])}`);
  }
  // words
  const text = html.replace(/<script[\s\S]*?<\/script>/g, "").replace(/<[^>]+>/g, " ");
  const words = text.split(/\s+/).filter(Boolean).length;
  if (isCourse && words < 1300) bad(f, `short page: ~${words} words`);
}
// glossary-internal links
for (const [slug, e] of Object.entries(G)) {
  for (const m of (e.def || "").matchAll(/href='([^']+)'/g)) {
    const [p, frag] = m[1].split("#");
    if (/^https?:/.test(p)) continue;
    if (!fs.existsSync(path.join(root, p))) bad(`glossary:${slug}`, `broken link ${m[1]}`);
    else if (frag && ids[p] && !ids[p].has(frag)) bad(`glossary:${slug}`, `broken anchor ${m[1]}`);
  }
  if (/href="/.test(e.def || "")) bad(`glossary:${slug}`, "use single-quoted hrefs");
}
console.log(problems ? `\n${problems} problem(s)` : `OK — ${onDisk.length} pages, ${Object.keys(G).length} glossary entries`);
process.exit(problems ? 1 : 0);
