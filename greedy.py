from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
#CORS(app)  # Enable CORS
CORS(app, resources={r"/solve": {"origins": "*"}})  # Allowing all domains for the /solve endpoint

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        board = data['board']
        width = data['width']
        solution = greedy_solver(board, width)
        return jsonify(solution)
    except KeyError as e:
        return jsonify({'error': 'Missing key in JSON data: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
def greedy_solver(board, width):
    moves = []
    # Scan for safe clicks or places to put flags based on basic Minesweeper rules
    for i, cell in enumerate(board):
        if cell['status'] == 'covered':
            # If it's a zero and no flags around, it's safe to click
            if cell['number'] == 0 and not cell['isFlagged']:
                moves.append({'index': i, 'action': 'click'})
                continue
            
            # If the number of flags around is equal to the number indicated by the number,
            # it's safe to click around the covered neighbors
            surrounding_cells = get_surrounding_cells(i, width)
            flagged_count = sum(1 for idx in surrounding_cells if board[idx]['isFlagged'])
            if flagged_count == cell['number']:
                for idx in surrounding_cells:
                    if not board[idx]['isFlagged'] and board[idx]['status'] == 'covered':
                        moves.append({'index': idx, 'action': 'click'})

    return moves

def get_surrounding_cells(index, width):
    surrounding = []
    row_start = index // width
    col_start = index % width

    for row in range(row_start-1, row_start+2):
        for col in range(col_start-1, col_start+2):
            if 0 <= row < width and 0 <= col < width:
                idx = row * width + col
                if idx != index:
                    surrounding.append(idx)
    return surrounding

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5001, debug=True)

