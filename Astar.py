from flask import Flask, request, jsonify
from flask_cors import CORS
from math import comb
from Heuristic import getHeuristic

app = Flask(__name__)
CORS(app, resources={r"/astar": {"origins": "*"}})  # Allowing all domains for the /astar endpoint
global firstMove
firstMove = True

@app.route('/astar', methods=['POST'])
def astar():
    global firstMove
    isNewBoard = True
    move = []
    data = request.get_json()
    board = data['board']
    width = data['width']

    for i in board:
        if(i['status'] ==  'checked'):
            print('In loop')
            isNewBoard = False
            break
    if(isNewBoard):
        firstMove = True

    if firstMove:
        move.append({'index': 0, 'action': 'click'})
        firstMove = False
    else:
        probs = setUp(board, width)
        minIndex = probs[0][1]
        minVal = probs[0][0]
        for i in probs:
            if (float(i[1]) < minVal):
                minIndex = i[0]
                minVal = i[1] 
        move.append({'index': minIndex, 'action': 'click'})  
    return jsonify(move)

def setUp(board, width):
    solvedEdge = []
    unsolvedEdge = []

    for i, cell in enumerate(board):
        if(cell['status'] == 'checked'):
            neighbors = getNeighbors(board, i, width)
            for i in neighbors:
                if(i['status'] == 'covered'):
                    solvedEdge.append(cell)
                    unsolvedEdge.append(neighbors)
                    break
    return (getHeuristic(solvedEdge, unsolvedEdge, board, width))



def getNeighbors(board, index, width):
    edge = []

    if(index % width != width -1): #check if right edge
        if(board[index + 1]['status'] == 'covered'): #right side of index
            edge.append(board[index + 1])

        if(index // width != 0 and board[index - width + 1]['status'] == 'covered'): #top right of index  
            edge.append(board[index - width + 1])

        if(index // width != width - 1 and board[index + width + 1]['status'] == 'covered'): #bottom right of index
            edge.append(board[index + width + 1])


    if(index % width != 0): #check if left edge
        if(board[index - 1]['status'] == 'covered'): #left side of index
            edge.append(board[index - 1])

        if(index // width != 0 and board[index - width - 1]['status'] == 'covered'): #top left of index
            edge.append(board[index - width - 1])

        if(index // width != width - 1 and board[index + width - 1]['status'] == 'covered'): #bottom left of index
            edge.append(board[index + width - 1])


    if(index // width != width - 1 and board[index + width]['status'] == 'covered'): #below index
        edge.append(board[index + width])

    if(index // width != 0 and board[index - width]['status'] == 'covered'): #above index
        edge.append(board[index - width])
    return edge


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
