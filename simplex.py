from fractions import Fraction
from pprint import pprint
import numpy as np
import math

automatic = False
maximization = False
minimization = not maximization
'''
-5	-4	0	0	0	0	0
6	4	1	0	0	0	24
1	2	0	1	0	0	6
-1	1	0	0	1	0	1
0	1	0	0	0	1	2

'''

'''
7
4
-3 -2 -1 0 0 0 0
-3 -1 -1 1 0 0 -3
3 -3 -1 0 1 0 -6
1 1 1 0 0 1 3
'''
'''
7
3
3 2 -1 0 1 0 5
'''


def pretty_print(A):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in A]))


# used to determine entering variable in dual simples
def optimality_ratio_test(row, z_row):
    m = len(z_row)

    best_j = -1
    best_j_val = 100000

    for j in range(m-1):  # m-1 to avoid the RHS column

        if row[j] >= 0:
            continue

        if abs(z_row[j] / row[j]) < best_j_val:
            best_j_val = abs(z_row[j] / row[j])
            best_j = j

    if best_j == -1:
        raise ValueError("No feasible solution")

    return best_j


# used to determine leaving variable in simplex
def feasibility_ratio_test(col, rhs_col):
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


# Pivot_column enters. pivot_row exits
def row_operation(A, pivot_row, pivot_column):
    print(f"Variable {pivot_column} enters, {pivot_row-1} leaves\n")
    num_rows, num_columns = A.shape

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


# improves optimality
# returns -1 if solution is optimal (all z-row coefficients positive in the case of maximization)
# Throws an error if the problem is unbounded
def optimality_iteration(A):
    n, m = A.shape

    # choose which variable to enter (pivot column)
    best_reduced_cost = 100000 if maximization else -100000
    pivot_column = -1

    for j in range(m-1):  # j < m-1 to skip RHS column
        print(A[0][j])
        if (maximization and A[0][j] < best_reduced_cost)\
                or (minimization and A[0][j] > best_reduced_cost):
            pivot_column = j
            best_reduced_cost = A[0][j]

    if (maximization and best_reduced_cost >= 0) or\
            (minimization and best_reduced_cost <= 0):
        print("Optimality Reached")
        return -1

    pivot_row = feasibility_ratio_test(A[:, pivot_column], A[:, m-1])
    row_operation(A, pivot_row, pivot_column)


# improves feasibility
# returns -1 if solution is feasible (all rhs values are positive)
# Throws an error if the problem is infeasible (all coefficients in the pivot are row non-negative)
def feasibility_iteration(A):
    n, m = A.shape
    # choose an infeasible variable to leave (pivot row)
    best_rhs = 1000000
    pivot_row = -1
    for i in range(n):
        if i == 0:  # skip z row
            continue

        if A[i][m-1] < best_rhs:
            pivot_row = i
            best_rhs = A[i][m-1]

    if pivot_row == -1:
        print("Feasibility achieved")
        return -1

    pivot_column = optimality_ratio_test(A[pivot_row, :], A[0, :])
    row_operation(A, pivot_row, pivot_column)


if __name__ == '__main__':

    n = int(input("Number of columns (including RHS column): "))
    m = int(input("Number of rows: "))
    A = np.empty(shape=(m, n), dtype=Fraction)
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

    while feasibility_iteration(A) != -1:
        pretty_print(A)

    while optimality_iteration(A) != -1:
        pretty_print(A)
    '''if ~automatic:
        while True:
            pivot_column = int(input("Enter entering var index: "))  # pivot column
            pivot_row = int(input("Enter leaving equation index: "))    # pivot row
            row_operation(A, pivot_row, pivot_column)

    else:
        pivot_column, pivot_row = next_iteration(A)
        while A[0][pivot_column] < 0:
            row_operation(A, pivot_row, pivot_column)
            pivot_column, pivot_row = next_iteration(A)'''




