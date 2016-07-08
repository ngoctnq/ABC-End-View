# SCRATCH PLACE - FOR DELETED CODE WHICH MIGHT BE USEFUL LATER

def bak_compare_3_edges_of_left_corners(board, constraint):
    val2_top = count_unique(constraint[0])
    val2_bot = count_unique(constraint[1])
    val2_left_1 = count_unique(constraint[2])
    val2_left_2 = count_unique(constraint[2][::-1])
    if val2_top < val2_bot or (val2_top == val2_bot and
            val2_left_1 < val2_left_2):
        flip_vertical(board, constraint)

def bak_convert_to_family_generator(board, constraint, choices):
    ''' Return a new permutation of top-bottom-left-right
        that is the family's generator.
        '''
    val1_top = count_element(constraint[0])
    val1_bot = count_element(constraint[1])
    val1_left = count_element(constraint[2])
    val1_right = count_element(constraint[3])
    val1_list = [val1_top, val1_bot, val1_left, val1_right]
    val1_max = max(val1_list)
    max1_count = val1_list.count(val1_max)
    if max1_count == 1:
        max1_pos = val1_list.index(val1_max)
        if max1_pos == 1:
            flip_vertical(board, constraint)
        elif max1_pos == 2:
            rotate_clockwise(board, constraint)
        elif max1_pos == 3:
            rotate_counter_clockwise(board, constraint)
        compare_left_and_right(board, constraint)
    elif max1_count == 2:
        if (val1_top == val1_max and val1_bot == val1_max) or \
                (val1_left == val1_max and val1_right == val1_max):
            if val1_left == val1_max and val1_right == val1_max:
                rotate_clockwise(board, constraint)
            compare_left_and_right(board, constraint)
            compare_top_and_bottom(board, constraint)
        else:
            if val1_top == val1_max and val1_right == val1_max:
                flip_horizontal(board, constraint)
            elif val1_bot == val1_max:
                if val1_left == val1_max:
                    flip_vertical(board, constraint)
                elif val1_right == val1_max:
                    rotate_clockwise(board, constraint)
                    rotate_clockwise(board, constraint)
            val1_bot = count_element(constraint[1])
            val1_right = count_element(constraint[3])
            if val1_bot < val1_right:
                flip_diagonal(board, constraint)
            elif val1_bot == val1_right:
                val2_top = count_unique(constraint[TOP])
                val2_left = count_unique(constraint[LEFT])
                if val2_top < val2_left:
                    flip_diagonal(board, constraint)
                elif val2_top == val2_left:
                    val2_bot = count_unique(constraint[BOTTOM])
                    val2_right = count_unique(constraint[RIGHT])
                    if val2_bot < val2_right:
                        flip_diagonal(board, constraint)
    elif max1_count == 3:
        if val1_top < val1_max:
            rotate_clockwise(board, constraint)
        elif val1_left < val1_max:
            flip_vertical(board, constraint)
        elif val1_bot < val1_max:
            rotate_counter_clockwise(board, constraint)
    else:
        # corners are numbered as follows:
        #   3   0
        #   2   1
        val2_corner0 = count_unique(constraint[0][::-1]) * \
            count_unique(constraint[3])
        val2_corner1 = count_unique(constraint[3][::-1]) * \
            count_unique(constraint[1][::-1])
        val2_corner2 = count_unique(constraint[1]) * \
            count_unique(constraint[2][::-1])
        val2_corner3 = count_unique(constraint[0]) * \
            count_unique(constraint[2])
        val2_corner_list = [val2_corner0, val2_corner1,
            val2_corner2, val2_corner3]
        val2_corner_max = max(val2_corner_list)
        max2_count = val2_corner_list.count(val2_corner_max)
        if max2_count == 1:
            if val2_corner0 == val2_corner_max:
                rotate_counter_clockwise(board, constraint)
            if val2_corner1 == val2_corner_max:
                rotate_clockwise(board, constraint)
                rotate_clockwise(board, constraint)
            if val2_corner2 == val2_corner_max:
                rotate_clockwise(board, constraint)

            val2_top = count_unique(constraint[0])
            val2_left = count_unique(constraint[2])
            if val2_top < val2_left:
                flip_diagonal(board, constraint)
        elif max2_count == 2:
            if val2_corner0 == val2_corner_max and \
                    val2_corner2 == val2_corner_max:
                rotate_counter_clockwise(board, constraint)
                compare_main_opposite_corners(board, constraint)
            elif val2_corner1 == val2_corner_max and \
                    val2_corner3 == val2_corner_max:
                compare_main_opposite_corners(board, constraint)
            else:
                if val2_corner0 == val2_corner_max:
                    if val2_corner3 == val2_corner_max:
                        rotate_counter_clockwise(board, constraint)
                    elif val2_corner1 == val2_corner_max:
                        rotate_clockwise(board, constraint)
                        rotate_clockwise(board, constraint)
                elif val2_corner2 == val2_corner_max and \
                        val2_corner1 == val2_corner_max:
                    rotate_clockwise(board, constraint)
                compare_3_edges_of_left_corners(board, constraint)
        elif max2_count == 3:
            if val2_corner0 < val2_corner_max:
                rotate_clockwise(board, constraint)
            elif val2_corner2 < val2_corner_max:
                rotate_counter_clockwise(board, constraint)
            elif val2_corner3 < val2_corner_max:
                rotate_clockwise(board, constraint)
                rotate_clockwise(board, constraint)
            val2_top = count_unique(constraint[0])
            val2_bot = count_unique(constraint[1])
            if val2_top < val2_bot:
                flip_vertical(board, constraint)
            elif val2_top == val2_bot:
                val2_left_1 = count_unique(constraint[2])
                val2_left_2 = count_unique(constraint[2][::-1])
                if val2_left_1 < val2_left_2:
                    flip_vertical(board, constraint)

    # log(stringify(board, constraint), DEV)

    # after transforming is swapping letters
    swap_letters_after_transformations(board, constraint, choices)

