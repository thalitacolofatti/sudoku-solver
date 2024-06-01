from queue import PriorityQueue
from copy import deepcopy

ALL_VALID = 511  # the bit string 111111111
VALID_DIGITS_STR = "123456789"

def popcount(x):
    # Função utilitária para obter o popcount (# de 1 bits) em uma string de bits
    return bin(x).count("1")

def get_vals_as_list(bstr):
    """
    Converte uma sequência de bits que codifica os valores possíveis de uma célula em um
    matriz de valores inteiros

    por exemplo. 100000010 => [2, 9]
    """
    val = 1
    vals = []
    while bstr != 0:
        if bstr & 1:
            vals.append(val)
        bstr >>= 1
        val += 1
    return vals

class Solver(object):

    def __init__(self, initial_board):
        self.start = initial_board
        self.visited_set = set()
        self.queue = PriorityQueue()

    def solve(self):
        """
        Esta é uma implementação do algoritmo A-star. O objetivo em
        cada estágio do jogo é selecionar um próximo movimento válido que maximize
        progresso em direção à meta em que o jogo sudoku é resolvido.
        """
        puzzle_state = self.start
        puzzle_state.fast_forward()
        dist = puzzle_state.get_dist_to_goal()
        self.queue.put((dist, puzzle_state))

        while not puzzle_state.is_complete() and self.queue.qsize():
            puzzle_state = self.queue.get()[1]
            puzzle_hash = str(puzzle_state)
            self.visited_set.add(puzzle_hash)

            for c in puzzle_state.create_children():
                if str(c) not in self.visited_set:
                    dist = c.get_dist_to_goal()
                    self.queue.put((dist, c))

        return puzzle_state

    def validate_solution(self, solution):
        # Executa verificações de integridade para validar a solução
        ROW_TOTAL = sum(range(1, 10))

        for r, row in enumerate(self.start.board):
            for c, val in enumerate(row):
                if val and val != solution.board[r][c]:
                    raise Exception("Tabuleiro inicial está manipulado!")

        for row in solution.board:
            if sum(row) != ROW_TOTAL:
                raise Exception("O total da linha %d não tem a soma!" % row)

        for col in range(9):
            col_total = sum([solution.board[row][col] for row in range(9)])
            if col_total != ROW_TOTAL:
                raise Exception("O total da coluna %d não tem a soma!" % col)

        for row_start in range(0, 9, 3):
            for col_start in range(0, 9, 3):
                subrows = []
                for i in range(3):
                    subrows.append(solution.board[row_start + i][col_start:col_start + 3])
                section_total = sum([sum(row) for row in subrows])
                if section_total != ROW_TOTAL:
                    raise Exception("O total do quadrante para o quadrante em (%d, %d) não tem a soma!" % (row_start, col_start))


class BoardState(object):
    # Descreve a instancia do tabuleiro. Uma matriz é usada para estrutura de dados.  
    def __init__(self, board):
        self.board = board
        self.f = 0
        self.g = 0
        self.h = 0
        self.possible_vals = [[ALL_VALID for _ in range(9)] for _ in range(9)]
        for r, row in enumerate(self.board):
            for c, val in enumerate(row):
                if val:
                    self.mark_value_invalid(r, c, val)

    def __lt__(self, other):
        return self.f < other.f

    def place_value(self, row, col, val):
        # Coloca o valor `val` na linha ou coluna e marca seu valor como seleção inválida nos demais locais do jogo.
        self.board[row][col] = val
        self.mark_value_invalid(row, col, val)

    def mark_value_invalid(self, row, col, val):
        # Marca o valor `val` onde não é mais uma opção válida
        self.possible_vals[row][col] = 0
        val_mask = (511 - (1 << val - 1))

        # Marca este valor como inválido para todas as células na linha especificada
        for c in range(9):
            self.possible_vals[row][c] &= val_mask

        # Marca este valor como inválido para todas as células na coluna especificada
        for r in range(9):
            self.possible_vals[r][col] &= val_mask

        # Marca este valor como inválido para todas as células no quadrado 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        end_row, end_col = start_row + 3, start_col + 3
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                self.possible_vals[r][c] &= val_mask

    def get_dist_to_goal(self):
        # Estabelece uma medida de distancia para a meta. Conta a quantidade de células preenchidas no tabuleiro.
        bool_map = [[bool(cell) for cell in row] for row in self.board]
        return sum([sum(r) for r in bool_map])

    def is_complete(self):
        return self.get_dist_to_goal() == 0

    def get_scored_next_steps(self):
        """
        Instancia e retorna uma fila de prioridade onde as células são priorizadas
        de acordo com o número de valores possíveis que podem assumir. Menos é melhor,
        porque significa uma probabilidade maior de selecionar o valor correto.
        """
        scored_steps = PriorityQueue()
        for r, row in enumerate(self.possible_vals):
            for c, val in enumerate(row):
                pc = popcount(val)
                # Add cells with # possible vals > 0 to the queue
                if pc:
                    poss_vals = get_vals_as_list(self.possible_vals[r][c])
                    scored_steps.put((pc, r, c, poss_vals))
        return scored_steps

    def fast_forward(self):
        """
        Examina o tabuleiro em busca dos próximos movimentos óbvios e realiza.

        Isso significa procurar repetidamente as células que marcamos
        como tendo um único valor possível e realmente colocar esse valor no
        quadro.
        """
        cells_need_updating = True
        while cells_need_updating:
            cells_need_updating = False
            for r, row in enumerate(self.possible_vals):
                for c, poss_vals in enumerate(row):
                    pc = popcount(poss_vals)
                    if pc == 1:
                        if not cells_need_updating:
                            cells_need_updating = True
                        val = get_vals_as_list(poss_vals)[0]
                        self.place_value(r, c, val)

    def create_children(self):
        """
        Aqui examina as alternativas disponíveis para o nosso próximo passo, conforme pontuado
        usando a função get_scored_next_steps. Nós simplesmente pegamos um dos melhores
        células avaliadas (menor vals possíveis) e criar estados de tabuleiro onde cada
        dos valores possíveis é selecionado.
        """
        next_steps = self.get_scored_next_steps()
        if not next_steps.empty():
            pc, row, col, choices = next_steps.get()
            children = []
            for val in choices:
                child = deepcopy(self)
                child.place_value(row, col, val)
                child.fast_forward()
                children.append(child)
            return children
        else:
            return []

    def pretty_print(self):
        int2str = lambda s: str(s) if s else ' '
        rows = [','.join(map(int2str, row)) for row in self.board]
        print('\n'.join(rows))

    def __str__(self):
        """
        Retorna um identificador de string exclusivo para este tabuleiro
        """
        return ''.join([''.join(map(str, row)) for row in self.board])
