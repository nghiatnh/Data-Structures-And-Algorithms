from random import random
from time import time
from typing import *
import numpy as np
import queue


class MatrixChainMultiplication:
    '''
    Matrix Chain Multiplication
    --------------

    Find minimum matrix chain multiply operation numbers and the way to multiply them.
    '''

    def __init__(self) -> None:
        self.optimized_result = []


    def solve(self, P: List[List[int]]) -> Tuple[int, List[int]]:
        n = len(P) - 1 # number of matrix

        self.optimized_result = [
            [0 for x in range(n)] for y in range(n)]

        self.optimal_chain = [[[] for x in range(n)] for y in range(n)]

        # Build table self.optimized_result[][] in bottom up manner
        for length in range(1, n + 1):
            for i in range(1, n + 1 - length):
                j = i + length
                if i == j:
                    self.optimized_result[i-1][j-1] = 0
                    self.optimal_chain[i-1][j-1] = [i, j]
                else:
                    k = min([x for x in range(i, j)], 
                    key=lambda k: self.optimized_result[i-1][k-1] + self.optimized_result[k][j-1] + P[i-1]*P[k]*P[j])
                    self.optimized_result[i-1][j-1] = self.optimized_result[i-1][k-1] + self.optimized_result[k][j-1] + P[i-1]*P[k]*P[j]
                    self.optimal_chain[i-1][j-1] = [i,k,j]

        result = []
        q = queue.LifoQueue()
        q.put(self.optimal_chain[0][n-1])
        while q.empty() == False:
            x = q.get()
            if len(x) != 0:
                if len(x) == 2:
                    result.append(list(set(x)))
                    continue

                if x[0] == x[1] - 1 == x[2] - 2:
                    result.append(x)
                elif x[0] >= x[1] - 1 and x[2] == x[1] + 1:
                    q.put(x[1:3])
                elif x[0] >= x[1] - 1 and x[2] > x[1] + 1:
                    q.put(self.optimal_chain[x[1]][x[2] - 1])
                    q.put(x[0:2])
                elif x[0] < x[1] - 1 and x[2] == x[1] + 1:
                    q.put([x[2], x[2]])
                    q.put(self.optimal_chain[x[0] - 1][x[1] - 1])
                else:
                    q.put(self.optimal_chain[x[1]][x[2] - 1])
                    q.put(self.optimal_chain[x[0] - 1][x[1] - 1])

        return (self.optimized_result[0][n-1], result)


# Testing
MCP = MatrixChainMultiplication()

result = MCP.solve([30, 35, 15, 5, 10, 20, 25])
print('The minimum multiplications: {}'.format(np.array(result[0])))
print('The chain of multiplications: {}'.format(result[1]))

