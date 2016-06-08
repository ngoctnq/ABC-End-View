#!/usr/bin/env python2
from utils import *

def test_board_generation(dim = 5, length_of_choices = 4, bool_int = 0):
    constraint = empty_constraint(dim)
    if bool_int == 0:
        diag = False
    else:
        diag = True
    choices_no_x = ''
    for i in range(length_of_choices):
        choices_no_x += chr(ord('A')+i)
    choices = choices_no_x + 'X'
    board = init_board(constraint, choices, diag)

    if diag:
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

    to_permute = list(choices + 'X'*(dim - len(choices)))
    random.shuffle(to_permute)
    for i in range(dim):
        board[0][i] = to_permute[i]
    to_permute = to_permute[1:]
    random.shuffle(to_permute)
    for i in range(dim-1):
        board[i+1][0] = to_permute[i]

    printOut(board)

    cancel_all(board, constraint, choices, diag)
    mass_optimize(board, constraint, choices, diag)
    printOut(board)
    print len(solve_from_partial(board, constraint, choices, diag, False)[0])

def test_diagonals(dim = 5):
    diag = False
    constraint = empty_constraint(dim)
    choices = ''
    for i in range(dim):
        choices += chr(ord('A')+i)
    board = init_board(constraint, choices, diag)
    for i in range(dim):
        board[i][i] = 'A'
    for i in range(dim):
        board[0][i] = choices[i]
    cancel_all(board, constraint, choices, diag)
    mass_optimize(board, constraint, choices, diag)
    result = solve_from_partial(board, constraint, choices, diag)
    solutions_list = result[0]
    for i in range(len(solutions_list)):
        print_anti_diag(solutions_list[i])
        # printOut(solutions_list[i],constraint)

def print_anti_diag(board):
    dim = len(board)
    for i in range(dim):
        print board[i][dim-1-i],
    print

# from this point onwards:
# the equivalent of the solver, but in 1-D
def sidequest(new_constraint, choices):
    optimize_array(new_constraint, choices)
    shit_to_solve = [new_constraint]
    solutions_list = []
    while len(shit_to_solve) != 0:
        solve_array(shit_to_solve, choices, solutions_list)
    return solutions_list

def solve_array(shit_to_solve, choices, solutions_list):
    # print len(shit_to_solve)
    data = shit_to_solve.pop()
    # print data
    if not is_legit_array(data, choices):
        return
    if is_deadend_array(data):
        solutions_list.append(data)
        return
    clone = deepcopy(data)
    mindex = min_index(data)
    if mindex == None:
        return
    data[mindex] = data[mindex][0]
    clone[mindex] = clone[mindex][1:]
    optimize_array(data, choices)
    optimize_array(clone, choices)
    shit_to_solve.append(clone)
    shit_to_solve.append(data)

def is_legit_array(board, choices):
    dim = len(board)
    maxX = dim-len(choices)+1
    temp = ''
    count = 0
    for j in range(dim):
        if board[j] == 'X':
            count += 1
        temp += board[j]
    if count > maxX:
        return False
    for j in choices:
        if j not in temp:
            return False
    if temp.count('X') < maxX:
        return False
    return True

def optimize_array(board, choices):
    dim = len(board)
    maxX = dim - len(choices) + 1
    changed = True
    while changed:
        changed = False
        for c in choices:
            if c != 'X':
                count = 0
                lastAppeared = -1
                for i in range(dim):
                    if c in board[i]:
                        if c == board[i]:
                            count = -1
                            break
                        count += 1
                        lastAppeared = i
                if count == 1 or count == -1:
                    changed = True
                    if count == 1:
                        board[lastAppeared] = c
                    for i in range(dim):
                        if board[i] != c:
                            board[i] = board[i].replace(c,'')
                    return
            else:
                xcount = 0
                xcount_pos = []
                for i in range(dim):
                    if board[i] == c:
                        xcount += 1
                    if c in board[i]:
                        xcount_pos.append(i)
                if xcount == maxX:
                    for i in range(dim):
                        if board[i] != c:
                            board[i] = board[i].replace(c,'')
                elif len(xcount_pos) == maxX:
                    for i in xcount_pos:
                        board[i] = 'X'

def is_deadend_array(new_constraint):
    for i in range(len(new_constraint)):
        if len(new_constraint[i]) != 1:
            return False
    return True

def min_index(new_constraint):
    dim = len(new_constraint)
    min_value = 10
    index = None
    for i in range(dim):
        length = len(new_constraint[i])
        if length == 2:
            return i
        else:
            if length < min_value and length > 2:
                min_value = length
                index = i
    return index

if __name__ == '__main__':
    test_diagonals()
