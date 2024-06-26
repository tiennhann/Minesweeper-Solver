from flask import Flask, request, jsonify
from flask_cors import CORS
from greedyAlgo import *

app = Flask(__name__)
CORS(app)   # enable CORS


@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    print(data)
    board = data['board']
    width = data['width']    
    action = find_safe_move(board, width)

    
    if action == -1:
        return jsonify([]) 
    
    return jsonify([{'index': action}])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)