'''
a trie of all suffixes
'''
from .iterate_seq import IterateSeq
from .suffix_trie_node import SuffixTrieNode


class SuffixTree:
    def __init__(self):
        self.root = SuffixTrieNode('')
        self.output = []
    
    def add(self, seq):
        for seq_surfix, pos in IterateSeq(seq).surfix():
            curr = self.root
            for s in seq_surfix:
                curr = curr.append(s)
            curr.position.append(pos)
        return curr
    
    def coalesce(self):
        '''
        combine non-branching paths
        '''
        parent = None
        for node in self.root.traverse():
            if node.is_leave:
                parent = None
            else:
                if parent is None:
                    parent = node
                else:
                    parent.combine(node)

    def search(self, sub:str):
        curr = self.root
        while (curr and sub):
            curr, sub = curr.search_children(sub)
        if curr and sub == '':
            end = curr.children[0]
            return end.position
        return None

