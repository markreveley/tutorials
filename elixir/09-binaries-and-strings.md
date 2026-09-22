# 09 — Binaries, strings, charlists, and complexity as a proof obligation

## Concept

### Bitstrings and binaries

A **bitstring** is a contiguous sequence of bits. A **binary** is a
bitstring whose length is a multiple of 8 — i.e. a byte array. Literal
syntax is `<<>>` with comma-separated *segments*:

```elixir
<<1, 2, 3>>                # three 8-bit segments; a binary
<<255>>                    # one byte
<<256>>                    # ⇒ <<0>>  — segments truncate mod 256 by default
<<1::4, 2::4>>             # two 4-bit segments ⇒ <<18>>, still a binary
<<1::1>>                   # one bit — a bitstring, NOT a binary
is_binary(<<1::1>>)        # false
is_bitstring(<<1::1>>)     # true
```

Segment modifiers, written after `::`, control size and interpretation:

```elixir
<<x::8>>          <<x::16>>      <<x::32>>          integer, big-endian by default
<<x::little-32>>  <<x::signed-8>>                   endianness, signedness
<<f::float-64>>                                     IEEE float
<<b::binary>>     <<b::binary-size(3)>>             a nested binary
<<c::utf8>>                                         one UTF-8 codepoint
```

Concatenation is `<>`; `byte_size/1` and `bit_size/1` measure.

### Strings are UTF-8 binaries

A double-quoted Elixir string *is* a binary containing UTF-8 bytes. There
is no separate string type:

```elixir
iex> "héllo" <> <<0>>
<<104, 195, 169, 108, 108, 111, 0>>
iex> is_binary("héllo")
true
iex> byte_size("héllo")
6                          # not 5: é takes two bytes
iex> String.length("héllo")
5
```

This is why `IO.inspect` sometimes prints a list of numbers instead of your
string: any binary that happens to be valid printable UTF-8 prints as a
string, and one that is not prints as bytes.

### Bytes, codepoints, graphemes

Three different notions of "character", and you must know which one you
mean:

```
byte        an 8-bit unit of the UTF-8 encoding        byte_size/1, :binary
codepoint   a Unicode scalar value (U+0041, U+0301)    String.codepoints/1
grapheme    a user-perceived character = a base        String.graphemes/1,
            codepoint plus its combining marks         String.length/1
```

```elixir
iex> s = "e" <> <<0x301::utf8>>    # "e" + COMBINING ACUTE ACCENT ⇒ "é"
"é"
iex> byte_size(s)
3
iex> length(String.codepoints(s))
2
iex> String.length(s)              # graphemes
1
iex> String.at(s, 0) == s
true
```

`String.length/1` counts **graphemes**, which is almost always what a human
means by "how long is this string". Leetcode inputs are ASCII, where all
three coincide — but do not carry that assumption anywhere else.

### Charlists

A charlist is an ordinary **list of codepoints**. Erlang's original string
type; Elixir keeps it for interop.

```elixir
iex> ~c"abc"
~c"abc"
iex> ~c"abc" == [97, 98, 99]
true
iex> String.to_charlist("héllo")
[104, 233, 108, 108, 111]        # 233 = é as a single codepoint
iex> List.to_string(~c"abc")
"abc"
```

You will meet charlists when calling Erlang libraries (`:io.format/2`,
`:filename`, `:os.cmd/1`) and when a list of small integers gets inspected
as `~c"..."` by surprise. Convert at the boundary; do not use them as your
working string type — a list of codepoints costs one cons cell (2 words)
per character and gives up O(1) size.

### `String` vs `:binary` vs `Kernel`

```
String.*      Unicode-aware: graphemes, case folding, normalisation.
              String.length/1, String.slice/3, String.split/2, String.upcase/1
:binary.*     Erlang, byte-level, no Unicode: :binary.part/3,
              :binary.split/2, :binary.match/2, :binary.copy/2
Kernel        byte_size/1, bit_size/1, binary_part/3, <>
```

Use `String` when the data is text. Use `:binary` and `binary_part/3` when
the data is bytes, or when you have already proved the input is ASCII and
you want the O(1) operations.

### Binary pattern matching

Patterns in `<<>>` destructure binaries the same way tuple patterns
destructure tuples — this is the feature that makes Elixir good at parsing:

```elixir
iex> <<a, b, rest::binary>> = "hello"
iex> {a, b, rest}
{104, 101, "llo"}

iex> <<"GET ", path::binary>> = "GET /index.html"
iex> path
"/index.html"

# a length-prefixed record: 1-byte version, 2-byte length, payload, tail
iex> <<v::8, len::16, payload::binary-size(len), tail::binary>> = <<1, 0, 3, "abc", "xy">>
iex> {v, payload, tail}
{1, "abc", "xy"}
```

