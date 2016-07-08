#!/usr/bin/env python2
from utils import *
from utils_janko import *
# from utils_matrix import *
from gentest import *

# from utils_nextgen import *
import random

# from distutils.core import setup
# import py2exe

''' Test file.
		put stuff to run here
	'''

# matrix_test()
print board_generator(4,2,0, test = False)
# solver_janko(77)

def compare_with_anna():
	f = open('ignore_this/failedPuzzlesData.csv', 'r')
	lst = f.readlines()
	del lst[0]
	# 480 is impossible
	del lst[-1]
	for i in range(len(lst)):
		lst[i] = lst[i].split(',')
	for i in range(len(lst)):
		no = int(lst[i][0])
		board, constraint, choices, diag = \
			janko_parser(janko_get_text(no))
		solution_list, trials = solve(board, constraint, choices, diag)
		if trials > 0:
			print no, trials

def test_generate(dim, choices, diag, clue_count, freq = None):
	satisfied = False
	choices = choices.upper()
	len_choices = len(choices)
	if dim > len(choices):
		choices += 'X'
	while not satisfied:
		clue_count_2 = clue_count
		board = generate_empty_board(dim)
		constraint = generate_empty_constraint(dim)
		populate_empty_board(board, choices)

		unfilled_clues = []
		for i in range(4):
			for j in range(dim):
				unfilled_clues.append([i,j])
		if freq is None:
			while clue_count_2 > 0:
				c = choices[random.randrange(len_choices)]
				idx = random.randrange(len(unfilled_clues))
				c_idx = unfilled_clues[idx]
				constraint[c_idx[0]][c_idx[1]] = c
				del unfilled_clues[idx]
				clue_count_2 -= 1
		else:
			raise NotImplementedError()
		convert_to_family_generator(board, constraint, choices)
		satisfied = not solve(board, constraint, choices, diag, True)
		sys.stdout.write('.')
	print '\nfound one!\n'
	print stringify(board, constraint)

# test_generate(4, 'ab', False, 6)

# setup(options = {
#         "py2exe": {
#             "dll_excludes": ["MSVCP90.dll"]
#         }
#     },
#     console=['utils_gui.py'])