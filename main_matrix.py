#!/usr/bin/env python2
from utils_matrix import *

l = [1,2,3,4]

for i in l:
	print i
	if i == 2:
		del l[l.index(i)]
	print l[l.index(i)]
	print l
