from typing import Generic, Optional, TypeVar, Callable, List, Tuple
from typing import Protocol, Any
from functools import reduce as functools_reduce


class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...


KT = TypeVar("KT", bound=SupportsLessThan)
VT = TypeVar("VT")
KT2 = TypeVar("KT2")
VT2 = TypeVar("VT2")


class BinaryTreeSet(Generic[KT, VT]):
    def __init__(
        self,
        key: KT,
        value: VT,
        left: Optional['BinaryTreeSet[KT, VT]'] = None,
        right: Optional['BinaryTreeSet[KT, VT]'] = None
    ):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def is_empty(self) -> bool:
        return (
            self.key is None and
            self.value is None and
            self.left is None and
            self.right is None
        )

    def __eq__(self, other):
        if not isinstance(other, BinaryTreeSet):
            return False
        return dict(to_list(self)) == dict(to_list(other))

    def __str__(self):
        if self.is_empty():
            return "{}"
        return "{" + ", ".join(f"{k}: {v}" for k, v in to_list(self)) + "}"

    def __iter__(self):
        if self.is_empty():
            return
        if self.left:
            yield from self.left
        yield (self.key, self.value)
        if self.right:
            yield from self.right


def empty() -> BinaryTreeSet[KT, VT]:
    return BinaryTreeSet(None, None)


def cons(
    pair: Tuple[KT, VT],
    tree: BinaryTreeSet[KT, VT]
) -> BinaryTreeSet[KT, VT]:
    k, v = pair
    if tree.is_empty():
        return BinaryTreeSet(k, v)
    if k == tree.key:
        return BinaryTreeSet(k, v, tree.left, tree.right)
    elif k < tree.key:
        return BinaryTreeSet(
            tree.key,
            tree.value,
            cons((k, v), tree.left or empty()),
            tree.right
        )
    else:
        return BinaryTreeSet(
            tree.key,
            tree.value,
            tree.left,
            cons((k, v), tree.right or empty())
        )


def from_list(pairs: List[Tuple[KT, VT]]) -> BinaryTreeSet[KT, VT]:
    tree: BinaryTreeSet[KT, VT] = empty()
    for k, v in pairs:
        tree = cons((k, v), tree)
    return tree


def to_list(
    tree: BinaryTreeSet[KT, VT]
) -> List[Tuple[KT, VT]]:
    if tree.is_empty():
        return []
    return (
        to_list(tree.left or empty()) +
        [(tree.key, tree.value)] +
        to_list(tree.right or empty())
    )


def member(k: KT, tree: BinaryTreeSet[KT, VT]) -> bool:
    if tree.is_empty():
        return False
    if k == tree.key:
        return True
    elif k < tree.key:
        return member(k, tree.left or empty())
    else:
        return member(k, tree.right or empty())


def length(tree: BinaryTreeSet[KT, VT]) -> int:
    return len(to_list(tree))


def remove(tree: BinaryTreeSet[KT, VT], k: KT) -> BinaryTreeSet[KT, VT]:
    if tree.is_empty():
        return tree
    if k < tree.key:
        return BinaryTreeSet(
            tree.key,
            tree.value,
            remove(tree.left or empty(), k),
            tree.right
        )
    elif k > tree.key:
        return BinaryTreeSet(
            tree.key,
            tree.value,
            tree.left,
            remove(tree.right or empty(), k)
        )
    else:
        if tree.left and not tree.left.is_empty():
            max_kv = to_list(tree.left)[-1]
            return BinaryTreeSet(
                max_kv[0], max_kv[1], remove(tree.left, max_kv[0]), tree.right
            )
        elif tree.right:
            return tree.right
        else:
            return empty()


def concat(
    a: BinaryTreeSet[KT, VT],
    b: BinaryTreeSet[KT, VT]
) -> BinaryTreeSet[KT, VT]:
    return from_list(to_list(a) + to_list(b))


def intersection(
    a: BinaryTreeSet[KT, VT],
    b: BinaryTreeSet[KT, VT]
) -> BinaryTreeSet[KT, VT]:
    return from_list([(k, v) for (k, v) in to_list(a) if member(k, b)])


def map_set(
    tree: BinaryTreeSet[KT, VT],
    f: Callable[[KT, VT], Tuple[KT2, VT2]]
) -> BinaryTreeSet[KT2, VT2]:
    return from_list([f(k, v) for (k, v) in to_list(tree)])


def filter_set(
    tree: BinaryTreeSet[KT, VT],
    predicate: Callable[[KT, VT], bool]
) -> BinaryTreeSet[KT, VT]:
    return from_list([(k, v) for (k, v) in to_list(tree) if predicate(k, v)])


def reduce_set(
    tree: BinaryTreeSet[KT, VT],
    func: Callable[[Tuple[KT, VT], VT2], VT2],
    initializer: VT2
) -> VT2:
    return functools_reduce(
        lambda acc, kv: func(kv, acc),
        to_list(tree),
        initializer
    )
