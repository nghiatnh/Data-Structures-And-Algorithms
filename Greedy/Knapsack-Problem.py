from random import random
from time import time
from typing import *


class Knapsack:
    '''
    Knapsack Problem
    --------------

    Find maximum cost and items for 0/1 Single Knapsack Problem using Greedy Algorithm
    '''
    def __init__(self) -> None:
        self.optimized_cost = 0
        self.optimized_result = []
        
    def solve(self, C : int, W : List[int], P : List[int]) -> Tuple[int, List[int]]:
        n = len(W)

        self.optimized_cost = 0
        self.optimized_result = [0 for x in range(n)]

        # Sort indexes of W and P base on P[i] / W[i]
        indexes = [x for x in range(n)]
        indexes.sort(key=lambda x: P[x] / W[x])

        sumW = 0
        for i in range(n):
            if W[indexes[i]] <= C - sumW:
                self.optimized_cost += P[indexes[i]]
                sumW += W[indexes[i]]
                self.optimized_result[indexes[i]] = 1

        return (self.optimized_cost, self.optimized_result)

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