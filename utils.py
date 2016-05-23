#!/usr/bin/env python
from copy import deepcopy
from timeit import default_timer
import random
from Tkinter import *
import tkMessageBox
import urllib2
from bs4 import BeautifulSoup

# generate an empty constraint
def empty_constraint(dim):
    constraint = [[],[]]
    for i in range(dim):
        constraint[0].append(['',''])
        constraint[1].append(['',''])
    return constraint

# fill X's into the board, in case the board is done for
def reset_board(board):
    dim = len(board)
    for i in range(dim):
        for j in range(dim):
            board[i][j] = 'X'

# find the coords of the box with least possible choices
def min_coord(board):
    dim = len(board)
    curr = None
    currMin = 10 # arbitrary large number
    for i in range(dim):
        for j in range(dim):
            currLen = len(board[i][j])
            if currLen == 2:
                return [i,j]
            if currLen < currMin and currLen > 1:
                currMin = currLen
                curr = [i,j]
    return curr

# if all boxes have at most 1 possible choice
def is_deadend(board):
    dim = len(board)
    for i in range(dim):
        for j in range(dim):
            if len(board[i][j]) > 1:
                return False
    return True

# if all boxes have no boxes with 0 choices
def has_no_null(board):
    dim = len(board)
    for i in range(dim):
        for j in range(dim):
            if len(board[i][j]) == 0:
                return False
    return True

# if the board is still solvable - not considering constraints
def is_legit(board, choices, diag):
    dim = len(board)
    maxX = dim-len(choices)+1
    # check rows
    for i in range(dim):
        temp = ''
        count = 0
        for j in range(dim):
            if board[i][j] == 'X':
                count += 1
            temp += board[i][j]
        if count > maxX:
            return False
        for j in choices:
            if j not in temp:
                return False
    # check columns
    for i in range(dim):
        temp = ''
        count = 0
        for j in range(dim):
            if board[j][i] == 'X':
                count += 1
            temp += board[j][i]
        if count > maxX:
            return False
        for j in choices:
            if j not in temp:
                return False   

    # check diagonals
    if diag:
        temp = ''
        count = 0
        for j in range(dim):
            if board[j][j] == 'X':
                count += 1
            temp += board[j][j]
        if count > maxX:
            return False
        for j in choices:
            if j not in temp:
                return False

        temp = ''
        count = 0
        for j in range(dim):
            if board[j][dim-1-j] == 'X':
                count += 1
            temp += board[j][dim-1-j]
        if count > maxX:
            return False
        for j in choices:
            if j not in temp:
                return False   

    return True

