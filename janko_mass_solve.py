#!/usr/bin/env python
import urllib2
from bs4 import BeautifulSoup
from utils import *

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
    del data[0]
    del data[-1]
        
    attributes = ['size','depth','options','clabels','rlabels']
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
                    constraint[1][i][0] = topConstraint[i]
            del data[0]
            del topConstraint
            #__________
            bottomConstraint = data[0].upper().encode('ascii','ignore').split()
            for i in range(dim):
                if bottomConstraint[i] != '-':
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
                    constraint[0][i][0] = leftConstraint[i]
            del data[0]
            del leftConstraint
            #__________
            rightConstraint = data[0].upper().encode('ascii','ignore').split()
            for i in range(dim):
                if rightConstraint[i] != '-':
                    constraint[0][i][1] = rightConstraint[i]
            del data[0]
            del rightConstraint

    # print constraint
    choices += 'X'
    result = solve(constraint, choices, diag)
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


f = open('janko_time','r+')
f.write('Problem no. Trials      Expansions\n')
for i in range(530):
    i += 1
    if i == 480:
    	continue
    print i
    detail = solver_janko(i, True)[1]
    f.write(str(i).ljust(12))
    f.write(str(detail[0]).ljust(12))
    f.write(str(detail[1]).ljust(12))
    f.write('\n')

f.close()
