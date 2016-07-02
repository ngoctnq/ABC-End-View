#!/usr/bin/env python2
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
logging = True
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
    ''' Remove a char from a label, and return if anything is changed.'''
    if char not in board[coord[0]][coord[1]]:
        return False
    else:
        board[coord[0]][coord[1]] = \
            board[coord[0]][coord[1]].replace(char, '')
        return True

def initial_reduction(board, constraint, choices):
    ''' Removes impossibles given by constraints.
        For example, if 'A' is given, with choices 'ABX' with dimension 4,
            then A cannot be in the last cell of a row/column.
        '''
    dim = get_dim(board)
    if 'X' in choices:
        len_choices_without_x = len(choices) - 1
    else:
        len_choices_without_x = len(choices)

    # top constraint
    for i in range(dim):
        for j in range(len_choices_without_x - 1):
            remove_char(board, [dim - 1 - j, i], constraint[0][i])
    # bottom constraint
    for i in range(dim):
        for j in range(len_choices_without_x - 1):
            remove_char(board, [j, i], constraint[1][i])
    # left constraint
    for i in range(dim):
        for j in range(len_choices_without_x - 1):
            remove_char(board, [i, dim - 1 - j], constraint[2][i])
    # right constraint
    for i in range(dim):
        for j in range(len_choices_without_x - 1):
            remove_char(board, [i, j], constraint[3][i])

def solve(board, constraint, choices, diag):
    ''' Master ABC Endview solver.
        Solve the board until unfilled is empty.
        '''
    dim = get_dim(board)
    initial_reduction(board, constraint, choices)
    unfilled = []
    for i in range(dim):
        for j in range(dim):
            unfilled.append([i,j])

    changed = True
    while changed and len(unfilled) != 0:
        changed = solve_core(board, constraint, choices, diag, unfilled)

def solve_core(board, constraint, choices, diag, unfilled):
    ''' Do propagation techniques here.
        Return whether anything have changed.
        '''
    changed = False
    for coord in unfilled:
        idx = unfilled.index(coord)
        deleted = True
        while deleted:
            if len(board[coord[0]][coord[1]] == 1):
                changed = update_after_fill(board, constraint,
                    choices, diag, coord) or changed
                del unfilled[idx]
            else:
                deleted = False
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

    # update on the row
    for i in range(dim):
        if i != y:
            changed = remove_char(board, [x, i], char) or changed

    # update on the column
    for i in range(dim):
        if i != x:
            changed = remove_char(board, [i, y], char) or changed

    # update on the diagonals
    if diag:
        if x == y:
            for i in range(dim):
                if i != x:
                    changed = remove_char(board, [i, i], char) or changed
        if x + y == dim - 1:
            for i in range(dim):
                if i != x:
                    changed = remove_char(board, [i, dim - 1 - i], char) \
                        or changed

    # update due to the max-X rule - then remove X from that row/column
    max_x = dim - len(choices) + 1

    # update due to constraint - all X til constraint's satisfied.

    return changed

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
    if logging:
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
    board, constraint, choices, diag = janko_parser(janko_get_text(480))
    print stringify(board, constraint, True)
