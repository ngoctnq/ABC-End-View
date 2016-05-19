#!/usr/bin/env python
from utils import *
from timeit import default_timer
from Tkinter import *
import tkMessageBox

# params: rows/columns, count, head/tail
# problem 209
# constraint = [[['A',''],['C','D'],['A',''],['','C'],['E',''],['','E'],['E','']],
#                [['A',''],['','A'],['B',''],['','B'],['','B'],['C','D'],['B','']]]
# choices = 'ABCDE'

# problem 3
# constraint = [[['',''],['',''],['A','']],[['','B'],['',''],['','']]]
# choices = 'AB'

# problem 176
constraint = [[['A',''],['','A'],['D',''],['',''],['','E'],['',''],],
               [['','E'],['','B'],['E',''],['','D'],['C',''],['','C']]]
choices = 'ABCDE'

# last problem of the month
# constraint = [[['',''], ['B',''], ['A',''], ['B',''], ['D','B'], ['B','A'], ['',''], ['','']],
#              [['D','B'], ['C','D'], ['','B'], ['C','D'], ['',''], ['C','B'], ['',''], ['','D']]]
# choices = 'ABCD'

# problem 77
# constraint = [[['F','C'], ['',''], ['A','C'], ['','D'], ['D','B'], ['D','B'], ['B','F'], ['','']],
#               [['','A'], ['',''], ['E','F'], ['D',''], ['F','E'], ['D','F'], ['','B'], ['','']]]
# choices = 'ABCDEF'

dim = len(constraint[0])
diag = True

is_input = False
# GUI to input problem
if __name__ == "__main__" and is_input == True:
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

    def not_cap_chars(word):
        for i in range(len(word)):
            if ord(word[i]) != ord('A')+i:
                return True
        return False

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
                
    root = Tk()
    root.withdraw()
    result = tkMessageBox.askquestion("ABC End View Solver", "Are diagonals required to have all characters?")
    if result == 'yes':
        diag = True
    else:
        diag = False
    #______________
    
# start initializing
choices += 'X'

def main():
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

def test():
    tic = default_timer()
    # insert code to test here
    main()
    # end of code insertion
    toc = default_timer()
    print "time taken in seconds:", toc-tic

# solving it
if __name__ == "__main__":
    # main()
    test()
