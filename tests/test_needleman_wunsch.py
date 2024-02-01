'''
pytest -s tests/test_needleman_wunsch.py
'''
from .helper import *
from src.aligner import NeedlemanWunsch as nw

@ddt
class TestNeedlemanWunsch(TestCase):

    @data(
        ['ACGCATCA', 'ACTGATTCA', 2, -3, -2,
            [[  0,  -2,  -4,  -6,  -8, -10, -12, -14, -16, -18],
             [ -2,   2,   0,  -2,  -4,  -6,  -8, -10, -12, -14],
             [ -4,   0,   4,   2,   0,  -2,  -4,  -6,  -8, -10],
             [ -6,  -2,   2,   1,   4,   2,   0,  -2,  -4,  -6],
             [ -8,  -4,   0,  -1,   2,   1,  -1,  -3,   0,  -2],
             [-10,  -6,  -2,  -3,   0,   4,   2,   0,  -2,   2],
             [-12,  -8,  -4,   0,  -2,   2,   6,   4,   2,   0],
             [-14, -10,  -6,  -2,  -3,   0,   4,   3,   6,   4],
             [-16, -12,  -8,  -4,  -5,  -1,   2,   1,   4,   8],],
        ],
        [
            'CTAAGT', 'CTCGT', 1, 0, 0,
            [[0, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1],
             [0, 1, 2, 2, 2, 2],
             [0, 1, 2, 2, 2, 2],
             [0, 1, 2, 2, 2, 2],
             [0, 1, 2, 2, 3, 3],
             [0, 1, 2, 2, 3, 4],],
        ],
    )
    @unpack
    def test_init_matrix(self, ref_seq, seq, match, mismatch, gap, expect):
        c = nw(ref_seq, match, mismatch, gap)
        c.init_matrix(seq)
        c.cal_score()
        assert np.array_equal(c.m, expect)


    @data(
        [
            'ACGCATCA', 'ACTGATTCA', 2, -3, -2,
            [(8, 8, 9), (6, 7, 8), (4, 6, 7), (6, 6, 6), (4, 5, 5), \
             (2, 4, 4), (4, 3, 4), (2, 2, 3), (4, 2, 2), (2, 1, 1)],
        ],
        [
            'CTAAGT', 'CTCGT', 1, -1, -2,
            [(1, 6, 5), (0, 5, 4), (0, 4, 4), (1, 3, 3), (2, 2, 2), (1, 1, 1)],
        ],
        [
            'CTAAGT', 'CTCGT', 1, 0, 0,
            [(4, 6, 5), (3, 5, 4), (2, 4, 3), (2, 3, 2), (2, 2, 2), (1, 1, 1)],
        ],
    )
    @unpack
    def test_trace_back(self, ref_seq, seq, match, mismatch, gap, expect):
        c = nw(ref_seq, match, mismatch, gap)
        c.init_matrix(seq)
        c.cal_score()
        path = c.trace_back()
        assert path == expect

    @data(
        ['ACGCATCA', 'ACTGATTCA', 7],
        ['CTAAGT', 'CTCGT', 4],
    )
    @unpack
    def test_count_max_matches(self, ref_seq, seq, expect):
        c = nw(ref_seq, 1, 0, 0)
        c.init_matrix(seq)
        c.cal_score()
        res = c.last_score()
        assert res == expect