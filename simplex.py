from fractions import Fraction
from pprint import pprint
import numpy as np

'''
5
4 
-16 -15 0 0 0 0
40 31 1 0 0 124
-1 1 0 1 0 1
1 0 0 0 1 3

'''

'''
6
4
696 399 -100 0 0 0 900
3 1 0 1 0 0 3
4 3 -1 0 1 0 6
1 2 0 0 0 1 4
'''


if __name__ == '__main__':

    print(Fraction("54/4"))
    n = int(input("Number of variables: "))
    m = int(input("Number of equations: "))
    A = np.empty(shape=(m, n+1), dtype=Fraction)  # + 1 for solution column
    num_rows, num_columns = A.shape

    for i in range(m):
        line = input()

        j = 0
        for s in line.split(" "):
            A[i][j] = Fraction(s)
            j += 1

    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in A]))

    while True:
        pivot_column = int(input("Enter entering var index: "))  # pivot column
        pivot_row = int(input("Enter leaving equation index: "))    # pivot row

        for row in range(num_rows):
            if row == pivot_row:
                # normalize pivot row
                divisor = A[pivot_row][pivot_column]
                for column in range(num_columns):
                    A[row][column] /= divisor

            else:
                # gauss jordan elimination
                factor = Fraction(A[row][pivot_column], A[pivot_row][pivot_column])

                for column in range(num_columns):
                    A[row][column] -= factor * A[pivot_row][column]

        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in A]))



