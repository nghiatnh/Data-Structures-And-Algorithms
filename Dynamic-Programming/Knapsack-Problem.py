from random import random
from time import time
from typing import *


class Knapsack:
    '''
    Knapsack Problem
    --------------

    Find maximum cost and items for 0/1 Single Knapsack Problem
    '''
    def __init__(self) -> None:
        self.optimized_cost = []
        self.optimized_result = []
        
    def solve(self, C : int, W : List[int], P : List[int]) -> Tuple[int, List[int]]:
        n = len(W)

        self.optimized_cost = [[0 for x in range(C + 1)] for x in range(n + 1)]
        self.optimized_result = [0 for x in range(n)]
 
        # Build table self.optimized_cost[][] in bottom up manner
        for i in range(n + 1):
            for w in range(C + 1):
                if i == 0 or w == 0:
                    self.optimized_cost[i][w] = 0
                elif W[i-1] <= w:
                    self.optimized_cost[i][w] = max(P[i-1]
                            + self.optimized_cost[i-1][w-W[i-1]], 
                                self.optimized_cost[i-1][w])
                else:
                    self.optimized_cost[i][w] = self.optimized_cost[i-1][w]

        # Find items to give optimal result
        i = n
        w = C
        while i > 0:
            if self.optimized_cost[i][w] != self.optimized_cost[i - 1][w]:
                self.optimized_result[i - 1] = 1
                w -= W[i - 1]
                i -= 1
            else:
                i -= 1
        return (self.optimized_cost[n][C], self.optimized_result)

# Testing
knapsack = Knapsack()
W = [int(random() * 100) + 1 for x in range(10)]
W.sort()
P = [int(random() * 100) for x in range(10)]
P.sort()
print("W = ", W)
print("P = ", P)
C = 100
t1 = time()
result = knapsack.solve(C, W, P)
print("Optimized cost: ", result[0])
print("Optimized items: ", result[1])
t2 = time()
print("Execution time with C = {0}: {1} seconds".format(C, t2 - t1))
C = 1000
t1 = time()
result = knapsack.solve(C, W, P)
print("Optimized cost: ", result[0])
print("Optimized items: ", result[1])
t2 = time()
print("Execution time with C = {0}: {1} seconds".format(C, t2 - t1))
C = 1000000
t1 = time()
result = knapsack.solve(C, W, P)
print("Optimized cost: ", result[0])
print("Optimized items: ", result[1])
t2 = time()
print("Execution time with C = {0}: {1} seconds".format(C, t2 - t1))