#!/usr/bin/env python
from utils import *

def test():
    dim = 4
    length_of_choices = 3
    bool_int = 0
    # criteria = solvable_without_trials
    criteria = has_unique_solution

    if bool_int == 0: 
        diag = False
    else:
        diag = True
    choices = ''
    for i in range(length_of_choices):
        choices += chr(ord('A')+i)
    board = generate(dim, choices, diag)
    while (is_ambiguous(board)):
        board = generate(dim, choices, diag)
    printOut(board)
    constraint = generate_constraint(board)
    choices += 'X'
    reduce_constraints(constraint, choices, diag, criteria)
    print constraint
    print init_board(constraint, choices, diag)

if __name__ == "__main__":
    test()
