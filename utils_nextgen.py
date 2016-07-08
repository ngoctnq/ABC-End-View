#!/usr/bin/env python2
from copy import deepcopy
import sys
# import urllib2
import random
# from bs4 import BeautifulSoup
''' A well documented digital conversion of ABC Endview puzzle.
    Ngoc Tran - 2016 || underlandian.com

    Formatting of the board:
    - board[i][j] denotes the i-th row, j-th column, zero-based.
    - constraint[i] denotes the constraints on the border,
        0, 1, 2, 3 are top, bottom, left, right, respectively.
    - choices is a sequence of letters to be filled in.
    '''

# flags, constants
TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3
LOG = -1
GUI = 9
DEV = 99

# INITIALIZATION SECTION
#___________

def get_dim(array):
    ''' Get dimension of the board.
        Works with both board and constraint.
        '''
    return len(array[0])

def generate_empty_board(dim):
    ''' Generate empty board.
        board is a 2-dimensional nested list, with 0 denotes empty,
        1 denotes X, and so on, as noted in primes.
        '''
    # initialize new board
    new_board = []
    # prevent internal caching
    for i in range(dim):
        new_row = []
        for j in range(dim):
            # append a new column
            new_row.append('')
        new_board.append(new_row)
    return new_board

def generate_empty_constraint(dim):
    ''' Generate empty constraint.
        also a 2-dimensional nested list, same denotation with board.
        0, 1, 2, 3 are top, bottom, left, right, respectively.
        '''
    # initialize new board
    new_constraint = []
    # prevent internal caching
    for i in range(4):
        new_row = []
        for j in range(dim):
            # append a new column
            new_row.append('')
        new_constraint.append(new_row)
    return new_constraint

def populate_empty_board(board, choices):
    ''' Fill all labels with choices. '''
    dim = get_dim(board)
    for i in range(dim):
        for j in range(dim):
            board[i][j] = choices

# SOLVING SECTION
#___________

def remove_char(board, coord, char):
    ''' Remove a char from a label, and return if anything is changed.
        This is the only place a cell can get emptied, so it'd raise an error.
        '''
    # log('removing '+char+' from coord '+str(coord))
    
    if char == '':
        raise ValueError('no character to replace')
    if char not in board[coord[0]][coord[1]]:
        return False
    else:
        board[coord[0]][coord[1]] = \
            board[coord[0]][coord[1]].replace(char, '')
    if board[coord[0]][coord[1]] == '':
        raise ValueError('empty cell at ' + str(coord))
    return True

def initial_reduction(board, constraint, choices):
    ''' Removes impossibles given by constraints.
        For example, if 'A' is given, with choices 'ABX' with dimension 4,
            then A cannot be in the last cell of a row/column.
        Also, if 2 A's are in the constraints, one of them is an X.
        '''
    dim = get_dim(board)
    max_x = dim - len(choices) + 1
    if 'X' in choices:
        len_choices_without_x = len(choices) - 1
    else:
        len_choices_without_x = len(choices)

    # top constraint
    for i in range(dim):
        if constraint[0][i] != '':
            for j in range(len_choices_without_x - 1):
                remove_char(board, [dim - 1 - j, i], constraint[0][i])
            for c in choices:
                if c != 'X' and c != constraint[0][i]:
                    remove_char(board, [0, i], c)
    # same-letter constraint implies X
    implied_x, implied_x_letters = implied_x_count(constraint, choices, TOP)
    if implied_x == max_x:
        for i in range(dim):
            if constraint[0][i] not in implied_x_letters:
                remove_char(board, [0, i], 'X')

    # bottom constraint
    for i in range(dim):
        if constraint[1][i] != '':
            for j in range(len_choices_without_x - 1):
                remove_char(board, [j, i], constraint[1][i])
            for c in choices:
                if c != 'X' and c != constraint[1][i]:
                    remove_char(board, [dim - 1, i], c)
    # same-letter constraint implies X
    implied_x, implied_x_letters = implied_x_count(constraint, choices, BOTTOM)
    if implied_x == max_x:
        for i in range(dim):
            if constraint[1][i] not in implied_x_letters:
                remove_char(board, [dim - 1, i], 'X')

    # left constraint
    for i in range(dim):
        if constraint[2][i] != '':
            for j in range(len_choices_without_x - 1):
                remove_char(board, [i, dim - 1 - j], constraint[2][i])
            for c in choices:
                if c != 'X' and c != constraint[2][i]:
                    remove_char(board, [i, 0], c)
    # same-letter constraint implies X
    implied_x, implied_x_letters = implied_x_count(constraint, choices, LEFT)
    if implied_x == max_x:
        for i in range(dim):
            if constraint[2][i] not in implied_x_letters:
                remove_char(board, [i, 0], 'X')

    # right constraint
    for i in range(dim):
        if constraint[3][i] != '':
            for j in range(len_choices_without_x - 1):
                remove_char(board, [i, j], constraint[3][i])
            for c in choices:
                if c != 'X' and c != constraint[3][i]:
                    remove_char(board, [i, dim - 1], c)
    # same-letter constraint implies X
    implied_x, implied_x_letters = implied_x_count(constraint, choices, RIGHT)
    if implied_x == max_x:
        for i in range(dim):
            if constraint[3][i] not in implied_x_letters:
                remove_char(board, [i, dim - 1], 'X')

def implied_x_count(constraint, choices, side):
    ''' Count implied exes caused by constraints of the same letter. '''
    implied_x = 0
    implied_x_letters = []
    if side == TOP:
        for c in choices:
            if c != 'X':
                count = constraint[0].count(c)
                if count > 1:
                    implied_x += (count - 1)
                    implied_x_letters.append(c)
    elif side == BOTTOM:
        for c in choices:
            if c != 'X':
                count = constraint[1].count(c)
                if count > 1:
                    implied_x += (count - 1)
                    implied_x_letters.append(c)
    elif side == LEFT:
        for c in choices:
            if c != 'X':
                count = constraint[2].count(c)
                if count > 1:
                    implied_x += (count - 1)
                    implied_x_letters.append(c)
    elif side == RIGHT:
        for c in choices:
            if c != 'X':
                count = constraint[3].count(c)
                if count > 1:
                    implied_x += (count - 1)
                    implied_x_letters.append(c)
    else:
        raise ValueError('not a valid side of constraint')
    return implied_x, implied_x_letters

