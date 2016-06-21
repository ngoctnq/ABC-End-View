#!/usr/bin/env python2
''' A matrix representation of ABC Endview puzzle.
	Ngoc Tran - 2016 || underlandian.com

	Formatting of the board:
	- board[i][j] denotes the i-th row, j-th column, zero-based.
	- constraint[i] denotes the constraints on the border,
		0, 1, 2, 3 are top, bottom, left, right, respectively.
	- A, B, C, and so on, are unique prime numbers. X is 1. No constraint is 0.
	'''

# execution flags
logging = True

# List of primes, cached for easy access - except for the first entry.
# Note: can be replaced by a lazy-evaluation Lisp-style list.
primes = [1,2,3,5,7,11,13,17,19,23,29]

# INITIALIZATION SECTION
# __________

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
	board is a 2-dimensional nested list, with 0 denotes empty,
		1 denotes X, and so on, as noted in primes.
	'''
def generate_empty_board(dim):
	# initialize new board
	new_board = []
	# prevent internal caching
	for i in range(dim):
		new_row = []
		for j in range(dim):
			# append a new column
			new_row.append(0)
		new_board.append(new_row)
	return new_board

''' Initialize the requirement equations with given constraint.
	Note: skip ones with no constraints.

	board and constraint are nested list of integers.
	choices denote the length of possible character.
		e.g.: 3 means A, B, and C; or equivalently, 2, 3, and 5.
	diag denotes if the board has to have diagonals.
	'''
# implementation note: something better than a nested list is good,
# 	but unfortunately lists aren't hashable, and editability is required.
def generate_equation_list(board, constraint, choices, diag):
	equation_list = []
	# dimension of the board
	dim = len(board[0])
	# maximum amount of X's per row/column
	max_x = dim - choices

	# columns
	for i in range(dim):
		new_equation = generate_empty_equation()
		for j in range(dim):
			# members are list of coordinates
			new_equation[0].append([j,i])
		for j in range(choices):
			new_equation[1].append(primes[j+1])
		equation_list.append(new_equation)

	# rows
	for i in range(dim):
		new_equation = generate_empty_equation()
		for j in range(dim):
			# members are list of coordinates
			new_equation[0].append([i,j])
		for j in range(choices):
			new_equation[1].append(primes[j+1])
		equation_list.append(new_equation)

	# diagonals
	if diag:
		# main diagonal
		new_equation = generate_empty_equation()
		for i in range(dim):
			# members are list of coordinates
			new_equation[0].append([i,i])
		for i in range(choices):
			new_equation[1].append(primes[j+1])
		equation_list.append(new_equation)

		# anti-diagonal
		new_equation = generate_empty_equation()
		for i in range(dim):
			# members are list of coordinates
			new_equation[0].append([i,dim-1-i])
		for i in range(choices):
			new_equation[1].append(primes[j+1])
		equation_list.append(new_equation)

	# top constraint
	constraint_list = constraint[0]
	for i in range(dim):
		if constraint_list[i] == 0:
			continue
		new_equation = generate_empty_equation()
		new_equation[0].append(constraint_list[i])
		for j in range(max_x + 1):
			new_equation[0].append([j,i])
		new_equation[1].append(0)
		equation_list.append(new_equation)

	# bottom constraint
	constraint_list = constraint[1]
	for i in range(dim):
		if constraint_list[i] == 0:
			continue
		new_equation = generate_empty_equation()
		new_equation[0].append(constraint_list[i])
		for j in range(max_x + 1):
			new_equation[0].append([dim-1-j,i])
		new_equation[1].append(0)
		equation_list.append(new_equation)

	# left constraint
	constraint_list = constraint[2]
	for i in range(dim):
		if constraint_list[i] == 0:
			continue
		new_equation = generate_empty_equation()
		new_equation[0].append(constraint_list[i])
		for j in range(max_x + 1):
			new_equation[0].append([i,j])
		new_equation[1].append(0)
		equation_list.append(new_equation)

	# right constraint
	constraint_list = constraint[3]
	for i in range(dim):
		if constraint_list[i] == 0:
			continue
		new_equation = generate_empty_equation()
		new_equation[0].append(constraint_list[i])
		for j in range(max_x + 1):
			new_equation[0].append([i,dim-1-j])
		new_equation[1].append(0)
		equation_list.append(new_equation)

	return equation_list

# CONSTRAINT REDUCTION SECTION
# __________

''' New mulitiplication algorithm.
	TODO: prove ring-ness or whatever. Probably will never get used.
	'''
def multiply(i, j):
	if i == j:
		if i in primes and i != 1:
			return 0
	return i * j

''' Check for obvious fills or unsolvable equations.
	Returns whether anything is changed.
	'''
def equation_list_check(board, equation_list):
	changed = False
	for constraint_equation in equation_list:
		# Border constraint
		if constraint_equation[1] == [0]:
			# unsolvable
			if len(constraint_equation[0]) == 1:
				equation_list[:] = [[[],[-1]]]
				return True
			if len(constraint_equation[0]) == 2:
				coord = constraint_equation[0][1]
				board[coord[0]][coord[1]] = constraint_equation[0][0]
				changed = True
				if logging:
					print 'filling', coord[0], coord[1],
					print int_to_char(constraint_equation[0][0])
		# Latin constraint
		else:
			if len(constraint_equation[1]) == 0:
				for coord in constraint_equation[0]:
					board[coord[0]][coord[1]] = 1
					if logging:
						print 'filling', coord[0], coord[1], 'X'
				changed = True
	return changed

''' Run constraint reduction on all equations which is in the list.
	Empty list means board is all filled.

	Status ints:
		+1 = satisfied
		+0 = unsatisfied
		-1 = invalid

	If constraint_list[0] is [],[-1],
		then the board is impossible. This is to help trial and error.
	'''
def equation_list_reduction(board, equation_list):
	if logging:
		print 'change detected, running equation_list_reduction'
	for constraint_equation in equation_list:
		status = equation_reduction(board, constraint_equation)
		if status == 1:
			del equation_list[equation_list.index(constraint_equation)]
		elif status == -1:
			print 'WARNING: rare case -bug?- impossible Latin constraint'
			equation_list[:] = [[[],[-1]]]
			break

''' Evaluate constraint reduction on each constraint equation.
	If both sides are equal, return True.
	Else, divides into border constraints and Latin constraints:
	- If border constraint (list of primes):
		Anything after a label different from constraint is negligible.
	- If Latin constraint (0 in result):
		Order does not matter.
	'''
def equation_reduction(board, constraint_equation):
	# Border constraint
	if constraint_equation[1] == [0]:
		for coord in constraint_equation[0][1:]:
			repeat = False
			if board[coord[0]][coord[1]] != 0:
				label_value = board[coord[0]][coord[1]]
				coord_index = constraint_equation[0].index(coord)
				if label_value == 1:
					del constraint_equation[0][coord_index]
					repeat = True
				# constraint satisfied
				elif label_value == constraint_equation[0][0]:
					return 1
				else:
					del constraint_equation[0][coord_index:]
				if coord_index + 1 == len(constraint_equation[0]):
					repeat = False
			# if something is removed, redo that index
			while repeat:
				repeat = False
				coord = constraint_equation[0][coord_index]
				if board[coord[0]][coord[1]] != 0:
					label_value = board[coord[0]][coord[1]]
					coord_index = constraint_equation[0].index(coord)
					if label_value == 1:
						del constraint_equation[0][coord_index]
						repeat = True
					# constraint satisfied
					elif label_value == constraint_equation[0][0]:
						return 1
					else:
						del constraint_equation[0][coord_index:]
					if coord_index + 1 == len(constraint_equation[0]):
						repeat = False
	# Latin constraint
	else:
		# if all Latin constraints are met
		if len(constraint_equation[1]) == 0:
			return 1
		for coord in constraint_equation[0]:
			repeat = False
			if board[coord[0]][coord[1]] != 0:
				label_value = board[coord[0]][coord[1]]
				coord_index = constraint_equation[0].index(coord)
				# if label is not in final product - very unlikely to happen
				if label_value in constraint_equation[1]:
					repeat = True
					del constraint_equation[0][coord_index]
					if label_value != 1:
						del constraint_equation[1] \
							[constraint_equation[1].index(label_value)]
					else:
						return -1
				if coord_index + 1 == len(constraint_equation[0]):
					repeat = False
			while repeat:
				repeat = False
				coord = constraint_equation[0][coord_index]
				if board[coord[0]][coord[1]] != 0:
					label_value = board[coord[0]][coord[1]]
					coord_index = constraint_equation[0].index(coord)
					# if label is not in final product - very unlikely to happen
					if label_value in constraint_equation[1]:
						repeat = True
						del constraint_equation[0][coord_index]
						if label_value != 1:
							del constraint_equation[1] \
								[constraint_equation[1].index(label_value)]
						else:
							return -1
					if coord_index + 1 == len(constraint_equation[0]):
						repeat = False
	return 0

# PRINTING SECTION
# __________

''' Return one horizontal border.
	Used in printOut.
	'''
def generate_horizontal_border(dim):
    hBorder = '  '
    for i in range(dim):
        hBorder += '+-'
        hBorder += '-'
        hBorder += '-'
    hBorder += '+'
    return hBorder

''' Return int to char.
	e.g., -1 is blank, 0 is - (X), 1 is A, and so on.
	'''
def int_to_char(i):
	if i > 1:
		return chr(ord('A') + primes.index(i) - 1)
	elif i == 1:
		return '-'
	elif i == 0:
		return ' '
	else:
		raise ValueError(str(i) + ' is not a valid int for a label')

''' Return a pretty printing the board.
	Reliant on '\n', be careful.
	'''
def stringify(board, constraint = None):
    dim = len(board)
    ret = ''
    horizontal_border = generate_horizontal_border(dim)
    if constraint == None:
        constraint = [[],[],[],[]]
        for i in range(dim):
            constraint[0].append(0)
            constraint[1].append(0)
            constraint[2].append(0)
            constraint[3].append(0)
    ret += '    '

    # top constraint
    for i in range(dim):
    	ret += int_to_char(constraint[0][i])
        ret += '   '
    ret += '\n'

    for i in range(dim):
        ret += horizontal_border
        ret += '\n'
        # left constraint
        ret += int_to_char(constraint[2][i])
        ret += ' '
        # board content
        for j in range(dim):
            ret += '| '
            ret += int_to_char(board[i][j])
            ret += ' '
        ret += '| '
        # right constraint
        ret += int_to_char(constraint[3][i])
        ret += '\n'
    ret += horizontal_border
    ret += '\n'
    ret += '    '

    # bottom constraint
    for i in range(dim):
    	ret += int_to_char(constraint[1][i])
        ret += '   '
    return ret

# WORK IN PROGRESS // TESTING SECTION
def shabby_printing(board, constraint, equation_list):
	print '\n'
	print '_'*50
	print 
	print stringify(board, constraint)
	print
	for i in equation_list:
		print i
	print

if __name__ == '__main__':
	dim = 4
	board = generate_empty_board(dim)
	constraint = [
		[0,0,2,0],
		[0,0,0,3],
		[0,3,0,0],
		[0,0,0,2]]
	equation_list = generate_equation_list(board, constraint, 2, False)
	shabby_printing(board, constraint, equation_list)

	equation_list[8][0][2:] = []
	equation_list[10][0][1:3] = []

	while True:
		if equation_list_check(board, equation_list) and \
				equation_list_reduction(board, equation_list) is None:
			shabby_printing(board, constraint, equation_list)
		else:
			break