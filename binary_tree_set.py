from typing import Generic, Optional, TypeVar, Callable, \
    List, Tuple, Protocol, Iterator, runtime_checkable
from functools import reduce as functools_reduce


@runtime_checkable
class SupportsLessThan(Protocol):
    def __lt__(self, other: object) -> bool: ...


KT = TypeVar("KT", bound=SupportsLessThan)
VT = TypeVar("VT")
KT2 = TypeVar("KT2", bound=SupportsLessThan)
VT2 = TypeVar("VT2")


class BinaryTreeSet(Generic[KT, VT]):
    def is_empty(self) -> bool:
        raise NotImplementedError

    def __iter__(self) -> Iterator[Tuple[KT, VT]]:
        if isinstance(self, Node):
            if not self.left.is_empty():
                yield from self.left
            yield (self.key, self.value)
            if not self.right.is_empty():
                yield from self.right

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BinaryTreeSet):
            return False
    
        def inorder_gen(node: BinaryTreeSet[KT, VT]):
            stack: List[BinaryTreeSet[KT, VT]] = []
            while stack or not node.is_empty():
                while not node.is_empty():
                    assert isinstance(node, Node)
                    stack.append(node)
                    node = node.left
                node = stack.pop()
                yield (node.key, node.value)
                node = node.right
    
        gen1 = inorder_gen(self)
        gen2 = inorder_gen(other)
    
        for pair1, pair2 in zip(gen1, gen2):
            if pair1 != pair2:
                return False
    
        # Check if both trees had the same number of nodes
        try:
            next(gen1)
            return False
        except StopIteration:
            pass
    
        try:
            next(gen2)
            return False
        except StopIteration:
            pass
    
        return True


    def __str__(self) -> str:
        if self.is_empty():
            return "{}"
        return "{" + ", ".join(f"{k}: {v}" for k, v in self) + "}"


class EmptyTree(BinaryTreeSet[KT, VT]):
    def is_empty(self) -> bool:
        return True

    def __iter__(self) -> Iterator[Tuple[KT, VT]]:
        return iter(())


class Node(BinaryTreeSet[KT, VT]):
    key: KT
    value: VT
    left: BinaryTreeSet[KT, VT]
    right: BinaryTreeSet[KT, VT]

    def __init__(
        self,
        key: KT,
        value: VT,
        left: Optional[BinaryTreeSet[KT, VT]] = None,
        right: Optional[BinaryTreeSet[KT, VT]] = None
    ) -> None:
        self.key = key
        self.value = value
        self.left = left or empty()
        self.right = right or empty()

    def is_empty(self) -> bool:
        return False

    def __iter__(self) -> Iterator[Tuple[KT, VT]]:
        if not self.left.is_empty():
            yield from self.left
        yield (self.key, self.value)
        if not self.right.is_empty():
            yield from self.right


def empty() -> BinaryTreeSet[KT, VT]:
    return EmptyTree()


def cons(
    pair: Tuple[KT, VT],
    tree: BinaryTreeSet[KT, VT]
) -> BinaryTreeSet[KT, VT]:
    k, v = pair
    if tree.is_empty():
        return Node(k, v)
    assert isinstance(tree, Node)
    if k == tree.key:
        return Node(k, v, tree.left, tree.right)
    elif k < tree.key:
        return Node(tree.key, tree.value, cons((k, v), tree.left), tree.right)
    else:
        return Node(tree.key, tree.value, tree.left, cons((k, v), tree.right))


def from_list(pairs: List[Tuple[KT, VT]]) -> BinaryTreeSet[KT, VT]:
    tree: BinaryTreeSet[KT, VT] = empty()
    for k, v in pairs:
        tree = cons((k, v), tree)
    return tree


def to_list(tree: BinaryTreeSet[KT, VT]) -> List[Tuple[KT, VT]]:
    return list(tree)


def member(k: KT, tree: BinaryTreeSet[KT, VT]) -> bool:
    if tree.is_empty():
        return False
    assert isinstance(tree, Node)
    if k == tree.key:
        return True
    elif k < tree.key:
        return member(k, tree.left)
    else:
        return member(k, tree.right)


def length(tree: BinaryTreeSet[KT, VT]) -> int:
    return sum(1 for _ in tree)


def remove(tree: BinaryTreeSet[KT, VT], k: KT) -> BinaryTreeSet[KT, VT]:
    if tree.is_empty():
        return tree
    assert isinstance(tree, Node)
    if k < tree.key:
        return Node(tree.key, tree.value, remove(tree.left, k), tree.right)
    elif k > tree.key:
        return Node(tree.key, tree.value, tree.left, remove(tree.right, k))
    else:
        if not tree.left.is_empty():
            max_kv = to_list(tree.left)[-1]
            return Node(
                max_kv[0],
                max_kv[1],
                remove(tree.left, max_kv[0]), tree.right
            )
        else:
            return tree.right


def concat(
    a: BinaryTreeSet[KT, VT],
    b: BinaryTreeSet[KT, VT]
) -> BinaryTreeSet[KT, VT]:
    result: BinaryTreeSet[KT, VT] = a
    for k, v in b:
        result = cons((k, v), result)
    return result


def intersection(
    a: BinaryTreeSet[KT, VT],
    b: BinaryTreeSet[KT, VT]
) -> List[Tuple[KT, VT]]:
    return [(k, v) for k, v in a if member(k, b)]


def map_set(
    tree: BinaryTreeSet[KT, VT],
    f: Callable[[KT, VT], Tuple[KT2, VT2]]
) -> BinaryTreeSet[KT2, VT2]:
    result: BinaryTreeSet[KT2, VT2] = empty()
    for k, v in tree:
        new_k, new_v = f(k, v)
        result = cons((new_k, new_v), result)
    return result


def filter_set(
    tree: BinaryTreeSet[KT, VT],
    predicate: Callable[[KT, VT], bool]
) -> BinaryTreeSet[KT, VT]:
    result: BinaryTreeSet[KT, VT] = empty()
    for k, v in tree:
        if predicate(k, v):
            result = cons((k, v), result)
    return result


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
