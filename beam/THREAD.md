# Primary reference thread

This is the source conversation that seeded this wiki. It is preserved verbatim
(tool-progress artifacts like "N steps" removed) as the primary reference for
the concepts explored here. The wiki does **not** follow this thread
sequentially — it reorganizes the material into a single mental-model ladder:
**Elixir → bytecode → memory representation → how the runtime reads it.**

External primary reference: **The BEAM Book** by Erik Stenman —
<https://blog.stenmans.org/theBeamBook> (source: <https://github.com/happi/theBeamBook>).

---

## Q1 — Where to start in the Elixir docs

> where is a good place to start in the elixir docs here

**A (summary):** Start in the **Pages tab → "Getting started"** (the official guided
tutorial): Introduction (install + IEx) → Basic types → Lists and tuples →
Pattern matching → `case`/`cond`/`if` → Anonymous functions → Modules and
functions → Keyword lists and maps → Structs → Recursion → Enumerables and
Streams → Protocols → Processes → IO. Then the **"Mix & OTP"** section
(Introduction to Mix → Agents → Supervisors → GenServer …).

Treat the **Modules tab** as reference, not a place to start reading. Bookmark
`Kernel`, `Enum`, `Stream`, `String`, `Map`, `List`, `Keyword`, and later
`GenServer`, `Supervisor`, `Task`, `Application`.

---

## Q2 — Structural vs semantic comparison (the string example)

> In the section on the difference between structural and semantic comparison,
> expand on this example: `"alien" < "office"` but `"álien" > "office"`.

**A (key points):**

- `<` does a **structural comparison**: it walks the two strings byte by byte
  and compares numeric values. The first differing byte decides. Fast,
  predictable, blind to human meaning.
- Elixir strings are **UTF-8 binaries**. ASCII letters are one byte (0–127):
  `a` = 97, `o` = 111, so `"alien" < "office"` (97 < 111). Matches intuition.
- `á` is **not** ASCII; in UTF-8 it is two bytes `0xC3 0xA1` (195, 161). The
  first byte of `"álien"` is **195**, vs `o` = 111. Since 195 > 111, the whole
  string `"álien"` sorts **after** `"office"`. The accent pushed the entire
  string past every single-byte ASCII letter.
- **Structural** = "how is this laid out as bytes?" (what `<`/`>` do; the basis
  for collections/sorting). **Semantic** = "what do these mean, and how should
  they be ordered for this purpose?" — for text that is collation order, where
  `álien` files next to `alien`, before `office`.
- Date/Time make the analogous point: structurally you can compare a `Time`
  with a `Date` (just data), but semantically it is nonsense — so those modules
  provide `compare/2` returning `:lt`/`:eq`/`:gt` and refuse meaningless
  comparisons.
- **Takeaway:** for user-facing text, don't rely on raw `<`/`>` or plain
  `Enum.sort/1`; use a collation-aware (Unicode Collation Algorithm) approach so
  `"álien"` lands before `"office"`.

---

## Q3 — Tuples: contiguous storage, expensive update, shared elements

> Expand on: tuples are stored contiguously; size/index access is fast;
> updating/adding is expensive (new tuple); but "the elements themselves are not
> copied" — entries are shared between old and new tuple except the replaced one.

**A (key points):**

- **"Stored contiguously"**: a tuple is one memory block — a header plus slots
  at fixed, evenly-spaced offsets. So `tuple_size/1` is reading the header
  number (**O(1)**), and `elem(t, i)` is arithmetic "start + i slots" (**O(1)**),
  regardless of size or position. Opposite of a linked list, where length/Nth
  require following the chain from the front (**O(n)**).
- **Why update is expensive**: data is immutable, so `put_elem/3` can't
  overwrite a slot. It allocates a **new tuple block** of the same size and fills
  it — cost grows with tuple size (**O(n)**). Tuples are poor for data you grow
  or rewrite often.
- **Structural sharing (the subtlety)**: "the elements themselves are not
  copied" means the **values** the slots point to are reused, not duplicated. A
  slot holds a **reference**. For `put_elem({:a,:b,:c,:d}, 2, :e)`, the new tuple
  is a fresh 4-slot container; slots 0,1,3 point to the same `:a`,`:b`,`:d`; only
  slot 2 points to new `:e`. Both tuples coexist; everything except the replaced
  entry is shared. For big maps/strings you'd be copying pointers, not the data.
- **Why only possible with immutability**: in a mutable language, sharing a
  pointer is dangerous (mutating through one alias is seen by the other). Since
  BEAM values are never mutated in place, sharing is always safe.
- **Rule of thumb**: tuples for fixed-size groupings you read often but rarely
  rewrite (`{:ok, result}`, `{:error, reason}`); lists when the collection grows,
  shrinks, or is processed element-by-element (prepend `[0 | list]` is O(1);
  append/index is O(n)).

