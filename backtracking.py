
class Backtracking:
    def __init__(self, board):
        self.board = board

    def is_valid_move(self, row, col, num):
        # Verifica a linha e a coluna
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        # Verifica o quadrante
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def solve_backtracking(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True

        row, col = empty_cell
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num
                if self.solve_backtracking():
                    return True
                self.board[row][col] = 0

        return False

    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None
