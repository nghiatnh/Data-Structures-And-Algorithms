# Fibonacci Heap Data Structure

- Implement Fibonacci Heap Data Structure:
  + Search 
  + Insert
  + Insert Multiple
  + Delete Min
  + Decrease Key
  + Delete Any Key
  + Union
  + Show

- Notes:
  + Value insert must be not in heap
  + Value delete must be in heap

# Fibonacci Heap:

A Fibonacci Heap contains:
  + List of Heap Tree Node (name roots)
  + Pointer to min root (name min)

-> Easy to insert, delete and union

A Heap Tree Node contains:
  + Integer value
  + Pointer to parent
  + List of children
  + Be marked or not (named isMarked)

-> Easy to find parent and children