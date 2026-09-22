"""Lesson 11 — Recursion, backtracking, linked lists, trees.

Run: python3 -m pytest exercises/11_patterns_trees.py
"""

from collections import deque


class ListNode:
    """A singly linked list node. `next` is a ListNode or None.

    Invariant for an *acyclic* list: following `next` from the head reaches
    None after exactly n steps, where n is the number of nodes.
    """

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


def from_list(values):
    """Build a linked list from `values`; return the head (None if empty).

    Postcondition: to_list(from_list(values)) == list(values). O(n) time.
    """
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head):
    """Flatten an acyclic linked list to a Python list.

    Precondition: the list reachable from `head` contains no cycle.
    O(n) time, O(n) space.
    """
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


class TreeNode:
    """A binary tree node. `left` and `right` are TreeNode or None."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


def build_tree(values):
    """Build a binary tree from a level-order list, None marking an absent child.

    build_tree([3, 9, 20, None, None, 15, 7]) is

            3
           / \\
          9   20
             /  \\
            15    7

    Precondition: values[0] is not None unless values is empty.
    O(n) time and space.
    """
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values):
            v = values[i]
            i += 1
            if v is not None:
                node.left = TreeNode(v)
                queue.append(node.left)
        if i < len(values):
            v = values[i]
            i += 1
            if v is not None:
                node.right = TreeNode(v)
                queue.append(node.right)
    return root


def reverse_list(head):
    """Reverse a singly linked list in place; return the new head.

    Precondition: the list is acyclic and has n >= 0 nodes.
    Postcondition: the returned head begins the same nodes in reverse order;
    the original head node's `next` is None.
    Invariant: `prev` heads the reversed prefix, `node` heads the untouched
    suffix, and reversed(prefix) + suffix is a permutation of the input.
    O(n) time, O(1) extra space.
    """
    raise NotImplementedError


def has_cycle(head):
    """Return True iff the list reachable from head contains a cycle.

    Precondition: head is a ListNode or None.
    Postcondition: True iff some node is reachable from itself in >= 1 steps.
    Floyd's tortoise and hare: slow advances 1, fast advances 2; they meet
    inside the cycle iff one exists.
    O(n) time, O(1) extra space.
    """
    raise NotImplementedError


def merge_two_lists(a, b):
    """Merge two sorted linked lists into one sorted list; return the head.

    Precondition: a and b are acyclic and non-decreasing.
    Postcondition: the result is non-decreasing and contains exactly the
    nodes of a and b, spliced (not copied), so both inputs are consumed.
    Ties take from `a`, which makes the merge stable.
    O(m + n) time, O(1) extra space.
    """
    raise NotImplementedError


def max_depth(root):
    """Return the number of nodes on the longest root-to-leaf path.

    Precondition: root is a TreeNode or None; the tree is finite.
    Postcondition: 0 for the empty tree, else 1 + max(depth(left), depth(right)).
    O(n) time, O(h) space for the call stack (h = height).
    """
    raise NotImplementedError


def level_order(root):
    """Return the node values level by level, left to right.

    Precondition: root is a TreeNode or None.
    Postcondition: result[d] lists the values at depth d, in left-to-right
    order; the result has max_depth(root) entries.
    O(n) time, O(w) space where w is the maximum level width.
    """
    raise NotImplementedError


def is_valid_bst(root):
    """Return True iff the tree satisfies the strict BST property.

    Precondition: node values are mutually comparable.
    Postcondition: True iff for every node x, every value in x's left subtree
    is < x.val and every value in x's right subtree is > x.val.
    Note the property is about whole subtrees, not just immediate children.
    O(n) time, O(h) space.
    """
    raise NotImplementedError


def permutations(nums):
    """Return every ordering of nums.

    Precondition: nums has distinct elements.
    Postcondition: the result has len(nums)! lists, each a permutation of
    nums, all distinct. Output order is unspecified.
    O(n! * n) time, O(n! * n) space for the output (O(n) working space).
    """
    raise NotImplementedError


def subsets(nums):
    """Return every subset of nums (the power set), each as a list.

    Precondition: nums has distinct elements.
    Postcondition: the result has 2**len(nums) lists, pairwise distinct as
    sets, each preserving the relative order of nums. Output order is
    unspecified.
    O(2**n * n) time, O(2**n * n) space for the output (O(n) working space).
    """
    raise NotImplementedError


# ---------------------------------------------------------------- tests

def test_from_list_and_to_list():
    assert to_list(from_list([])) == []
    assert to_list(from_list([1, 2, 3])) == [1, 2, 3]
    assert from_list([]) is None


def test_reverse_list():
    assert to_list(reverse_list(from_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    assert to_list(reverse_list(from_list([1]))) == [1]
    assert reverse_list(from_list([])) is None
    head = from_list([1, 2])
    new_head = reverse_list(head)
    assert head.next is None            # old head is now the tail
    assert new_head.val == 2


def test_has_cycle():
    assert has_cycle(None) is False
    assert has_cycle(from_list([1, 2, 3])) is False
    head = from_list([3, 2, 0, -4])
    tail = head
    while tail.next is not None:
        tail = tail.next
    tail.next = head.next               # cycle back to the second node
    assert has_cycle(head) is True
    self_loop = ListNode(1)
    self_loop.next = self_loop
    assert has_cycle(self_loop) is True


def test_merge_two_lists():
    got = merge_two_lists(from_list([1, 2, 4]), from_list([1, 3, 4]))
    assert to_list(got) == [1, 1, 2, 3, 4, 4]
    assert to_list(merge_two_lists(from_list([]), from_list([0]))) == [0]
    assert merge_two_lists(from_list([]), from_list([])) is None
    assert to_list(merge_two_lists(from_list([5]), from_list([1, 2]))) == [1, 2, 5]


def test_max_depth():
    assert max_depth(None) == 0
    assert max_depth(build_tree([1])) == 1
    assert max_depth(build_tree([3, 9, 20, None, None, 15, 7])) == 3
    assert max_depth(build_tree([1, 2, None, 3, None, 4])) == 4


def test_level_order():
    assert level_order(None) == []
    assert level_order(build_tree([1])) == [[1]]
    assert level_order(build_tree([3, 9, 20, None, None, 15, 7])) == [
        [3], [9, 20], [15, 7]
    ]
    assert level_order(build_tree([1, 2, 3, 4, None, None, 5])) == [
        [1], [2, 3], [4, 5]
    ]


def test_is_valid_bst():
    assert is_valid_bst(None) is True
    assert is_valid_bst(build_tree([2, 1, 3])) is True
    assert is_valid_bst(build_tree([5, 1, 4, None, None, 3, 6])) is False
    # right child of the root is larger than the root but smaller than it
    # further down: only a subtree-wide bound catches this.
    assert is_valid_bst(build_tree([5, 4, 6, None, None, 3, 7])) is False
    assert is_valid_bst(build_tree([1, 1])) is False        # strictness
    assert is_valid_bst(build_tree([8, 3, 10, 1, 6, None, 14])) is True


def test_permutations():
    got = permutations([1, 2, 3])
    assert len(got) == 6
    assert sorted(got) == [[1, 2, 3], [1, 3, 2], [2, 1, 3],
                           [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    assert permutations([]) == [[]]
    assert permutations([7]) == [[7]]
    assert len(permutations([1, 2, 3, 4])) == 24


def test_subsets():
    got = subsets([1, 2, 3])
    assert len(got) == 8
    assert sorted(got) == [[], [1], [1, 2], [1, 2, 3], [1, 3],
                           [2], [2, 3], [3]]
    assert subsets([]) == [[]]
    assert len(subsets([1, 2, 3, 4, 5])) == 32
    for s in got:
        assert s == sorted(s)           # relative order preserved
