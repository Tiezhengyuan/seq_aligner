'''
pytest -s tests/test_trie.py
'''
from .helper import *
from src.aligner import TrieNode


@ddt
class TestTrieNode(TestCase):

    def test_root(self):
        root = TrieNode('')
        assert root.val == ''

    def test_append(self):
        root = TrieNode('')
        node1 = root.append('a')
        node2 = node1.append('b')

        assert root.val == ''
        assert root.parent == None
        assert root.children == {'a': node1}

        assert node1.val == 'a'
        assert node1.parent == root
        assert node1.children == {'b': node2}

        assert node2.val == 'b'
        assert node2.parent == node1
        assert node2.children == {}

    def test_cut(self):
        '''
        root
          |
          a
         / \
        b1 b2
            \
             c
        '''
        root = TrieNode('')
        a = root.append('a')
        b1 = a.append('b1')
        b2 = a.append('b2')
        c = b2.append('c')

        res = c.cut()
        assert b2.children == {}
        assert c.parent is None

        assert root.children == {'a': a}
        res = a.cut()
        assert root.children == {}
        assert a.parent is None
        assert res == a


    def test_traverse(self):
        '''
        root
          |
          a
         / \
        b1 b2
            \
             c
        '''
        root = TrieNode('')
        res = [i.val for i in root.traverse()]
        assert res == []

        node1 = root.append('a')
        node2 = node1.append('b1')
        node3 = node1.append('b2')
        node4 = node3.append('c')
        res = [i.val for i in root.traverse()]
        assert res == ['a', 'b1', 'b2', 'c']
        res = [i.val for i in node1.traverse()]
        assert res == ['b1', 'b2', 'c']
        res = [i.val for i in node2.traverse()]
        assert res == []
        res = [i.val for i in node3.traverse()]
        assert res == ['c']
        res = [i.val for i in node4.traverse()]
        assert res == []

    def test_trace_tranch(self):
        '''
        root
          |
          a
         / \
        b1 b2
           / \
          c1 c2
          /
         d1
         |
         e1
        '''
        root = TrieNode('')
        a = root.append('a')
        b1 = a.append('b1')
        b2 = a.append('b2')
        c1 = b2.append('c1')
        c2 = b2.append('c2')
        d1 = c1.append('d1')
        e1 = d1.append('e1')

        res = e1.trace_branch()
        assert res == c1
        res = d1.trace_branch()
        assert res == c1
        res = c1.trace_branch()
        assert res == c1
        res = c2.trace_branch()
        assert res == c2
        res = b2.trace_branch()
        assert res == b2
        res = a.trace_branch()
        assert res == root