def solve(board, constraint, choices, diag = False, short_circuit = False,
    no_trials = False):
    ''' Master ABC Endview solver.
        Solve the board until unfilled is empty.
        If short_circuit flag is set to True, then return whether the problem
            has more than 1 solution.
        If no_trials flag is set to True, then return the "solution" achieved
            without using trial-and-error.
        '''
    dim = get_dim(board)
    board = deepcopy(board)
    
    # if we are really (un)lucky, then it won't even pass the valet round
    try:
        initial_reduction(board, constraint, choices)
    except ValueError:
        if short_circuit:
            return 0
        else:
            return [], 0

    unfilled = []
    for i in range(dim):
        for j in range(dim):
            unfilled.append([i,j])
    solution_list = []

    # log(stringify(board, constraint, True))

    trials = solve_core(board, constraint, choices, diag,
        unfilled, solution_list, short_circuit, no_trials)

    if short_circuit:
        return len(solution_list)
    else:
        if no_trials:
            return solution_list[0]
        else:
            return solution_list, trials

def solve_core(board, constraint, choices, diag, unfilled, solution_list,
    short_circuit = False, no_trials = False):
    ''' Main solving method, with trial-and-error.
        If short_circuit flag is set to True, then when the problem is
            determined to have more than 1 solution, it terminates instantly.
        '''
    if short_circuit and len(solution_list) > 1:
        return 0

    changed = True
    try:
        while changed and len(unfilled) != 0:
            changed = fill_obvious_label(board, constraint, choices,
                diag, unfilled)
        changed = check_for_only_choices(board, choices, diag)
    except ValueError:
        # this means it yields an invalid board
        return 0
    # if something is changed, tail call to keep trying solving
    if changed:
        return solve_core(board, constraint, choices, diag,
            unfilled, solution_list, short_circuit, no_trials)
    else:
        if no_trials:
            solution_list.append(board)
            return 0

        # if everything is filled
        if len(unfilled) == 0:
            solution_list.append(board)
            return 0
        # trial and error

        # see where it gets stuck
        # log("STUCK", DEV)
        # log(stringify(board, constraint, True), DEV)

        x, y = fewest_choices_cell(board, unfilled)
        new_board = deepcopy(board)
        new_unfilled = deepcopy(unfilled)
        new_board[x][y] = new_board[x][y][0]
        board[x][y] = board[x][y][1:]

        return 1 + \
            solve_core(new_board, constraint, choices, diag,
                new_unfilled, solution_list, short_circuit) + \
            solve_core(board, constraint, choices, diag,
                unfilled, solution_list, short_circuit)

def fewest_choices_cell(board, unfilled):
    ''' Find the cell with the fewest choice. '''
    # placeholder
    min_choice = 999
    x = -1
    y = -1
    for coord in unfilled:
        no_of_choices = len(board[coord[0]][coord[1]])
        if no_of_choices == 1:
            continue
        elif no_of_choices == 2:
            x = coord[0]
            y = coord[1]
            break
        elif no_of_choices < min_choice and \
                no_of_choices > 1:
            x = coord[0]
            y = coord[1]
            min_choice = no_of_choices
    if x == -1 and y == -1:
        raise ValueError("FATAL: unexpected error in fewest_choices_cell")
    return x, y

def check_for_only_choices(board, choices, diag):
    ''' If a row/column only have a place to fill a letter, it gets filled. '''
    dim = get_dim(board)
    max_x = dim - len(choices) + 1
    changed = False

    for c in choices: 
        if c != 'X':
            # check rows
            for i in range(dim):
                letter_found = 0
                for j in range(dim):
                    if c in board[i][j]:
                        letter_found += 1
                    if letter_found > 1:
                        break
                if letter_found == 1:
                    for j in range(dim):
                        if c in board[i][j]:
                            for char in choices:
                                if char != c:
                                    changed = remove_char(board, [i, j], char)\
                                        or changed
            # check columns
            for i in range(dim):
                letter_found = 0
                for j in range(dim):
                    if c in board[j][i]:
                        letter_found += 1
                    if letter_found > 1:
                        break
                if letter_found == 1:
                    for j in range(dim):
                        if c in board[j][i]:
                            for char in choices:
                                if char != c:
                                    changed = remove_char(board, [j, i], char)\
                                        or changed
            # check diagonals
            if diag:
                # check main diagonal
                letter_found = 0
                for i in range(dim):
                    if c in board[i][i]:
                        letter_found += 1
                    if letter_found > 1:
                        break
                if letter_found == 1:
                    for i in range(dim):
                        if c in board[i][i]:
                            for char in choices:
                                if char != c:
                                    changed = remove_char(board, [i, i], char)\
                                        or changed
                # check anti diagonal
                letter_found = 0
                for i in range(dim):
                    if c in board[i][dim - 1 - i]:
                        letter_found += 1
                    if letter_found > 1:
                        break
                if letter_found == 1:
                    for i in range(dim):
                        if c in board[i][dim - 1 - i]:
                            for char in choices:
                                if char != c:
                                    changed = remove_char(board,
                                        [i, dim - 1 - i], char) or changed
        # there can be more than one X
        else:
            # check rows
            for i in range(dim):
                x_count = 0
                for j in range(dim):
                    if 'X' in board[i][j]:
                        x_count += 1
                if x_count == max_x:
                    for j in range(dim):
                        if 'X' in board[i][j]:
                            for c in choices:
                                if c != 'X':
                                    changed = remove_char(board,
                                        [i, j], c) or changed
                elif x_count < max_x:
                    raise ValueError('FATAL! fewer exes than should ' + \
                        'in row ' + str(i))
            # check column
            for i in range(dim):
                x_count = 0
                for j in range(dim):
                    if 'X' in board[j][i]:
                        x_count += 1
                if x_count == max_x:
                    for j in range(dim):
                        if 'X' in board[j][i]:
                            for c in choices:
                                if c != 'X':
                                    changed = remove_char(board,
                                        [j, i], c) or changed
                elif x_count < max_x:
                    raise ValueError('FATAL! fewer exes than should ' + \
                        'in column ' + str(i))
            # check diagonals
            if diag:
                # main diagonal
                x_count = 0
                for i in range(dim):
                    if 'X' in board[i][i]:
                        x_count += 1
                if x_count == max_x:
                    for i in range(dim):
                        if 'X' in board[i][i]:
                            for c in choices:
                                if c != 'X':
                                    changed = remove_char(board, [i, i], c)\
                                        or changed
                elif x_count < max_x:
                    raise ValueError('FATAL! too few exes on main diagonal')
                # anti diagonal
                x_count = 0
                for i in range(dim):
                    if 'X' in board[i][dim - 1 - i]:
                        x_count += 1
                if x_count == max_x:
                    for i in range(dim):
                        if 'X' in board[i][dim - 1 - i]:
                            for c in choices:
                                if c != 'X':
                                    changed = remove_char(board,
                                        [i, dim - 1 - i], c) or changed
                elif x_count < max_x:
                    raise ValueError('FATAL! too few exes on anti diagonal')

    return changed

