from .helper import *
from src.aligner import SuffixTree

STR1='ATAATA'
'''
suffix:
$       6
A$      5
TA$     4
ATA$    3
AATA$   2
TAATA$  1
ATAATA$ 0

suffix trie
       root
    /   |    \
   $6   A      T
      / | \     \
    $5  T  A     A
        |   \   /  \
        A   T   $4  A
      / |   |       |
     $3 A   A       T
        |   |       |
        T   $2      A
        |           |
        A          $1
        |
        $0

coalesced suffix trie
        root
    /   |       \
   $6   A        TA
      / |  \     |  \
    $5 TA   ATA  $4  ATA
       /  \   |       |
      $3  ATA $2      $1
           |      
           $0     

'''



@ddt
class TestSuffixTrie(TestCase):

    @data(
        [
            STR1, 
            ['$', 'A', '$', 'T', 'A', '$', 'A', 'T', 'A', '$', 'A', 'T', \
                'A', '$', 'T', 'A', '$', 'A', 'T', 'A', '$'],
            [[6,], [5,], [3,], [0,], [2,], [4,], [1,]],
        ],
    )
    @unpack
    def test_add(self, seq, expect, expect_pos):
        t = SuffixTree()
        t.add(seq)
        nodes = t.root.traverse()
        values, positions = [], []
        for i in nodes:
            values.append(i.val)
            if i.val == '$':
                positions.append(i.position)
        assert values == expect
        assert positions == expect_pos

    @data(
        [
            STR1,
            ['$', 'A', '$', 'TA', '$', 'ATA', '$', 'ATA', '$', 'TA', '$', 'ATA', '$'],
            [[6], [5], [3], [0], [2], [4], [1]],
        ],
    )
    @unpack
    def test_coalesce(self, seq, expect, expect_pos):
        t = SuffixTree()
        t.add(seq)
        t.coalesce()
        nodes = t.root.traverse()
        values, positions = [], []
        for i in nodes:
            values.append(i.val)
            if i.val == '$':
                positions.append(i.position)
        assert values == expect
        assert positions == expect_pos

    @data(
        ['TA', [4]],
        ['TAA', None],
    )
    @unpack
    def test_search(self, seq, expect):
        t = SuffixTree()
        t.add(STR1)
        t.coalesce()
        res = t.search(seq)
        assert res == expect