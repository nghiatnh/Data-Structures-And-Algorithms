from math import inf
from random import random
from typing import Dict, List
from graphviz import Graph
import graphviz


class HeapTreeNode:
    '''
    Heap Tree Node
    ----
        Feature of Heap Tree Node:
        + Contains value of node
        + Link to parent and children
        + Be marked or not
    '''
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.parent: HeapTreeNode = None
        self.children: List[HeapTreeNode] = []
        self.isMarked = False

    def __str__(self) -> str:
        return str(self.value)


class FibonacciHeap:
    '''
    Fibonacci Heap
    ----
        Features of Fibonacci Heap:
        + Set of heap-ordered trees.
        + Maintain pointer to minimum element.
        + Set of marked nodes.
        + Lazily defer consolidation until next delete-min.
        + Easily insertion and decrease key
        + Difficultly searching
    '''
    def __init__(self) -> None:
        self.min : HeapTreeNode = None
        self.roots : List[HeapTreeNode] = []

    def __str__(self) -> str:
        return "Fibonacci Heap: " + str(self.min)

    def show(self, fileName : str = None) -> None:
        '''
        Save to pdf and display heap
        '''
        if self.is_empty():
            print('Empty Heap!')
            return
        dot = Graph()

        # Min -> red color
        # Marked -> black color
        # Other -> green color
        # Links from roots -> red color
        # Links from parent to children -> black color
        lastRoot = None
        for curRoot in self.roots:
            # Create root nodes
            dot.node(str(curRoot.value),str(curRoot.value), color='red' if curRoot is self.min else 'green')

            # Create edge from left root to right root
            if lastRoot:
                dot.edge(str(lastRoot.value), str(curRoot.value), constraint='false', color='red')

            waitNodes = curRoot.children.copy()
            while len(waitNodes) > 0:
                curNode = waitNodes.pop(0)
                # Create nodes
                dot.node(str(curNode.value),str(curNode.value), color='black' if curNode.isMarked else 'green')
                # Create an edge from parent to this node
                if curNode.parent:
                    dot.edge(str(curNode.parent.value), str(curNode.value))
                waitNodes += curNode.children.copy()

            lastRoot = curRoot

        # Save and render image
        if fileName is None:
            fileName = './fibonacci-heap.gv'
        dot.save(fileName)
        dot.render(fileName, view=True)

    def is_empty(self) -> bool:
        '''
        Return True if min is None or roots list is empty
        '''
        return self.min is None or len(self.roots) == 0

    def search(self, value : int) -> HeapTreeNode:
        '''
        Search a node with value equal given value
        '''
        if self.is_empty() or value < self.min.value:
            return None

        # If value < value of node -> do not traverse the node children
        # Traverse all root
        for curRoot in self.roots:
            if value == curRoot.value:
                return curRoot
            elif value > curRoot.value:
                waitNodes = curRoot.children.copy()
                while len(waitNodes) > 0:
                    curNode = waitNodes.pop()
                    if curNode.value == value:
                        return curNode
                    elif value > curNode.value:
                        waitNodes = curNode.children.copy() + waitNodes

        return None

    def insert(self, value: int) -> None:
        '''
        Insert new node to roots list and update min
        '''
        newNode : HeapTreeNode = HeapTreeNode(value=value)

        self.roots.append(newNode)

        if self.is_empty():
            self.min = newNode
        else:
            if newNode.value < self.min.value:
                self.min = newNode

    def insert_root(self, node: HeapTreeNode) -> HeapTreeNode:
        '''
        Insert new root to heap and update min
        '''
        node.parent = None
        node.isMarked = False

        self.roots.append(node)
        
        if self.is_empty():
            self.min = node
        else:
            if node.value < self.min.value:
                self.min = node
            
        return node

    def insert_multiple(self, values: List[int]) -> None:
        '''
        Insert multiple values to heap
        '''
        for value in values:
            self.insert(value)

    def delete_min(self) -> None:
        '''
        Delete min node in the heap, then consolidate it
        '''
        if self.is_empty():
            return

        childrenOfMin = self.min.children

        self.roots.remove(self.min)

        # Put all children of min to root
        for node in childrenOfMin:
            self.insert_root(node)

        self.__consolidate()

    def decrease_key(self, node : HeapTreeNode, value : int) -> None:
        '''
        Decrease value of a node and reconstruct heap
        '''
        if node.parent is None:
            return
        
        if value < node.parent.value:
            node.value = value
            self.__reconstruct(node)
        else:
            node.value = value

    def delete(self, node : HeapTreeNode) -> None:
        '''
        Delete any node in heap : decrease it to -infinity, then delete it
        '''
        self.decrease_key(node, -inf)
        self.delete_min()

    def union(self, heap) -> None:
        '''
        Union other heap to this heap
        '''
        heap : FibonacciHeap = heap

        self.roots += heap.roots
        if heap.min.value < self.min.value:
            self.min = self.roots[self.roots.index(heap.min)]

    def __reconstruct(self, node : HeapTreeNode) -> None:
        '''
        Reconstruct heap after decrease key
        '''
        if node.parent is None:
            return

        parent = node.parent
        children = node
        parent.children.remove(node)
        root = self.insert_root(children)
        root.isMarked = False
        if parent.isMarked:
            self.__reconstruct(parent)
        else:
            parent.isMarked = parent.parent != None

    def __consolidate(self) -> None:
        '''
        Consolidate heap after delete min node
        '''
        if self.is_empty():
            return

        i = 0
        min : HeapTreeNode = self.roots[0]
        ranks = {}

        while i < len(self.roots):
            curRoot = self.roots[i]

            # Check min node while consolidate
            if curRoot.value < min.value:
                min = curRoot

            # Search the same rank before
            rank = len(curRoot.children)
            sameRankRoot : HeapTreeNode = ranks.get(rank, None)

            # If 2 root same rank -> union them
            # Else, put the current node rank to dictionary
            if sameRankRoot and sameRankRoot != curRoot:
                ranks.pop(rank)
                '''
                Union 2 root, put the larger root to children of smaller, then update links to delete larger root
                '''

                if sameRankRoot.value < curRoot.value:
                    sameRankRoot.children.append(curRoot)
                    curRoot.parent = sameRankRoot
                    self.roots.remove(curRoot)
                    i = self.roots.index(sameRankRoot)
                else:
                    curRoot.children.append(sameRankRoot)
                    sameRankRoot.parent = curRoot
                    self.roots.remove(sameRankRoot)
                    i = self.roots.index(curRoot)

            else:
                ranks[rank] = curRoot
                i += 1
        # Update min 
        self.min = min

import time
FH = FibonacciHeap()
time1 = time.time()
FH.insert_multiple([3 * x for x in range(200000)])
time2 = time.time()
print("insert: ", time2 - time1)
time1 = time.time()
FH.delete_min()
time2 = time.time()
print("delete min: ", time2 - time1)
time1 = time.time()
FH.delete_min()
time2 = time.time()
print("delete min 2: ", time2 - time1)
# FH.delete_min()
# FH.show()
print("After delete 2 min node: ", FH)

FH1 = FibonacciHeap()
FH1.insert_multiple([3 * x+1 for x in range(2000)])
FH1.delete_min()
time1 = time.time()
FH1.union(FH)
time2 = time.time()
print("union: ", time2 - time1)
print("After delete 1 min node", FH1)