Only the **last** segment may have unspecified size, and a variable size
(`binary-size(len)`) must refer to a variable bound earlier in the same
pattern — left to right. Recursion over a binary is the same shape as
recursion over a list:

```elixir
def count_bytes(<<>>), do: 0
def count_bytes(<<_b, rest::binary>>), do: 1 + count_bytes(rest)
```

For text, use the `utf8` modifier so you step by codepoint, not byte:

```elixir
def count_codepoints(<<>>), do: 0
def count_codepoints(<<_c::utf8, rest::binary>>), do: 1 + count_codepoints(rest)
```

## Grounding: complexity is a proof obligation

A complexity claim is a theorem about a program. You discharge it by
structural reasoning over the representation — not by benchmarking.

### The representation

A binary value is a header plus bytes. The header records the **byte
length**. A *sub-binary* is a third thing: a small record holding a
reference to a base binary, an offset, and a length.

```
binary   = { size, bytes[0..size-1] }
subbin   = { base: binary, offset, size }     — no bytes of its own
```

### Claim 1: `byte_size/1` is O(1)

Immediate: the size is a field of the header, so `byte_size` is one memory
read. No traversal is possible to require, because the value is stored. ∎

### Claim 2: `String.length/1` is Θ(n) in the number of bytes

First recall the UTF-8 encoding:

```
U+0000  ..U+007F     0xxxxxxx                              1 byte
U+0080  ..U+07FF     110xxxxx 10xxxxxx                     2 bytes
U+0800  ..U+FFFF     1110xxxx 10xxxxxx 10xxxxxx            3 bytes
U+10000 ..U+10FFFF   11110xxx 10xxxxxx 10xxxxxx 10xxxxxx   4 bytes
```

*Upper bound.* The width of a codepoint is determined by the number of
leading 1-bits of its first byte, which is one read. So a scan that reads
the lead byte, skips `w` bytes, and repeats visits each byte O(1) times and
counts every codepoint. Grapheme clustering needs at most one codepoint of
lookahead (is the next codepoint a combining mark?), which does not change
the asymptotics. Hence O(n).

*Lower bound.* Suppose an algorithm A computes `String.length(s)` while
reading fewer than n bytes of an n-byte string. Then there is some byte
position i that A never reads. Choose s to be n ASCII bytes, so
`String.length(s) = n`; A returns n. Now form s' by replacing byte i with
`0xC3` and byte i+1 with `0xA9` (the two bytes of "é"), which is a valid
UTF-8 string of the same byte length but with n−1 codepoints. A cannot
distinguish s from s' if it never reads position i, so it returns n on s'
too — wrong. Hence every correct algorithm reads all n bytes: Ω(n). ∎

Combining: `String.length/1` is Θ(n). The deep reason is that UTF-8 is a
**variable-width** encoding, so the map from codepoint index to byte offset
is a prefix sum of content-dependent widths — and a prefix sum is not
computable without reading the content.

Corollary: `String.at(s, i)` and `String.slice(s, i, k)` are O(i) and
O(i+k), not O(1). A loop `for i <- 0..n-1, do: String.at(s, i)` is O(n²).
Convert once to a list of graphemes and walk that instead.

### Claim 3: slicing on byte boundaries is O(1)

`binary_part(bin, offset, len)` and `:binary.part/3` return a **sub-binary**:
a `{base, offset, size}` record. Constructing it is constant work and
copies no bytes; the base binary is kept alive by the reference.

```elixir
iex> big = :binary.copy("x", 1_000_000)
iex> small = binary_part(big, 0, 10)      # O(1); shares `big`
```

The cost is retention: `small` keeps all 1 MB alive. `:binary.copy(small)`
forces a real copy when you want to drop the base. Note the contrast with
`String.slice/3`, which must first find grapheme boundaries — O(i+k) by
Claim 2 — and only then can slice cheaply.

### Claim 4: `<>`-building in a loop is O(n²); iodata makes it O(n)

Take `Enum.reduce(pieces, "", fn p, acc -> acc <> p end)` over n pieces
each of k bytes.

`a <> b` allocates a fresh binary of size `|a| + |b|` and copies both
operands into it. So step i (1-based) copies `|acc| + k = (i−1)k + k = ik`
bytes. Total:

```
Σ(i = 1..n) i·k  =  k · n(n+1)/2  =  Θ(k·n²)
```

Quadratic in the number of pieces. Now the fix. **Iodata** is a nested list
whose leaves are binaries or bytes; every function that writes bytes
(`IO.write/2`, `File.write/2`, `IO.iodata_to_binary/1`) accepts it directly:

