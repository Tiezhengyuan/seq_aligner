
from .helper import *
from src.aligner import SuffixTrieNode

class TestSuffixTrieNode(TestCase):
    def test_node(self):
        '''
       root
        | \
        a  ba
        |   
        ab  
        '''
        root = SuffixTrieNode()
        a = root.append('a')
        ba = root.append('ba')
        ab = a.append('ab')

        assert root.val == ''
        assert root.parent is None
        assert root.children == [a, ba]
        
        assert a.val == 'a'
        assert a.parent == root
        assert a.children == [ab,]
        assert ba.val == 'ba'
        assert ba.parent == root
        assert ba.children == []
        assert ab.val == 'ab'
        assert ab.parent == a
        assert ab.children == []

    def test_combine(self):
        '''
       root
        | \
        a  ba
        |   
        b
        |
        c
        '''
        root = SuffixTrieNode()
        a = root.append('a')
        ba = root.append('ba')
        b = a.append('b')
        c = b.append('c')

        a.combine(b)
        assert a.val == 'ab'
        assert a.children == [c,]
        assert c.parent == a


    def test_search_children(self):
        '''
       root
        | \
        a  ba
        |   
        ab  
        '''
        root = SuffixTrieNode()
        a = root.append('a')
        ba = root.append('ba')
        ab = a.append('ab')

        # detect
        res = root.search_children('a')
        assert res[0] == a
        assert res[1] == ''
        res = root.search_children('ba')
        assert res[0] == ba
        assert res[1] == ''
        res = root.search_children('bac')
        assert res[0] == ba
        assert res[1] == 'c'
        # no matching
        res = root.search_children('b')
        assert res[0] == None
        assert res[1] == 'b'

        # other node
        res = a.search_children('a')
        assert res[0] == None
        assert res[1] == 'a'
        res = a.search_children('ab')
        assert res[0] == ab
        assert res[1] == ''
        res = a.search_children('abac')
        assert res[0] == ab
        assert res[1] == 'ac'

        print(res)