from flask import Flask, request, jsonify
from flask_cors import CORS
from Heuristic import getHeuristic, getBombNum

app = Flask(__name__)
CORS(app, resources={r"/solve": {"origins": "*"}})

@app.route('/solve', methods=['POST'])
def greedy():
    data = request.get_json()
    board = data['board']
    width = data['width']
    last_click_index = None

    if is_new_board(board):
        # If it's the new board, make a safe initial move (typically at the corner or center)
        move_index = get_initial_move_index(board, width)
        move = [{'index': move_index, 'action': 'click'}]
        last_click_index = move_index
        
    else:
        # Run the heuristic to get probabilities for each covered cell
        probs = setUp(board, width)
        if last_click_index is not None:
            neighbors = set([idx for idx in getNeighbors(board, last_click_index, width)])
            probs = [p for p in probs if p[0] in neighbors]
        # Choose the move with the lowest probability of containing a bomb
        min_prob = min(probs, key=lambda x: x[1])
        move = [{'index': min_prob[0], 'action': 'click'}]
        last_click_index = min_prob[0]

    print ('last indesx', last_click_index)
    return jsonify(move)

def is_new_board(board):
    return all(cell['status'] == 'covered' for cell in board)

def get_initial_move_index(board, width):
    index = 0
    for cell in board:
        if getBombNum(board, cell['index'], width) == 0 and cell['number'] != -1:
            index = int(cell['index'])
    return index

def setUp(board, width):
    solvedEdge = []
    unsolvedEdge = []

    for i, cell in enumerate(board):
        if cell['status'] == 'checked':
            neighbors = getNeighbors(board, i, width)
            for neighbor in neighbors:
                if neighbor['status'] == 'covered':
                    solvedEdge.append(cell)
                    unsolvedEdge.append(neighbors)
                    break
    return getHeuristic(solvedEdge, unsolvedEdge, board, width)

def getNeighbors(board, index, width):
    neighbors = []
    # Define neighbor coordinates as tuples of delta rows and delta columns
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    row, col = divmod(index, width)
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < width and 0 <= nc < width:
            neighbor_idx = nr * width + nc
            if board[neighbor_idx]['status'] == 'covered':
                neighbors.append(board[neighbor_idx])

    return neighbors



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)