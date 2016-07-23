#!/usr/bin/env python2
from utils_core import *
''' A module transforming the boards into an unique representation.
    Ngoc Tran - 2016 || underlandian.com
    '''

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
    ''' Create a letter-swap order after transforming the board. '''
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

def execute_changes(board, constraint, functions_used, swap_order,
                    reverse = False):
    ''' Execute all changes in list, including swapping.
        Includes optional reverse flag.
        '''
    
    # log(functions_used, DEV)
    # log(swap_order, DEV)
    # log(reverse, DEV)
    
    if reverse:
        for function in reversed(functions_used):
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
    ''' Return the complement transformation. '''
    if func is rotate_clockwise:
        return rotate_counter_clockwise
    elif func is rotate_counter_clockwise:
        return rotate_clockwise
    elif func is flip_horizontal or func is flip_vertical or \
            func is flip_diagonal or func is flip_anti_diagonal:
        return func
    else:
        return ValueError('not an invertible function')
