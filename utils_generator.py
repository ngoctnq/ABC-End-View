#!/usr/bin/env python2
from utils_core import *
from utils_input import omni_to_letter
from utils_transform import *
import random
import sys
''' A module generating Endview puzzles.
    Ngoc Tran - 2016 || underlandian.com
    '''

def generate_bogo(dim, choices, diag = False, clue_count = 0):
    ''' Generate a board with clue_count number of clue.
        Random until terminate.
        '''
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
        while clue_count_2 > 0:
            c = choices[random.randrange(len_choices)]
            idx = random.randrange(len(unfilled_clues))
            c_idx = unfilled_clues[idx]
            constraint[c_idx[0]][c_idx[1]] = c
            del unfilled_clues[idx]
            clue_count_2 -= 1
        convert_to_family_generator(board, constraint, choices)
        satisfied = not solve(board, constraint, choices, diag, True)
        sys.stdout.write('.')
    log('\nfound one!\n', GUI)
    log(stringify(board, constraint), GUI)

def generate_prefill(dim, choices, diag = False):
    ''' Generate from a prefilled Latin board. '''
    if type(choices) is type(0):
        no_of_choices = choices
        choices = ''
        for i in range(no_of_choices):
            choices += omni_to_letter(i + 1)
    choices = choices.upper()
    if dim > len(choices):
        choices += 'X'    

    empty_board = generate_empty_board(dim)
    populate_empty_board(empty_board, choices)

    while True:
        board = generate_endview_board(dim, choices, diag)
        constraint = generate_endview_constraint(board)
        if solve(empty_board, constraint, choices, diag, True) == 1:
            break
        else:
            sys.stdout.write('-')

    remaining_constraint = []
    for i in range(4):
        for j in range(dim):
            remaining_constraint.append([i, j])
    while len(remaining_constraint) != 0:
        pos = random.randrange(len(remaining_constraint))
        coord = remaining_constraint[pos]
        x = coord[0]
        y = coord[1]
        backup_val = constraint[x][y]
        del remaining_constraint[pos]
        constraint[x][y] = ''
        no_of_slns = solve(empty_board, constraint, choices, diag, True)
        if no_of_slns == 0:
            raise ValueError('cannot have such constraint with no slns')
        elif no_of_slns == 2:
            constraint[x][y] = backup_val
    return constraint

def generate_endview_board(dim, choices, diag):
    ''' Generate a prefilled Endview board without constraint. 
        Note: do not try to find a diagonal board with dimension 3.
        '''
    board = generate_empty_board(dim)
    constraint = generate_empty_constraint(dim)
    populate_empty_board(board, choices)
    
    if diag:
        # generate main diagonal first
        # not formally proven, but a diagonal board always exist
        to_permute = list(choices + 'X'*(dim - len(choices)))
        random.shuffle(to_permute)
        for i in range(dim):
            board[i][i] = to_permute[i]
    
    while True:
        no_of_slns = solve(board, constraint, choices, diag, True)
        if no_of_slns == 0:
            sys.stdout.write('.')
            return generate_endview_board(dim, choices, diag)
        elif no_of_slns == 1:
            solutions_list, trials = solve(board, constraint, choices, diag)
            return solutions_list[0]
        else:
            partially_solved = solve(board, constraint, choices, diag, no_trials = True)
            while True:
                x = random.randrange(dim)
                y = random.randrange(dim)
                if len(partially_solved[x][y]) > 1:
                    break
            possible_choices = list(partially_solved[x][y])
            while True:
                if len(possible_choices) == 0:
                    sys.stdout.write('.')
                    return generate_endview_board(dim, choices, diag)
                else:
                    pos = random.randrange(len(possible_choices))
                    board[x][y] = possible_choices[pos]
                    if solve(board, constraint, choices, diag, True) > 0:
                        break
                    else:
                        del possible_choices[pos]

def generate_endview_constraint(board):
    ''' Generate Endview constraint from an original board. '''
    dim = get_dim(board)
    constraint = generate_empty_constraint(dim)
    # top
    for i in range(dim):
        j = 0
        while j < dim:
            if board[j][i] != 'X':
                constraint[0][i] = board[j][i]
                break
            else:
                j += 1
    # bottom
    for i in range(dim):
        j = 0
        while j < dim:
            if board[dim - 1 - j][i] != 'X':
                constraint[1][i] = board[dim - 1 - j][i]
                break
            else:
                j += 1
    # left
    for i in range(dim):
        j = 0
        while j < dim:
            if board[i][j] != 'X':
                constraint[2][i] = board[i][j]
                break
            else:
                j += 1
    # right
    for i in range(dim):
        j = 0
        while j < dim:
            if board[i][dim - 1 - j] != 'X':
                constraint[3][i] = board[i][dim - 1 - j]
                break
            else:
                j += 1
    return constraint


if __name__ == '__main__':
    dim = int(sys.argv[1])
    choices = int(sys.argv[2])
    if type(choices) is type(0):
        no_of_choices = choices
        choices = ''
        for i in range(no_of_choices):
            choices += omni_to_letter(i + 1)
    if dim > len(choices):
        choices += 'X'
    board = generate_empty_board(dim)
    constraint = generate_prefill(dim, choices, False)
    populate_empty_board(board, choices)
    diag = False
    constraint_count = 0
    for i in range(4):
        for j in range(dim):
            if constraint[i][j] != '':
                constraint_count += 1
    convert_to_family_generator(board, constraint, choices)

    print
    solve_print(board, constraint, choices, diag)
    print 'constraint count:', constraint_count