# Kirov reporting！- lab 1 - variant 3 - Set based on binary tree

This project implements a Set based on a binary search tree (BST) structure,
demonstrating an immutable persistent data structure.
It supports core set operations and functional programming paradigms.

## Project Structure

- `binary_tree_set.py` — Implementation of the `BinaryTreeSet` class with methods
for insertion,deletion, membership checks, and functional operations.
- `test_binary_tree_set.py` — Comprehensive unit tests and property-based tests
(PBT) for the BST implementation.

## Features

### Core Functionality

- **Insertion (`cons`)**  
  Add key-value pairs while maintaining BST properties.
  Duplicate keys replace existing values.

- **Deletion (`remove`)**  
  Remove elements by key. Automatically reorganizes the tree structure.

- **Membership Check (`member`)**  
  Efficiently check if a key exists in the tree.

- **Size (`length`)**  
  Get the number of elements in the tree.

- **Conversion**  
   - `from_list(lst)`: Build a tree from a list of key-value pairs.
   - `to_list()`: Convert the tree to an ordered list.

- **Set Operations**  
   - `concat(tree1, tree2)`: Merge two trees.
   - `intersection(tree1, tree2)`: Return a tree with common keys.

### Functional Operations

- **`filter_set(predicate)`**  
  Create a new tree with elements satisfying the predicate `(key, value) -> bool`.

- **`map_set(func)`**  
  Apply a function `(key, value) -> (new_key, new_value)` to all elements, producing a transformed tree.

- **`reduce_set(func, initial)`**  
  Aggregate values using a reducer function `(key_value_pair, accumulator) -> new_accumulator`.

### Property-Based Tests (PBT)

- **Round-trip List Conversion**  
  Validate `from_list` and `to_list` consistency.

- **Length Consistency**  
  Ensure tree size matches the number of unique keys.

- **Associativity of Concatenation**  
  Verify `concat(a, concat(b, c)) == concat(concat(a, b), c)`.

- **Filter Subset Property**  
  Confirm filtered elements satisfy the predicate.

## Usage Example

```python
# Create a tree from a list
tree = from_list([(3, 'c'), (1, 'a'), (2, 'b')])

# Insert a new element
tree = cons((4, 'd'), tree)

# Remove an element
tree = remove(tree, 2)

# Functional operations
mapped_tree = map_set(tree, lambda k, v: (k*2, v.upper()))
filtered_tree = filter_set(tree, lambda k, v: k % 2 == 1)

# Reduce to sum values
total = reduce_set(tree, lambda kv, acc: kv[1] + acc, 0)
```

## Changelog

- **07.04.2025 - 1**
- Added comprehensive test suite including unit tests and property-based tests.

- **01.04.2025 - 0**
- Initial implementation.
- Basic tests.

## Design Notes

- **Immutable Persistent Structure**  
  All operations return new trees, preserving previous versions.

- **BST Organization**  
  Keys are stored in-order, enabling efficient lookups (O(log n) in balanced cases).

- **Collision Handling**  
  Duplicate keys overwrite existing values during insertion.

- **Testing Rigor**  
  Combines unit tests with Hypothesis-based property tests for robustness.

## Contribution

- Implementation & Documentation: `Sun Jiajian (<sunakagi@163.com>)`  
- Test Development: `Yang Liang (<2663048219@qq.com>)`  

---

*Built with Python type hints. Compatible with Python 3.8+. Requires `hypothesis` for PBT.*
