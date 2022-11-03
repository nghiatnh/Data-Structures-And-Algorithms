from random import random
from time import time


class Knapsack:
    '''
    Unbounded Knapsack Problem
    '''
    def __init__(self) -> None:
        self.optimized_result = []
        
    def solve(self, C, W, P) -> int:
        for i in range(C + 1):
            if i == 0:
                self.optimized_result.append(0)
                continue
            self.optimized_result.append(max([self.optimized_result[i - W[j]] + P[j] if i >= W[j] else 0 for j in range(len(W))]))
        return self.optimized_result[-1]

knapsack = Knapsack()
W = [int(random() * 100) + 1 for x in range(10)]
W.sort()
P = [int(random() * 100) for x in range(10)]
P.sort()
print("W = ", W)
print("P = ", P)
C = 100
t1 = time()
print("Optimized cost: ", knapsack.solve(C, W, P))
t2 = time()
print("Execution time with C = {0}: {1} seconds".format(C, t2 - t1))
C = 1000
t1 = time()
print("Optimized cost: ", knapsack.solve(C, W, P))
t2 = time()
print("Execution time with C = {0}: {1} seconds".format(C, t2 - t1))
C = 1000000
t1 = time()
print("Optimized cost: ", knapsack.solve(C, W, P))
t2 = time()
print("Execution time with C = {0}: {1} seconds".format(C, t2 - t1))