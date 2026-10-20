#!/usr/bin/env node
/* eval-tut QA: nav paths exist, every page is in nav, internal hrefs/src + anchors resolve,
   data-g slugs exist and are marked once per page, every h2/h3 has an id, template invariants hold,
   <pre> blocks have no unescaped '<' or '&', cite links have a title, course pages have a srcbox
   and a pitfall/warn box, glossary defs use single-quoted hrefs that resolve.
   Usage: node research/qa.js   (adapted from linux/linux-tut/research/qa.js) */
const fs = require("fs"), path = require("path");
const root = path.join(__dirname, "..");
global.window = {};
require(path.join(root, "assets/nav-data.js"));
require(path.join(root, "assets/glossary-data.js"));
const NAV = window.NAV, G = window.GLOSSARY;
const navPaths = NAV.flatMap(m => m.pages.map(p => p.path));
let problems = 0;
const bad = (f, msg) => { problems++; console.log(`${f}: ${msg}`); };

for (const p of navPaths) if (!fs.existsSync(path.join(root, p))) bad(p, "in nav but missing on disk");
const onDisk = ["index.html", "glossary.html", "bibliography.html"].filter(f => fs.existsSync(path.join(root, f)))
  .concat(...["pages", "appendices"].map(d => fs.readdirSync(path.join(root, d)).filter(f => f.endsWith(".html")).map(f => `${d}/${f}`)));
for (const f of onDisk) if (!navPaths.includes(f)) bad(f, "on disk but not in nav");