def fill_obvious_label(board, constraint, choices, diag, unfilled):
    ''' Fill cells that have only one possible letter. '''
    changed = False
    for coord in unfilled:
        if len(board[coord[0]][coord[1]]) == 1:
            idx = unfilled.index(coord)
            update_after_fill(board, constraint, choices, diag, coord)
            changed = True
            del unfilled[idx]
            break
    return changed

def update_after_fill(board, constraint, choices, diag, coord):
    ''' Update the board after a cell is filled.
        Return whether anything have changed.
        '''
    dim = get_dim(board)
    x = coord[0]
    y = coord[1]
    char = board[x][y]
    changed = False
    max_x = dim - len(choices) + 1

    # update row/column of that letter's existence
    if char != 'X':
        # row
        for i in range(dim):
            if i != y:
                changed = remove_char(board, [x, i], char) or changed

        # column
        for i in range(dim):
            if i != x:
                changed = remove_char(board, [i, y], char) or changed
    else:
        # update due to the max-X rule - then remove X from that row/column
        # max_x in row
        x_count_real = 0
        for i in range(dim):
            if board[x][i] == 'X':
                x_count_real += 1
        if x_count_real == max_x:
            for i in range(dim):
                if board[x][i] != 'X':
                    changed = remove_char(board, [x, i], 'X') or changed
        elif x_count_real > max_x:
            raise ValueError('FATAL! more exes than should in row ' + str(x))
        # max_x in column
        x_count_real = 0
        for i in range(dim):
            if 'X' in board[i][y]:
                if board[i][y] == 'X':
                    x_count_real += 1
        if x_count_real == max_x:
            for i in range(dim):
                if board[i][y] != 'X':
                    changed = remove_char(board, [i, y], 'X') or changed
        elif x_count_real > max_x:
            raise ValueError('FATAL! more exes than should in column '+ str(y))

    # update on the diagonals
    if diag:
        if char != 'X':
            if x == y:
                for i in range(dim):
                    if i != x:
                        changed = remove_char(board, [i, i], char) or changed
            if x + y == dim - 1:
                for i in range(dim):
                    if i != x:
                        changed = remove_char(board, [i, dim - 1 - i], char) \
                            or changed
        else:
            # run general max_x rule on both diagonals
            # main diagonal
            x_count_real = 0
            for i in range(dim):
                if board[i][i] == 'X':
                    x_count_real += 1
            if x_count_real == max_x:
                for i in range(dim):
                    if board[i][i] != 'X':
                        changed = remove_char(board, [i, i], 'X') or changed
            elif x_count_real > max_x:
                raise ValueError('FATAL! too many exes on main diagonal')

            # anti-diagonal
            x_count_real = 0
            for i in range(dim):
                if board[i][dim - 1 - i] == 'X':
                    x_count_real += 1
            if x_count_real == max_x:
                for i in range(dim):
                    if board[i][dim - 1 - i] != 'X':
                        changed = remove_char(board, [i, dim - 1 - i], 'X')\
                            or changed
            elif x_count_real > max_x:
                raise ValueError('FATAL! too many exes on anti diagonal')

    # update due to constraint:
    # if X is in the earlier group: all X til constraint's satisfied
    # if X is in the latter group: the constraint has to be satisfied earlier
    if char == 'X':
        # top
        if constraint[0][y] != '':
            if x in range(max_x + 1):
                for i in range(max_x + 1):
                    if board[i][y] == constraint[0][y]:
                        break
                    elif board[i][y] == 'X':
                        continue
                    else:
                        for c in choices:
                            if c != 'X' and c != constraint[0][y]:
                                changed = remove_char(board, [i, y], c) \
                                    or changed
                        break
            else:
                x_count_real = 0
                for i in range(max_x + 1, dim):
                    if board[i][y] == 'X':
                        x_count_real += 1
                for i in range(x_count_real):
                    changed = remove_char(board, [max_x - i, y], 
                        constraint[0][y]) or changed

        # bottom
        if constraint[1][y] != '':
            if x in range(dim - max_x - 1, dim):
                for i in range(max_x + 1):
                    if board[dim - 1 - i][y] == constraint[1][y]:
                        break
                    elif board[dim - 1 - i][y] == 'X':
                        continue
                    else:
                        for c in choices:
                            if c != 'X' and c != constraint[1][y]:
                                changed = remove_char(board,
                                    [dim - 1 - i, y], c) or changed
                        break
            else:
                x_count_real = 0
                for i in range(dim - max_x - 1):
                    if board[i][y] == 'X':
                        x_count_real += 1
                for i in range(x_count_real):
                    changed = remove_char(board, [dim - max_x - 1 + i, y], 
                        constraint[1][y]) or changed
        # left
        if constraint[2][x] != '':
            if y in range(max_x + 1):
                for i in range(max_x + 1):
                    if board[x][i] == constraint[2][x]:
                        break
                    elif board[x][i] == 'X':
                        continue
                    else:
                        for c in choices:
                            if c != 'X' and c != constraint[2][x]:
                                changed = remove_char(board, [x, i], c) \
                                    or changed
                        break
            else:
                x_count_real = 0
                for i in range(max_x + 1, dim):
                    if board[x][i] == 'X':
                        x_count_real += 1
                for i in range(x_count_real):
                    changed = remove_char(board, [x, max_x - i], 
                        constraint[2][x]) or changed
        # right
        if constraint[3][x] != '':
            if y in range(dim - max_x - 1, dim):
                for i in range(max_x + 1):
                    if board[x][dim - 1 - i] == constraint[3][x]:
                        break
                    elif board[x][dim - 1 - i] == 'X':
                        continue
                    else:
                        for c in choices:
                            if c != 'X' and c != constraint[3][x]:
                                changed = remove_char(board,
                                    [x, dim - 1 - i], c) or changed
                        break
            else:
                x_count_real = 0
                for i in range(dim - max_x - 1):
                    if board[x][i] == 'X':
                        x_count_real += 1
                for i in range(x_count_real):
                    changed = remove_char(board, [x, dim - max_x - 1 + i], 
                        constraint[3][x]) or changed
    else:
        # top
        if char == constraint[0][y]:
            for i in range(max_x + 1):
                if board[i][y] == char:
                    break
                else:
                    for c in choices:
                        if c != 'X':
                            changed = remove_char(board, [i, y], c) or changed
        # if it's not constraint, then anything after that isn't
        elif constraint[0][y] != '':
            for i in range(x + 1, dim):
                changed = remove_char(board, [i, y], constraint[0][y]) \
                    or changed
        # bottom
        if char == constraint[1][y]:
            for i in range(max_x + 1):
                if board[dim - 1 - i][y] == char:
                    break
                else:
                    for c in choices:
                        if c != 'X':
                            changed = remove_char(board, [dim - 1 - i, y], c) \
                                or changed
        # if it's not constraint, then anything after that isn't
        elif constraint[1][y] != '':
            for i in range(x):
                changed = remove_char(board, [i, y],
                    constraint[1][y]) or changed
        # left
        if char == constraint[2][x]:
            for i in range(max_x + 1):
                if board[x][i] == char:
                    break
                else:
                    for c in choices:
                        if c != 'X':
                            changed = remove_char(board, [x, i], c) or changed
        # if it's not constraint, then anything after that isn't
        elif constraint[2][x] != '':
            for i in range(y + 1, dim):
                changed = remove_char(board, [x, i], constraint[2][x]) \
                    or changed
        # right
        if char == constraint[3][x]:
            for i in range(max_x + 1):
                if board[x][dim - 1 - i] == char:
                    break
                else:
                    for c in choices:
                        if c != 'X':
                            changed = remove_char(board, [x, dim - 1 - i], c) \
                                or changed
        # if it's not constraint, then anything after that isn't
        elif constraint[3][x] != '':
            for i in range(y):
                changed = remove_char(board, [x, i],
                    constraint[3][x]) or changed

    return changed

