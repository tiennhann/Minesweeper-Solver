from flask import Flask, request, jsonify
from flask_cors import CORS
from greedyAlgo import *

app = Flask(__name__)
CORS(app)   # enable CORS


@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    board = data['board']
    width = data['width']    
    print(data)
    action = solve_minesweeper(board, width)
    print('My move', action)
    return jsonify(action)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)