```elixir
iex> IO.iodata_to_binary(["a", ["b", "c"], "d"])
"abcd"
iex> IO.iodata_length(["ab", ["c"]])
3
```

Build with `[acc, piece]` or `[piece | acc]` — a single cons cell, O(1),
copying nothing:

```elixir
iex> pieces = ["a", "b", "c"]
iex> pieces |> Enum.reduce([], fn p, acc -> [acc, p] end) |> IO.iodata_to_binary()
"abc"
```

Cost: n conses at O(1) = Θ(n), then one flatten that copies each byte
exactly once = Θ(k·n). Total Θ(k·n) — linear, and with a strictly smaller
constant than the quadratic version's *first* iteration alone once n is
large. ∎

Two honest footnotes. (1) The BEAM special-cases the pattern
`acc = <<acc::binary, new::binary>>` where `acc` is the sole reference to
an appendable binary: it over-allocates and appends in amortised O(1), so
that exact shape can be linear. Anything that breaks sole ownership —
keeping an intermediate, sharing it, or using `<>` with the accumulator
second — falls back to copying, and you get the quadratic. (2) If the
result is going straight to IO, skip `IO.iodata_to_binary` entirely and
hand the iodata over; the flatten never happens.

The moral for leetcode: **prefer a list of pieces reversed once at the
end** (lesson 5's accumulator pattern) over repeated `<>`. It is the same
transformation, and it has the same proof.

## Worked examples

```elixir
iex> String.split("a,b,,c", ",")
["a", "b", "", "c"]
iex> String.split("  a  b ")                 # whitespace, trims
["a", "b"]
iex> String.graphemes("héllo") |> Enum.reverse() |> Enum.join()
"olléh"
iex> String.reverse("héllo")                 # same thing, grapheme-aware
"olléh"

iex> for <<c <- "abc">>, do: c               # binary comprehension, byte-wise
[97, 98, 99]
iex> for <<c::utf8 <- "héllo">>, do: c       # codepoint-wise
[104, 233, 108, 108, 111]

iex> ?a                                      # codepoint literal
97
iex> "abc" |> to_charlist() |> Enum.map(&(&1 - ?a))
[0, 1, 2]

iex> :binary.match("hello world", "o")       # {offset, length}
{4, 1}
iex> :binary.part("hello", 1, 3)             # O(1) sub-binary
"ell"
```

The `&(&1 - ?a)` trick — map a lowercase letter to 0..25 — is the standard
way to build a 26-slot frequency array or trie index in a leetcode problem.

## Exercises

`exercises/09_strings.exs`. Hints:

- `counts/1`: `byte_size/1`, `String.codepoints/1` + `length/1`,
  `String.length/1`. Three different answers for the same string.
- `codepoint_byte_sizes/1`: `String.codepoints/1` then `byte_size/1` on
  each. This is the UTF-8 table above, observed.
- `parse_packet/1`: one binary pattern with `binary-size(len)`, plus a
  catch-all clause returning `:error`.
- `split_at_bytes/2`: `binary_part/3` twice. Guard `n` against
  `byte_size/1` so you never build an out-of-range part.
- `join/2`: `Enum.intersperse/2` gives you iodata for free; finish with
  `IO.iodata_to_binary/1`. Do not use `<>` in a fold.
- `reverse_graphemes/1`: graphemes, reverse, join — and check it against
  a combining-mark string.
- `letter_counts/1`: fold over `String.to_charlist/1` into a map keyed by
  `c - ?a`.

## Leetcode at this stage

String problems are now unblocked, as long as you keep the complexity
proofs in mind (no `String.at/2` in a loop):

- 344 Reverse String — graphemes or a byte-wise accumulator.
- 242 Valid Anagram — frequency map over `to_charlist/1`.
- 383 Ransom Note — same map, subtract.
- 387 First Unique Character in a String — one pass to count, one to find.
- 14 Longest Common Prefix — recurse on `<<c::utf8, rest::binary>>`.
- 28 Find the Index of the First Occurrence — `:binary.match/2` gives the
  answer, but write the two-pointer version yourself (lesson 11).
- 415 Add Strings — charlists, `?0` offsets, iodata for the result.

Questions before moving on:

1. Why is `byte_size("héllo") == 6` but `String.length("héllo") == 5`?
2. You hold a 10-byte slice of a 10 MB binary and the 10 MB is otherwise
   garbage. How much memory is retained, and what call fixes it?
3. Rewrite `Enum.reduce(xs, "", &(&2 <> &1))` as iodata. What changed
   asymptotically, and what did not change about the final bytes?
