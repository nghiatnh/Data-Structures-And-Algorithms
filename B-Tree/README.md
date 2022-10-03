# B-Tree Data Structure

- Implement B-Tree Data Structure:

  - Search
  - Insert
  - Delete
  - Show

- Notes:
  - Value insert must be not in tree
  - Value delete can be in tree or not

# B-Tree:

B-Tree features:

- All leaves are at the same level.
- Order of B-Tree is maximum children of a node
- Every node except the root must contain at least t-1 keys. The root may contain a minimum of 1 key.
- All internal node contain the order number of keys
- Number of children of a node is equal to the number of keys in it plus 1.
- All keys of a node are sorted in increasing order.
- Insertion of a Node in B-Tree happens only at Leaf Node.

-> Easy to search, insert and delete ( time complexity are O(N.logN) )
