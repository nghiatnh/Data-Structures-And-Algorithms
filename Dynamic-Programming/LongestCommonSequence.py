class LongestCommonSequence:
    '''
    Longest Common Sequence
    -----------

    Find longest common sequence length and the value of that Sequence using Dynamic Programing
    '''

    def __init__(self) -> None:
        self.optimized_result = []

    def solve(self, A : str, B : str) -> str:
        lenA = len(A)
        lenB = len(B)
        self.optimized_result = [
            [0 for x in range(lenB + 1)] for y in range(lenA + 1)]

        for i in range(lenA + 1):
            for j in range(lenB + 1):
                if i == 0 or j == 0:
                    self.optimized_result[i][j] = 0
                elif A[i - 1] == B[j - 1]:
                    self.optimized_result[i][j] = self.optimized_result[i-1][j-1] + 1
                else:
                    self.optimized_result[i][j] = max(
                        self.optimized_result[i-1][j], self.optimized_result[i][j-1])

        # Trace path
        result = ''
        i = lenA
        j = lenB
        while i > 0 and j > 0:
            if self.optimized_result[i][j] == self.optimized_result[i-1][j]:
                i -= 1
            elif self.optimized_result[i][j] == self.optimized_result[i][j-1]:
                j -= 1
            else:
                result = A[i - 1] + result
                i -= 1
                j -= 1

        return (self.optimized_result[lenA][lenB], result)

# Testing

LCS = LongestCommonSequence()
result = LCS.solve('ABCD', 'ACBDCD')
print('Longest length: {}'.format(result[0]))
print('Longest sequence: {}'.format(result[1]))
