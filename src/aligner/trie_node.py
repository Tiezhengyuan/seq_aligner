'''
node of Trie
'''
from typing import Iterable

class TrieNode:
    def __init__(self, val=None):
        self.val = str(val) if val else ''
        self.parent = None
        self.children = {}
        self.is_end = False
    
    @property
    def is_root(self):
        '''
        value of root is empty
        root node has no parent
        '''
        return True if self.parent is None else False

    @property
    def is_leave(self):
        '''
        leave node has not children
        '''
        return True if self.children == {} else False

    def append(self, new_val):
        # the code is existing
        if new_val in self.children:
            return self.children[new_val]
        # create new node as child
        new_node = TrieNode(new_val)
        new_node.parent = self
        # update parent
        self.children[new_val] = new_node
        return new_node

    def cut(self):
        '''
        remove itself including children
        cut the link from its parent.
        Note: don't delete the node
        '''
        if self.parent:
            del self.parent.children[self.val]
            self.parent = None
            return self
    
    def traverse(self) -> Iterable:
        '''
        walk through all children nodes 
        bredth-first search
        '''
        if self.children:
            for child in self.children.values():
                yield child
                yield from child.traverse()

    def trace_branch(self):
        '''
        go up all the way till the branch
        return the head node of the branch
        '''
        if self.parent:
            if len(self.parent.children) == 1:
                return self.parent.trace_branch()
        return self
