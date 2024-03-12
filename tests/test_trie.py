'''
pytest -s tests/test_trie.py
'''
from .helper import *
from src.aligner import Trie


@ddt
class TestTrie(TestCase):

    @data(
        [['ATGC',], 'C'],
        [['ATGC', 'TGGG'], 'G'],
    )
    @unpack
    def test_insert(self, input, expect):
        t = Trie()
        for s in input:
            res = t.insert(s)
        assert res.val == expect


    @data(
        [['ATGC',], ['ATGC',]],
        # different seq
        [['ATGC','TGTG'], ['ATGC','TGTG']],
        # duplicated seq
        [['ATGC','ATGC',], ['ATGC',]],
        # longer seq
        [['ATGC','ATGCATG'], ['ATGC','ATGCATG'],],
    )
    @unpack
    def test_scan(self, input, expect):
        t = Trie()
        for s in input:
            t.insert(s)
        res = t.scan()
        assert res == expect

    @data(
        ['AT', 'T'],
        ['CTT', None],
    )
    @unpack
    def test_get_prefix(self, input, expect_val):
        t = Trie()
        for s in ['ATGC', 'ATGC', 'ATGCGGA', 'ATGCATGC', 'TTGAAA']:
            t.insert(s)
        node = t.get_prefix(input)
        if node:
            assert node.val == expect_val
        else:
            assert node == expect_val

    @data(
        # parent node
        ['AT', 'AT'],
        # leave node
        ['TTGAAA', 'TTGAAA'],
    )
    @unpack
    def test_trace(self, input, expect):
        t = Trie()
        for s in ['ATGC', 'ATGC', 'ATGCGGA', 'ATGCATGC', 'TTGAAA']:
            t.insert(s)
        node = t.get_prefix(input)
        res = t.trace(node)
        assert res == expect

    @data(
        ['AT', ['GC', 'GCGGA', 'GCATGC']],
        ['TTGAAA', []],
        ['TTGAA', ['A']],
    )
    @unpack
    def test_get_surfix(self, input, expect):
        t = Trie()
        for s in ['ATGC', 'ATGC', 'ATGCGGA', 'ATGCATGC', 'TTGAAA']:
            t.insert(s)
        node = t.get_prefix(input)
        res = t.get_surfix(node)
        assert res == expect


    @data(
        ['AT', ['ATGC', 'ATGCGGA', 'ATGCATGC']],
        ['TTGAAA', []],
        ['TTGAA', ['TTGAAA']],
    )
    @unpack
    def test_search(self, input, expect):
        t = Trie()
        for s in ['ATGC', 'ATGC', 'ATGCGGA', 'ATGCATGC', 'TTGAAA']:
            t.insert(s)
        res = t.search(input)
        assert res == expect

    @data(
        ['AT', 11, ['TTGA']],
        ['ATGCG', 3, ['ATGC', 'ATGCATGC', 'TTGA']],
        ['T', 4, ['ATGC', 'ATGCGGA', 'ATGCATGC']],
    )
    @unpack
    def test_delete(self, input, deleted, expect):
        '''
           ROOT
          /  \
          A   T
          |   |
          T   T
          |   |
          G   G
          |   |
          C   A
         / \
        G   A
        |   |
        G   T
        |   |
        A   G
            |
            C
        '''
        t = Trie()
        for s in ['ATGC', 'ATGC', 'ATGCGGA', 'ATGCATGC', 'TTGA']:
            t.insert(s)
        count = t.delete(input)
        assert count == deleted
        res = t.scan()
        assert res == expect
