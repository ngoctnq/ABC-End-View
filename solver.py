#!/usr/bin/env python2
from utils import *
from timeit import default_timer

# params: rows/columns, count, head/tail
# problem 209
# constraint = [[['A',''],['C','D'],['A',''],['','C'],['E',''],['','E'],['E','']],
#                [['A',''],['','A'],['B',''],['','B'],['','B'],['C','D'],['B','']]]
# choices = 'ABCDE'

# problem 3
# constraint = [[['',''],['',''],['A','']],[['','B'],['',''],['','']]]
# choices = 'AB'

# problem 176
# constraint = [[['A',''],['','A'],['D',''],['',''],['','E'],['',''],],
#                [['','E'],['','B'],['E',''],['','D'],['C',''],['','C']]]
# choices = 'ABCDE'

# last problem of the month
# constraint = [[['',''], ['B',''], ['A',''], ['B',''], ['D','B'], ['B','A'], ['',''], ['','']],
#              [['D','B'], ['C','D'], ['','B'], ['C','D'], ['',''], ['C','B'], ['',''], ['','D']]]
# choices = 'ABCD'

# problem 77
# constraint = [[['F','C'], ['',''], ['A','C'], ['','D'], ['D','B'], ['D','B'], ['B','F'], ['','']],
#               [['','A'], ['',''], ['E','F'], ['D',''], ['F','E'], ['D','F'], ['','B'], ['','']]]
# choices = 'ABCDEF'

# problem 480
constraint = [[['B', 'C'], ['G', 'A'], ['A', 'E'], ['F', 'D'], ['C', 'B'], ['E', 'C'], ['D', 'F'], ['D', 'G']], [['', 'D'], ['G', 'F'], ['F', 'E'], ['D', 'B'], ['', ''], ['', 'C'], ['F', 'A'], ['C', 'G']]]
choices = 'ABCDEFG'

choices += 'X'
dim = len(constraint[0])
diag = False

def main():
    printOut(init_board(constraint, choices, diag))
    result = solve(constraint, choices, diag)
    solutions_list = result[0]
    counts = result[1]
    for i in range(len(solutions_list)):
        print 'Solution #'+str(i+1)+"\n"
        printOut(solutions_list[i], constraint)
        print
    print "total number of solutions:", len(solutions_list)
    print "total number of trials:", counts[0]
    print "total number of expansions:", counts[1]

def test(main):
    tic = default_timer()
    # insert code to test here
    main()
    # end of code insertion
    toc = default_timer()
    print "time taken in seconds:", toc-tic

def check_if_sln_exists(dim = 8, choices = 'ABCDEFX'):
    constraint = empty_constraint(dim)
    board = init_board(constraint, choices, diag)
    solutions_list = solve(constraint, choices, diag, True)[0]
    printOut(solutions_list[0])

is_input = False
# GUI to input problem
if is_input is True:
    solver()
else:
    # solving it
    # main()
    # test(check_if_sln_exists)
    test(main)
