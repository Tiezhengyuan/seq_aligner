'''
'''

import numpy as np

class DotMatrix:
    def __init__(self, ref_seq:str):
        self.ref_seq = ref_seq
        self.ref_len = len(ref_seq)
        self.m = None
    
    def build(self, seq:str):
        self.seq = seq
        self.seq_len = len(seq)

        # build matrix: ref_seq is in rows
        self.m = np.zeros((self.ref_len, self.seq_len), dtype='int8')
        for i in range(0, self.ref_len):
            s1 = self.ref_seq[i]
            self.m[i] = [s1 == s2 for s2 in self.seq]
        return self.m

    def is_identical(self, seq:str):
        '''
        check if two sequences are identical
        Note: length of seq >= ref_seq
        '''
        self.build(seq)
        diag = np.diagonal(self.m)
        return sum(diag) == self.ref_len
    
    def is_reversion(self, seq:str=None):
        '''
        check if two sequences are reverse to each other
        Note: length of seq >= ref_seq
        '''
        if seq is None:
            self.build(self.ref_seq)
        else:
            self.build(seq[::-1])
        diag = np.diagonal(self.m)
        return sum(diag) == self.ref_len

    def detect_repeats(self, min_len:int=None):
        '''
        repeat region
        example: TTTT in GATTTTCAG
        '''
        if min_len is None:
            min_len = 3
        self.build(self.ref_seq)
        pool = []
        for i in range(0, self.ref_len):
            pass
    
    def repeat(self, i:int, j:int):
        if self.m[i, j]:
            pass
    


