from fractions import Fraction
from pprint import pprint
import numpy as np
import math
'''
7
5
-21/24 -9/24 -12/24 0 0 0 0 0
1 1/2 3/4 1 0 0 0 60000
1 0 0 0 1 0 0 48000
0 1 0 0 0 1 0 120000
0 0 1 0 0 0 1 144000

'''


def ratio_test(col, rhs_col):
    min_i = -1
    min_val = 100000000000

    for i in range(len(col)):
        if i == 0:  # skip z row
            continue

        if col[i] > 0 and rhs_col[i] / col[i] < min_val:
            min_val = rhs_col[i] / col[i]
            min_i = i

    if min_val == 100000000000:
        raise ValueError("Unbounded")

    return min_i


def next_iteration(A):
    m = A.shape[1]  # number of columns

    min_j = -1
    min_val = 10000000000
    for j in range(m-1):  # choose the most negative coefficient in z row, excluding the RHS column
        if A[0][j] < min_val:
            min_val = A[0][j]
            min_j = j

    min_i = ratio_test(A[:, min_j], A[:, m-1])

    return min_j, min_i


if __name__ == '__main__':
    automatic = True

    n = int(input("Number of variables: "))
    m = int(input("Number of equations: "))
    A = np.empty(shape=(m, n+1), dtype=Fraction)  # + 1 for solution column
    num_rows, num_columns = A.shape

    for i in range(m):
        line = input()

        j = 0
        for s in line.split():
            try:
                A[i][j] = Fraction(s)
                j += 1
            except ValueError:
                print(f"Could not parse \"{s} , i = {i}, j = {j}")
                exit(0)

    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in A]))

    pivot_column, pivot_row = next_iteration(A)
    while A[0][pivot_column] < 0:
        print(f"Variable {pivot_column} enters, {pivot_row-1} leaves\n")
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

        print('----------------------------------------------------------------')
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in A]))
        pivot_column, pivot_row = next_iteration(A)




