from .helper import *
from src.aligner import IterateSeq
@ddt
class TestIterateSeq(TestCase):
    @data(
        ['ATGCGA', 3, None, ['ATG', 'TGC', 'GCG', 'CGA']],
        ['ATG', -3, None, ['A', 'T', 'G']],
        ['ATGCGA', 3, 1, ['TGC', 'GCG', 'CGA']],
    )
    @unpack
    def test_kmers(self, seq, k, start, expect):
        res = IterateSeq(seq).kmers(k, start)
        assert list(res) == expect

    @data(
        ['ATGC', ['$', 'A$', 'AT$', 'ATG$', 'ATGC$']],
    )
    @unpack
    def test_prefix(self, seq, expect):
        res = IterateSeq(seq).prefix()
        assert list(res) == expect

    @data(
        ['ATGC', [('$', 4), ('C$', 3), ('GC$', 2), ('TGC$', 1), ('ATGC$', 0)]],
    )
    @unpack
    def test_surfix(self, seq, expect):
        res = IterateSeq(seq).surfix()
        assert list(res) == expect
        