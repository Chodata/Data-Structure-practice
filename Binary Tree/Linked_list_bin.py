#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 13:40:48 2018

@author: dittaya
"""

class Tree:
    # abstract methods
    class Position:
        def element(self):
            raise NotImplementedError('must be implemented')
        def __eq__(self, other):
            raise NotImplementedError('must be implemented')
        def __neq__(self, other):
            return not (self == other)
    def root(self):
        raise NotImplementedError('must be implemented')
    def parent(self, p):
        raise NotImplementedError('must be implemented')
    def num_children(self, p):
        raise NotImplementedError('must be implemented')
    def children(self, p):
        raise NotImplementedError('must be implemented')
    def __len__(self):
        raise NotImplementedError('must be implemented')
    def positions(self):
        raise NotImplementedError('must be implemented')
    
    # concrete methods
    def is_root(self, p):
        return p == self.root()
    def is_leaf(self, p):
        return self.num_children(p) == 0
    def is_empty(self):
        return self.num_children == 0
    def depth(self, p):
        if self.root() == p:
            return 0
        else:
            return 1+self.depth(self.parent())
    def height_bad(self):
        return max(self.depth(p) for p in self.positions() if p.is_leaf())
    
    def _height(self, p):
        if self.is_leaf(p):
            return 0
        else:
            return 1+max(self._height(p) for p in self.children())
    def height(self, p):
        if p is None:
            return 0
        else:
            return self._height(self.root())

    def preorder(self, p):
        if p is not None:
            yield p
            for child in self.children(p):
                for node in self.preorder(child):
                    yield node

    def postorder(self, p):
        if p is not None:
            for child in self.children(p):
                for node in self.preorder(child):
                    yield node
            yield p
    

class BinaryTree(Tree):
    # abstract methods
    def left(self, p):
        raise NotImplementedError('must be implemented')
    def right(self, p):
        raise NotImplementedError('must be implemented')
    def sibling(self, p):
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)
    
    # override children in Tree
    def children(self, p):
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    # special case for binary tree
#    def preorder(self, p):
#        if p is not None:
#            yield p
#            for c in self.preorder(self.left(p)):
#                yield c
#            for c in self.preorder(self.right(p)):
#                yield c
    
    def inorder(self, p):
        if p is not None:
            for c in self.preorder(self.left(p)):
                yield c
            yield p
            for c in self.preorder(self.right(p)):
                yield c
    
    def positions(self):
        return self.preorder(self.root())                
        
    def __iter__(self):
        for p in self.positions():
            yield p.element()

    
class LinkedBinaryTree(BinaryTree):
    class _Node:
        __slots__ = '_element', '_parent', '_left', '_right'
        def __init__(self, e, parent=None, left=None, right=None):
            self._element = e
            self._parent = parent
            self._left = left
            self._right = right
        def parent(self):
            return self._parent
        def element(self):
            return self._element
        def left(self):
            return self._left
        def right(self):
            return self._right

    # overried Tree.Position
    class Position(BinaryTree.Position):
        def __init__(self, node, container):
            self._node = node
            self._container = container
        
        def element(self):
            return self._node._element
        
        def __eq__(self, other):
            return type(self) is type(other) and self._node is other._node

    def __init__(self):
        self._root = None
        self._size = 0
    
    def root(self):
        return self._make_position(self._root)

    def _validate(self, p):
        if isinstance(p, self.Position) \
            and p._container is self \
            and p._node._parent is not p._node: # loop back for deleted node
            return p._node
        else:
            raise Exception('Invalid position')

    def _make_position(self, node):
        if node is None:
            return None
        else:
            return self.Position(node, self)

    def parent(self, p):
        node  = self._validate(p)
        return self._make_position(node._parent)
    
    def left(self, p):
        node  = self._validate(p)
        return self._make_position(node._left)
    
    def right(self, p):
        node  = self._validate(p)
        return self._make_position(node._right)
        
    def num_children(self, p):
        node  = self._validate(p)
        n_child = 0
        if node._left != None:
            n_child += 1
        if node._right != None:
            n_child += 1
        return n_child

    def is_leaf(self,p):
        return self.num_children(p) == 0
    
    def is_root(self, p):
        return self.root() == p
    
    def __len__(self):
        return self._size
    
    def add_root(self, e):
        if self._size != 0:
            raise Exception('The tree is not empty')
        else:
            self._root = self._Node(e)
            self._size = 1
            return self._make_position(self._root)
    
    def add_left(self, p, e):
        node = self._validate(p)
        if node._left !=  None:
            raise Exception('Left subtree is not empty')
        else:
            newnode = self._Node(e, node)
            node._left = newnode
            self._size += 1
        return self._make_position(newnode)
        
    def add_right(self, p, e):
        node = self._validate(p)
        if node._right !=  None:
            raise Exception('Right subtree is not empty')
        else:
            newnode = self._Node(e, node)
            node._right = newnode
            self._size += 1
        return self._make_position(newnode)

    def set(self, p, e):
        node = self._validate(p)
        old_element = node._element
        node._element = e     
        return old_element
    
    def attach(self, p, T1, T2):
        if not self.is_leaf(p):
            raise Exception('p is not a leaf')
        else:
            node = self._validate(p)
            if T1 is not None:
                left_root = T1.root()
                node._left = left_root._node
                self._size += len(T1)
            if T2 is not None:
                right_root = T2.root()
                node._right = right_root._node
                self._size += len(T2)
        return p
    
    def remove(self, p):
        if not self.is_leaf(p):
            raise Exception('p is not leaf')
        else:
            node = self._validate(p)
            if len(self) > 1:
                parent_node = node._parent
                if node == parent_node._left:
                    parent_node._left = None
                else:
                    parent_node._right = None
                node._parent = node
            else:
                node._parent = node
                self._root = None
            self._size -= 1
        return node._element
        


if __name__ == '__main__':
    t1 = LinkedBinaryTree()
#    t1 = ArrayBinaryTree()

    p = t1.add_root(10)
    p1 = t1.add_left(p, 1)
    p2 = t1.add_right(p, 20)
    print(len(t1))
    print('--')
    for e in t1:
        print(e)
    print('--')
    try:
        t1.add_left(p, 10)
        t1.add_right(p, 20)
    except Exception:
        pass
    t1.set(p, 2)
    for pos in t1.inorder(p):
        print(pos.element())

    print("--")
    t1.remove(p2)
    print(len(t1))
    print('--')
    t2 = LinkedBinaryTree()
    t2.add_root(100)
    t1.attach(p1, None, t2)
    for e in t1:
        print(e)
