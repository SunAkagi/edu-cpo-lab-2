import itertools

from binary_tree_set import concat, cons, from_list, \
    intersection, length, member, remove, to_list, empty, map_set, \
    filter_set, reduce_set
from hypothesis import given, strategies as st


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

    assert intersection(l1, l2) == ((1, 2),(2,1)) or intersection(l1, l2) == ((2, 1),(1,2))
    assert intersection(l1, l2) == l2  or intersection(l1, l2) == ((2, 1),(1,2))
    assert intersection(l1, empty_tree) == ()
    assert intersection(
        l1,
        cons((1, 2), empty_tree)
    ) == intersection((1, 2), empty_tree)

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


def test_empty():
    t = empty()
    assert t.is_empty()
    assert to_list(t) == []


def test_cons():
    t = empty()
    t = cons((1, 'a'), t)
    assert to_list(t) == [(1, 'a')]


def test_from_list_and_to_list():
    lst = [(2, 'b'), (1, 'a'), (3, 'c')]
    t = from_list(lst)
    out = to_list(t)
    assert sorted(out) == sorted(lst)


def test_member():
    t = from_list([(1, 'a'), (2, 'b')])
    assert member(1, t) is True
    assert member(3, t) is False


def test_remove():
    t = from_list([(1, 'a'), (2, 'b'), (3, 'c')])
    t2 = remove(t, 2)
    assert not member(2, t2)
    assert sorted(to_list(t2)) == [(1, 'a'), (3, 'c')]


def test_concat():
    a = from_list([(1, 'a')])
    b = from_list([(2, 'b')])
    c = concat(a, b)
    assert sorted(to_list(c)) == [(1, 'a'), (2, 'b')]


def test_intersection():
    a = from_list([(1, 'a'), (2, 'b')])
    b = from_list([(2, 'B'), (3, 'c')])
    i = intersection(a, b)
    assert to_list(i) == [(2, 'b')]


def test_map_set():
    t = from_list([(1, 10), (2, 20)])
    t2 = map_set(t, lambda k, v: (k * 2, v + 1))
    assert sorted(to_list(t2)) == [(2, 11), (4, 21)]


def test_filter_set():
    t = from_list([(1, 10), (2, 20), (3, 30)])
    t2 = filter_set(t, lambda k, v: k % 2 == 1)
    assert sorted(to_list(t2)) == [(1, 10), (3, 30)]


def test_reduce_set():
    t = from_list([(1, 10), (2, 20), (3, 30)])
    s = reduce_set(t, lambda kv, acc: kv[1] + acc, 0)
    assert s == 60


@given(st.lists(st.tuples(st.integers(), st.text())))
def test_roundtrip_list(xs):
    tree = from_list(xs)
    out = to_list(tree)
    d = dict(xs)
    assert dict(out) == d


@given(st.lists(st.tuples(st.integers(), st.integers())))
def test_length(xs):
    tree = from_list(xs)
    assert length(tree) == len(dict(xs))


@given(st.lists(st.tuples(st.integers(), st.integers())))
def test_concat_identity(xs):
    t = from_list(xs)
    assert concat(t, empty()) == t
    assert concat(empty(), t) == t


@given(
    st.lists(st.tuples(st.integers(), st.integers())),
    st.lists(st.tuples(st.integers(), st.integers())),
    st.lists(st.tuples(st.integers(), st.integers()))
)
def test_concat_associativity(xs, ys, zs):
    a = from_list(xs)
    b = from_list(ys)
    c = from_list(zs)
    assert concat(concat(a, b), c) == concat(a, concat(b, c))


@given(
    st.lists(st.tuples(st.integers(), st.integers()))
)
def test_map_set_preserves_keys(xs):
    tree = from_list(xs)
    result = map_set(tree, lambda k, v: (k + 1, v))
    assert all(isinstance(k, int) for k, _ in to_list(result))


@given(
    st.lists(st.tuples(st.integers(), st.integers()))
)
def test_filter_subset(xs):
    def pred(k, v):
        return k % 2 == 0

    tree = from_list(xs)
    filtered = filter_set(tree, pred)
    assert all(pred(k, v) for k, v in to_list(filtered))


@given(
    st.lists(st.tuples(st.integers(), st.integers()))
)
def test_remove_deletes(xs):
    tree = from_list(xs)
    for k, _ in xs:
        tree = remove(tree, k)
    assert to_list(tree) == []
