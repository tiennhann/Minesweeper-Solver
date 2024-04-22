from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/astar": {"origins": "*"}})  # Allowing all domains for the /astar endpoint


@app.route('/astar', methods=['POST'])
def astar():
    data = request.get_json()
    board = data['board']
    width = data['width']
    setUp(board, width)
    return jsonify(board)

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



def getNeighbors(board, index, width):
    edge = []

    if(index % width != width -1): #check if right edge
        if(board[index + 1]['status'] == 'covered'): #right side of index
            edge.append(board[index + 1])

        if(board[index - width + 1]['status'] == 'covered' and index // width != 0): #top right of index  
            edge.append(board[index - width + 1])

        if(board[index + width + 1]['status'] == 'covered' and index // width != width - 1): #bottom right of index
            edge.append(board[index + width + 1])


    if(index % width != 0): #check if left edge
        if(board[index - 1]['status'] == 'covered'): #left side of index
            edge.append(board[index - 1])

        if(board[index - width - 1]['status'] == 'covered' and index // width != 0): #top left of index
            edge.append(board[index - width - 1])

        if(board[index + width - 1]['status'] == 'covered' and index // width != width - 1): #bottom left of index
            edge.append(board[index + width - 1])


    if(board[index + width]['status'] == 'covered' and index // width != width - 1): #below index
        edge.append(board[index + width])

    if(board[index - width]['status'] == 'covered' and index // width != 0): #above index
        edge.append(board[index - width])
    return edge



def getBombNum(board, index, width):
    bombcount = 0

    if(index % width != width -1): #check if right edge
        if(board[index + 1]['number'] == -1): #right side of index
            bombcount += 1

        if(board[index - width + 1]['number'] == -1 and index // width != 0): #top right of index  
            bombcount += 1

        if(board[index + width + 1]['number'] == -1 and index // width != width - 1): #bottom right of index
            bombcount += 1


    if(index % width != 0): #check if left edge
        if(board[index - 1]['number'] == -1): #left side of index
            bombcount += 1

        if(board[index - width - 1]['number'] == -1 and index // width != 0): #top left of index
            bombcount += 1

        if(board[index + width - 1]['number'] == -1 and index // width != width - 1): #bottom left of index
            bombcount += 1


    if(board[index + width]['number'] == -1 and index // width != width - 1): #below index
        bombcount += 1

    if(board[index - width]['number'] == -1 and index // width != 0): #above index
        bombcount += 1
    return bombcount


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
