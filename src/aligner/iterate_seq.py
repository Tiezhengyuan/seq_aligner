

from typing import Iterable

class IterateSeq:

    def __init__(self, seq):
        self.seq = seq

    @property
    def seq_len(self):
        return len(self.seq)
    
    def kmers(self, k:int, start:int=None) -> Iterable:
        '''
        k-mers
        '''
        if k < 1: k = 1
        if start is None: start = 0
        for i in range(start, self.seq_len-k+1):
            yield self.seq[i:i+k]
    
    def prefix(self) -> Iterable:
        '''
        prefix + $
        '''
        for i in range(0, self.seq_len + 1):
            yield self.seq[0:i] + '$'

    def surfix(self) -> Iterable:
        '''
        surfix + $
        '''
        for i in range(self.seq_len, -1, -1):
            sub = self.seq[i:self.seq_len] + '$'
            # surfix in key, position in value
            yield (sub, i)