# do human stuff to reduce bruteforce workload
def cancel_all(board, constraint, choices, diag):
    dim = len(constraint[0])
    maxX = dim-len(choices)+1
    changed = True
    while changed:
        changed = False
        # cancel first rows/columns - as nothing can occur before the constraint
        # check rows
        for i in range(dim):
            pos = 0
            if constraint[0][i][0] != '':
                while True:
                    if pos == dim:
                        break
                    if board[i][pos] == constraint[0][i][0]:
                        break
                    if board[i][pos] == 'X':
                        pos += 1
                    else:
                        for j in choices:
                            if j != 'X' and j != constraint[0][i][0]:
                                board[i][pos] = board[i][pos].replace(j,'')
                        break
            pos = -1
            if constraint[0][i][1] != '':
                while True:
                    if pos == -1-dim:
                        break
                    if board[i][pos] == constraint[0][i][1]:
                        break
                    if board[i][pos] == 'X':
                        pos -= 1
                    else:
                        for j in choices:
                            if j != 'X' and j != constraint[0][i][1]:
                                board[i][pos] = board[i][pos].replace(j,'')
                        break

        # check columns
        for i in range(dim):
            pos = 0
            if constraint[1][i][0] != '':
                while True:
                    if pos == dim:
                        break
                    if board[i][pos] == constraint[1][i][0]:
                        break
                    if board[pos][i] == 'X':
                        pos += 1
                    else:
                        for j in choices:
                            if j != 'X' and j != constraint[1][i][0]:
                                board[pos][i] = board[pos][i].replace(j,'')
                        break
            pos = -1
            if constraint[1][i][1] != '':
                while True:
                    if pos == -1-dim:
                        break
                    if board[pos][i] == constraint[1][i][1]:
                        break
                    if board[pos][i] == 'X':
                        pos -= 1
                    else:
                        for j in choices:
                            if j != 'X' and j != constraint[1][i][1]:
                                board[pos][i] = board[pos][i].replace(j,'')
                        break

        # check for assignments: if a row/column has only one box to put a char,
        # then that box gets that char
        for c in choices:
            if c != 'X':
                # check rows
                for i in range(dim):
                    count = 0
                    lastAppeared = -1
                    for j in range(dim):
                        if c in board[i][j]:
                            if c == board[i][j]:
                                count = -1
                                break
                            count += 1
                            lastAppeared = j
                    if count == 1:
                        changed = True
                        board[i][lastAppeared] = c
                        optimize(board,constraint,choices,diag,[i,lastAppeared])
                        cancel_all(board, constraint, choices, diag)
                        return

                # check columns
                for i in range(dim):
                    count = 0
                    lastAppeared = -1
                    for j in range(dim):
                        if c in board[j][i]:
                            if c == board[j][i]:
                                count = -1
                                break
                            count += 1
                            lastAppeared = j
                    if count == 1:
                        changed = True
                        board[lastAppeared][i] = c
                        optimize(board,constraint,choices,diag,[lastAppeared,i])
                        cancel_all(board, constraint, choices, diag)
                        return

                # check diagonals
                if diag:
                    count = 0
                    lastAppeared = -1
                    for j in range(dim):
                        if c in board[j][j]:
                            if c == board[j][j]:
                                count = -1
                                break
                            count += 1
                            lastAppeared = j
                    if count == 1:
                        changed = True
                        board[lastAppeared][lastAppeared] = c
                        optimize(board,constraint,choices,diag,[lastAppeared,lastAppeared])
                        cancel_all(board, constraint, choices, diag)
                        return

                    count = 0
                    lastAppeared = -1
                    for j in range(dim):
                        if c in board[j][dim-1-j]:
                            if c == board[j][dim-1-j]:
                                count = -1
                                break
                            count += 1
                            lastAppeared = j
                    if count == 1:
                        changed = True
                        board[lastAppeared][dim-1-lastAppeared] = c
                        optimize(board,constraint,choices,diag,[lastAppeared,dim-1-lastAppeared])
                        cancel_all(board, constraint, choices, diag)
                        return
            else:
                # check rows
                for i in range(dim):
                    xcount = 0
                    xcount_pos = []
                    for j in range(dim):
                        if board[i][j] == c:
                            xcount += 1
                        if c in board[i][j]:
                            xcount_pos.append(j)
                    if xcount == maxX:
                        for j in range(dim):
                            if board[i][j] != c:
                                board[i][j] = board[i][j].replace(c,'')
                    elif len(xcount_pos) == maxX:
                        for j in xcount_pos:
                            board[i][j] = 'X'

                # check columns
                for i in range(dim):
                    xcount = 0
                    xcount_pos = []
                    for j in range(dim):
                        if board[j][i] == c:
                            xcount += 1
                        if c in board[j][i]:
                            xcount_pos.append(j)
                    if xcount == maxX:
                        for j in range(dim):
                            if board[j][i] != c:
                                board[j][i] = board[j][i].replace(c,'')
                    elif len(xcount_pos) == maxX:
                        for j in xcount_pos:
                            board[j][i] = 'X'

                # check diagonals
                if diag:
                    xcount = 0
                    xcout_pos = []
                    for j in range(dim):
                        if board[j][j] == c:
                            xcount += 1
                        if c in board[j][j]:
                            xcount_pos.append(j)
                    if xcount == maxX:
                        for j in range(dim):
                            if board[j][j] != c:
                                board[j][j] = board[j][j].replace(c,'')
                    elif len(xcount_pos) == maxX:
                        for j in xcount_pos:
                            board[j][j] = 'X'

                    xcount = 0
                    xcount_pos = []
                    for j in range(dim):
                        if board[j][dim-1-j] == c:
                            xcount += 1
                        if c in board[j][dim-1-j]:
                            xcount_pos.append(j)
                    if xcount == maxX:
                        for j in range(dim):
                            if board[j][dim-1-j] != c:
                                board[j][dim-1-j] = board[j][dim-1-j].replace(c,'')
                    elif len(xcount_pos) == maxX:
                        for j in xcount_pos:
                            board[j][dim-1-j] = 'X'

