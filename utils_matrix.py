#!/usr/bin/env python2
from bs4 import BeautifulSoup
import urllib2

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

def get_dim(array):
    ''' The reverse of generation - getting the dimension from array. '''
    return len(array[0])

def generate_empty_equation():
    ''' Generate empty equation.
        Equation has the form [[list_of_members],[list_of_primes]]
        '''
    new_equation = []
    # prevent internal caching
    for i in range(2):
        new_equation.append([])
    return new_equation

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
            new_row.append(0)
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
            new_row.append(0)
        new_constraint.append(new_row)
    return new_constraint

# implementation note: something better than a nested list is good,
#   but unfortunately lists aren't hashable, and editability is required.
def generate_equation_list(board, constraint, choices, diag):
    ''' Initialize the requirement equations with given constraint.
        Note: skip ones with no constraints.

        board and constraint are nested list of integers.
        choices denote the length of possible character.
            e.g.: 3 means A, B, and C; or equivalently, 2, 3, and 5.
        diag denotes if the board has to have diagonals.
        '''
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

#   TODO: prove ring-ness or whatever. Probably will never get used.
def multiply(i, j):
    ''' New mulitiplication algorithm. '''
    if i == j:
        if i in primes and i != 1:
            return 0
    return i * j

def equation_list_check(board, equation_list):
    ''' Check for obvious fills or unsolvable equations.
        Returns whether anything is changed.
        '''
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
                log('filling ' + str(coord) + ' '
                    + int_to_char(constraint_equation[0][0]))
        # Latin constraint
        else:
            if len(constraint_equation[1]) == 0:
                for coord in constraint_equation[0]:
                    board[coord[0]][coord[1]] = 1
                    log('filling ' + str(coord) + ' X')
                changed = True
    return changed

def equation_list_reduction(board, equation_list):
    ''' Run constraint reduction on all equations which is in the list.
        Empty list means board is all filled.

        Status ints:
            +1 = satisfied
            +0 = unsatisfied
            -1 = invalid

        If constraint_list[0] is [],[-1],
            then the board is impossible. This is to help trial and error.
        '''
    log('change detected, running equation_list_reduction', 2)
    for constraint_equation in equation_list:
        status = equation_reduction(board, constraint_equation)
        if status == 1:
            del equation_list[equation_list.index(constraint_equation)]
        elif status == -1:
            log('WARNING: rare case -bug?- impossible Latin constraint', 0)
            equation_list[:] = [[[],[-1]]]
            break

def equation_reduction(board, constraint_equation):
    ''' Evaluate constraint reduction on each constraint equation.
        If both sides are equal, return True.
        Else, divides into border constraints and Latin constraints:
        - If border constraint (list of primes):
            Anything after a label different from constraint is negligible.
        - If Latin constraint (0 in result):
            Order does not matter.
        '''
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

def equation_list_init(board, constraint, choices, diag):
    ''' Run first when having a partial board.
        @return equation_list
        '''
    equation_list = generate_equation_list(board, constraint, choices, diag)
    equation_list_reduction(board, equation_list)
    return equation_list

# PRINTING SECTION
# __________

def generate_horizontal_border(dim):
    ''' Return one horizontal border.
        Used in printOut.
       '''
    hBorder = '  '
    for i in range(dim):
        hBorder += '+-'
        hBorder += '-'
        hBorder += '-'
    hBorder += '+'
    return hBorder

def int_to_char(i):
    ''' Return int to char.
        e.g., -1 is blank, 0 is - (X), 1 is A, and so on.
        '''
    if i > 1:
        return chr(ord('A') + primes.index(i) - 1)
    elif i == 1:
        return '-'
    elif i == 0:
        return ' '
    else:
        raise ValueError(str(i) + ' is not a valid int for a label')

def stringify(board, constraint = None):
    ''' Return a pretty printing the board.
        Reliant on '\n', be careful.
        '''
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

def log(msg, priority = 1):
    ''' for logging purposes, can change stream or write to file. '''
    if logging:
        print msg

# JANKO PARSER SECTION
# __________

# Note: commenting out if beautifulsoup4 is not present.
def janko_get_text(no = 0):
    ''' Get the problem from janko site.
        Will cache into a folder.
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
            attributes.remove('depth')
            choices = depth
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
                    try:
                        constraint[0][i] = chr(int(topConstraint[i])+ord('A')-1)
                    except:
                        constraint[0][i] = topConstraint[i]
            del data[0]
            del topConstraint
            #__________
            bottomConstraint = data[0].upper().split()
            for i in range(dim):
                if bottomConstraint[i] != '-':
                    try:
                        constraint[1][i] = chr(int(bottomConstraint[i])+ord('A')-1)
                    except:
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
                    try:
                        constraint[2][i] = chr(int(leftConstraint[i])+ord('A')-1)
                    except:
                        constraint[2][i] = leftConstraint[i]
            del data[0]
            del leftConstraint
            #__________
            rightConstraint = data[0].upper().split()
            for i in range(dim):
                if rightConstraint[i] != '-':
                    try:
                        constraint[3][i] = chr(int(rightConstraint[i])+ord('A')-1)
                    except:
                        constraint[3][i] = rightConstraint[i]
            del data[0]
            del rightConstraint
        # problem lmao
        board = generate_empty_board(dim)
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

    equation_list[8][0][2:] = []
    equation_list[10][0][1:3] = []

    equation_list = equation_list_init(board, constraint, 2, False)
    shabby_printing(board, constraint, equation_list)

    while True:
        if equation_list_check(board, equation_list) and \
                equation_list_reduction(board, equation_list) is None:
            shabby_printing(board, constraint, equation_list)
        else:
            break