const read = f => fs.readFileSync(path.join(root, f), "utf8");
const ids = {};
for (const f of onDisk) ids[f] = new Set([...read(f).matchAll(/\sid="([^"]+)"/g)].map(m => m[1]));

const only = process.argv.slice(2);
for (const f of onDisk) {
  const html = read(f), dir = path.dirname(f), isCourse = dir === "pages", deep = dir !== ".";
  const pre = deep ? "../" : "";
  for (const need of [`href="${pre}assets/style.css"`, `src="${pre}assets/nav-data.js"`, `src="${pre}assets/glossary-data.js"`, `src="${pre}assets/wiki.js"`,
    'class="sidebar" data-nav', '<main class="page">', 'class="kicker"', "<h1", 'class="lede"', "· Understanding LLM Evals</title>"])
    if (!html.includes(need) && !(f === "index.html" && need.includes("</title>"))) bad(f, `template: missing ${need}`);
  if ((html.match(/<h1/g) || []).length !== 1) bad(f, "must have exactly one h1");
  for (const m of html.matchAll(/<h[23](?![^>]*\sid=)[^>]*>/g)) if (f !== "index.html") bad(f, `heading without id: ${m[0]}`);
  const seen = new Set();
  for (const m of html.matchAll(/\sid="([^"]+)"/g)) { if (seen.has(m[1])) bad(f, `duplicate id ${m[1]}`); seen.add(m[1]); }
  if (isCourse) {
    if (!html.includes('class="srcbox"')) bad(f, "course page lacks .srcbox");
    if (!/class="(pitfall|warn)"/.test(html)) bad(f, "course page lacks pitfall/warn");
  }
  // hrefs and srcs
  for (const m of html.matchAll(/<(?:a|link|script)\s[^>]*(?:href|src)="([^"]+)"[^>]*>/g)) {
    const href = m[1], tag = m[0];
    if (/^(https?:|mailto:)/.test(href)) { if (/class="cite"/.test(tag) && !/title="/.test(tag)) bad(f, `cite without title: ${href}`); continue; }
    if (/class="cite"/.test(tag)) bad(f, `cite with non-http href: ${href}`);
    const [p, frag] = href.split("#");
    const target = p ? path.normalize(path.join(dir, p)) : f;
    if (target.startsWith("..")) {                   // sibling course link
      if (!fs.existsSync(path.join(root, target))) bad(f, `broken sibling-course link ${href}`);
      continue;
    }
    if (!fs.existsSync(path.join(root, target))) { bad(f, `broken link ${href}`); continue; }
    if (frag && target === "glossary.html") { if (!G[frag] && !/^letter-/.test(frag)) bad(f, `glossary anchor unknown: ${frag}`); }
    else if (frag && ids[target] && !ids[target].has(frag)) bad(f, `broken anchor ${href}`);
  }
  // glossary slugs: must exist, marked once per page, never inside h1/h2/h3/lede
  const marked = {};
  for (const m of html.matchAll(/data-g="([^"]+)"/g)) { if (!G[m[1]]) bad(f, `unknown glossary slug ${m[1]}`); marked[m[1]] = (marked[m[1]] || 0) + 1; }
  for (const [s, n] of Object.entries(marked)) if (n > 1) bad(f, `term ${s} marked ${n}x (first mention only)`);
  for (const m of html.matchAll(/<(h[123]|p class="lede")[^>]*>[\s\S]*?<\/(?:h[123]|p)>/g)) if (/data-g=/.test(m[0])) console.log(`WARN ${f}: term marked inside heading/lede (style only): ${m[0].slice(0, 50).replace(/\s+/g, " ")}`);
  // pre blocks
  for (const m of html.matchAll(/<pre[^>]*>([\s\S]*?)<\/pre>/g)) {
    const inner = m[1].replace(/<\/?(span|a|strong|em|code|mark|b|i)(\s[^>]*)?>/g, "");
    const lt = inner.match(/<[^\n]{0,40}/);
    if (lt) bad(f, `unescaped '<' inside <pre>: ${JSON.stringify(lt[0])}`);
    const amp = inner.match(/&(?!(amp|lt|gt|quot|apos|nbsp|hellip|mdash|ndash|larr|rarr|#\d+|#x[0-9a-fA-F]+);)[^\n]{0,20}/);
    if (amp) bad(f, `unescaped '&' inside <pre>: ${JSON.stringify(amp[0])}`);
  }
  // body prose word count (course pages), excluding scripts, pre blocks, tables and the source box
  if (isCourse && (only.length === 0 || only.includes(f))) {
    const body = html.replace(/<script[\s\S]*?<\/script>/g, "").replace(/<pre[\s\S]*?<\/pre>/g, "")
      .replace(/<table[\s\S]*?<\/table>/g, "").replace(/<div class="srcbox">[\s\S]*?<\/div>/g, "")
      .replace(/<div class="diagram">[\s\S]*?<\/div>/g, "").replace(/<[^>]+>/g, " ");
    const words = body.split(/\s+/).filter(Boolean).length;
    if (words < 700) bad(f, `short page: ~${words} words`);   // existing course pages run ~750–1,200 by this loose count; Module 8 pages ~2,200
    if (only.length) console.log(`${f}: ~${words} words of prose`);
  }
}
// glossary-internal links
for (const [slug, e] of Object.entries(G)) {
  for (const m of (e.def || "").matchAll(/href='([^']+)'/g)) {
    const [p, frag] = m[1].split("#");
    if (/^https?:/.test(p)) continue;
    if (!fs.existsSync(path.join(root, p))) bad(`glossary:${slug}`, `broken link ${m[1]}`);
    else if (frag && p === "glossary.html") { if (!G[frag]) bad(`glossary:${slug}`, `unknown glossary anchor ${frag}`); }
    else if (frag && ids[p] && !ids[p].has(frag)) bad(`glossary:${slug}`, `broken anchor ${m[1]}`);
  }
  if (/href="/.test(e.def || "")) bad(`glossary:${slug}`, "use single-quoted hrefs");
  for (const s of e.see || []) if (!G[s]) bad(`glossary:${slug}`, `see-also points to unknown slug ${s}`);
}
console.log(problems ? `\n${problems} problem(s)` : `OK — ${onDisk.length} pages, ${Object.keys(G).length} glossary entries`);
process.exit(problems ? 1 : 0);
