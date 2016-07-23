#!/usr/bin/env python2
from utils_core import *
from utils_generator import *

def solve2(board, constraint, choices, diag = False, short_circuit = False,
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

    trials = solve_core2(board, constraint, choices, diag,
        unfilled, solution_list, short_circuit, no_trials)

    if short_circuit:
        return len(solution_list)
    elif no_trials:
        return solution_list[0]
    else:
        return solution_list, trials

def solve_core2(board, constraint, choices, diag, unfilled, solution_list,
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
        return solve_core2(board, constraint, choices, diag,
            unfilled, solution_list, short_circuit, no_trials)
    else:
        if no_trials:
            solution_list.append(board)
            return 0

        # if everything is filled
        if len(unfilled) == 0:
            generate_prefill2(board, choices, diag)
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
            solve_core2(new_board, constraint, choices, diag,
                new_unfilled, solution_list, short_circuit) + \
            solve_core2(board, constraint, choices, diag,
                unfilled, solution_list, short_circuit)

def generate_prefill2(board, choices, diag = False):
    ''' Generate from a prefilled Latin board. '''
    dim = get_dim(board)
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

    constraint = generate_endview_constraint(board)
    if solve(empty_board, constraint, choices, diag, True) == 1:
        print
        print stringify(board, constraint)
        exit()
    else:
        sys.stdout.write('.')
        sys.stdout.flush()

def createString(num):
    string = ""
    for i in range(num):
        string += chr(65+i)
    return string

if __name__ == '__main__':
    dim = 6
    board = generate_empty_board(dim)
    constraint = generate_empty_constraint(dim)
    choices = createString(dim)
    diag = False
    populate_empty_board(board, choices)
    for i in range(dim):
        board[0][i] = chr(ord('A') + i)
    solve2(board, constraint, choices, diag)