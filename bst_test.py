import itertools

from binary_tree_set import BinaryTreeSet, concat, cons, from_list, intersection, length, \
    member, remove, to_list, empty, map_set, filter_set, reduce_set


def test_api():
    empty_tree = empty()
    assert str(cons((1, None), empty_tree)) == "{1: None}"
    l1 = cons((1, None), cons((2, 1), empty_tree))
    l2 = cons((2, 1), cons((1, None), empty_tree))
    assert str(empty_tree) == "{}"
    assert str(l1) == "{1: None, 2: 1}" or str(l1) == "{2: 1, 1: None}"
    assert empty_tree != l1
    assert empty_tree != l2
    assert l1 == l2
    assert l1 == cons((1, None), cons((2, 1), l1))
    assert length(empty_tree) == 0
    assert length(l1) == 2
    assert length(l2) == 2

    assert str(remove(l1, (1, None)) == "{2: 1}"
    assert str(remove(l1, (2, 1)) == "{1: None}"

    assert not member((1, None), empty_tree)
    assert member((1, None), l1)
    assert member((2, 1), l1)
    assert not member((3,None), l1)

    assert intersection(l1, l2) == l1
    assert intersection(l1, l2) == l2
    assert intersection(l1, empty_tree) == empty_tree
    assert intersection(l1, cons((1, None), empty_tree)) == cons((1, None), empty_tree)

    assert to_list(l1) == [(1, None), (2, 1)] or to_list(l1) == [(2, 1), (1, None)]
    assert l1 == from_list([(1, None), (2, 1)])
    assert l1 == from_list([(2, 1), (1, None), (2, 1)])
    assert concat(l1, l2) == from_list([(1, None), (2, 1), (2, 1), (1, None)])

    buf = []
    for e in l1:
        buf.append(e)
    assert buf in map(list, itertools.permutations([(2, 1), (1, None)]))

    lst = to_list(l1) + to_list(l2)
    for e in l1:
        lst.remove(e)

    for e in l2:
        lst.remove(e)
    assert lst == []

    f1 = filter_set(l1, lambda k, v: v is not None)
    assert to_list(f1) == [(2, 1)]
    assert length(f1) == 1
    assert not member((1, None), f1)
    assert member((2, 1), f1)

    f2 = filter_set(l1, lambda k, v: False)
    assert f2 == empty_tree
    assert length(f2) == 0

    m1 = map_set(l1, lambda k, v: (k, str(v) + "_val"))
    vals = [v for v, _ in to_list(m1)]
    assert "None_val" in vals and "1_key" in keys
    assert length(m1) == 2

    r = reduce_set(l1, lambda kv, acc: acc + [kv[1]], [])
    assert sorted(r) == sorted([None, 1])

    e1 = empty()
    assert str(e1) == "{}"
    assert length(e1) == 0
    assert not member((0, 0), e1)
    assert to_list(e1) == []
