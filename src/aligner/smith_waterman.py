'''
'''
import pandas as pd
import numpy as np

class SmithWaterman:
    def __init__(self, ref_seq, match, mismatch, gap):
        self.ref_seq = ref_seq
        self.ref_len = len(ref_seq) + 1
        self.seq = None
        self.m = None
        self.last_i, self.last_j = 0, 0
        self.match = match if match else 1
        self.mismatch = mismatch if mismatch else -1
        self.gap = gap if gap else -2
    
    def init_matrix(self, seq:str):
        self.seq = seq
        self.seq_len = len(seq) + 1
        self.m = np.zeros((self.ref_len, self.seq_len), dtype='int8')
        self.m[0, 1:] = np.arange(self.gap, self.seq_len*self.gap, self.gap, dtype='int8')
        self.m[1:, 0] = np.arange(self.gap, self.ref_len*self.gap, self.gap, dtype='int8')
        # print(self.m)
    
    def cal_score(self):
        for i in range(1, self.ref_len):
            for j in range(1, self.seq_len):
                top = self.m[i-1, j] + self.gap
                s = self.match if self.ref_seq[i-1] == self.seq[j-1] else self.mismatch
                diag = self.m[i-1, j-1] + s
                left = self.m[i, j-1] + self.gap
                self.m[i, j] = np.max([top, diag, left, 0])
                if self.m[i,j] >= self.m[self.last_i, self.last_j]:
                    self.last_i = i
                    self.last_j = j
    



