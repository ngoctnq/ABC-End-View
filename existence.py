#!/usr/bin/env python
from utils import *

def test(dim = 6, length_of_choices = 5, bool_int = 1):
    constraint = empty_constraint(dim)
    generation_count = 0
    if bool_int == 0:
        diag = False
    else:
        diag = True
    choices_no_x = ''
    for i in range(length_of_choices):
        choices_no_x += chr(ord('A')+i)
    choices = choices_no_x + 'X'
    board = init_board(constraint, choices, diag)

    to_permute = list(choices + 'X'*(dim - len(choices)))
    random.shuffle(to_permute)
    for i in range(dim):
        board[i][i] = to_permute[i]
    cancel_all(board, constraint, choices, diag)
    mass_optimize(board, constraint, choices, diag)
    new_constraint = []
    for i in range(dim):
        new_constraint.append(board[i][dim-1-i])
    data = sidequest(new_constraint, choices)
    # print data

    pos = random.randrange(len(data))
    for i in range(dim):
        board[i][dim-1-i] = data[pos][i]
    
    printOut(board)

    cancel_all(board, constraint, choices, diag)
    mass_optimize(board, constraint, choices, diag)
    printOut(board)
    print len(solve_from_partial(board, constraint, choices, diag, False)[0])

if __name__ == '__main__':
    test()