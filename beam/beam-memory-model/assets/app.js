/* ============================================================
   Shared chrome + diagram helpers for the Elixir→BEAM wiki.
   Pages call WIKI.mount('<slug>') after their <main> content.
   ============================================================ */
const WIKI = (() => {
  const PAGES = [
    { slug: 'index',                 rung: '·', title: 'Overview',                  level: 'the ladder',
      blurb: 'Why these layers, and how to read them.' },
    { slug: 'elixir-to-bytecode',    rung: '1', title: 'From Elixir to Bytecode',   level: 'source',
      blurb: 'Your code is rewritten, not transliterated, into a register machine.' },
    { slug: 'machine-word-and-tags', rung: '2', title: 'The Machine Word & Tags',   level: 'terms',
      blurb: 'One word, self-describing. Immediates vs boxed, and the tag-bit trick.' },
    { slug: 'tuples-vs-lists',       rung: '3', title: 'Tuples vs Lists in Memory', level: 'structures',
      blurb: 'Contiguous block vs linked cons cells — where O(1) and O(n) come from.' },
    { slug: 'structural-sharing',    rung: '4', title: 'Structural Sharing',        level: 'structures',
      blurb: 'The graph-of-arrows model: where "shared, not copied" values actually live.' },
    { slug: 'atoms-and-atom-table',  rung: '5', title: 'Atoms & the Atom Table',    level: 'structures',
      blurb: 'A name that is its own identity — interned once, globally.' },
    { slug: 'maps',                  rung: '6', title: 'Maps: Flat & Hashed',       level: 'structures',
      blurb: 'Two layouts behind one syntax: a sorted flatmap, then a hash-array-mapped trie.' },
    { slug: 'runtime-reads-memory',  rung: '7', title: 'How the Runtime Reads It',  level: 'metal',
      blurb: 'Tag → mask → dereference → header. The BEAM as a native program over the OS.' },
    { slug: 'gc-and-process-memory', rung: '8', title: 'GC & Process Memory',       level: 'metal',
      blurb: 'Stack↔heap in one block; a per-process copying generational collector.' },
    { slug: 'message-passing',       rung: '9', title: 'Message Passing & Copying', level: 'metal',
      blurb: 'Isolated heaps mean messages are copied — except big binaries, shared off-heap.' },
    { slug: 'structural-vs-semantic',rung: '10',title: 'Structural vs Semantic',    level: 'payoff',
      blurb: 'Why "álien" > "office": representation leaking into observable order.' },
  ];

  let atRoot = false; // true when the current page is index.html (one level up from pages/)

  function mount(slug) {
    atRoot = (slug === 'index');
    const cur = PAGES.findIndex(p => p.slug === slug);
    document.querySelectorAll('[data-nav]').forEach(el => {
      el.innerHTML = navHTML(slug);
    });
    document.querySelectorAll('[data-pager]').forEach(el => {
      el.innerHTML = pagerHTML(cur);
    });
    glossify();
  }

  // Resolve a link to `slug` relative to whichever page we're currently on.
  function href(slug) {
    if (atRoot) return slug === 'index' ? 'index.html' : 'pages/' + slug + '.html';
    return slug === 'index' ? '../index.html' : slug + '.html';
  }

  function navHTML(slug) {
    let groups = { 'source':[], 'terms':[], 'structures':[], 'metal':[], 'payoff':[], 'the ladder':[] };
    PAGES.forEach(p => groups[p.level].push(p));
    const order = ['the ladder','source','terms','structures','metal','payoff'];
    const labels = { 'the ladder':'Start', 'source':'1 · Source', 'terms':'2 · Terms',
                     'structures':'3 · Data structures', 'metal':'4 · The metal', 'payoff':'Applied' };
    let h = `<div class="brand"><b>BEAM</b> ▸ memory model</div>
             <p class="tagline">Extending the mental model from Elixir down through bytecode and memory.</p>`;
    for (const g of order) {
      if (!groups[g].length) continue;
      h += `<div class="nav-section">${labels[g]}</div><div class="nav">`;
      for (const p of groups[g]) {
        const active = p.slug === slug ? ' class="active"' : '';
        const r = p.slug === 'index' ? '' : `<span class="rung">${p.rung}</span>`;
        h += `<a href="${href(p.slug)}"${active}>${r}<span>${p.title}</span></a>`;
      }
      h += `</div>`;
    }
    return h;
  }

  function pagerHTML(cur) {
    const prev = PAGES[cur - 1], next = PAGES[cur + 1];
    let h = '';
    h += prev ? `<a class="prev" href="${href(prev.slug)}"><span class="dir">← previous</span>
                 <span class="ttl">${prev.title}</span></a>` : `<span></span>`;
    h += next ? `<a class="next" href="${href(next.slug)}"><span class="dir">next →</span>
                 <span class="ttl">${next.title}</span></a>` : `<span></span>`;
    return h;
  }

  /* ---- diagram helper: draw an SVG arrow between two DOM rects ---- */
  function drawArrow(svg, fromEl, toEl, opts = {}) {
    const box = svg.getBoundingClientRect();
    const a = fromEl.getBoundingClientRect();
    const b = toEl.getBoundingClientRect();
    const x1 = a.right - box.left, y1 = a.top + a.height/2 - box.top;
    const x2 = b.left - box.left,  y2 = b.top + b.height/2 - box.top;
    const dx = Math.max(40, (x2 - x1) * 0.5);
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', `M ${x1} ${y1} C ${x1+dx} ${y1}, ${x2-dx} ${y2}, ${x2} ${y2}`);
    path.setAttribute('fill', 'none');
    path.setAttribute('stroke', opts.color || 'var(--boxed)');
    path.setAttribute('stroke-width', opts.width || 2);
    path.setAttribute('marker-end', 'url(#arrowhead)');
    if (opts.dash) path.setAttribute('stroke-dasharray', '5 4');
    if (opts.cls) path.setAttribute('class', opts.cls);
    svg.appendChild(path);
    return path;
  }
  function arrowDefs(color) {
    return `<defs><marker id="arrowhead" markerWidth="9" markerHeight="9" refX="7" refY="3"
            orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="${color || 'var(--boxed)'}"/></marker></defs>`;
  }

  /* ---- glossary: hover/focus tooltips on known inline code ---- */
  const GLOSSARY = {
    'put_elem': { sig: 'Kernel.put_elem(tuple, index, value)', mod: 'Kernel · auto-imported · → :erlang.setelement/3',
      desc: 'Returns a <b>new</b> tuple with the zero-based <code>index</code> set to <code>value</code>. The original is untouched — an immutable update.' },
    'elem': { sig: 'Kernel.elem(tuple, index)', mod: 'Kernel · auto-imported',
      desc: 'Reads the element at the zero-based <code>index</code>. O(1): a direct offset into the tuple block.' },
    'tuple_size': { sig: 'Kernel.tuple_size(tuple)', mod: 'Kernel · auto-imported',
      desc: 'Number of elements, read straight from the tuple’s header word. O(1).' },
    'length': { sig: 'Kernel.length(list)', mod: 'Kernel · auto-imported',
      desc: 'Counts list elements by walking the chain to <code>[]</code>. O(n).' },
    'byte_size': { sig: 'Kernel.byte_size(bitstring)', mod: 'Kernel · auto-imported',
      desc: 'Size in bytes of a binary/bitstring, read from its header. O(1).' },
    'Enum.sort': { sig: 'Enum.sort(enumerable)', mod: 'Enum · Elixir stdlib',
      desc: 'Sorts by Erlang term order (≤) by default. For strings that is raw byte order — see rung 10.' },
    'String.to_atom': { sig: 'String.to_atom(string)', mod: 'String · Elixir stdlib',
      desc: 'Interns the string as an atom, creating it if new. Unbounded use can exhaust the global atom table — see rung 5.' },
    'String.to_existing_atom': { sig: 'String.to_existing_atom(string)', mod: 'String · Elixir stdlib',
      desc: 'Like <code>to_atom</code>, but raises if the atom does not already exist — the safe form for untrusted input.' },
    ':erts_debug.size': { sig: 'erts_debug:size(term)', mod: 'Erlang · :erts_debug',
      desc: 'Word size of a term, counting shared sub-terms <i>once</i>. Compare with flat_size to reveal sharing.' },
    ':erts_debug.flat_size': { sig: 'erts_debug:flat_size(term)', mod: 'Erlang · :erts_debug',
      desc: 'Word size of a term as if fully copied with <b>no</b> sharing — what sending it as a message would cost.' },
    ':binary.copy': { sig: 'binary:copy(binary)', mod: 'Erlang · :binary',
      desc: 'Returns a standalone copy of a binary — used to stop a small sub-binary from pinning a large shared one.' },
    'binary_to_term': { sig: 'erlang:binary_to_term(binary)', mod: 'Erlang · :erlang',
      desc: 'Decodes the external term format back into a term. Inverse of <code>term_to_binary</code>.' },
    '%{}': { sig: '%{} — map literal', mod: 'Elixir syntax',
      desc: 'Constructs a map. Empty here; with pairs (<code>%{a: 1}</code>) it builds a populated map.' },
    '|>': { sig: '|> — the pipe operator', mod: 'Elixir syntax',
      desc: '<code>x |> f(y)</code> is <code>f(x, y)</code>: threads the left value in as the first argument of the call on the right.' },
    '[]': { sig: '[] — the empty list (nil)', mod: 'Elixir / BEAM',
      desc: 'An immediate value, not a heap object. Also the tail that terminates every proper list.' },
  };

  // Map an inline-code string to a glossary key, if any.
  function glossKey(txt) {
    if (GLOSSARY[txt]) return txt;                       // exact construct/token match
    // function forms: Mod.fun(  Mod.fun/2  :mod.fun(  fun(  fun/1
    const re = /(:?[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*[?!]?)\s*(?:\(|\/\d)/g;
    let m;
    while ((m = re.exec(txt)) !== null) {
      if (GLOSSARY[m[1]]) return m[1];
    }
    return null;
  }

  function glossify() {
    const codes = Array.from(document.querySelectorAll('.page code'));
    codes.forEach(el => {
      // skip code blocks, viz chrome (overflow:hidden clips popups), and already-done
      if (el.closest('pre') || el.closest('.viz') || el.closest('.gloss-pop') || el.classList.contains('gloss')) return;
      const key = glossKey(el.textContent.trim());
      if (!key) return;
      const g = GLOSSARY[key];
      const pop = document.createElement('span');
      pop.className = 'gloss-pop';
      pop.setAttribute('role', 'tooltip');
      pop.innerHTML = `<span class="gp-sig">${g.sig}</span>` +
                      `<span class="gp-mod">${g.mod}</span>` +
                      `<span class="gp-desc">${g.desc}</span>`;
      el.classList.add('gloss');
      el.setAttribute('tabindex', '0');
      el.appendChild(pop);
    });
  }

  return { mount, PAGES, drawArrow, arrowDefs, glossify };
})();