# INPUT SECTION
#___________

def not_cap_chars(word):
    ''' Check if all are capital and sequential from A. '''
    if len(word) == 0:
        raise ValueError('no choices entered')
    for i in range(len(word)):
        if ord(word[i]) != ord('A')+i:
            return True
    return False

def input_gui():
    ''' GUI to input a problem. '''
    print 'ABC ENDVIEW SOLVER'
    print

    not_entered = True
    while not_entered:
        text = raw_input("Dimension (n x n)? ")
        try:
            dim = int(text)
            not_entered = False
            if dim < 2:
                raise ValueError
        except ValueError:
            print "Value error!", "Dimension has to be an integer greater than 1!"

    constraint = generate_empty_constraint(dim)
    #______________
    not_entered = True
    while not_entered:
        choices = raw_input("Characters to fill in, with no delimiters: ") \
            .upper()
        if not_cap_chars(choices):
            print "String error!", "Only sequencial letters are allowed."
        elif len(choices) > dim:
            print "String error!", "Number of choices must be less than " + \
                "or equal to " + str(dim) + "."
        else:
            not_entered = False
    #______________
    not_entered = True
    while not_entered:
        constraint_sub = raw_input("Insert column-beginning constraints " + \
            "- Continuously, '-' for none: ").upper()
        if len(constraint_sub) != dim:
            print "Constraints error!", \
                "Number of constraints must be exactly "+str(dim)+"."
        else:
            legit = True
            while legit:
                for i in range(dim):
                    if constraint_sub[i] in choices:
                        constraint[0][i] = constraint_sub[i]
                    elif constraint_sub[i] != '-':
                        legit = False
                        print "String error!", constraint_sub[i] + \
                            " is not a valid entry!"
                        break
                if i == dim-1:
                    break
            if legit:
                not_entered = False
    #______________
    not_entered = True
    while not_entered:
        constraint_sub = raw_input("Insert column-ending constraints " + \
            "- Continuously, '-' for none: ").upper()
        if len(constraint_sub) != dim:
            print "Constraints error!", \
                "Number of constraints must be exactly "+str(dim)+"."
        else:
            legit = True
            while legit:
                for i in range(dim):
                    if constraint_sub[i] in choices:
                        constraint[1][i] = constraint_sub[i]
                    elif constraint_sub[i] != '-':
                        legit = False
                        print "String error!", constraint_sub[i] + \
                            " is not a valid entry!"
                        break
                if i == dim-1:
                    break
            if legit:
                not_entered = False
    #______________
    not_entered = True
    while not_entered:
        constraint_sub = raw_input("Insert row-beginning constraints - " + \
            "Continuously, '-' for none: ").upper()
        if len(constraint_sub) != dim:
            print "Constraints error!", \
                "Number of constraints must be exactly " + str(dim) + "."
        else:
            legit = True
            while legit:
                for i in range(dim):
                    if constraint_sub[i] in choices:
                        constraint[2][i] = constraint_sub[i]
                    elif constraint_sub[i] != '-':
                        legit = False
                        print "String error!", constraint_sub[i] + \
                            " is not a valid entry!"
                        break
                if i == dim-1:
                    break
            if legit:
                not_entered = False
    #______________
    not_entered = True
    while not_entered:
        constraint_sub = raw_input("Insert row-ending constraints - " + \
            "Continuously, '-' for none: ").upper()
        if len(constraint_sub) != dim:
            print "Constraints error!", \
                "Number of constraints must be exactly "+str(dim)+"."
        else:
            legit = True
            while legit:
                for i in range(dim):
                    if constraint_sub[i] in choices:
                        constraint[3][i] = constraint_sub[i]
                    elif constraint_sub[i] != '-':
                        legit = False
                        print "String error!", constraint_sub[i]+\
                            " is not a valid entry!"
                        break
                if i == dim-1:
                    break
            if legit:
                not_entered = False
    #______________
    not_entered = True
    while not_entered:
        not_entered = False
        result = raw_input("Are diagonals required to have all characters? ") \
            .upper()
        if result in ['YES','Y','1']:
            diag = True
        elif result in ['NO','N','0']:
            diag = False
        else:
            print 'Not a valid answer!'
            not_entered = True
    # start initializing
    if dim > len(choices):
        choices += 'X'
    #______________
    not_entered = True
    while not_entered:
        not_entered = False
        result = raw_input("Are there prefilled boxes? ").upper()
        if result in ['YES','Y','1']:
            partial = True
        elif result in ['NO','N','0']:
            partial = False
        else:
            print 'Not a valid answer!'
            not_entered = True
    #______________
    board = generate_empty_board(dim)
    populate_empty_board(board, choices)
    if partial:
        print "Input coordinates and corresponding value, " + \
            "blankspace-separated; blank to end."
        while True:
            result = raw_input().upper()
            if result == '':
                break
            else:
                try:
                    clues = result.split()
                    if len(clues) != 3:
                        raise ValueError
                    i = int(clues[0])-1
                    j = int(clues[1])-1
                    if len(clues[2])!= 1 or clues[2] == 'X' or \
                        clues[2] not in choices:
                        raise ValueError
                    if i<0 or j<0 or i>=dim or j>=dim:
                        raise ValueError
                    board[i][j] = clues[2]
                except:
                    print 'Not a valid input! Ignored last input.'
    print 'All input taken!'
    return board, constraint, choices, diag

