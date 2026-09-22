# Elixir → BEAM: a memory-model wiki

An interactive, self-contained HTML/JS wiki that extends the mental model from
**Elixir abstractions down through bytecode, term representation, and memory
management** in the BEAM. Built as a single mental-model *ladder* rather than a
flat reference.

## Run it

No build step, no server. Open **`index.html`** in any browser
(double-click, or `open index.html` on macOS). Pages are plain HTML with shared
CSS/JS in `assets/`.

## Structure

```
elixir-beam-memory-model/
  index.html                 home — the ladder + conventions
  THREAD.md                  the source conversation (primary reference)
  README.md                  this file
  assets/
    style.css                shared design system
    app.js                   nav rendering + SVG arrow helpers
  pages/
    elixir-to-bytecode.html      1 · source → register-machine bytecode
    machine-word-and-tags.html   2 · the word; immediates vs boxed; tag bits
    tuples-vs-lists.html         3 · contiguous block vs cons cells (O(1)/O(n))
    structural-sharing.html      4 · the graph-of-arrows model (centerpiece)
    atoms-and-atom-table.html    5 · interning; the global atom table
    maps.html                    6 · flatmap (sorted arrays) vs HAMT hashmap
    runtime-reads-memory.html    7 · tag→mask→deref→header; BEAM over the OS
    gc-and-process-memory.html   8 · stack↔heap; copying generational GC
    message-passing.html         9 · isolated heaps → copying; binary exception
    structural-vs-semantic.html 10 · byte order vs collation (the payoff)
```

## Interactive pieces (one per page, where it earns its place)

- **2** — 64-bit word explorer: switch term types, see tag/value/address bits, mask a pointer.
- **3** — access-cost animation: tuple jumps O(1), list walks O(n).
- **4** — graph-of-arrows: `put_elem` builds a new block that shares the unchanged
  elements; plus a stepped M/t1/t2 address-level walkthrough.
- **5** — interning: two processes resolve the same atom to one global table slot.
- **6** — maps: flatmap (shared keys tuple + new values array) vs a HAMT lookup/update with path-copying.
- **7** — the VM decode loop: step a word through tag → mask → dereference → header.
- **8** — copying generational GC: live terms copied & promoted, garbage reclaimed by not copying.
- **9** — two isolated heaps: small term deep-copied vs big binary shared off-heap (refcount).
- **10** — live UTF-8 byte comparator: why `"álien" > "office"`.

## Sources & accuracy

Primary external reference: **The BEAM Book** by Erik Stenman —
<https://blog.stenmans.org/theBeamBook> (source:
<https://github.com/happi/theBeamBook>). Bit-level claims (tags, the 60-bit
small-int range, header layout, cons-cell size, per-process GC) are cited inline
with `Ch.x` markers and were checked against the book's chapter sources
(esp. Ch.4 *The Erlang Type System and Tags*, Ch.3 *Processes*).

These are **implementation details, not language guarantees** — exact bit
layouts can shift across OTP versions and 32/64-bit. The observable Elixir
behavior is stable; the mechanism is "how it works today."

The seeding conversation is preserved verbatim in [`THREAD.md`](THREAD.md).
