from flask import Flask, request, jsonify
from flask_cors import CORS
from Heuristic import getHeuristic, getBombNum
from Astar import getNeighbors

app = Flask(__name__)
CORS(app, resources={r"/minimax": {"origins": "*"}})  # Allow all domains for the /minimax endpoint

FIRST_MOVE = True  # Global variable to track the first move
Flags = []

@app.route('/minimax', methods=['POST'])
def minimax():
    global FIRST_MOVE
    is_new_board = True
    move = []
    data = request.get_json()
    board = data['board']
    width = data['width']  # Set width to 7 for a 7x7 game board

    for cell in board:
        if cell['status'] == 'checked':
            is_new_board = False
            break

    if is_new_board:
        FIRST_MOVE = True

    if FIRST_MOVE:
        ind = 0
        for i, cell in enumerate(board):
            if(getBombNum(board, i, width) == 0 and cell['number'] != -1):
                ind = i
                break

        move.append({'index': i, 'action': 'click'})
        
        FIRST_MOVE = False
    else:
        probabilities = set_up(board, width)
        min_index = probabilities[0][0]
        min_val = probabilities[0][1] 
        max_index = probabilities[0][0]#tuple index was backwards for these 1 = prob 0 = index

        hasBomb = False

        for probability in probabilities:
            isFlagged = False
            for cell in board:
                if cell['index'] == probability[0]:
                    print(' in index')
                    if cell['isFlagged'] == True:
                        print('in flag')
                        isFlagged = True            #check if space is flagged

            if float(probability[1]) < min_val:
                min_index = probability[0]
                min_val = probability[1]

            if float(probability[1]) == 1 and not isFlagged: #this actually causes issues since it may flag a square thats not a bomb but has the highest prob to be one (still chance to not be)
                max_index = probability[0]
                hasBomb = True

            
        move.append({'index': min_index, 'action': 'click'})#minimize
        if hasBomb:
            move.append({'index': max_index, 'action': 'flag'})#maximize when agent has available move
        

    return jsonify(move)


def get_best_move(board, width):
    """
    Determine the best move using the minimax algorithm.

    Args:
        board (list): The game board represented as a list of cells.
        width (int): The width of the game board.

    Returns:
        dict: The best move (index and action) determined by the minimax algorithm.
    """
    _, best_score, best_move = minimax_decision(board, width, True)
    return best_move, best_score


def minimax_decision(board, width, maximizing_player):
    """
    Recursive function implementing the minimax decision-making process.

    Args:
        board (list): The game board represented as a list of cells.
        width (int): The width of the game board.
        maximizing_player (bool): Flag indicating whether the current player is maximizing.

    Returns:
        Tuple (None, score, best_move) representing the best move and its evaluation score.
    """

    if maximizing_player:
        max_score = float('-inf')
        best_move = None

        for i, cell in enumerate(board):
            if cell['status'] == 'covered':
                board_copy = board[:]  # Create a copy of the board
                board_copy[i]['status'] = 'checked'  # Simulate clicking the cell
                _,score, _ = minimax_decision(board_copy, width, False)
                if score > max_score:
                    max_score = score
                    best_move = {'index': i, 'action': 'click'}  # Consider 'click' action
        return None, max_score, best_move
    else:
        min_score = float('inf')
        best_move = None

        for i, cell in enumerate(board):
            if cell['status'] == 'covered':
                board_copy = board[:]  # Create a copy of the board
                board_copy[i]['status'] = 'flagged'  # Simulate flagging the cell
                _, score, _ = minimax_decision(board_copy, width, True)
                if score < min_score:
                    min_score = score
                    best_move = {'index': i, 'action': 'flag'}  # Consider 'flag' action
        return None, min_score, best_move


def set_up(board, width):
    """
    Set up the board for heuristic evaluation.

    Args:
        board (list): The game board represented as a list of cells.
        width (int): The width of the game board.

    Returns:
        list: List of tuples representing heuristic probabilities.
    """
    solved_edge = []
    unsolved_edge = []

    for i, cell in enumerate(board):
        if cell['status'] == 'checked':
            neighbors = getNeighbors(board, i, width)
            for n in neighbors:
                if n['status'] == 'covered':
                    solved_edge.append(cell)
                    unsolved_edge.append(neighbors)
                    break

    return getHeuristic(solved_edge, unsolved_edge, board, width)


def get_neighbors(board, index, width):
    """
    Helper function to get neighboring cells of a given cell index on the board.

    Args:
        board (list): The game board represented as a list of cells.
        index (int): The index of the cell for which neighbors are to be retrieved.
        width (int): The width of the game board.

    Returns:
        list: List of neighboring cells.
    """
    edge = []

    if index % width != width - 1:  # Check if right edge
        right_index = index + 1
        if board[right_index]['status'] == 'covered':
            edge.append(board[right_index])

    if index % width != 0:  # Check if left edge
        left_index = index - 1
        if board[left_index]['status'] == 'covered':
            edge.append(board[left_index])

    if index // width != 0:  # Check if top edge
        top_index = index - width
        if board[top_index]['status'] == 'covered':
            edge.append(board[top_index])

    if index // width != (len(board) // width) - 1:  # Check if bottom edge
        bottom_index = index + width
        print("Bottom Index:", bottom_index)  # Add debug print statement
        if board[bottom_index]['status'] == 'covered':
            edge.append(board[bottom_index])

    return edge


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
 