# JANKO SECTION
#___________

def janko_get_text(no = 0):
    ''' Get the problem from janko site.
        Will cache into a folder if not existed.
        '''
    directory = 'janko_cache'
    if directory[-1] != '/':
        directory += '/'

    if no == 0:
        print 'Janko.at problem solver'
        not_entered = True
        while not_entered:
            text = raw_input("Problem number? ")
            try:
                no = int(text)
                if no > 530 or no < 1:
                    print 'Not a valid question number!'
                else:
                    not_entered = False
            except:
                print 'Not a valid number!'

    # test if file existed, i.e. cached
    no = str(no).zfill(3)
    directory += (no+'.txt')
    try:
        file = open(directory,'r')
        log('file '+directory+' opened successfully.', LOG)
    except:
        log('file '+directory+' does not exist, caching...', LOG)
        url = 'http://www.janko.at/Raetsel/Abc-End-View/'+no+'.a.htm'
        file = urllib2.urlopen(url)
        html_doc = file.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        data = soup.data.get_text().split('\n')

        # remove some unnecessary newlines
        del data[0]
        del data[-1]
        # cache the received data
        file = open(directory,'w')
        for line in data[:-1]:
            file.write(line.encode('ascii','ignore'))
            file.write('\n')
        file.write(data[-1])
        file.close()
        log('file '+directory+' saved successfully.', LOG)
    else:
        data = file.read().split('\n')
        file.close()

    return data

def janko_parser(data):
    ''' Janko parser - return the board and its constraints.
        @return board, constraint, choices, diag
        '''
    choices = 0
    diag = False

    attributes = ['size','depth','options','clabels','rlabels','problem']
    while True:
        while len(data) > 0:
            if len(data[0]) == 0 or data[0].split()[0] not in attributes:
                del data[0]
            else:
                break
        if len(data) == 0:
            break
        if data[0].split()[0] == 'size':
            dim = int(data[0].split()[1])
            constraint = generate_empty_constraint(dim)
            attributes.remove('size')
        if data[0].split()[0] == 'depth':
            depth = int(data[0].split()[1])
            choices = ''
            for i in range(depth):
                choices += chr(ord('A') + i)
            if depth < dim:
                choices += 'X'
            attributes.remove('depth')
        if data[0].split()[0] == 'options':
            attributes.remove('options')
            diag = True
        # top/bottom
        if data[0].split()[0] == 'clabels':
            attributes.remove('clabels')
            del data[0]
            topConstraint = data[0].upper().split()
            for i in range(dim):
                if topConstraint[i] != '-':
                    constraint[0][i] = omni_to_letter(topConstraint[i])
            del data[0]
            del topConstraint
            #__________
            bottomConstraint = data[0].upper().split()
            for i in range(dim):
                if bottomConstraint[i] != '-':
                    constraint[1][i] = omni_to_letter(bottomConstraint[i])
            del data[0]
            del bottomConstraint
            #__________
        # left/right
        if data[0].split()[0] == 'rlabels':
            attributes.remove('rlabels')
            del data[0]
            leftConstraint = data[0].upper().split()
            for i in range(dim):
                if leftConstraint[i] != '-':
                    constraint[2][i] = omni_to_letter(leftConstraint[i])
            del data[0]
            del leftConstraint
            #__________
            rightConstraint = data[0].upper().split()
            for i in range(dim):
                if rightConstraint[i] != '-':
                    constraint[3][i] = omni_to_letter(rightConstraint[i])
            del data[0]
            del rightConstraint
        # problem lmao
        board = generate_empty_board(dim)
        populate_empty_board(board, choices)
        if data[0].split()[0] == 'problem':
            attributes.remove('problem')
            del data[0]
            for i in range(dim):
                clues = data[0].upper().split()
                del data[0]
                for j in range(dim):
                    if clues[j] != '-':
                        board[i][j] = omni_to_letter(clues[j])

    return board, constraint, choices, diag

def omni_to_letter(c):
    ''' Convert number to letter. 
        Some problems on Janko has numbers instead of letters in the source
            code, confusing the solver.
        '''
    try:
        i = int(c)
        return chr(ord('A') - 1 + i)
    except:
        # not an int means its a normal character
        return c