def bak_compare_left_and_right(board, constraint):
    ''' Compare if a horizontal flip is necessary.
        Return whether changed.
        '''
    val1_left = count_element(constraint[2])
    val1_right = count_element(constraint[3])
    val2_left = count_unique(constraint[2])
    val2_right = count_unique(constraint[3])
    if val1_left < val1_right or \
            (val1_left == val1_right and val2_left < val2_right):
        flip_horizontal(board, constraint)
        return True
    return False

def bak_compare_top_and_bottom(board, constraint):
    ''' Compare if a vertical flip is necessary.
        Return whether changed.
        '''
    val1_top = count_element(constraint[0])
    val1_bot = count_element(constraint[1])
    val2_top = count_unique(constraint[0])
    val2_bot = count_unique(constraint[1])
    if val1_top < val1_bot or \
            (val1_top == val1_bot and val2_top < val2_bot):
        flip_vertical(board, constraint)
        return True
    return False

def bak_compare_main_opposite_corners(board, constraint):
    val2_top = count_unique(constraint[0])
    val2_bot = count_unique(constraint[1][::-1])
    val2_left = count_unique(constraint[2])
    val2_right = count_unique(constraint[3][::-1])
    val2_list = [val2_top, val2_bot, val2_left, val2_right]
    val2_max = max(val2_list)
    max2_count = val2_list.count(val2_max)
    if max2_count == 1:
        if val2_bot == val2_max:
            rotate_clockwise(board, constraint)
            rotate_clockwise(board, constraint)
        elif val2_left == val2_max:
            flip_diagonal(board, constraint)
        elif val2_right == val2_max:
            flip_anti_diagonal(board, constraint)
    elif max2_count == 2:
        # diagonally symmetric
        if val2_left == val2_max:
            flip_diagonal(board, constraint)
    # 3 cannot happen, 4 doesn't matter (perfect symmetry)
