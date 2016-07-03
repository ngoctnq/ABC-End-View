#!/usr/bin/env python2
from copy import deepcopy
import urllib2
from bs4 import BeautifulSoup
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
    implied_x = 0
    implied_x_letters = []
    for c in choices:
        if c != 'X':
            count = constraint[0].count(c)
            if count > 1:
                implied_x += (count - 1)
                implied_x_letters.append(c)
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
    implied_x = 0
    implied_x_letters = []
    for c in choices:
        if c != 'X':
            count = constraint[1].count(c)
            if count > 1:
                implied_x += (count - 1)
                implied_x_letters.append(c)
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
    implied_x = 0
    implied_x_letters = []
    for c in choices:
        if c != 'X':
            count = constraint[2].count(c)
            if count > 1:
                implied_x += (count - 1)
                implied_x_letters.append(c)
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
    implied_x = 0
    implied_x_letters = []
    for c in choices:
        if c != 'X':
            count = constraint[3].count(c)
            if count > 1:
                implied_x += (count - 1)
                implied_x_letters.append(c)
    if implied_x == max_x:
        for i in range(dim):
            if constraint[3][i] not in implied_x_letters:
                remove_char(board, [i, dim - 1], 'X')

def solve(board, constraint, choices, diag, short_circuit = False):
    ''' Master ABC Endview solver.
        Solve the board until unfilled is empty.
        If short_circuit flag is set to True, then return whether the problem
            has more than 1 solution.
        '''
    dim = get_dim(board)
    initial_reduction(board, constraint, choices)
    unfilled = []
    for i in range(dim):
        for j in range(dim):
            unfilled.append([i,j])
    solution_list = []

    # log(stringify(board, constraint, True))

    trials = solve_core(board, constraint, choices, diag,
        unfilled, solution_list, short_circuit)

    if short_circuit:
        return len(solution_list) > 1
    else:
        return solution_list, trials

def solve_core(board, constraint, choices, diag, unfilled, solution_list,
        short_circuit = False):
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
            unfilled, solution_list)
    else:
        # if everything is filled
        if len(unfilled) == 0:
            solution_list.append(board)
            return 0
        # trial and error

        # see where it gets stuck
        # log("STUCK")
        # log(stringify(board, constraint, True))

        x, y = fewest_choices_cell(board, unfilled)
        new_board = deepcopy(board)
        new_unfilled = deepcopy(unfilled)
        new_board[x][y] = new_board[x][y][0]
        board[x][y] = board[x][y][1:]

        return 1 + \
            solve_core(new_board, constraint, choices, diag,
                new_unfilled, solution_list) + \
            solve_core(board, constraint, choices, diag,
                unfilled, solution_list)

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

    # update due to constraint - all X til constraint's satisfied.
    if char == 'X':
        # top
        if constraint[0][y] != '':
            for i in range(max_x + 1):
                if board[i][y] == constraint[0][y]:
                    break
                elif board[i][y] == 'X':
                    continue
                else:
                    for c in choices:
                        if c != 'X' and c != constraint[0][y]:
                            changed = remove_char(board, [i, y], c) or changed
                    break
        # bottom
        if constraint[1][y] != '':
            for i in range(max_x + 1):
                if board[dim - 1 - i][y] == constraint[1][y]:
                    break
                elif board[dim - 1 - i][y] == 'X':
                    continue
                else:
                    for c in choices:
                        if c != 'X' and c != constraint[1][y]:
                            changed = remove_char(board, [dim - 1 - i, y], c)\
                                or changed
                    break
        # left
        if constraint[2][x] != '':
            for i in range(max_x + 1):
                if board[x][i] == constraint[2][x]:
                    break
                elif board[x][i] == 'X':
                    continue
                else:
                    for c in choices:
                        if c != 'X' and c != constraint[2][x]:
                            changed = remove_char(board, [x, i], c) or changed
                    break
        # right
        if constraint[3][x] != '':
            for i in range(max_x + 1):
                if board[x][dim - 1 - i] == constraint[3][x]:
                    break
                elif board[x][dim - 1 - i] == 'X':
                    continue
                else:
                    for c in choices:
                        if c != 'X' and c != constraint[3][x]:
                            changed = remove_char(board, [x, dim - 1 - i], c)\
                                or changed
                    break
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
        log('file '+directory+' opened successfully.', 2)
    except:
        log('file '+directory+' does not exist, caching...', 2)
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
        log('file '+directory+' saved successfully.', 2)
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
                    constraint[0][i] = topConstraint[i]
            del data[0]
            del topConstraint
            #__________
            bottomConstraint = data[0].upper().split()
            for i in range(dim):
                if bottomConstraint[i] != '-':
                    constraint[1][i] = bottomConstraint[i]
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
                    constraint[2][i] = leftConstraint[i]
            del data[0]
            del leftConstraint
            #__________
            rightConstraint = data[0].upper().split()
            for i in range(dim):
                if rightConstraint[i] != '-':
                    constraint[3][i] = rightConstraint[i]
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
                        board[i][j] = clues[j]

    return board, constraint, choices, diag

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

def log(msg, priority = 1):
    ''' for logging purposes, can change stream or write to file. '''
    print msg

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

def swap_letter(board, constraint, perm):
    ''' Swap letters in the given permutations.
        Assuming perm is a valid rearrangement, partial or complete,
            of choices.
        '''
    dim = get_dim(board)
    for i in range(dim):
        for j in range(dim):
            if board[i][j] in perm:
                board[i][j] = perm.index(board[i][j])
    perm = perm[1:] + perm[0]
    for i in range(dim):
        for j in range(dim):
            if type(board[i][j]) is type(0):
                board[i][j] = perm[board[i][j]]

# EXECUTION SECTION
#___________

if __name__ == '__main__':
    board, constraint, choices, diag = janko_parser(janko_get_text(46))
    # board, constraint, choices, diag = input_gui()
    solution_list, trials = solve(board, constraint, choices, diag)
    print 'number of trials:', trials
    print 'number of slns  :', len(solution_list)
    for i in solution_list:
        print 
        print stringify(i, constraint, True)