# considering a filled box of coord, do human stuff on the lines the box is in
def optimize(board, constraint, choices, diag, coord):
    dim = len(board)
    if not is_legit(board, choices, diag):
        reset_board(board)
        return
    # check top
    if board[coord[0]][coord[1]] != '':
        # check rows
        if board[coord[0]][coord[1]] == constraint[0][coord[0]][0]:
            for j in range(coord[1]):
                board[coord[0]][j] = 'X'
        if board[coord[0]][coord[1]] == constraint[0][coord[0]][1]:
            for j in range(coord[1]+1,dim):
                board[coord[0]][j] = 'X'
        # check columns
        if board[coord[0]][coord[1]] == constraint[1][coord[1]][0]:
            for i in range(coord[0]):
                board[i][coord[1]] = 'X'
        if board[coord[0]][coord[1]] == constraint[1][coord[1]][1]:
            for i in range(coord[0]+1,dim):
                board[i][coord[1]] = 'X'

    # clear all
    if len(board[coord[0]][coord[1]]) != 1:
        raise ValueError('Not supposed to reduce a nonsingular string!')
    if board[coord[0]][coord[1]] != 'X':
        for i in range(dim):
            if i != coord[0]:
                board[i][coord[1]] = board[i][coord[1]].replace(board[coord[0]][coord[1]],'')
        for j in range(dim):
            if j != coord[1]:
                board[coord[0]][j] = board[coord[0]][j].replace(board[coord[0]][coord[1]],'')
        if diag:
            if coord[0] == coord[1]:
                for i in range(dim):
                    if i != coord[0]:
                        board[i][i] = board[i][i].replace(board[coord[0]][coord[1]],'')
            if coord[0]+coord[1] == dim-1:
                for i in range(dim):
                    if i != coord[0]:
                        board[i][dim-1-i] = board[i][dim-1-i].replace(board[coord[0]][coord[1]],'')
    else: # if an X is filled, recancel constraints.
        # check row, beginning
        xcount = 0
        for i in range(dim-len(choices)+1, dim):
            if board[coord[0]][i] == 'X':
                xcount += 1
        maxConstraint = dim - len(choices) + 1 - xcount
        for i in range(maxConstraint+1, dim-len(choices)+2):
            board[coord[0]][i] = board[coord[0]][i].replace(constraint[0][coord[0]][0],'')
        # check row, end
        xcount = 0
        for i in range(0, len(choices)-1):
            if board[coord[0]][i] == 'X':
                xcount += 1
        maxConstraint = dim - len(choices) + 1 - xcount
        for i in range(len(choices)-2, dim-maxConstraint-1):
            board[coord[0]][i] = board[coord[0]][i].replace(constraint[0][coord[0]][1],'')
        # check column, beginning
        xcount = 0
        for i in range(dim-len(choices)+1, dim):
            if board[i][coord[1]] == 'X':
                xcount += 1
        maxConstraint = dim - len(choices) + 1 - xcount
        for i in range(maxConstraint+1, dim-len(choices)+2):
            board[i][coord[1]] = board[i][coord[1]].replace(constraint[1][coord[1]][0],'')
        # check column, end
        xcount = 0
        for i in range(0, len(choices)-1):
            if board[i][coord[1]] == 'X':
                xcount += 1
        maxConstraint = dim - len(choices) + 1 - xcount
        for i in range(len(choices)-2, dim-maxConstraint-1):
            board[i][coord[1]] = board[i][coord[1]].replace(constraint[1][coord[1]][1],'')

    # TODO: unoptimized as cancel all board rather than
    # just one character and its corresponding columns and rows
    cancel_all(board, constraint, choices, diag)

# print the border, used in printOut
def printBorder(maxChar, dim):
    print ' ',
    for i in range(dim):
        print '+',
        print '-'*maxChar,
    print '+ '

# pretty printing the board
def printOut(board, constraint = None):
    dim = len(board)
    if constraint == None:
        constraint = [[],[]]
        for i in range(dim):
            constraint[0].append(['',''])
            constraint[1].append(['',''])
    maxChar = 0
    for i in range(dim):
        for j in range(dim):
            if maxChar < len(board[i][j]):
                maxChar = len(board[i][j])
    
    print '   ',
    for i in range(dim):
        print constraint[1][i][0].center(maxChar),
        print ' ',
    print

    for i in range(dim):
        printBorder(maxChar, dim)
        print constraint[0][i][0].center(1),
        for j in range(dim):
            print '|',
            if board[i][j] == 'X':
                print '.'.center(maxChar),
            else:
                print board[i][j].center(maxChar),
        print '|',
        print constraint[0][i][1].center(1)
    printBorder(maxChar,dim)
    print '   ',
    for i in range(dim):
        print constraint[1][i][1].center(maxChar),
        print ' ',
    print

