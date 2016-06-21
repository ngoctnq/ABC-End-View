#!/usr/bin/env python2

# A matrix representation of ABC Endview puzzle
# Ngoc Tran - 2016 || underlandian.com

# Formatting of the board:
# - board[i][j] denotes the i-th row, j-th column, zero-based.
# - constraint[i] denotes the constraints on the border,
# 	0, 1, 2, 3 are top, bottom, left, right, respectively.
# - A, B, C, and so on, are unique prime numbers. X is 1. No constraint is 0.

''' List of primes, cached for easy access - except for the first entry.
	Note: can be replaced by a lazy-evaluation Lisp-style list.
	'''
primes = [1,2,3,5,7,11,13,17,19,23,29]

''' Generate empty equation.
	Equation has the form [[list_of_members],[list_of_primes]]
	'''
def generate_empty_equation():
	# initialize new equation, [1] is the content, [2] is the result
	new_equation = []
	# prevent internal caching
	for i in range(2):
		new_equation.append([])
	return new_equation

''' Generate empty board.
	board is a 2-dimensional nested list, with -1 denotes empty,
		0 denotes X, and so on.
	'''
def generate_empty_board(dim):
	# initialize new board
	new_board = []
	# prevent internal caching
	for i in range(dim):
		new_board.append([])
	return new_board

''' Initialize the requirement equations with given constraint.
	Note: can skip ones with no constraints, but put anyway - improvement is
		minimal, while harder to understand from scratch.

	board and constraint are nested list of integers.
	choices denote the length of possible character.
		e.g.: 3 means A, B, and C; or equivalently, 2, 3, and 5.
	diag denotes if the board has to have diagonals.
	'''
def generate_equation_list(board, constraint, choices, diag):
	equation_list = []
	# dimension of the board
	dim = len(board[0])
	# columns
	for i in range(dim):
		new_equation = generate_empty_equation()
		equation_list.append(new_equation)
	# rows
	# diagonals
	# top constraint
	return equation_list
