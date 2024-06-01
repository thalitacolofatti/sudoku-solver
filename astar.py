import heapq
from copy import deepcopy

class SolverAStar:
    def __init__(self, board):
        self.board = board
        self.queue = []
        initial_heuristic = self.heuristic(board)
        heapq.heappush(self.queue, (initial_heuristic, deepcopy(board)))
        self.visited = set()

    def is_valid_move(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False

        return True

    def heuristic(self, board):
        return sum(row.count(0) for row in board)
    
    def find_empty_cell(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def solve(self):
        while self.queue:
            _, current_board = heapq.heappop(self.queue)
            board_hash = self.board_to_string(current_board)
            if board_hash in self.visited:
                continue
            self.visited.add(board_hash)

            empty_cell = self.find_empty_cell(current_board)
            if not empty_cell:
                self.board = current_board
                return True

            row, col = empty_cell
            for num in range(1, 10):
                if self.is_valid_move(current_board, row, col, num):
                    new_board = deepcopy(current_board)
                    new_board[row][col] = num
                    new_heuristic = self.heuristic(new_board)
                    heapq.heappush(self.queue, (new_heuristic, new_board))

        return False

    def board_to_string(self, board):
        return ''.join([''.join(map(str, row)) for row in board])

    def get_solution(self):
        return self.board