---

## Q4 — Do lists/tuples only hold pointers? Can you view/manipulate memory?

> To reiterate: both lists (linked) and tuples can ONLY contain pointers to data
> held in memory — they cannot "hold" unique copies of data itself? Is there any
> way in Elixir to view or manipulate memory locations, or is the use of pointers
> invisible to the user?

**A — correction to the "pointers only" model:**

- The BEAM splits values into two categories:
  - **Immediates** fit entirely in one machine word — small integers (the bits
    *are* the number), atoms (the slot holds an immediate index into the global
    atom table). No separate object is pointed at.
  - **Boxed values** are too big for a word — tuples, bignums, floats, binaries,
    maps — so the slot holds a **tagged pointer** to an object on the process heap.
- Precise statement: a tuple slot / list cell holds **one tagged word** —
  sometimes the value (immediate), sometimes a pointer (boxed). "Elements not
  copied" matters most for the boxed case.
- **Tagging**: a few bits of every word are a tag saying what the rest means
  (fixnum, cons pointer, tuple pointer, atom…). Invisible to you.
- **Within a process**, sharing is free. **Across processes**, sending a message
  generally **copies** data into the receiver's heap (each process has its own
  isolated, independently GC'd heap). Exception: **large binaries (>64 bytes)**
  live off-heap in a shared area and are passed by reference.

**A — viewing/manipulating memory:**

- **No** pointers, addresses, pointer arithmetic, or dereferencing in the C/Rust
  sense. This is deliberate (safety): no dangling pointers, buffer overflows,
  use-after-free, because the language never hands you an address.
- You can **inspect** at a higher level: `:erts_debug.size/1` (size in words,
  counting sharing) vs `:erts_debug.flat_size/1` (as if fully copied) — comparing
  them demonstrates structural sharing empirically. `Process.info(pid, :memory)`,
  `:erlang.memory/0`, `:observer.start()`.
- Raw memory work means leaving the managed world via **NIFs** (C/Rust) or
  **Ports** — and leaving the safety guarantees behind.

---

## Q5 — Machine words, immediate vs boxed, atoms, dereferencing, runtime, heaps, ERTS

> How big is a machine word? How does the BEAM determine if a value is an
> immediate, or that size but persisted elsewhere? For the atom, the slot is
> memory holding an index into a global atom table — how is the slot known to
> belong to the atom? Is there a connected descriptor saying "treat this as an
> atom"? Is this tagging? By "dereference a slot" you mean treat it as a pointer
> and get what it points at? Is this the compiler's or the runtime's domain?
> Technically what is a "runtime" — an application? a binary? What is a process
> heap? What does :erts stand for?

**A (key points):**

- **Machine word**: the CPU/runtime's natural unit. 64-bit system → 8 bytes;
  32-bit → 4 bytes. It is the BEAM's fundamental cell size. A 64-bit small int is
  ~60 value bits + 4 tag bits (so ~±2^59); beyond that it's promoted to a boxed
  **bignum**.
- **Tagging** (the central trick): pointers to heap objects are **aligned**, so
  the lowest bits of any real pointer are always zero — "free real estate"
  repurposed as a **tag**. A **primary tag** distinguishes cons pointer / boxed
  pointer / immediate / header. Sub-tags split immediates (small int / atom / nil
  / …). The BEAM reads the tag bits of a word to know whether to dereference or
  read it directly. The answer is encoded in the value itself — no side lookup.
- **Atom case**: the slot **is** the atom — its tag bits self-describe it
  ("atom"), and the payload bits **are** an index into the global, VM-wide,
  interned atom table (which stores the name, length, hash). No external
  descriptor points at the slot; values are self-identifying.
- **Compiler vs runtime**: the compiler knows the representations and bakes
  compile-time constants into the right tagged form and emits "build a tuple"
  instructions; the **runtime** does the live interpretation of tags, heap
  allocation, atom interning, GC.
- **What a "runtime" is**: the BEAM runtime is a **native executable (C
  program)** — launching Elixir launches this VM, which loads and runs your
  compiled `.beam` bytecode and provides the managed world (memory model, GC,
  lightweight-process scheduler, message passing, atom table, I/O…).
- **Process heap**: a BEAM process is a lightweight VM-managed unit of
  concurrency (millions possible), each with its **own private heap** where its
  boxed terms live; stack and heap grow toward each other. Private heaps →
  **per-process GC** (pause only one process) and → **message copying** across
  processes (except large binaries).
- **ERTS** = **Erlang Run-Time System** — the whole runtime (BEAM emulator +
  allocators, schedulers, BIFs, drivers). `:erts_debug` is a low-level interface
  into it.

---

