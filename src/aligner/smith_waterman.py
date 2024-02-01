'''
local alignment: Smith-Waterman algorithm
detect all matched sub-sequences
'''
import pandas as pd
import numpy as np

class SmithWaterman:
    def __init__(self, ref_seq, match, mismatch, gap):
        self.ref_seq = ref_seq
        self.ref_len = len(ref_seq) + 1
        self.seq = None
        self.m = None
        # could be multiple subseq
        self.max_score = 0
        self.pool = []
        self.last_point = []
        self.match = match if match else 1
        self.mismatch = mismatch if mismatch else -1
        self.gap = gap if gap else -2
    
    def init_matrix(self, seq:str):
        self.seq = seq
        self.seq_len = len(seq) + 1
        self.m = np.zeros((self.ref_len, self.seq_len), dtype='int8')
        self.m[0, 1:] = np.arange(self.gap, self.seq_len*self.gap, self.gap, dtype='int8')
        self.m[1:, 0] = np.arange(self.gap, self.ref_len*self.gap, self.gap, dtype='int8')
    
    def cal_score(self):
        for i in range(1, self.ref_len):
            for j in range(1, self.seq_len):
                top = self.m[i-1, j] + self.gap
                s = self.match if self.ref_seq[i-1] == self.seq[j-1] else self.mismatch
                diag = self.m[i-1, j-1] + s
                left = self.m[i, j-1] + self.gap
                self.m[i, j] = np.max([top, diag, left, 0])
                if self.m[i,j] > self.max_score:
                    self.max_score = self.m[i, j]
                    self.last_point = [(i, j),]
                elif self.m[i,j] == self.max_score:
                    self.last_point.append((i, j))
    
    def traces(self):
        paths = []
        for i, j in self.last_point:
            next_point, path = (self.m[i, j], i, j), []
            self.trace_back(next_point, path)
            if path:
                paths.append(path)
        return paths

    def trace_back(self, next_point, path):
        # add point
        if next_point[0] == 0 or (path and next_point[0] > path[-1][0]):
            return path
        path.append(next_point)

        # 
        next = []
        i, j = next_point[1], next_point[2]
        if i > 1 and j > 1 :
            diag = (self.m[i-1, j-1], i-1, j-1)
            next = [diag,]
        if i > 1:
            top = (self.m[i-1, j], i-1, j)
            if not next or (next and self.m[i-1, j] > next[0][0]):
                next = [top,]
        if j > 1:
            left = (self.m[i, j-1], i, j-1)
            if not next or (next and self.m[i,j-1] > next[0][0]):
                next = [left,]

        for next_point in next:
            return self.trace_back(next_point, path)



