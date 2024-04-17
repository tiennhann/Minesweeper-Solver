from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # enable CORS

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    board = data['board']
    width = data['width']
    solution = open_safe_squares(board)
    return jsonify(solution)

def open_safe_squares(board):
    moves = []
    # Iterate over each cell in the board
    for i, cell in enumerate(board):
        # Check if the cell is covered and not flagged
        if cell['status'] == 'covered':
            # Only interact with cells that do not have a bomb
            if cell['number'] != -1:  # Assuming 0 means no adjacent bomb
                moves.append({'index': i, 'action': 'click'})
            else:
                moves.append({'index': i, 'action': 'flag'})
    return moves

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
