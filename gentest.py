import random
from utils import *

def available_boxes(board):
    dim = len(board)
    ret = []
    for i in range(dim):
        for j in range(dim):
            if len(board[i][j]) > 1:
                ret.append([i,j])
    return ret

def generate(dim, choices, diag):
    choices = choices.upper() + 'X'
    constraint = [[],[]]
    for i in range(dim):
        constraint[0].append(['',''])
        constraint[1].append(['',''])
    board = init_board(constraint, choices, diag)
    while not is_deadend(board):
        avail = available_boxes(board)
        pos = avail[random.randrange(len(avail))]
        x = pos[0]
        y = pos[1]
        z = random.randrange(len(board[x][y]))
        board[x][y] = board[x][y][z]
        optimize(board, constraint, choices, diag, [x,y])
        mass_optimize(board, constraint, choices, diag)
    return board
    
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

def available_constraints(constraint):
    acc = []
    for i in range(2):
        for j in range(len(constraint[0])):
            for k in range(2):
                if constraint[i][j][k] != '':
                    acc.append([i,j,k])
    return acc

def reduce_constraints(constraint, choices, diag):
    cons = available_constraints(constraint)
    temp = ''
    pos_temp = [-1,-1,-1]
    while len(cons) > 0:
        if solvable_without_trials(constraint, choices, diag):
            pos = random.randrange(len(cons))
            temp = constraint[cons[pos][0]][cons[pos][1]][cons[pos][2]]
            pos_temp = cons[pos]
            constraint[cons[pos][0]][cons[pos][1]][cons[pos][2]] = ''
            del cons[pos]
        else:
            constraint[pos_temp[0]][pos_temp[1]][pos_temp[2]] = temp
    if not solvable_without_trials(constraint, choices, diag):
        constraint[pos_temp[0]][pos_temp[1]][pos_temp[2]] = temp

def test():
    dim = 3
    length_of_choices = 2
    bool_int = 0
    if bool_int == 0: 
        diag = False
    else:
        diag = True
    choices = ''
    for i in range(length_of_choices):
        choices += chr(ord('A')+i)
    board = generate(dim, choices, diag)
    constraint = generate_constraint(board)
    choices += 'X'
    reduce_constraints(constraint, choices, diag)
    print constraint
    print init_board(constraint, choices, diag)
