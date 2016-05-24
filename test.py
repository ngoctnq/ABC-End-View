#!/usr/bin/env python
from utils import *
constraint = empty_constraint(5)
choices = 'ABCDX'
diag = False
board = init_board(constraint, choices, diag)
board[0][0] = 'A'
board[0][1] = 'B'
board[0][2] = 'C'
board[0][3] = 'D'
board[0][4] = 'X'
board[1][0] = 'D'
board[2][0] = 'C'
board[3][0] = 'X'
board[1][4] = 'B'
board[2][4] = 'D'
board[3][4] = 'C'
board[4][0] = 'B'
board[4][1] = 'X'
board[4][2] = 'D'
board[4][3] = 'C'
board[4][4] = 'A'
cancel_all(board, constraint, choices, diag)
mass_optimize(board, constraint, choices, diag)
solutions_list = solve_from_partial(board, constraint, choices, diag)[0]
for i in solutions_list:
	printOut(i)