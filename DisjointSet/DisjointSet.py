from __future__ import annotations
from typing import *

class DisjointSet_LinkedList:
    '''
    Disjoint Set
    ----------

    Disjoint set data structure using Linked List.

    Disjoint set contains:
    - sets: Tuple with key is the node value, value is the representative of Linked List.

    Example::

        s = DisjointSet_LinkedList()

        s.makeSet(5) # 5 -> 5
        s.makeSet(6) # 6 -> 6
        s.makeSet(7) # 7 -> 7
        s.makeSet(8) # 8 -> 8

        s.union(5,6) # 5,6 -> 5
        s.union(6,7) # 5,6,7 -> 5

        print(s.findSet(5)) # 5
        print(s.findSet(6)) # 5
        print(s.findSet(7)) # 5
        print(s.findSet(8)) # 8

    This data structure is slow because taking O(N1 + N2) for Union operation. You should use Disjoint_Forest data structure instead.
    - N1: Length of first set
    - N2: Length of second set
    '''

    class __LinkedListNode:
        '''
        Linked List Node
        ---------

        Contain representative, next node and value of node in set
        '''
        def __init__(self, value : object = 0) -> None:
            self.representative : DisjointSet_LinkedList.__LinkedListNode | None = self
            self.next : DisjointSet_LinkedList.__LinkedListNode | None = None
            self.value : object = value

        def __eq__(self, __o: object) -> bool:
            return self.value.__eq__(__o.value)

        def __str__(self) -> str:
            return str(self.value)

    #-------------------------------#

    def __init__(self) -> None:
        self.sets : Tuple[object, DisjointSet_LinkedList.__LinkedListNode] = {}

    def makeSet(self, x : object) -> None:
        '''
        Create a new set that contain only x.
        '''
        self.sets[x] = DisjointSet_LinkedList.__LinkedListNode(x)

    def union(self, x : object, y : object) -> DisjointSet_LinkedList.__LinkedListNode:
        '''
        Union 2 sets that contain x and y. The new representative is representative of x.
        '''
        a = self.findSet(x)
        b = self.findSet(y)
        curB = b
        while not curB is None:
            curB.representative = a.representative
            curB = curB.next
        
        curA = a
        while not curA.next is None:
            curA = curA.next

        curA.next = b

        self.sets[x] = self.sets[y] = a

        return a.representative

    def findSet(self, x : object) -> DisjointSet_LinkedList.__LinkedListNode:
        '''
        Find representative of a node in set
        '''
        return self.sets[x].representative

class DisjointSet_Forest:
    '''
    Disjoint Set
    ----------

    Disjoint set data structure using Forest.

    Disjoint set contains:
    - rank: Tuple with key is the node value, value is the rank of its representative node.
    - parent: Tuple with key is the node value, value is the parent of this node.

    Example::

        s = DisjointSet_Forest()

        s.makeSet(5) # 5 -> 5
        s.makeSet(6) # 6 -> 6
        s.makeSet(7) # 7 -> 7
        s.makeSet(8) # 8 -> 8

        s.union(5,6) # 5,6 -> 6
        s.union(6,7) # 5,6,7 -> 6

        print(s.findSet(5)) # 6
        print(s.findSet(6)) # 6
        print(s.findSet(7)) # 6
        print(s.findSet(8)) # 8

    This data structure is fast because taking O(1) for Union operation.
    '''

    def __init__(self) -> None:
        self.rank : Tuple[object, int] = {}
        self.parent : Tuple[object, object] = {}

    def makeSet(self, x : object) -> None:
        '''
        Create a new set that contain only x.
        '''
        self.parent[x] = x
        self.rank[x] = 0

    def union(self, x : object, y : object) -> DisjointSet_LinkedList.__LinkedListNode:
        '''
        Union 2 sets that contain x and y. The new representative is representative of x.
        '''
        a = self.findSet(x)
        b = self.findSet(y)
        
        if self.rank[a] > self.rank[b]:
            self.parent[b] = a
        else:
            self.parent[a] = b
            if self.rank[x] == self.rank[b]:
                self.rank[b] += 1

    def findSet(self, x : object) -> DisjointSet_LinkedList.__LinkedListNode:
        '''
        Find representative of a node in set
        '''
        if x != self.parent[x]:
            self.parent[x] = self.findSet(self.parent[x])
        
        return self.parent[x]