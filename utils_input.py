#!/usr/bin/env python2
from utils_core import *
import sys
import urllib2
import importlib
''' A module taking input and solve Endview puzzles.
    Ngoc Tran - 2016 || underlandian.com
    '''

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
        log('file '+directory+' opened successfully.', LOG)
    except:
    	bs4 = importlib.import_module('bs4')
    	BeautifulSoup = getattr(bs4, 'BeautifulSoup')
        log('file '+directory+' does not exist, caching...', LOG)
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
        log('file '+directory+' saved successfully.', LOG)
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
                    constraint[0][i] = omni_to_letter(topConstraint[i])
            del data[0]
            del topConstraint
            #__________
            bottomConstraint = data[0].upper().split()
            for i in range(dim):
                if bottomConstraint[i] != '-':
                    constraint[1][i] = omni_to_letter(bottomConstraint[i])
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
                    constraint[2][i] = omni_to_letter(leftConstraint[i])
            del data[0]
            del leftConstraint
            #__________
            rightConstraint = data[0].upper().split()
            for i in range(dim):
                if rightConstraint[i] != '-':
                    constraint[3][i] = omni_to_letter(rightConstraint[i])
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
                        board[i][j] = omni_to_letter(clues[j])

    return board, constraint, choices, diag

# INPUT SECTION
#___________

def not_cap_chars(word):
    ''' Check if all are capital and sequential from A. '''
    if len(word) == 0:
        raise ValueError('no choices entered')
    for i in range(len(word)):
        if ord(word[i]) != ord('A')+i:
            return True
    return False

def omni_to_letter(c):
    ''' Convert number to letter. 
        Some problems on Janko has numbers instead of letters in the source
            code, confusing the solver.
        '''
    try:
        i = int(c)
        return chr(ord('A') - 1 + i)
    except:
        # not an int means its a normal character
        return c

def input_gui():
    ''' GUI to input a problem. '''
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

    constraint = generate_empty_constraint(dim)
    #______________
    not_entered = True
    while not_entered:
        choices = raw_input("Characters to fill in, with no delimiters: ") \
            .upper()
        if not_cap_chars(choices):
            print "String error!", "Only sequencial letters are allowed."
        elif len(choices) > dim:
            print "String error!", "Number of choices must be less than " + \
                "or equal to " + str(dim) + "."
        else:
            not_entered = False
    #______________
    not_entered = True
    while not_entered:
        constraint_sub = raw_input("Insert column-beginning constraints " + \
            "- Continuously, '-' for none: ").upper()
        if len(constraint_sub) != dim:
            print "Constraints error!", \
                "Number of constraints must be exactly "+str(dim)+"."
        else:
            legit = True
            while legit:
                for i in range(dim):
                    if constraint_sub[i] in choices:
                        constraint[0][i] = constraint_sub[i]
                    elif constraint_sub[i] != '-':
                        legit = False
                        print "String error!", constraint_sub[i] + \
                            " is not a valid entry!"
                        break
                if i == dim-1:
                    break
            if legit:
                not_entered = False
    #______________
    not_entered = True
    while not_entered:
        constraint_sub = raw_input("Insert column-ending constraints " + \
            "- Continuously, '-' for none: ").upper()
        if len(constraint_sub) != dim:
            print "Constraints error!", \
                "Number of constraints must be exactly "+str(dim)+"."
        else:
            legit = True
            while legit:
                for i in range(dim):
                    if constraint_sub[i] in choices:
                        constraint[1][i] = constraint_sub[i]
                    elif constraint_sub[i] != '-':
                        legit = False
                        print "String error!", constraint_sub[i] + \
                            " is not a valid entry!"
                        break
                if i == dim-1:
                    break
            if legit:
                not_entered = False
    #______________
    not_entered = True
    while not_entered:
        constraint_sub = raw_input("Insert row-beginning constraints - " + \
            "Continuously, '-' for none: ").upper()
        if len(constraint_sub) != dim:
            print "Constraints error!", \
                "Number of constraints must be exactly " + str(dim) + "."
        else:
            legit = True
            while legit:
                for i in range(dim):
                    if constraint_sub[i] in choices:
                        constraint[2][i] = constraint_sub[i]
                    elif constraint_sub[i] != '-':
                        legit = False
                        print "String error!", constraint_sub[i] + \
                            " is not a valid entry!"
                        break
                if i == dim-1:
                    break
            if legit:
                not_entered = False
    #______________
    not_entered = True
    while not_entered:
        constraint_sub = raw_input("Insert row-ending constraints - " + \
            "Continuously, '-' for none: ").upper()
        if len(constraint_sub) != dim:
            print "Constraints error!", \
                "Number of constraints must be exactly "+str(dim)+"."
        else:
            legit = True
            while legit:
                for i in range(dim):
                    if constraint_sub[i] in choices:
                        constraint[3][i] = constraint_sub[i]
                    elif constraint_sub[i] != '-':
                        legit = False
                        print "String error!", constraint_sub[i]+\
                            " is not a valid entry!"
                        break
                if i == dim-1:
                    break
            if legit:
                not_entered = False
    #______________
    not_entered = True
    while not_entered:
        not_entered = False
        result = raw_input("Are diagonals required to have all characters? ") \
            .upper()
        if result in ['YES','Y','1']:
            diag = True
        elif result in ['NO','N','0']:
            diag = False
        else:
            print 'Not a valid answer!'
            not_entered = True
    # start initializing
    if dim > len(choices):
        choices += 'X'
    #______________
    not_entered = True
    while not_entered:
        not_entered = False
        result = raw_input("Are there prefilled boxes? ").upper()
        if result in ['YES','Y','1']:
            partial = True
        elif result in ['NO','N','0']:
            partial = False
        else:
            print 'Not a valid answer!'
            not_entered = True
    #______________
    board = generate_empty_board(dim)
    populate_empty_board(board, choices)
    if partial:
        print "Input coordinates and corresponding value, " + \
            "blankspace-separated; blank to end."
        while True:
            result = raw_input().upper()
            if result == '':
                break
            else:
                try:
                    clues = result.split()
                    if len(clues) != 3:
                        raise ValueError
                    i = int(clues[0])-1
                    j = int(clues[1])-1
                    if len(clues[2])!= 1 or clues[2] == 'X' or \
                        clues[2] not in choices:
                        raise ValueError
                    if i<0 or j<0 or i>=dim or j>=dim:
                        raise ValueError
                    board[i][j] = clues[2]
                except:
                    print 'Not a valid input! Ignored last input.'
    print 'All input taken!'
    return board, constraint, choices, diag


def solve_main(no = -1):
    ''' Pretty printing the output of a solver.
        -1 triggers the input prompt, else get redirected to janko getter.
        '''
    # log('\nABC Endview Solver', GUI)
    if no == -1:
        board, constraint, choices, diag = input_gui()
    else:
        board, constraint, choices, diag = janko_parser(janko_get_text(no))

    solve_print(board, constraint, choices, diag)

# EXECUTION SECTION
#__________

if __name__ == '__main__':
    solve_main(int(sys.argv[1]))