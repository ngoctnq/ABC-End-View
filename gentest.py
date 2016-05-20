#!/usr/bin/env python
from utils import *
import matplotlib.pyplot as plt

def test(dim = 5, length_of_choices = 3, bool_int = 0, criteria = has_unique_solution):
    # criteria = solvable_without_trials
    # criteria = has_unique_solution

    # constraint = [[],[]]
    # for i in range(dim):
    #     constraint[0].append(['',''])
    #     constraint[1].append(['',''])

    generation_count = 0
    if bool_int == 0: 
        diag = False
    else:
        diag = True
    choices_no_x = ''
    for i in range(length_of_choices):
        choices_no_x += chr(ord('A')+i)
    choices = choices_no_x + 'X'
    board = generate(dim, choices_no_x, diag)

    # fullX = init_board(constraint, choices, diag)
    # reset_board(fullX)
    # while not equal(board, fullX):
    #     board = generate(dim, choices_no_x, diag)
    # printOut(board)

    generation_count += 1
    constraint = generate_constraint(board)
    while not has_unique_solution(constraint, choices, diag):
        board = generate(dim, choices_no_x, diag)
        # printOut(board)
        generation_count += 1
        constraint = generate_constraint(board)
    reduce_constraints(constraint, choices, diag, criteria)
    # printOut(init_board(constraint, choices, diag), constraint)
    printOut(board, constraint)
    print "--- after generating", generation_count, "trials"
    # return generation_count

if __name__ == "__main__":
    # data = []
    # for i in range(100):
    #     print i
    #     data.append(test(5,4))
    # data.sort()
    # print data
    test(6,5,0)