## Q6 — Why low bits are zero; masking; tags vs header; source of these claims; atoms global; compiler vs runtime; "emulator" vs BEAM; VMs vs Docker

> Is it the BEAM-as-runtime-VM reading memory and executing per how it identifies
> locations? Why are the lowest bits of a genuine pointer necessarily zero? What
> is "mask off the tag bits"? Don't the tag bits tell the type of the
> pointed-to data? You're going past the docs ("elements not copied") — where is
> this from? Atom table is VM-wide — do atoms cut across processes / act as
> globals? So atoms have a tag identifying the payload as an atom-table index?
> Does the compiler or runtime initialize these blocks? Why "BEAM emulator" not
> "the BEAM"? Is every VM (Docker etc.) ultimately a binary like the BEAM? Is "a
> CPU/OS-independent environment for bytecode" a functional definition of a VM?

**A (key points):**

- **Yes** — the BEAM is a running native program that, at execution time,
  inspects each word, reads its tag bits, and decides what to do.
- **Why low bits are zero — alignment**: boxed objects are placed at addresses
  that are multiples of the word size (8 on 64-bit). A multiple of 8 ends in
  `000` in binary (8 = 2³), so the low 3 bits of a real pointer carry no
  information and are safe to overwrite with a tag.
  *(Wiki correction: ERTS actually reserves only the low **2** bits as the
  primary tag, exploiting "at least two bits" of alignment so the scheme works on
  both 32- and 64-bit — BEAM Book Ch.4.2.)*
- **"Mask off the tag bits"** = bitwise-AND with a mask like `…11111000` to clear
  the tag bits and recover the clean aligned address, then follow it.
- **Tags vs header — two-stage typing**: the pointer's tag only says "boxed
  pointer, go dereference." The **precise** type (tuple? bignum? float? map?) is
  in the **header word** — the first word of the boxed object — which encodes
  type + arity. Immediates are fully described by their tag alone.
- **Source of the low-level claims**: training knowledge of the BEAM/ERTS
  implementation, primarily **The BEAM Book** (Erik Stenman) and Erlang/OTP
  source. Caveat: implementation detail, not language guarantee; exact bit
  layouts can change across OTP versions and 32/64-bit. The observable behavior
  the docs promise is stable.
- **Atoms global but not variables**: the table is VM-wide and atoms are
  **interned** — every `:ok` everywhere is the same index, which is why atom
  comparison is cheap. But atoms carry no mutable state; they're globally-shared
  **constants/symbols**, not variables. **Footgun**: atoms are never
  garbage-collected and the table has a fixed max (~1,048,576) — never create
  atoms from untrusted input (`String.to_atom/1`); use `String.to_existing_atom/1`.
- **Atom word**: an atom is an **immediate** — no "following memory"; the whole
  thing fits in one word: tag bits say "atom", the remaining bits of the same
  word **are** the index.
- **Compiler vs runtime (split, leaning runtime)**: compiler bakes
  known-at-compile-time literals into properly-tagged form (module literal area)
  and emits build-instructions; the runtime does all **live** allocation and
  tagging on the process heap.
- **"BEAM emulator" vs "the BEAM"**: BEAM = the abstract machine (Bogdan/Björn's
  Erlang Abstract Machine) / bytecode format; the **emulator** = the concrete C
  program that emulates it on real hardware. Casual speech uses "the BEAM" for
  the running program too.
- **VMs and Docker**: two senses of "VM": a **process/language VM** (BEAM, JVM,
  CPython, CLR) — a native binary emulating an *invented* instruction set to run
  bytecode; and a **system VM** (VMware, VirtualBox, QEMU, hypervisors) —
  virtualizes *real hardware* so a whole guest OS runs inside. **Docker is
  neither** — containers are regular host processes isolated by kernel features
  (namespaces, cgroups); no emulated machine, no guest OS. (On macOS/Windows
  Docker runs a hidden Linux system-VM to provide a kernel.)
- "A CPU/OS-independent environment in which bytecode runs" functionally defines
  a **process/language VM** specifically — the category the BEAM belongs to; not
  a system VM/hypervisor.

---

## Q7 — Bytecode ↔ Elixir mapping; alignment "value vs address"; header type lookup; the mental model of "shared not copied"; training data; "tagged pointer"

> Is the bytecode a 1:1 map to the Elixir, or does the compiler change it
> semantically? Does "build a tuple from these values" mean "build a tuple that
> references via pointer the values located elsewhere"? Re alignment: isn't 8 =
> 2³ just the start place for an object? Is an object a word? If so why can't the
> word use all bits for the value? Is the value at these points actually an
> address, not a value? Re header word: does the runtime have its own
> word-value→type lookup table? How does the VM get access to memory at all? Re
> "shared, not copied" — I have trouble building a mental model of *where* the
> elements exist if not copied and just "shared"; they feel "out there"
> somewhere. Re "reconstructing from memory" — you mean training data? Re "hands
> back a tagged pointer" — meaning it creates a tagged pointer in memory?

