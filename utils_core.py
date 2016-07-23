#!/usr/bin/env python2
from copy import deepcopy
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
    elif no_trials:
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
        Reliant on '\\n', be careful.
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
        print msg
        # pass
    else:
        print msg
        # pass

def solve_print(board, constraint, choices, diag):
    ''' Pretty printing the output of a solver. '''
    solution_list, trials = solve(board, constraint, choices, diag)
    log('__________\n', GUI)
    log('number of trials: ' + str(trials), GUI)
    log('number of slns  : ' + str(len(solution_list)), GUI)
    log('__________\n', GUI)
    for i in range(len(solution_list)):
        log('Solution #' + str(i + 1)+'\n', GUI)
        log(stringify(solution_list[i], constraint), GUI)
        log('\n', GUI)
