from math import comb
from flask import Flask, request, jsonify
from flask_cors import CORS
from math import comb

app = Flask(__name__)
CORS(app, resources={r"/astar": {"origins": "*"}})  # Allowing all domains for the /astar endpoint

def getHeuristic(solEdge, unsolEdge, board, width):
    solBombCounts = [] #numb of boms for each seen edge
    unsolIndex = [] #index of each unsolved square
    unsolPos = [] #index mapping to solutions

    for i in solEdge:
        solBombCounts.append(getBombNum(board, i['index'], width)) #loop to fill bombcounts
    
    for i in unsolEdge:
        temp = []
        for j in i:
            temp.append(int(j['index']))
            if j['index'] not in unsolIndex:
                unsolIndex.append(j['index']) #loop to fill unSolindex with indeces
        unsolPos.append(temp)
    
    BombProb = checkCombos(unsolIndex, board, solBombCounts, unsolPos)

    for i, col in enumerate(unsolEdge):
        if(len(col) == solBombCounts[i]):
            for j, ind in enumerate(col):
                for k, indComp in enumerate(unsolIndex):
                    if(unsolIndex[k] == int(ind['index'])): #loop to make squares that are certainly mines have a probability of 100%
                        BombProb[k] = 1

    newTProb = 0
    for i in BombProb:
        if (i != 1):
            newTProb += i #get prob total after fixing bombs excluding known Bombs
    for i, ind in enumerate(BombProb):
        if (ind != 1):
            if(newTProb == 0):
                BombProb[i] == 0
            else:
                BombProb[i] = ind / newTProb #normalize after fixing known bombs

    retTuple = []
    for i, ind in enumerate(unsolIndex):
        retTuple.append((ind, BombProb[i]))
    return retTuple

def getBombNum(board, index, width): #get number of bombs around square to use in hueristic 
    bombcount = 0

    if(index % width != width -1): #check if right edge
        if(board[index + 1]['number'] == -1): #right side of index
            bombcount += 1

        if(index // width != 0 and board[index - width + 1]['number'] == -1): #top right of index  
            bombcount += 1

        if(index // width != width - 1 and board[index + width + 1]['number'] == -1): #bottom right of index
            bombcount += 1


    if(index % width != 0): #check if left edge
        if(board[index - 1]['number'] == -1): #left side of index
            bombcount += 1

        if(index // width != 0 and board[index - width - 1]['number'] == -1): #top left of index
            bombcount += 1

        if(index // width != width - 1 and board[index + width - 1]['number'] == -1): #bottom left of index
            bombcount += 1


    if(index // width != width - 1 and board[index + width]['number'] == -1): #below index
        bombcount += 1

    if(index // width != 0 and board[index - width]['number'] == -1): #above index
        bombcount += 1

    return bombcount
                
def checkCombos(indexes, board, bombcount, unsolPos): #returns back list of probabilities, indexes correlate with arr passed as 'indexes'
    bombPos = []
    for i in range(len(unsolPos)):
        bombPos.append([])
        for j in range(len(unsolPos[i])):
            bombPos[i].append(None)
    bombProb = []
    for i in indexes:
        bombProb.append(None)


    def rep(current, depth):
        if (depth == N):
            for k, CurMap in enumerate(indexes):
                for i, ColNum in enumerate(unsolPos):
                    for j, cellInd in enumerate(ColNum): #map bomb choices to layout for easy bomb count checking
                        if (cellInd == CurMap):
                            bombPos[i][j] = current[k]

            valid = True
            for i, bCol in enumerate(bombPos): 
                bCount = bombcount[i]
                colbCount = 0
                for j in bCol:
                    if(j == 1):
                        colbCount += 1 #increment for bombs in col
                if(bCount != colbCount): #stop if realCount != col Count
                    valid = False
                    break
            
            
            if(valid):
                count = 0
                for i in current:
                    if(i == 1):
                        count += 1
                
                for i, prob in enumerate(bombProb):
                    if(bombProb[i] == None):
                        bombProb[i] = 0
                    #print(str(getRemainingBombs(board)) + " " + str(count))
                    bombProb[i] += current[i] * comb(getRemainingSpace(board) - len(indexes), getRemainingBombs(board))
            return
        for val in [1, 0]: # 1= bomb 0 = safe
            current.append(val)
            rep(current, depth + 1)
            current.pop()
    
    N = len(indexes)
    totalProb = 0
    rep([], 0)
    return bombProb

def getRemainingSpace(board):
    count = 0
    for i in board:
        if (i['status'] == 'covered'):
            count += 1
    return count

def getRemainingBombs(board):
    count = 0
    for i in board:
        if (i['status'] == 'covered' and i['number'] == -1):
            count += 1
    return count