# call optimize on all filled boxes
def mass_optimize(board, constraint, choices, diag):
    dim = len(board)
    if not is_legit(board, choices, diag):
        reset_board(board)
        return
    for i in range(dim):
        for j in range(dim):
            if len(board[i][j]) == 1:
                optimize(board,constraint,choices,diag,[i,j])

# make the initial board to be solved based on constraints and choices
def init_board(constraint, choices, diag):
    # yo fuck Python and its initialization man
    dim = len(constraint[0])
    board = []
    for i in range(dim):
        board.append([])
        for j in range(dim):
            board[i].append(choices)
    # optimize
    for i in range(dim):
        # head // j = 0
        for j in range(dim-len(choices)+2, dim):
            board[i][j] = board[i][j].replace(constraint[0][i][0],'')
            board[j][i] = board[j][i].replace(constraint[1][i][0],'')
        # toe // j = 1
        for j in range(0, len(choices)-2):
            board[i][j] = board[i][j].replace(constraint[0][i][1],'')
            board[j][i] = board[j][i].replace(constraint[1][i][1],'')
    # check only case
    cancel_all(board, constraint, choices, diag)
    mass_optimize(board, constraint, choices, diag)
    return board

# solve the puzzle with given parameters - choices is [trials_count, expansions_count]
def solve_core(shit_to_solve, constraint, choices, diag, solutions_list, counts):
    board = shit_to_solve.pop()
    # counts are, respectively, trials and expansions counts.
    counts[0] += 1

    if is_legit(board, choices, diag):
        if is_deadend(board):
            # then it is a solution
            solutions_list.append(board)
        
            # if short_circuit:    
            #     shit_to_solve[:] = []
            #     return
        else:
            if has_no_null(board):
                minc = min_coord(board)
                if minc == None:
                    return

                counts[1] += 1

                new_board = deepcopy(board)
                new_board[minc[0]][minc[1]] = new_board[minc[0]][minc[1]][0]
                board[minc[0]][minc[1]] = board[minc[0]][minc[1]][1:]
                
                cancel_all(board, constraint, choices, diag)
                cancel_all(new_board, constraint, choices, diag)
                mass_optimize(board, constraint, choices, diag)
                mass_optimize(new_board, constraint, choices, diag)
                
                shit_to_solve.append(board)
                shit_to_solve.append(new_board)

# check if after cancelling, the answer is given
def solvable_without_trials(constraint, choices, diag):
    board = init_board(constraint, choices, diag)
    ret = is_legit(board, choices, diag) and is_deadend(board)
    return ret

# comprehensive solving
def solve(constraint, choices, diag, short_circuit = False):
    shit_to_solve = [init_board(constraint, choices, diag)]
    # counts are trials and expansions, respectively
    counts = [0,0]
    solutions_list = []
    while len(shit_to_solve) != 0 and (len(solutions_list) < 2 or not short_circuit):
        solve_core(shit_to_solve, constraint, choices, diag, solutions_list, counts)
    return [solutions_list, counts]

# would stop abruptly if a second solution is found
def solve_from_partial(board, constraint, choices, diag, short_circuit = False):
    shit_to_solve = [board]
    # counts are trials and expansions, respectively
    counts = [0,0]
    solutions_list = []
    while len(shit_to_solve) != 0 and (len(solutions_list) < 2 or not short_circuit):
        # printOut(shit_to_solve[0])
        solve_core(shit_to_solve, constraint, choices, diag, solutions_list, counts)
    return [solutions_list, counts]

# check if having unique solutions ?/ EXCEPTION for board being at bottom of param list
def has_unique_solution(constraint, choices, diag):
    return 1 == len(solve(constraint, choices, diag, True)[0])

