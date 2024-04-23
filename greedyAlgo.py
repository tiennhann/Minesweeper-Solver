from flask import Flask, request, jsonify

app = Flask(__name__)

def solve_minesweeper(board, width):
    actions = []

    def index(row, col):
        return row * width + col
    
    def inBounds(row, col):
        return 0 <= row < width and 0 <= col < width
    
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    cells = {}

    for cell in board:
        row = cell['index'] // width
        col = cell['index'] % width
        cells[(row, col)] = {
            'status': cell['status'],
            'isFlagged': cell['isFlagged'],
            'numbers': int(cell['number']) if 'number' in cell and cell['number'].isdigit() else 0
        }

    for (row, col), cell in cells.items():
        if cell['status'] == 'checked' and cell['number'] > 0:
            count_flags = 0
            count_covered = 0
            neighbors = []

            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if inBounds(nr, nc):
                    neighbor = cells.get((nr,nc))
                    if neighbor:
                        if neighbor['status'] == 'covered' and not neighbor['isFlagged']:
                            neighbor.append((nr,nc))
                            count_covered += 1
                        elif neighbor['isFlagged']:
                            count_flags += 1
            
            if count_flags == cell['number'] and count_covered > 0:
                for (nr,nc) in neighbors:
                    if not cells[(nc,nr)]['isFlagged'] and cells[(nc,nr)]['status'] == 'covered':
                        actions.append({'index': index(nr, nc), 'action': 'click'})
                    
                    elif (count_flags + count_covered == cell['numbber']) and count_covered > 0:
                        for (nr,nc) in neighbors:
                            if not cells[(nc,nr)]['isFlagged']:
                                actions.append({'index':index(nr,nc), 'action': 'flag'})

    return actions