'''
pytest -s tests/test_smith_waterman.py
'''
from .helper import *
from src.aligner import DotMatrix as dm

@ddt
class TestDotMatrix(TestCase):

    @data(
        ['CGTAACT', 'CGTATCCT', 
         [[ 1,  0,  0,  0,  0,  1,  1,  0,],
            [ 0,  1,  0,  0,  0,  0,  0,  0,],
            [ 0,  0,  1,  0,  1,  0,  0,  1,],
            [ 0,  0,  0,  1,  0,  0,  0,  0,],
            [ 0,  0,  0,  1,  0,  0,  0,  0,],
            [ 1,  0,  0,  0,  0,  1,  1,  0,],
            [ 0,  0,  1,  0,  1,  0,  0,  1,],],
        ],
        ['CGTAACT','CGTAACT',
          [[1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 1],],
        ],
    )
    @unpack
    def test_build(self, seq1, seq2, expect):
        res = dm(seq1).build(seq2)
        assert np.array_equal(res, expect)
    
    @data(
        # 
        ['CGTAACT','CGTAACT', True],
        ['CGTAACT','CGTAACTA', True],
        #seq2<seq1
        ['CGTAACT','CGTAAC', False],
        # mismatch
        ['CGTAACT','CGTAAAT', False],
    )
    @unpack
    def test_is_identical(self, seq1, seq2, expect):
        res = dm(seq1).is_identical(seq2)
        assert res == expect

    @data(
        # reverse sequence
        ['CGTAACT','TCAATGC', True],
        # palindrome
        ['MAXISTAYAWAYATSIXAM', None, True],
        ['CGTAACT','TCAACGC', False],
    )
    @unpack
    def test_is_reversion(self, seq1, seq2, expect):
        res = dm(seq1).is_reversion(seq2)
        assert res == expect

    # @data(
    #     ['GAATTC', True],
    #     ['MAXISTAYAWAYATSIXAM', True]
    # )
    # @unpack
    # def test_is_(self, seq, expect):
    #     c = dm(seq, seq)
    #     c.build()
    #     print(c.m)