# keeps removing constraints til least solvable
def reduce_constraints(constraint, choices, diag, criteria):
    cons = available_constraints(constraint)
    temp = ''
    pos_temp = [-1,-1,-1]
    dim = len(constraint[0])
    while len(cons) > 0:
        # print len(cons)
        if criteria(constraint, choices, diag):
            pos = random.randrange(len(cons))
            temp = constraint[cons[pos][0]][cons[pos][1]][cons[pos][2]]
            pos_temp = cons[pos]
            constraint[cons[pos][0]][cons[pos][1]][cons[pos][2]] = ''
            del cons[pos]
        else:
            if len(cons) == 4*dim:
                print 'RIP - this board does not have an unique solution even with all available clues.'
                return
            constraint[pos_temp[0]][pos_temp[1]][pos_temp[2]] = temp
    if not criteria(constraint, choices, diag):
        constraint[pos_temp[0]][pos_temp[1]][pos_temp[2]] = temp

# return the positions of all unfilled boxes - NOT min_coord
def available_boxes(board):
    dim = len(board)
    ret = []
    for i in range(dim):
        for j in range(dim):
            if len(board[i][j]) > 1:
                ret.append([i,j])
    return ret

# NOT WORKING PROPERLY
# generate a board with given dimension and choices, if not working, retry.
def generate(dim, choices_no_x, diag, trials_count = 1):
    tic = default_timer()
    choices = choices_no_x.upper() + 'X'
    constraint = empty_constraint(dim)
    board = init_board(constraint, choices, diag)
    # temp_board = None

    if diag:
        # generate main diagonal first
        to_permute = list(choices + 'X'*(dim - len(choices)))
        random.shuffle(to_permute)
        for i in range(dim):
            board[i][i] = to_permute[i]
        cancel_all(board, constraint, choices, diag)
        mass_optimize(board, constraint, choices, diag)
        # do not generate antidiagonal, it can end up having zero solutions.

    while True:
        deadend = is_deadend(board)
        legit = is_legit(board, choices, diag)
        if legit and not deadend:
            # printOut(board)
            # temp_board = deepcopy(board)
            avail = available_boxes(board)
            pos = avail[random.randrange(len(avail))]
            x = pos[0]
            y = pos[1]
            z = random.randrange(len(board[x][y]))
            # print x,y,board[x][y][z]
            board[x][y] = board[x][y][z]
            optimize(board, constraint, choices, diag, [x,y])
            mass_optimize(board, constraint, choices, diag)
        elif legit:
            toc = default_timer()
            print "taken",toc-tic,"seconds"
            return board
        else:
            print "deadend, retrying..."
            toc = default_timer()
            print "taken",toc-tic,"seconds"
            # printOut(temp_board)
            # printOut(board)
            # board = temp_board
            return generate(dim, choices_no_x, diag, trials_count+1)

# generate full constraints for a given board
def generate_constraint(board):
    dim = len(board[0])
    constraint = [[],[]]
    for i in range(dim):
        constraint[0].append(['',''])
        constraint[1].append(['',''])
    # check rows
    for i in range(dim):
        # beginning
        pos = 0
        while board[i][pos] == 'X':
            pos += 1
        constraint[0][i][0] = board[i][pos]
        # end
        pos = -1
        while board[i][pos] == 'X':
            pos -= 1
        constraint[0][i][1] = board[i][pos]
    # check columns
    for i in range(dim):
        # beginning
        pos = 0
        while board[pos][i] == 'X':
            pos += 1
        constraint[1][i][0] = board[pos][i]
        # end
        pos = -1
        while board[pos][i] == 'X':
            pos -= 1
        constraint[1][i][1] = board[pos][i]
    return constraint

# return positions of all the constraints there are
def available_constraints(constraint):
    acc = []
    for i in range(2):
        for j in range(len(constraint[0])):
            for k in range(2):
                if constraint[i][j][k] != '':
                    acc.append([i,j,k])
    return acc 

# check if 2 boards are equal
def equal(board1, board2):
    dim = len(board1)
    for i in range(dim):
        for j in range(dim):
            if board1[i][j]!=board2[i][j]:
                return False
    return True 

# check if all are capital and sequential from A
def not_cap_chars(word):
    for i in range(len(word)):
        if ord(word[i]) != ord('A')+i:
            return True
    return False

