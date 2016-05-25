#!/usr/bin/env python2
from utils import *

def board_generator(dim = 5, length_of_choices = 3, bool_int = 0, \
                    criteria = has_unique_solution, test = False):
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
        print 'retrying... - the',generation_count,'time'
        board = generate(dim, choices_no_x, diag)
        # printOut(board)
        generation_count += 1
        constraint = generate_constraint(board)
        # printOut(board, constraint)
    if not test:
        reduce_constraints(constraint, choices, diag, criteria)
        # printOut(init_board(constraint, choices, diag), constraint)
        printOut(board, constraint)
        print "--- after generating", generation_count, "trials"
    return generation_count

def collision_test(file_name = 'data', file_mode = 'r+'):
    f = open(file_name, file_mode)

    data = []
    for i in range(10000):
        print i
        data.append(test(8,6,0))
    data.sort()
    f.write('8-6-0\n')
    f.write(repr(data))
    f.write('\n\n')

    data = []
    for i in range(10000):
        print i
        data.append(test(8,7,0))
    data.sort()
    f.write('8-7-0\n')
    f.write(repr(data))
    f.write('\n\n')

    data = []
    for i in range(10000):
        print i
        data.append(test(8,6,1))
    data.sort()
    f.write('8-6-1\n')
    f.write(repr(data))
    f.write('\n\n')

    data = []
    for i in range(10000):
        print i
        data.append(test(8,7,1))
    data.sort()
    f.write('8-7-1\n')
    f.write(repr(data))
    f.write('\n\n')

    f.close()

if __name__ == "__main__":
    print board_generator(8,7,0, test = True)
