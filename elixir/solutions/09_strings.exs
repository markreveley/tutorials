ExUnit.start()

defmodule Strings do
  @moduledoc "Lesson 09: binaries, UTF-8 strings, charlists, complexity."

  @doc """
  Return {bytes, codepoints, graphemes} for a string. All three differ for
  text with multi-byte codepoints and combining marks.
  """
  def counts(s) do
    {byte_size(s), length(String.codepoints(s)), String.length(s)}
  end

  @doc """
  The byte width of each codepoint, in order. Observes the UTF-8 table:
  every entry is 1, 2, 3, or 4.
  """
  def codepoint_byte_sizes(s) do
    s |> String.codepoints() |> Enum.map(&byte_size/1)
  end

  @doc """
  Parse a length-prefixed packet: 1-byte version, 2-byte big-endian
  payload length, payload, then whatever is left.
  {:ok, {version, payload, rest}} or :error if the bytes do not fit.
  """
  def parse_packet(<<version::8, len::16, payload::binary-size(len), rest::binary>>) do
    {:ok, {version, payload, rest}}
  end

  def parse_packet(_bin), do: :error

  @doc """
  Split a binary at byte offset n into {prefix, suffix}, in O(1).
  n is clamped to 0..byte_size(bin).
  """
  def split_at_bytes(bin, n) do
    k = n |> max(0) |> min(byte_size(bin))
    {binary_part(bin, 0, k), binary_part(bin, k, byte_size(bin) - k)}
  end

  @doc """
  Join a list of binaries with a separator, building iodata and flattening
  once. O(total bytes), not O(pieces^2).
  """
  def join(parts, sep) do
    parts |> Enum.intersperse(sep) |> IO.iodata_to_binary()
  end

  @doc "Reverse a string by graphemes, so combining marks stay attached."
  def reverse_graphemes(s) do
    s |> String.graphemes() |> Enum.reverse() |> Enum.join()
  end

  @doc """
  Count the lowercase ASCII letters of a string into a map keyed by
  0..25 (that is, codepoint - ?a). Ignores everything else.
  """
  def letter_counts(s) do
    s
    |> String.to_charlist()
    |> Enum.filter(fn c -> c >= ?a and c <= ?z end)
    |> Enum.reduce(%{}, fn c, acc -> Map.update(acc, c - ?a, 1, &(&1 + 1)) end)
  end
end

defmodule StringsTest do
  use ExUnit.Case

  @combining "e" <> <<0x301::utf8>>

  test "counts" do
    assert Strings.counts("hello") == {5, 5, 5}
    assert Strings.counts("héllo") == {6, 5, 5}
    assert Strings.counts(@combining) == {3, 2, 1}
    assert Strings.counts("") == {0, 0, 0}
  end

  test "codepoint_byte_sizes" do
    assert Strings.codepoint_byte_sizes("héllo") == [1, 2, 1, 1, 1]
    assert Strings.codepoint_byte_sizes(@combining) == [1, 2]
    assert Strings.codepoint_byte_sizes("€") == [3]
    assert Strings.codepoint_byte_sizes("") == []
  end

  test "parse_packet" do
    assert Strings.parse_packet(<<1, 0, 3, "abc", "xy">>) == {:ok, {1, "abc", "xy"}}
    assert Strings.parse_packet(<<7, 0, 0, "rest">>) == {:ok, {7, "", "rest"}}
    assert Strings.parse_packet(<<1, 0, 5, "ab">>) == :error
    assert Strings.parse_packet(<<>>) == :error
  end

  test "split_at_bytes" do
    assert Strings.split_at_bytes("hello", 2) == {"he", "llo"}
    assert Strings.split_at_bytes("hello", 0) == {"", "hello"}
    assert Strings.split_at_bytes("hello", 99) == {"hello", ""}
    assert Strings.split_at_bytes("hello", -1) == {"", "hello"}
  end

  test "join" do
    assert Strings.join(["a", "b", "c"], ",") == "a,b,c"
    assert Strings.join(["a"], ",") == "a"
    assert Strings.join([], ",") == ""
    assert Strings.join(["x", "y"], "") == "xy"
  end

  test "reverse_graphemes" do
    assert Strings.reverse_graphemes("hello") == "olleh"
    assert Strings.reverse_graphemes("héllo") == "olléh"
    assert Strings.reverse_graphemes(@combining <> "x") == "x" <> @combining
    assert Strings.reverse_graphemes("") == ""
  end

  test "letter_counts" do
    assert Strings.letter_counts("banana") == %{0 => 3, 1 => 1, 13 => 2}
    assert Strings.letter_counts("aA b") == %{0 => 1, 1 => 1}
    assert Strings.letter_counts("") == %{}
  end
end
