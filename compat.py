#!/usr/bin/env python2
from utils import empty_constraint

# convert top-bottom-left-right to the old constraint
def new_to_old_constraint(constraint):
    dim = len(constraint[0])
    new_const = empty_constraint(dim)
    for i in range(dim):
        # left
        new_const[0][i][0] = constraint[2][i]
        # right
        new_const[0][i][1] = constraint[3][i]
        # top
        new_const[1][i][0] = constraint[0][i]
        # bottom
        new_const[1][i][1] = constraint[1][i]
    return new_const

# convert old constraint to top-bottom-left-right
def old_to_new_constraint(constraint):
    dim = len(constraint[0])
    new_constraint = []
    # prevent internal caching
    for i in range(4):
        new_row = []
        for j in range(dim):
            # append a new column
            new_row.append(0)
        new_constraint.append(new_row)
    for i in range(dim):
        # left
        new_constraint[2][i] = constraint[0][i][0]
        # right
        new_constraint[3][i] = constraint[0][i][1]
        # top
        new_constraint[0][i] = constraint[1][i][0]
        # bottom
        new_constraint[1][i] = constraint[1][i][1]
    return new_constraint