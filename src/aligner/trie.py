
from .trie_node import TrieNode

class Trie:
    def __init__(self):
        self.root = TrieNode('')
        self.output = []
    
    def insert(self, seq:str):
        curr = self.root
        for s in seq:
            curr = curr.append(s)
        curr.is_end = True
        return curr

    def dfs(self, node:TrieNode, prefix:str):
        '''
        depth-first search
        '''
        if node.is_end:
            self.output.append(prefix)
        for val, child in node.children.items():
            self.dfs(child, prefix + val)

    def scan(self):
        '''
        retrieve all strings
        '''
        self.output = []
        for prefix, node in self.root.children.items():
            self.dfs(node, prefix)
        return self.output

    def search(self, prefix:str) -> list:
        '''
        search exact matching prefix
        return all strings
        '''
        prefix_end_node = self.get_prefix(prefix)
        if prefix_end_node:
            prefix = self.trace(prefix_end_node)
            self.get_surfix(prefix_end_node)
            self.output = [prefix + i for i in self.output]
            return self.output
        return None

    def get_prefix(self, prefix:str):
        '''
        exact matching prefix
        return the end node
        '''
        if not prefix:
            return None
        # start from root
        curr = self.root
        for s in prefix:
            if s in curr.children:
                curr = curr.children[s]
            else:
                return None
        return curr

    def trace(self, node:TrieNode):
        '''
        get prefix given an node which could be either leave or other one node
        '''
        prefix = node.val
        curr = node
        while curr.parent:
            curr = curr.parent
            prefix = curr.val + prefix
        return prefix

    def get_surfix(self, node:TrieNode=None):
        if not node:
            node = self.root
        self.output = []
        for surfix, child in node.children.items():
            self.dfs(child, surfix)
        return self.output

    def delete(self, prefix:str):
        '''
        trim branches of trie
        return number of deleted nodes
        '''
        prefix_end_node = self.get_prefix(prefix)
        branch_node = prefix_end_node.trace_branch()
        branch_node.cut()
        pool = list(branch_node.traverse())
        n= 1
        for p in pool:
            del p
            n+=1
        del branch_node
        return n