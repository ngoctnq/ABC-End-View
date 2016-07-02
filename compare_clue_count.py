#!/usr/bin/env python2
from utils_matrix import janko_get_text
from utils_nextgen import *
def compare_clue_count():
    dir = 'janko_stat/clue_compare.txt'
    file = open(dir, 'w')
    file.write("No.  Dim  Chc  Dgn  Prt  T/B  L/R  Dff  Rto\n")
    for i in range(530):
        board, constraint, choices, diag = janko_parser(janko_get_text(i+1))
        file.write(str(i+1).zfill(3))
        file.write('  ')
        dim = len(board)
        file.write(str(dim).ljust(3))
        file.write('  ')
        file.write(str(choices).ljust(3))
        file.write('  ')
        if diag:
            dgn = 1
        else:
            dgn = 0
        file.write(str(dgn).ljust(3))
        file.write('  ')
        file.write(str('N/A').ljust(3))
        file.write('  ')
        tb = 0
        for i in range(dim):
            if constraint[0][i] != '':
                tb += 1
            if constraint[1][i] != '':
                tb += 1
        file.write(str(tb).ljust(3))
        file.write('  ')
        lr = 0
        for i in range(dim):
            if constraint[2][i] != '':
                lr += 1
            if constraint[3][i] != '':
                lr += 1
        file.write(str(lr).ljust(3))
        file.write('  ')
        diff = abs(tb-lr)
        file.write(str(diff).ljust(3))
        file.write('  ')
        ratio = max(tb, lr)/min(tb, lr)
        file.write(str(ratio).ljust(3))
        file.write('\n')

if __name__ == '__main__':
    compare_clue_count()