# PRINTING SECTION
#___________

def generate_horizontal_border(dim, ljust_value = 1):
    ''' Return one horizontal border.
        Used in stringify().
       '''
    hBorder = '  '
    for i in range(dim):
        hBorder += '+-'
        hBorder += '-' * ljust_value
        hBorder += '-'
    hBorder += '+'
    return hBorder

def stringify(board, constraint = None, dev = False):
    ''' Return a pretty printing the board.
        Reliant on '\n', be careful.
        '''
    dim = len(board)
    ret = ''
    if constraint == None:
        constraint = generate_empty_constraint(dim)

    ljust_value = 1
    if dev:
        for i in range(dim):
            for j in range(dim):
                if len(board[i][j]) > ljust_value:
                    ljust_value = len(board[i][j])

    horizontal_border = generate_horizontal_border(dim, ljust_value)

    # top constraint
    ret += '    '
    for i in range(dim):
        ret += constraint[0][i].center(ljust_value)
        ret += '   '
    ret += '\n'

    for i in range(dim):
        ret += horizontal_border
        ret += '\n'
        # left constraint
        ret += constraint[2][i].center(1)
        ret += ' '
        # board content
        for j in range(dim):
            ret += '| '
            if len(board[i][j]) == 1:
                if board[i][j] != 'X':
                    ret += board[i][j].center(ljust_value)
                else:
                    ret += '-'.center(ljust_value)
            else:
                if dev:
                    ret += board[i][j].center(ljust_value)
                else:
                    ret += ''.center(ljust_value)
            ret += ' '
        ret += '| '
        # right constraint
        ret += constraint[3][i].center(1)
        ret += '\n'
    ret += horizontal_border
    ret += '\n'

    # bottom constraint
    ret += '    '
    for i in range(dim):
        ret += constraint[1][i].center(ljust_value)
        ret += '   '
    return ret

def log(msg, priority = LOG):
    ''' for logging purposes, can change stream or write to file. '''
    if priority == LOG:
        # print 'LOG:', msg
        pass
    elif priority == DEV:
        print msg
    elif priority == GUI:
        # print msg
        pass
    else:
        print msg
        # pass

def solve_main(no = -1):
    ''' Pretty printing the output of a solver.
        -1 triggers the input prompt, else get redirected to janko getter.
        '''
    log('\nABC Endview Solver', GUI)
    if no == -1:
        board, constraint, choices, diag = input_gui()
    else:
        board, constraint, choices, diag = janko_parser(janko_get_text(no))

    # log(stringify(board, constraint, True), DEV)

    solution_list, trials = solve(board, constraint, choices, diag)
    log('__________\n', GUI)
    log('number of trials: ' + str(trials), GUI)
    log('number of slns  : ' + str(len(solution_list)), GUI)
    log('__________\n', GUI)
    for i in range(len(solution_list)):
        log('Solution #' + str(i + 1)+'\n', GUI)
        log(stringify(solution_list[i], constraint), GUI)
        log('\n', GUI)

    # if True:
    # if trials > 0:
        # log(str(no).ljust(3) + ' ' + \
        #     str(len(solution_list)).rjust(3) + ' ' + \
        #     str(trials).rjust(3), DEV)

# EXPERIMENTAL SECTION FROM NOW ON
# TRANSFORMATION SECTION
#__________

def swap_board(board, coord1, coord2):
    ''' Swap two cells' labels. '''
    temp = board[coord1[0]][coord1[1]]
    board[coord1[0]][coord1[1]] = board[coord2[0]][coord2[1]]
    board[coord2[0]][coord2[1]] = temp

def swap_constraint(constraint, pos11, pos12, pos21, pos22):
    ''' Swap two constraints. '''
    temp = constraint[pos11][pos12]
    constraint[pos11][pos12] = constraint[pos21][pos22]
    constraint[pos21][pos22] = temp

def rotate_clockwise(board, constraint):
    ''' Rotate the board clockwise. '''
    dim = get_dim(board)
    x_max = int(dim/2)
    if dim % 2 == 0:
        y_max = x_max
    else:
        y_max = x_max + 1
    # flip the constraints
    for i in range(dim):
        swap_constraint(constraint, TOP, i, RIGHT, i)
        swap_constraint(constraint, LEFT, i, BOTTOM, i)
        swap_constraint(constraint, TOP, i, BOTTOM, i)
    for i in range(x_max):
        swap_constraint(constraint, TOP, i, TOP, dim - 1 - i)
        swap_constraint(constraint, BOTTOM, i, BOTTOM, dim - 1 - i)
    # flip the board
    # how in works: partition the board into 4 small rectangles/square
    for i in range(x_max):
        for j in range(y_max):
            swap_board(board, [i, j], [j, dim - 1 - i])
            swap_board(board, [dim - 1 - i, dim - 1 - j], [dim - 1 - j, i])
            swap_board(board, [i, j], [dim - 1 - i, dim - 1 - j])

def flip_diagonal(board, constraint):
    ''' Flip the board along the main diagonal. '''
    dim = get_dim(board)
    # flip the constraints
    for i in range(dim):
        swap_constraint(constraint, TOP, i, LEFT, i)
        swap_constraint(constraint, RIGHT, i, BOTTOM, i)
    # flip the board
    for i in range(dim):
        for j in range(i, dim):
            swap_board(board, [i, j], [j, i])

def rotate_counter_clockwise(board, constraint):
    ''' Rotate the board counter-clockwise.
        Executed lazily by calling rotate_clockwise() three times.
        '''
    for i in range(3):
        rotate_clockwise(board, constraint)

def flip_anti_diagonal(board, constraint):
    ''' Flip the board anti-diagonally.
        Lazily: diagonal flip -> 2 rotations.
        '''
    flip_diagonal(board, constraint)
    rotate_clockwise(board, constraint)
    rotate_clockwise(board, constraint)

def flip_vertical(board, constraint):
    ''' Flip the board vertically.
        Lazily, diagonal flip -> counter-clockwise rotation.
        '''
    flip_diagonal(board, constraint)
    rotate_counter_clockwise(board, constraint)

