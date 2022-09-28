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


class HeapTreeRoot:
    '''
    Heap Tree Root
    ----
        Feature of Heap Tree Root:
        + Contains a node link to its children
        + Link to left and right root
        + Union 2 root easily
    '''
    def __init__(self, value: int = None) -> None:
        self.root: HeapTreeNode = None if value is None else HeapTreeNode(
            value=value)
        self.right: HeapTreeRoot = None
        self.left: HeapTreeRoot = None

    def __str__(self) -> str:
        if self.is_empty():
            return 'Empty Heap!'
        return "Fibonacci Heap: " + str(self.root.value)

    def is_empty(self) -> bool:
        '''
        Return True if root is None
        '''
        return self.root is None

    def union(self, root: HeapTreeNode) -> None:
        '''
        Add a root to children of this root
        '''
        if not self.is_empty():
            self.root.children.append(root)
            root.parent = self.root


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
        self.min: HeapTreeRoot = None

    def __str__(self) -> str:
        return str(self.min)

    def show(self, fileName : str = None) -> None:
        '''
        Save to pdf and display heap
        '''
        if self.is_empty():
            print('Empty Heap!')
            return
        dot = Graph()
        curRoot = self.min
        flag = 'right'

        # Min -> red color
        # Marked -> black color
        # Other -> green color
        # Links from roots -> red color
        # Links from parent to children -> black color
        while curRoot:
            # Create root nodes
            dot.node(str(curRoot.root.value),str(curRoot.root.value), color='red' if curRoot is self.min else 'green')

            # Create edge from left root to right root
            if curRoot.left and curRoot != self.min and flag == 'right':
                dot.edge(str(curRoot.left.root.value), str(curRoot.root.value), constraint='false', color='red')
            elif curRoot.right and flag == 'left':
                dot.edge(str(curRoot.root.value), str(curRoot.right.root.value), constraint='false', color='red')

            waitNodes = curRoot.root.children.copy()
            while len(waitNodes) > 0:
                curNode = waitNodes.pop(0)
                # Create nodes
                dot.node(str(curNode.value),str(curNode.value), color='black' if curNode.isMarked else 'green')
                # Create an edge from parent to this node
                if curNode.parent:
                    dot.edge(str(curNode.parent.value), str(curNode.value))
                waitNodes += curNode.children.copy()

            curRoot = curRoot.right if flag == 'right' else curRoot.left
            
            # Change traverse direction 
            if not curRoot and flag == 'right':
                flag = 'left'
                curRoot = self.min.left

        # Save and render image
        if fileName is None:
            fileName = 'fibonacci-heap.gv'
        dot.save(fileName)
        dot.render(fileName, view=True)

    def is_empty(self) -> bool:
        '''
        Return True if min is None
        '''
        return self.min is None

    def search(self, value : int) -> HeapTreeNode:
        '''
        Search a node with value equal given value
        '''
        if self.is_empty() or value < self.min.root.value:
            return None
        
        curRoot = self.min
        flag = 'right'

        # If value < value of node -> do not traverse the node children
        # Traverse all root
        while curRoot:
            if value == curRoot.root.value:
                return curRoot.root
            elif value > curRoot.root.value:
                waitNodes = curRoot.root.children.copy()
                while len(waitNodes) > 0:
                    curNode = waitNodes.pop()
                    if curNode.value == value:
                        return curNode
                    elif value > curNode.value:
                        waitNodes = curNode.children.copy() + waitNodes

            curRoot = curRoot.right if flag == 'right' else curRoot.left

            # Change traverse direction
            if not curRoot and flag == 'right':
                flag = 'left'
                curRoot = self.min.left
        
        return None

    def insert(self, value: int) -> None:
        '''
        Insert new node to the right of min node and update min
        '''
        if self.is_empty():
            self.min = HeapTreeRoot(value=value)
        else:
            newNode = HeapTreeRoot(value=value)

            # Update min
            # If new node is min then min -> new node
            # Else new node is right node of min
            newNode.left = self.min
            newNode.right = self.min.right

            if self.min.right:
                self.min.right.left = newNode
            self.min.right = newNode

            if newNode.root.value < self.min.root.value:
                self.min = newNode

    def insert_root(self, node: HeapTreeNode) -> HeapTreeRoot:
        '''
        Insert new root to heap
        '''
        node.parent = None
        node.isMarked = False
        root = HeapTreeRoot()
        root.root = node
        if self.is_empty():
            self.min = root
        else:
            newNode = root

            # Update min
            # If new node is min then min -> new node
            # Else new node is right node of min
            newNode.right = self.min
            newNode.left = self.min.left

            if self.min.left:
                self.min.left.right = newNode
            self.min.left = newNode

            if newNode.root.value < self.min.root.value:
                self.min = newNode
        return root

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
        childrenOfMin = self.min.root.children

        # Delete min, relink its left and right
        if self.min.right:
            self.min.right.left = self.min.left
        if self.min.left:
            self.min.left.right = self.min.right
        self.min = self.min.right if self.min.right else self.min.left

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
            self.reconstruct(node)
        else:
            node.value = value

    def delete(self, node : HeapTreeNode) -> None:
        '''
        Delete any node in heap : decrease it to -infinity, then delete it
        '''
        self.decrease_key(node, -inf)
        self.delete_min()

    def reconstruct(self, node : HeapTreeNode) -> None:
        '''
        Reconstruct heap after decrease key
        '''
        if node.parent is None:
            return

        parent = node.parent
        children = node
        parent.children.remove(node)
        root = self.insert_root(children)
        root.root.isMarked = False
        if parent.isMarked:
            self.reconstruct(parent)
        else:
            parent.isMarked = parent.parent != None

    def __union_root(self, sameRankRoot : HeapTreeRoot, curRoot : HeapTreeRoot) -> HeapTreeRoot:
        '''
        Union 2 root, put the larger root to children of smaller, then update links to delete larger root
        '''
        if sameRankRoot.root.value < curRoot.root.value:
            sameRankRoot.union(curRoot.root)
            if curRoot.left:
                curRoot.left.right = curRoot.right
            if curRoot.right:
                curRoot.right.left = curRoot.left

            return sameRankRoot
        else:
            curRoot.union(sameRankRoot.root)
            if sameRankRoot.left:
                sameRankRoot.left.right = sameRankRoot.right
            if sameRankRoot.right:
                sameRankRoot.right.left = sameRankRoot.left

            return curRoot

    def __consolidate(self) -> None:
        '''
        Consolidate heap after delete min node
        '''
        if self.is_empty():
            return

        curRoot = self.min
        min = self.min
        ranks = {}
        
        # Set current root to left most root
        while curRoot.left:
            curRoot = curRoot.left

        while curRoot:
            # Check min node while consolidate
            if curRoot.root.value < min.root.value:
                min = curRoot

            # Search the same rank before
            rank = len(curRoot.root.children)
            sameRankRoot = ranks.get(rank, None)

            # If 2 root same rank -> union them
            # Else, put the current node rank to dictionary
            if sameRankRoot:
                ranks.pop(rank)
                nextRoot = self.__union_root(sameRankRoot, curRoot)
            else:
                ranks[rank] = curRoot
                nextRoot = curRoot.right
            curRoot = nextRoot

        # Update min 
        self.min = min


FH = FibonacciHeap()
FH.insert_multiple([3 * x for x in range(10)])
print(FH)
FH.delete_min()
FH.delete_min()
node = FH.search(24)
FH.show()
FH.delete(node)
FH.show()
print(FH)
