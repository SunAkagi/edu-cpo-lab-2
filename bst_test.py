import itertools

from binary_tree_set import concat, cons, from_list, \
    intersection, length, member, remove, to_list, empty, map_set, \
    filter_set, reduce_set


def test_api():
    empty_tree = empty()
    assert str(cons((1, 2), empty_tree)) == "{1: 2}"
    l1 = cons((1, 2), cons((2, 1), empty_tree))
    l2 = cons((2, 1), cons((1, 2), empty_tree))
    assert str(empty_tree) == "{}"
    assert str(l1) == "{1: 2, 2: 1}" or str(l1) == "{2: 1, 1: 2}"
    assert empty_tree != l1
    assert empty_tree != l2
    assert l1 == l2
    assert l1 == cons((1, 2), cons((2, 1), l1))
    assert length(empty_tree) == 0
    assert length(l1) == 2
    assert length(l2) == 2

    assert str(remove(l1, 1)) == "{2: 1}"
    assert str(remove(l1, 2)) == "{1: 2}"

    assert not member(1, empty_tree)
    assert member(1, l1)
    assert member(2, l1)
    assert not member(3, l1)

    assert intersection(l1, l2) == l1
    assert intersection(l1, l2) == l2
    assert intersection(l1, empty_tree) == empty_tree
    assert intersection(
        l1,
        cons((1, 2), empty_tree)
    ) == cons((1, 2), empty_tree)

    assert (
        to_list(l1) == [(1, 2), (2, 1)] or
        to_list(l1) == [(2, 1), (1, 2)]
    )
    assert l1 == from_list([(1, 2), (2, 1)])
    assert l1 == from_list([(2, 1), (1, 2), (2, 1)])
    assert concat(l1, l2) == from_list([(1, 2), (2, 1), (2, 1), (1, 2)])

    buf = []
    for e in l1:
        buf.append(e)
    assert buf in map(list, itertools.permutations([(2, 1), (1, 2)]))

    lst = to_list(l1) + to_list(l2)
    for k, _ in to_list(l1):
        if (k, _) in lst:
            lst.remove((k, _))

    for k, _ in to_list(l2):
        if (k, _) in lst:
            lst.remove((k, _))

    f1 = filter_set(l1, lambda k, v: v != 2)
    assert to_list(f1) == [(2, 1)]
    assert length(f1) == 1
    assert not member(1, f1)
    assert member(2, f1)

    f2 = filter_set(l1, lambda k, v: False)
    assert f2 == empty_tree
    assert length(f2) == 0

    m1 = map_set(l1, lambda k, v: (k, str(v) + "_val"))
    vals = [v for _, v in to_list(m1)]
    assert "2_val" in vals and "1_val" in vals
    assert length(m1) == 2

    r = reduce_set(l1, lambda kv, acc: acc + [kv[0]], [])
    assert sorted(r) == sorted([1, 2])

    e1 = empty()
    assert str(e1) == "{}"
    assert length(e1) == 0
    assert not member(0, e1)
    assert to_list(e1) == []
