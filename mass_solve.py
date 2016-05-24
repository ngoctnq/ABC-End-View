from utils import *

f = open('janko_time','r+')
f.write('Problem no. Trials      Expansions\n')
for i in range(530):
    i += 1
    print i
    detail = solver_janko(i, True)[1]
    f.write(str(i).ljust(12))
    f.write(str(detail[0]).ljust(12))
    f.write(str(detail[1]).ljust(12))
    f.write('\n')

f.close()