# solver function - GUI asking for input
def solver_gui():
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

    constraint = [[],[]]
    for i in range(dim):
        constraint[0].append(['',''])
        constraint[1].append(['',''])
    #______________
    not_entered = True
    while not_entered:
        choices = raw_input("Characters to fill in, with no delimiters: ").upper()
        if not_cap_chars(choices):
            print "String error!", "Only sequencial capital letters are allowed."
        elif len(choices) >= dim:
            print "String error!", "Number of choices must be less than "+str(dim)+"."
        else:
            not_entered = False
    #______________
    not_entered = True
    while not_entered:
        constraint_sub = raw_input("Insert row-beginning constraints - Continuously, '-' for none: ").upper()
        if len(constraint_sub) != dim:
            print "Constraints error!", "Number of constraints must be exactly "+str(dim)+"."
        else:
            legit = True
            while legit:
                for i in range(dim):
                    if constraint_sub[i] in choices:
                        constraint[0][i][0] = constraint_sub[i]
                    elif constraint_sub[i] != '-':
                        legit = False
                        print "String error!", constraint_sub[i]+" is not a valid entry!"
                        break
                if i == dim-1:
                    break
            if legit:
                not_entered = False
    #______________
    not_entered = True
    while not_entered:
        constraint_sub = raw_input("Insert row-ending constraints - Continuously, '-' for none: ").upper()
        if len(constraint_sub) != dim:
            print "Constraints error!", "Number of constraints must be exactly "+str(dim)+"."
        else:
            legit = True
            while legit:
                for i in range(dim):
                    if constraint_sub[i] in choices:
                        constraint[0][i][1] = constraint_sub[i]
                    elif constraint_sub[i] != '-':
                        legit = False
                        print "String error!", constraint_sub[i]+" is not a valid entry!"
                        break
                if i == dim-1:
                    break
            if legit:
                not_entered = False
    #______________
    not_entered = True
    while not_entered:
        constraint_sub = raw_input("Insert column-beginning constraints - Continuously, '-' for none: ").upper()
        if len(constraint_sub) != dim:
            print "Constraints error!", "Number of constraints must be exactly "+str(dim)+"."
        else:
            legit = True
            while legit:
                for i in range(dim):
                    if constraint_sub[i] in choices:
                        constraint[1][i][0] = constraint_sub[i]
                    elif constraint_sub[i] != '-':
                        legit = False
                        print "String error!", constraint_sub[i]+" is not a valid entry!"
                        break
                if i == dim-1:
                    break
            if legit:
                not_entered = False
    #______________
    not_entered = True
    while not_entered:
        constraint_sub = raw_input("Insert column-ending constraints - Continuously, '-' for none: ").upper()
        if len(constraint_sub) != dim:
            print "Constraints error!", "Number of constraints must be exactly "+str(dim)+"."
        else:
            legit = True
            while legit:
                for i in range(dim):
                    if constraint_sub[i] in choices:
                        constraint[1][i][1] = constraint_sub[i]
                    elif constraint_sub[i] != '-':
                        legit = False
                        print "String error!", constraint_sub[i]+" is not a valid entry!"
                        break
                if i == dim-1:
                    break
            if legit:
                not_entered = False
    #______________     
    not_entered = True
    while not_entered:
        not_entered = False
        result = raw_input("Are diagonals required to have all characters? ").upper()
        if result in ['YES','Y','1']:
            diag = True
        elif result in ['NO','N','0']:
            diag = False
        else:
            print 'Not a valid answer!'
            not_entered = True
    #______________
    # start initializing
    choices += 'X'
    result = solve(constraint, choices, diag)
    solutions_list = result[0]
    counts = result[1]
    for i in range(len(solutions_list)):
        print 'Solution #'+str(i+1)+"\n"
        printOut(solutions_list[i], constraint)
        print
    print "total number of solutions:", len(solutions_list)
    print "total number of trials:", counts[0]
    print "total number of expansions:", counts[1]

def solver_janko():
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
    url = 'http://www.janko.at/Raetsel/Abc-End-View/'+str(no).zfill(3)+'.a.htm'
    file = urllib2.urlopen(url)
    html_doc = file.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = soup.data
    print data

    choices += 'X'
    result = solve(constraint, choices, diag)
    solutions_list = result[0]
    counts = result[1]
    for i in range(len(solutions_list)):
        print 'Solution #'+str(i+1)+"\n"
        printOut(solutions_list[i], constraint)
        print
    print "total number of solutions:", len(solutions_list)
    print "total number of trials:", counts[0]
    print "total number of expansions:", counts[1]

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

solver_janko()