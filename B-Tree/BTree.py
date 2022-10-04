from time import time
from typing import List, Tuple
from graphviz import Digraph, nohtml

class BTreeNode:
    '''
    # B-Tree Node
    
        A B-Tree Node contains:
        + All keys of node
        + All children of node
        + Parent link and index of this node in parent node
    '''
    def __init__(self, keys : List[int] = [], children = [], parent = (None, -1)) -> None:
        self.keys : List[int] = keys
        self.children : List[BTreeNode] = children
        self.parent : Tuple[BTreeNode, int] = parent

    def __str__(self) -> str:
        return "node-" + ''.join(str(x) for x in self.keys)

    def isLeaf(self) -> bool:
        return len(self.children) == 0

class BTree:
    '''
    # B-Tree
    
        B-Tree features:
        + All leaves are at the same level.
        + Order of B-Tree is maximum children of a node
        + Every node except the root must contain at least t-1 keys. The root may contain a minimum of 1 key.
        + All internal node contain the order number of keys
        + Number of children of a node is equal to the number of keys in it plus 1.
        + All keys of a node are sorted in increasing order. 
        + Insertion of a Node in B-Tree happens only at Leaf Node.
    '''

    def __init__(self, order : int) -> None:
        if order < 3:
            raise Exception("The smallest order of B-Tree must be 3")

        self.__order : int = order
        self.root : BTreeNode = BTreeNode()

    def __str__(self) -> str:
        return "BTree-root: " + str(self.root.keys) 

    def search(self, key : int) -> Tuple[BTreeNode, int]:
        '''
        Return node and index of key in this node. Return (None, -1) if not found
        '''
        curNode = self.root
        while True:
            if key in curNode.keys:
                return (curNode, curNode.keys.index(key))
            
            if len(curNode.children) == 0:
                return (None, -1)
            
            i = 0
            while i < len(curNode.keys) and curNode.keys[i] < key:
                i += 1

            curNode = curNode.children[i]

    def isEmpty(self):
        return len(self.root.keys) == 0

    def insert(self, key : int) -> None:
        '''
        Insert new key to B-Tree
        '''
        
        # Search position to insert
        (node, index) = self.__searchToInsert(key)

        if node is None:
            print("Key has been in tree!")
            return

        # If node is full -> split node, then insert
        if len(node.keys) == self.__order - 1:
            (node, index) = self.__splitNode(node, index)
            node.keys.insert(index, key)
        else:
            node.keys.insert(index, key)

    def delete(self, key : int) -> int:
        '''
        Search and delete a key in B-Tree, return the deleted key
        '''

        (node, index) = self.search(key)
        if node is None:
            print('Can not find key!')
            return

        if node.isLeaf():
            node.keys = node.keys[ : index] + node.keys[index + 1 : ]
            self.__fixUnderflow(node)
        
        # Search most right of left child and swap it
        else:
            curNode = node.children[index]
            while not curNode.isLeaf():
                curNode = curNode.children[-1]

            node.keys[index] = curNode.keys[-1]

            curNode.keys = curNode.keys[ : index] + curNode.keys[index + 1 : ]
            
            self.__fixUnderflow(curNode)

    def show(self, fileName = None):
        '''
        Save tree to .pdf file and display tree using graphviz
        '''
        dot = Digraph(filename='./btree.gv' if fileName is None else fileName, node_attr={"shape" : "record", "height" : ".1"})
        
        waitNodes = [self.root]
        while len(waitNodes) > 0:
            curNode = waitNodes.pop()
            
            # Create a node
            label = "<f0> "
            for i in range(len(curNode.keys)):
                label += "| <f{}> {}| <f{}>".format(2*i + 1, curNode.keys[i], 2*i + 2)
            dot.node(str(curNode), nohtml(label))
            
            # Create edge from parent to this node if not be root
            (parent, index) = curNode.parent
            if not parent is None:
                dot.edge(str(parent)+":f{}".format(2 * index), str(curNode))
            waitNodes += curNode.children

        dot.view()

    def __searchToInsert(self, key : int) -> Tuple[BTreeNode, int]:
        '''
        Search appropriate position to insert
        '''
        curNode = self.root
        while True:
            if key in curNode.keys:
                return (None, -1)

            i = 0
            while i < len(curNode.keys) and curNode.keys[i] < key:
                i += 1

            if len(curNode.children) == 0:
                return (curNode, i)

            curNode = curNode.children[i]
        
    def __fixUnderflow(self, node : BTreeNode) -> None:

        # Case 1 : node is not underflow
        if len(node.keys) > round(self.__order / 2) - 2:
            return


        (parent, index) = node.parent
        if parent is None:
            if len(node.keys) == 0:
                self.root = node.children[0]
                node.children[0].parent = (None, -1)
            return

        # Case 2: Right sibling has at least m/2 keys -> Rotate left
        if index < len(parent.keys) and len(parent.children[index + 1].keys) >= round(self.__order / 2):
            rightSibling = parent.children[index + 1]

            node.keys.append(parent.keys[index])
            
            if len(rightSibling.children) > 0:
                node.children.append(rightSibling.children[0])
                node.children[-1].parent = (node, len(node.children) - 1)
                rightSibling.children = rightSibling.children[1 : ]
                for i in range(len(rightSibling.children)):
                    rightSibling.children[i].parent = (rightSibling, i)
            
            parent.keys[index] = rightSibling.keys[0]
            rightSibling.keys = rightSibling.keys[1:]

        # Case 3: Left sibling has at least m/2 keys -> Rotate right
        elif index > 0 and len(parent.children[index - 1].keys) >= round(self.__order / 2):
            leftSibling = parent.children[index - 1]

            node.keys.append(parent.keys[index-1])
            
            if len(leftSibling.children) > 0:
                node.children.append(leftSibling.children[-1])
                node.children[-1].parent = (node, len(node.children) - 1)
                leftSibling.children = leftSibling.children[ : len(node.children) - 1]
                for i in range(len(leftSibling.children)):
                    leftSibling.children[i].parent = (leftSibling, i)
            
            parent.keys[index - 1] = leftSibling.keys[-1]
            leftSibling.keys = leftSibling.keys[:len(leftSibling.keys) - 1]

        # Case 4: Both left and right sibling has at most m/2 - 1 keys
        elif index < len(parent.keys) and len(parent.children[index + 1].keys) <= round(self.__order / 2) - 1:
            parent.children[index + 1].keys.insert(0, parent.keys[index])
            parent.children[index + 1].keys = parent.children[index].keys + parent.children[index + 1].keys
            parent.children[index + 1].children = parent.children[index].children + parent.children[index + 1].children
            
            for i in range(len(parent.children[index + 1].children)):
                parent.children[index + 1].children[i].parent = (parent.children[index + 1], i)

            parent.keys = parent.keys[:index] + parent.keys[index+1:]
            parent.children = parent.children[:index] + parent.children[index+1:]
            for i in range(len(parent.children)):
                parent.children[i].parent = (parent, i)

        elif index > 0 and len(parent.children[index - 1].keys) <= round(self.__order / 2) - 1:
            parent.children[index - 1].keys.append(parent.keys[index - 1])
            parent.children[index - 1].keys += parent.children[index].keys
            parent.children[index - 1].children += parent.children[index].children
            
            for i in range(len(parent.children[index - 1].children)):
                parent.children[index - 1].children[i].parent = (parent.children[index - 1], i)

            parent.keys = parent.keys[:index-1] + parent.keys[index:]
            parent.children = parent.children[:index] + parent.children[index+1:]
            for i in range(len(parent.children)):
                parent.children[i].parent = (parent, i)

        # propagate up
        self.__fixUnderflow(parent)


    def __splitNode(self, node : BTreeNode, index : int) -> Tuple[BTreeNode, int]:
        '''
        Split a node, then return new position that can insert
        '''
        medianPosition = self.__order // 2
        (parent, nodeIndex) = node.parent

        # f root node, create new root node
        if parent is None:
            parent = BTreeNode(keys=[], children=[], parent=(None, -1))
            nodeIndex = 0
            self.root = parent

        # Insert median to parent keys, if parent is full -> repeat split parent node
        parent.keys.insert(nodeIndex, node.keys[medianPosition])
        if len(parent.keys) > self.__order - 1:
            parent.keys = parent.keys[:nodeIndex] + parent.keys[nodeIndex + 1 :]
            (parent, nodeIndex) = self.__splitNode(parent, nodeIndex)
            parent.keys.insert(nodeIndex, node.keys[medianPosition])

        # If parent has child -> remove it
        # Example:            
        #   [1 , 3]           [1]        [3]
        #   /  | \     ->     / \  and   / \
        # [0 , 2, 4]        [0]  [2]    [] [4]
        if nodeIndex < len(parent.children):
            parent.children = parent.children[:nodeIndex] + parent.children[nodeIndex + 1:]

        # Copy all child from left nodes of median to new left node and right nodes of median to new right node
        node1 = BTreeNode(keys = node.keys[: medianPosition], children=node.children[ : medianPosition + 1], parent=(parent, nodeIndex))       
        for i in range(len(node1.children)):
            node1.children[i].parent = (node1, i)
        parent.children.insert(nodeIndex, node1)
        
        node1 = BTreeNode(keys = node.keys[medianPosition + 1 :], children=node.children[medianPosition + 1:], parent=(parent, nodeIndex + 1))
        for i in range(len(node1.children)):
            node1.children[i].parent = (node1, i)
        parent.children.insert(nodeIndex + 1, node1)

        # Return new position that can insert
        if index <= medianPosition:
            return (parent.children[nodeIndex], index)
        else:
            return (parent.children[nodeIndex + 1], index - 1 - medianPosition)
        

N = 40
btree : BTree = BTree(6)
for i in range(1, N + 1):
    btree.insert(i)

btree.delete(17)
btree.delete(18)
# btree.delete(19)

btree.show()