def flip_horizontal(board, constraint):
    ''' Flip the board horizontally.
        Lazily, diagonal flip -> clockwise rotation.
        '''
    flip_diagonal(board, constraint)
    rotate_clockwise(board, constraint)

def swap_letters(board, constraint, perm):
    ''' Swap letters in the given permutations.
        Assuming perm is a valid rearrangement, partial or complete,
            of choices.
        '''
    dim = get_dim(board)

    for i in range(dim):
        for j in range(dim):
            if board[i][j] in perm:
                board[i][j] = perm.index(board[i][j])
        for k in range(4):
            if constraint[k][i] in perm:
                constraint[k][i] = perm.index(constraint[k][i])

    sorted_perm = sorted(perm)

    for i in range(dim):
        for j in range(dim):
            if type(board[i][j]) is type(0):
                board[i][j] = sorted_perm[board[i][j]]
        for k in range(4):
            if type(constraint[k][i]) is type(0):
                constraint[k][i] = sorted_perm[constraint[k][i]]

# BOARD FAMILY CONVERSION SECTION
#__________

def constraint_score(constraint, side, choices, inverted = False):
    ''' Comparing edges based on nondiversity and clue counts. '''
    max_choice = len(choices)
    if choices[-1] == 'X':
        max_choice -= 1
    constraint = constraint[side]
    dim = len(constraint)
    no_of_empty = constraint.count('')
    dim - no_of_empty

    if inverted:
        constraint = constraint[::-1]
    unique_score = 0
    seen = ['']
    for c in constraint:
        if c not in seen:
            seen.append(c)

    for i in range(dim):
        c = constraint[i]
        power = dim - 1 - i
        seen_index = seen.index(c)

        if seen_index == 0:
            seen_index = max_choice
        unique_score += (max_choice - seen_index) * (10 ** power)
    score = ((dim - no_of_empty) * (10 ** (max_choice + 1)) + unique_score)
    if score > 0:
        return score
    else:
        return 1

def calculate_corner(constraint, corner, choices):
    # combining the 2 scores from the sides.
    # corners are numbered as follows:
    #   3   0
    #   2   1
    if corner == 0:
        return constraint_score(constraint, TOP, choices, True) * \
            constraint_score(constraint, RIGHT, choices)
    if corner == 1:
        return constraint_score(constraint, RIGHT, choices, True) * \
            constraint_score(constraint, BOTTOM, choices, True)
    if corner == 2:
        return constraint_score(constraint, LEFT, choices, True) * \
            constraint_score(constraint, BOTTOM, choices)
    if corner == 3:
        return constraint_score(constraint, TOP, choices) * \
            constraint_score(constraint, LEFT, choices)

def calculate_corner_stat(constraint, choices):
    ''' Return corner_list of scores, max, and, how many ties at max. '''
    corner_0 = calculate_corner(constraint, 0, choices)
    corner_1 = calculate_corner(constraint, 1, choices)
    corner_2 = calculate_corner(constraint, 2, choices)
    corner_3 = calculate_corner(constraint, 3, choices)
    corner_list = [corner_0, corner_1, corner_2, corner_3]
    corner_max = max(corner_list)
    max_count = corner_list.count(corner_max)
    return corner_list, corner_max, max_count