**A (key points):**

- **Not 1:1**: source → AST → (macro expansion, `if`→`case`, pipes rewritten) →
  Core Erlang → SSA forms → optimizations (dead-code elimination, inlining,
  register reuse) → BEAM bytecode. One Elixir line may become several
  instructions or several lines collapse. Behavior is preserved; structure is
  not. Bytecode is also lower-level vocabulary — a **register machine**
  (registers, allocation, loads) none of which appears in your source.
- **"Build a tuple from these values"** = allocate a tuple object (header
  type=tuple, arity=N) and fill N slots with the current tagged words. Boxed
  values → slots hold **pointers** to values elsewhere; immediates → slot holds
  the value directly. Matches "references, not embedded copies."
- **Alignment "value vs address"** — the key resolution: two different one-word
  uses. (1) A **slot** inside a tuple/variable/list cell. (2) An **address** in
  RAM where a boxed object lives. Alignment is about **addresses**: the allocator
  places each boxed block at an address that's a multiple of 8, so blocks start
  only at 0, 8, 16, 24… → low 3 bits always `000` → reused as a tag. So `8 = 2³`
  is about **where blocks start**, not word size. A pointer-word can't use all
  bits for a value because it isn't holding a value — it's holding an **address**
  (with spare low bits). An **immediate** word *does* use almost all bits for the
  value (minus a few tag bits — why a small int isn't full 64-bit).
- **Header type ID — no lookup table**: the header word **encodes the type
  directly** in its bits (a few type-tag bits + size/arity); the C emulator has a
  hardcoded `switch` on those bits. (Contrast the **atom** table, which exists
  only because an atom needs to map a small index to a variable-length name.)
- **How the VM gets memory**: the BEAM is a native process, so the OS gives it a
  virtual address space (via `mmap`/`malloc`); the BEAM grabs big regions and
  **sub-manages** them with its own allocators, carving out process heaps and
  boxed objects. Two levels: OS → BEAM process; BEAM → its world of Elixir
  processes. "Reading memory" is ordinary C pointer dereferencing inside its own
  address space.
- **The mental model that resolves "shared, not copied"** (the crux): every
  boxed value lives at **exactly one place** — a block on some process's heap. A
  tuple is **not** a box containing its elements; it is a small block whose slots
  hold **pointers (arrows)** to where the elements already live. Concrete: map
  `M` at address 1000; `t1 = {M, :a}` is a new block at 2000 whose slot 0 holds
  the number **1000** (an arrow to `M`) and slot 1 holds immediate `:a`. `t2 =
  put_elem(t1, 1, :b)` is another new block at 3000 whose slot 0 **also** holds
  1000 — the **same arrow to the same M**. Now `M` has two arrows pointing at it,
  one copy at one address. **That** is "shared, not copied." Safe **because of
  immutability** — nothing can mutate `M` in place, so it doesn't matter that two
  tuples point at it. The unease is correct *for mutable languages*; Elixir
  defuses it. Model: stop imagining nested containers; imagine a **graph of small
  blocks connected by arrows**, leaf values existing once with many arrows
  pointing at them. "Copied" = new leaf block allocated; "shared" = just another
  arrow to the existing block.
- **"From memory"** = yes, from **training data** (patterns/facts learned in
  training, e.g. The BEAM Book, Erlang/OTP), not a live source this session.
- **"Hands back a tagged pointer"**: the **allocation** creates the block
  (header + slots) on the heap; the tagged pointer is the **one word** that
  refers to it, and it goes wherever the result is needed — a register, a
  variable binding, or a slot of another container. The pointer is a lightweight
  one-word token copied around freely (copying an arrow is cheap; copying the
  block is what we avoid). When `t1` and `t2` "share" `M`, the one-word arrow
  `1000` was written into two slots.
- **Demonstration suggested**: `:erts_debug.size/1` (counts sharing) vs
  `:erts_debug.flat_size/1` (pretends no sharing) — build a structure with shared
  sub-terms and watch `size` < `flat_size`.

---

## Reader profile (inferred, used to calibrate the wiki)

- Comfortable in a high-level language; **not** a C/systems programmer (asked
  what masking, a word, alignment are).
- **Strong systems intuition** — independently arrived at the "value vs address"
  distinction.
- Learns by **building precise mental models** and asks "why" repeatedly; resists
  hand-wavy "it's just out there somewhere."
- The specific sticking point that unlocked everything: **where do "shared, not
  copied" elements physically live** → answered by the *graph-of-arrows* model.
  This is the emotional/conceptual center of the wiki.
