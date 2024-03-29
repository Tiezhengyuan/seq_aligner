'''
pytest -s tests/test_smith_waterman.py
'''
from .helper import *
from src.aligner import SmithWaterman as sw

@ddt
class TestNeedlemanWunsch(TestCase):

    @data(
        ['ACGCATCA', 'ACTGATTCA', 2, -3, -2,
            [[  0,  -2,  -4,  -6,  -8, -10, -12, -14, -16, -18],
             [ -2,   2,   0,   0,   0,   0,   0,   0,   0,   0],
             [ -4,   0,   4,   2,   0,   0,   0,   0,   2,   0],
             [ -6,   0,   2,   1,   4,   2,   0,   0,   0,   0],
             [ -8,   0,   2,   0,   2,   1,   0,   0,   2,   0],
             [-10,   0,   0,   0,   0,   4,   2,   0,   0,   4],
             [-12,   0,   0,   2,   0,   2,   6,   4,   2,   2],
             [-14,   0,   2,   0,   0,   0,   4,   3,   6,   4],
             [-16,   0,   0,   0,   0,   2,   2,   1,   4,   8],],

        ],
        [
            'CTAAGT', 'CTCGT', 1, 0, 0,
            [[  0,  -2,  -4,  -6,  -8, -10],
             [ -2,   1,   0,   0,   0,   0],
             [ -4,   0,   2,   0,   0,   1],
             [ -6,   0,   0,   1,   0,   0],
             [ -8,   0,   0,   0,   0,   0],
             [-10,   0,   0,   0,   1,   0],
             [-12,   0,   1,   0,   0,   2],],
        ],
        [
            'TCTATATCCGT', 'ATGCATCCCATGAC', 2, -3, -2,
            [[0, -2, -4, -6, -8, -10, -12, -14, -16, -18, -20, -22, -24, -26, -28],
                [-2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [-4, 0, 0, 0, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 2],
                [-6, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0],
                [-8, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0],
                [-10, 0, 2, 0, 0, 0, 4, 2, 0, 0, 0, 4, 2, 0, 0],
                [-12, 0, 0, 0, 0, 2, 2, 1, 0, 0, 2, 2, 1, 4, 2],
                [-14, 0, 2, 0, 0, 0, 4, 2, 0, 0, 0, 4, 2, 2, 1],
                [-16, 0, 0, 0, 2, 0, 2, 6, 4, 2, 0, 2, 1, 0, 4],
                [-18, 0, 0, 0, 2, 0, 0, 4, 8, 6, 4, 2, 0, 0, 2],
                [-20, 0, 0, 2, 0, 0, 0, 2, 6, 5, 3, 1, 4, 2, 0],
                [-22, 0, 2, 0, 0, 0, 2, 0, 4, 3, 2, 5, 3, 1, 0],],
        ],
    )
    @unpack
    def test_init_matrix(self, ref_seq, seq, match, mismatch, gap, expect):
        c = sw(ref_seq, match, mismatch, gap)
        c.init_matrix(seq)
        c.cal_score()
        assert np.array_equal(c.m, expect)


    @data(
        # start-point is not 0
        [
            'ACGCATCA', 'ACTGATTCA', 2, -3, -2,
            [
                [(8, 8, 9), (6, 7, 8), (4, 6, 7)]
            ],
        ],
        # multiple matches
        [
            'CTAAGT', 'CTCGT', 1, 0, 0,
            [
                [(2, 2, 2), (1, 1, 1)],
                [(2, 6, 5), (1, 5, 4)]
            ],
        ],
        # typical alignment: start from max value to 0, only one match
        [
            'TCTATATCCGT', 'ATGCATCCCATGAC', 2, -3, -2, 
            [
                [(8, 9, 8), (6, 8, 7), (4, 7, 6), (2, 6, 5)]
            ],
        ],
    )
    @unpack
    def test_trace_back(self, ref_seq, seq, match, mismatch, gap, expect):
        c = sw(ref_seq, match, mismatch, gap)
        c.init_matrix(seq)
        c.cal_score()
        paths = c.traces()
        assert paths == expect