def convert_to_family_generator(board, constraint, choices,
    functions_used = []):
    ''' Change the whole board and constraint with basic transformations
            and letter switches into a new one that is the family's generator.
        Return the list of functions used in order.
        '''
    corner_list, corner_max, max_count = \
        calculate_corner_stat(constraint, choices)
    if max_count == 1:
        idx = corner_list.index(corner_max)
        if idx == 0:
            rotate_counter_clockwise(board, constraint)
            functions_used.append(rotate_counter_clockwise)
        elif idx == 1:
            rotate_clockwise(board, constraint)
            rotate_clockwise(board, constraint)
            functions_used.append(rotate_clockwise)
            functions_used.append(rotate_clockwise)
        elif idx == 2:
            rotate_clockwise(board, constraint)
            functions_used.append(rotate_clockwise)
        if constraint_score(constraint, TOP, choices) < \
                constraint_score(constraint, LEFT, choices):
            flip_diagonal(board, constraint)
            functions_used.append(flip_diagonal)
    elif max_count == 2:
        # opposite sides
        if corner_list[0] == corner_max and corner_list[2] == corner_max:
            rotate_counter_clockwise(board, constraint)
            functions_used.append(rotate_counter_clockwise)
            convert_to_family_generator(board, constraint, choices,
                functions_used)
            return
        elif corner_list[1] == corner_max and corner_list[3] == corner_max:
            score_top = constraint_score(constraint, TOP, choices)
            score_bottom = \
                constraint_score(constraint, BOTTOM, choices, True)
            score_left = constraint_score(constraint, LEFT, choices)
            score_right = \
                constraint_score(constraint, RIGHT, choices, True)
            score_list = [score_top, score_bottom, score_left, score_right]
            score_max = max(score_list)
            if score_list.count(score_max) == 1:
                if score_list[1] == score_max:
                    rotate_clockwise(board, constraint)
                    rotate_clockwise(board, constraint)
                    functions_used.append(rotate_clockwise)
                    functions_used.append(rotate_clockwise)
                elif score_list[2] == score_max:
                    flip_diagonal(board, constraint)
                    functions_used.append(flip_diagonal)
                elif score_list[3] == score_max:
                    flip_anti_diagonal(board, constraint)
                    functions_used.append(flip_anti_diagonal)
            elif score_list.count(score_max) == 2:
                # same corner
                if score_list[1] == score_max and score_list[3] == score_max:
                    # should never happen based on math
                    raise ValueError\
                        ('cannot have same score sides on max corner')
                    rotate_clockwise(board, constraint)
                    rotate_clockwise(board, constraint)
                    functions_used.append(rotate_clockwise)
                    functions_used.append(rotate_clockwise)
                    convert_to_family_generator(board, constraint, choices,
                        functions_used)
                    return
                elif score_list[0] == score_max and score_list[2] == score_max:
                    # should never happen
                    raise ValueError\
                        ('cannot have same score sides on max corner')
                # opposite corner
                elif score_list[2] == score_max and score_list[3] == score_max:
                    flip_anti_diagonal(board, constraint)
                    functions_used.append(flip_anti_diagonal)
                    convert_to_family_generator(board, constraint, choices,
                        functions_used)
                    return
                elif score_list[0] == score_max and score_list[1] == score_max:
                    if score_list[2] < score_list[3]:
                        rotate_clockwise(board, constraint)
                        rotate_clockwise(board, constraint)
                        functions_used.append(rotate_clockwise)
                        functions_used.append(rotate_clockwise)
                # connecting other corner                    
                elif score_list[0] == score_max and score_list[3] == score_max:
                    # symmetric
                    pass
                elif score_list[1] == score_max and score_list[2] == score_max:
                    flip_diagonal(board, constraint)
                    functions_used.append(flip_diagonal)
            else:
                raise ValueError('max count = 2 with >2 equal sides?')
        # adjacent sides
        elif corner_list[0] == corner_max:
            if corner_list[3] == corner_max:
                rotate_counter_clockwise(board, constraint)
                functions_used.append(rotate_counter_clockwise)
                convert_to_family_generator(board, constraint, choices,
                    functions_used)
                return
            elif corner_list[1] == corner_max:
                rotate_clockwise(board, constraint)
                rotate_clockwise(board, constraint)
                functions_used.append(rotate_clockwise)
                functions_used.append(rotate_clockwise)
                convert_to_family_generator(board, constraint, choices,
                    functions_used)
                return
        elif corner_list[2] == corner_max:
            if corner_list[1] == corner_max:
                rotate_clockwise(board, constraint)
                functions_used.append(rotate_clockwise)
                convert_to_family_generator(board, constraint, choices, 
                    functions_used)
                return
            else:
                if constraint_score(constraint, TOP, choices) < \
                        constraint_score(constraint, BOTTOM, choices) or \
                        (constraint_score(constraint, TOP, choices) == \
                        constraint_score(constraint, BOTTOM, choices) and \
                        constraint_score(constraint, LEFT, choices) < \
                        constraint_score(constraint, LEFT, choices, True)):
                    flip_vertical(board, constraint)
                    functions_used.append(flip_vertical)
    elif max_count == 3:
        # put the lowest corner on bottom right
        if corner_list[0] < corner_max:
            rotate_clockwise(board, constraint)
            functions_used.append(rotate_clockwise)
        elif corner_list[2] < corner_max:
            rotate_counter_clockwise(board, constraint)
            functions_used.append(rotate_counter_clockwise)
        elif corner_list[3] < corner_max:
            rotate_clockwise(board, constraint)
            rotate_clockwise(board, constraint)
            functions_used.append(rotate_clockwise)
            functions_used.append(rotate_clockwise)
    else:
        # order of preference: top, left, bottom, right
        # probably won't happen, or if it would it'd be perfectly symmetrical?
        log('----------', DEV)
        log('CHECK IF BOARD IS PERFECTLY SYMMETRICAL', DEV)
        log(stringify(board, constraint), DEV)
        log('----------', DEV)
        pass

    # log(stringify(board, constraint), DEV)

    # after transforming is swapping letters
    swap_order = \
        swap_letters_after_transformations(board, constraint, choices)
    return functions_used, swap_order

def swap_letters_after_transformations(board, constraint, choices):
    list_of_chars = []
    for c in constraint[0]:
        if c not in list_of_chars:
            list_of_chars.append(c)
    for c in constraint[2]:
        if c not in list_of_chars:
            list_of_chars.append(c)
    for c in constraint[1]:
        if c not in list_of_chars:
            list_of_chars.append(c)
    for c in constraint[3]:
        if c not in list_of_chars:
            list_of_chars.append(c)
    try:
        list_of_chars.remove('')
    except ValueError:
        # god bless if there are maximum no of constraints
        pass
    for c in choices:
        if c != 'X' and c not in list_of_chars:
            list_of_chars.append(c)
    swap_letters(board, constraint, list_of_chars)
    return list_of_chars

def execute_changes(board, constraint, functions_used, swap_order, reverse = False):
    ''' Revert all changes made, mostly from convert_to_family_generator. '''
    if reverse:
        for function in functions_used:
            invert_transformation(function)(board, constraint)
            sorted_swap = sorted(swap_order)
            new_swap_order = [None] * len(swap_order)
            for i in range(len(swap_order)):
                old_char = sorted_swap[i]
                new_char = swap_order[i]
                new_swap_order[sorted_swap.index(new_char)] = old_char
            swap_letters(board, constraint, new_swap_order) 
    else:
        for function in functions_used:
            function(board, constraint)
            swap_letters(board, constraint, swap_order)

def invert_transformation(func):
    if func is rotate_clockwise:
        return rotate_counter_clockwise
    elif func is rotate_counter_clockwise:
        return rotate_clockwise
    elif func is flip_horizontal or func is flip_vertical or \
            func is flip_diagonal or func is flip_anti_diagonal:
        return func
    else:
        return ValueError('not an invertible function')

# CONSTRAINT GENERATION SECTION
#__________

''' First, sort 1 and 2.
    Second, no more than dim - len(choices) + 1 same constraint.
    '''

def test_generate(dim, choices, diag = False, clue_count = 0, freq = None):
    satisfied = False
    choices = choices.upper()
    len_choices = len(choices)
    if dim > len(choices):
        choices += 'X'
    if clue_count == 0:
        clue_count_min = 0
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
    log('\nfound one!\n', GUI)
    log(stringify(board, constraint), GUI)


# EXECUTION SECTION
#__________

if __name__ == '__main__':
    no = int(sys.argv[1])
    board, constraint, choices, diag = janko_parser(janko_get_text(no))
    print stringify(board, constraint)
    # TODO: REMEMBER TO CLONE
    # functions_used, swap_order = \
    #     convert_to_family_generator(board, constraint, choices)
    # print stringify(board, constraint)
    # execute_changes(board, constraint, functions_used, swap_order, True)
    # print stringify(board, constraint)
    # if constraint_score(constraint, TOP, choices) < \
    #         constraint_score(constraint, BOTTOM, choices):
    #     print 'TOP < BOTTOM'
    solution_list, trials = solve(board, constraint, choices, diag)
    for solution in solution_list:
        print stringify(solution, constraint)