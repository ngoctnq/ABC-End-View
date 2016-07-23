import itertools
import copy

##You can ignore the double comments. That was a first pass, awful brute force attempt.

def getBoards():
    size = 4
    letters = createString(size)
    perms = list(itertools.permutations(letters))
##    combos = itertools.combinations(range(720),6)
    #boards = open("4x4.txt", "w")
##    for c in combos:
##        print(c)
##        board = list(c)
##        for i in range(6):
##                board[i] = list(perms[int(board[i])])
##        notBoard = False
##        transpose = [[[] for x in range(len(board))] for y in range(len(board))]
##        for row in range(len(board)):
##            for col in range(len(board)):
##                transpose[col][row] = board[row][col]
##        for row in transpose:
##            for i in row:
##                if row.count(i) > 1:
##                    notBoard = True
##
##        if not notBoard:
##            print(board)
##            for row in board:
##                boards.write(row+"\n")
##            boards.write("\n")
    c = 0
    allBoards = []
    for p in perms:
        #print(p)
        boards = []
        boards.append([list(p)])
        for i in range(size-1):
            newBoards = []
            for board in boards:
                for row in perms:
                    valid = True
##                    print(board)
##                    print(row)
                    for j in range(size):
                        for k in range(len(board)):
                            if board[-1-k][j] == row[j]:
                                valid = False
                    if valid:
                        newBoard = copy.deepcopy(board)
                        newBoard.append(list(row))
##                        print(newBoard)
                        newBoards.append(newBoard)
            boards = copy.deepcopy(newBoards)
        for board in boards:
            allBoards.append(board)
    c=0
    for b in allBoards:
        c += 1
        print(b)

    print("Total num of boards: " + str(c))
    print("Done")

def createString(num):
    string = ""
    for i in range(num):
        string += chr(65+i)
    return string
