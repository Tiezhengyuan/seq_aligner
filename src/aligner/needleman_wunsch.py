'''
Needleman-Wunsch algorithm

longest common subsequences

default scores: 
match=1, mismatch=0, gap=-1
'''
import pandas as pd
import numpy as np

class NeedlemanWunsch:
    def __init__(self,
            ref_seq:str,
            match:int=None,
            mismatch:int=None,
            gap:int=None
        ):
        self.ref_seq = ref_seq
        self.ref_len = len(self.ref_seq) + 1
        self.m = None
        # scoring
        self.match = match if match is not None and match > 0 else 1
        self.mismatch = mismatch if mismatch is not None and mismatch <= 0 else 0
        self.gap = gap if gap is not None and gap <= 0 else -1

    def init_matrix(self, seq:str):
        self.seq = seq
        self.seq_len = len(self.seq) + 1
        self.m = np.zeros((self.ref_len, self.seq_len), dtype='int8')
        if self.gap < 0:
            self.m[0, 1:] = np.arange(self.gap, self.gap*self.seq_len, self.gap, dtype='int8')
            self.m[1:, 0] = np.arange(self.gap, self.gap*self.ref_len, self.gap, dtype='int8')
        # print('\n', self.m)
        return self

    def cal_score(self):
        '''
        update self.m
        '''
        for i in range(1, self.ref_len):
            # top = self.m[i-1, 1:] + self.gap
            # s = np.array([self.match if self.ref_seq[i-1]==j else self.mismatch for j in self.seq])
            # diag = np.add(self.m[i-1, :-1], s)
            for j in range(1, self.seq_len):
                top = self.m[i-1, j] + self.gap
                s = self.match if self.ref_seq[i-1] == self.seq[j-1] else self.mismatch
                diag = self.m[i-1, j-1] + s
                left = self.m[i, j-1] + self.gap
                self.m[i,j] = max([top, diag, left])

    
    def trace_back(self, pool:list=None, next_point=None) -> int:
        if pool is None:
            pool = []
        if next_point is None:
            i, j = self.m.shape[0] - 1, self.m.shape[1] - 1
            next_point = (self.m[i, j], i, j)
        
        #check current point
        i, j = next_point[1], next_point[2]
        if i==0 and j == 0:
            return pool
        pool.append(next_point)

        # move
        next = []
        if i > 0 and j > 0:
            diag = (self.m[i-1, j-1], i-1, j-1)
            next = [diag,]
        if i > 0:
            top = (self.m[i-1, j], i-1, j)
            if next and top[0] > next[0][0]:
                next = [top,]    
        if j > 0:
            left = (self.m[i, j-1], i, j-1)
            if next and left[0] > next[0][0]:
                next = [left,]

        for next_point in next:
            return self.trace_back(pool, next_point)

    def print_path(self, path):
        df = pd.DataFrame(self.m[1:, 1:], index=list(self.ref_seq), \
            columns=list(self.seq), dtype='int8')
        print('\n', df)
        print(path)

    def last_score(self):
        '''
        count maximum matches
        match =0 , mismatch/gap=0
        '''
        i, j = self.m.shape[0] - 1, self.m.shape[1] - 1
        return self.m[i, j]