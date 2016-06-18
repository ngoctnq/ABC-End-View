#!/usr/bin/env python
import urllib2
from bs4 import BeautifulSoup
from utils import *
import sys

stat = {}

def constraint_count(constraint):
    count = 0
    dim = len(constraint[0])
    for i in range(2):
        for j in range(dim):
            for k in range(2):
                if constraint[i][j][k] != '':
                    count += 1
    return count

def add_stat(constraint, choices, diag, partial):
    if diag:
        diagi = 1
    else:
        diagi = 0
    if partial:
        partiali = 1
    else:
        partiali = 0
    try:
        stat[(len(constraint[0]),len(choices)-1,diagi,partiali)] =\
        min(constraint_count(constraint),
            stat[((len(constraint[0]),len(choices)-1,diagi,partiali))])
    except:
        stat[(len(constraint[0]),len(choices)-1,diagi,partiali)] =\
        constraint_count(constraint)

def solver_janko(no = 0, pass_on = False):
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

    url = 'http://www.janko.at/Raetsel/Abc-End-View/'+str(no).zfill(3)+'.a.htm'
    file = urllib2.urlopen(url)
    html_doc = file.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = soup.data.get_text().split('\n')

    choices = ''
    diag = False
    constraint = [[],[]]
    partial = False
    del data[0]
    del data[-1]

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
            for i in range(dim):
                constraint[0].append(['',''])
                constraint[1].append(['',''])
            attributes.remove('size')
        if data[0].split()[0] == 'depth':
            depth = int(data[0].split()[1])
            attributes.remove('depth')
            for i in range(depth):
                choices += chr(ord('A')+i)
            if dim > len(choices):
                choices += 'X'
        if data[0].split()[0] == 'options':
            attributes.remove('options')
            diag = True
        # top/bottom
        if data[0].split()[0] == 'clabels':
            attributes.remove('clabels')
            del data[0]
            topConstraint = data[0].upper().encode('ascii','ignore').split()
            for i in range(dim):
                if topConstraint[i] != '-':
                    try:
                        constraint[1][i][0] = chr(int(topConstraint[i])+ord('A')-1)
                    except:
                        constraint[1][i][0] = topConstraint[i]
            del data[0]
            del topConstraint
            #__________
            bottomConstraint = data[0].upper().encode('ascii','ignore').split()
            for i in range(dim):
                if bottomConstraint[i] != '-':
                    try:
                        constraint[1][i][1] = chr(int(bottomConstraint[i])+ord('A')-1)
                    except:
                        constraint[1][i][1] = bottomConstraint[i]
            del data[0]
            del bottomConstraint
            #__________
        # left/right
        if data[0].split()[0] == 'rlabels':
            attributes.remove('rlabels')
            del data[0]
            leftConstraint = data[0].upper().encode('ascii','ignore').split()
            for i in range(dim):
                if leftConstraint[i] != '-':
                    try:
                        constraint[0][i][0] = chr(int(leftConstraint[i])+ord('A')-1)
                    except:
                        constraint[0][i][0] = leftConstraint[i]
            del data[0]
            del leftConstraint
            #__________
            rightConstraint = data[0].upper().encode('ascii','ignore').split()
            for i in range(dim):
                if rightConstraint[i] != '-':
                    try:
                        constraint[0][i][1] = chr(int(rightConstraint[i])+ord('A')-1)
                    except:
                        constraint[0][i][1] = rightConstraint[i]
            del data[0]
            del rightConstraint
        # problem lmao
        if data[0].split()[0] == 'problem':
            attributes.remove('problem')
            del data[0]
            partial = True
            board = init_board(constraint, choices, diag)
            for i in range(dim):
                clues = data[0].upper().encode('ascii','ignore').split()
                del data[0]
                for j in range(dim):
                    if clues[j] != '-':
                        board[i][j] = clues[j]
            cancel_all(board, constraint, choices, diag)
            mass_optimize(board, constraint, choices, diag)

    add_stat(constraint, choices, diag, partial)
    
    # print constraint, partial, choices
    # printOut(init_board(constraint, choices, diag))
    if not partial:
        result = solve(constraint, choices, diag)
    else:
        result = solve_from_partial(board, constraint, choices, diag)
    if pass_on:
        return result
    else:
        solutions_list = result[0]
        counts = result[1]
        for i in range(len(solutions_list)):
            print 'Solution #'+str(i+1)+"\n"
            printOut(solutions_list[i], constraint)
            print
        print "total number of solutions:", len(solutions_list)
        print "total number of trials:", counts[0]
        print "total number of expansions:", counts[1]

def janko_mass_solve(file_name = 'janko_time', file_mode = 'w', skip = True):
    try:
        f = open(file_name, file_mode)
        f.write('Problem no. No. of slns Trials      Expansions\n')
        for i in range(530):
            i += 1
            if skip:
                if i == 480:
                    continue
            print i
            solution = solver_janko(i, True)
            detail = solution[1]
            f.write(str(i).ljust(12))
            f.write(str(len(solution[0])).ljust(12))
            f.write(str(detail[0]).ljust(12))
            f.write(str(detail[1]).ljust(12))
            f.write('\n')

        f.close()
    except:
        f.close()
        raise

def solve_480():
    orig_stdout = sys.stdout
    result = solver_janko(480, True)
    f = open('480_general','w')
    f.write(str(len(result[0]))+' '+str(result[1][0])+' '+str(result[1][1]))
    f.close()

    for i in range(len(result[0])):
        f = open('480_'+str(i).zfill(5),'w')
        sys.stdout = f
        printOut(result[0][i])
        f.close()

    sys.stdout = orig_stdout

def solve_480_with_sort():
    result = solver_janko(480, True)
    print 'stat', result[1]
    solutions_list = result[0]
    solutions_list.sort()
    duplicate = 0
    for i in range(len(solutions_list)-1):
        if solutions_list[i] == solutions_list[i+1]:
            duplicate += 1
    print 'duplicate', duplicate

def janko_mass_stat():
    for i in range(530):
        i += 1
        if i == 480:
            continue
        print i
        solver_janko(i, True)
    for i in stat:
        print i, stat[i]

if __name__ == "__main__":
    janko_mass_solve()
    # solver_janko(61)