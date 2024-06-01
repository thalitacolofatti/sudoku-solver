from random import sample, randint
from selection import SelectNumber, SelectGame
from copy import deepcopy
from astar import SolverAStar
from backtracking import Backtracking
import time

def create_line_coordinates(cell_size: int) -> list[list[tuple]]:
    """Cria as coordenadas x, y para desenhar as linhas do tabuleiro"""
    points = []
    for y in range(1, 9):
        # linhas horizontais
        temp = []
        temp.append((0, y * cell_size)) # pontos x, y [(0, 80), (0, 160), (0, 240), (0, 320) ...]
        temp.append((720, y * cell_size)) # pontos x, y [(720, 80), (720, 160), (720, 240), (720, 320) ...]
        points.append(temp)

    for x in range(1, 10):
        # linhas verticais - de 1 a 10 para fechar o lado direito
        temp = []
        temp.append((x * cell_size, 0)) # pontos x, y [(80, 0), (160, 0), (240, 0), (320, 0) ...]
        temp.append((x * cell_size, 720)) # pontos x, y [(80, 720), (160, 720), (240, 720), (320, 720) ...]
        points.append(temp)
    return points

SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE

def pattern(row_num: int, col_num:int) -> int:
    """ 
        Calcula um padrão que é usado para distribuir os números pelo tabuleiro de forma que satisfaça as regras do Sudoku. 
        row_num % SUB_GRID_SIZE pega o índice dentro da subgrade atual.
        row_num // SUB_GRID_SIZE calcula em qual subgrade (na horizontal) está.
        col_num é o índice da coluna atual.
        SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num combina essas informações para gerar uma posição na grade.
        GRID_SIZE (% GRID_SIZE) garante que a posição esteja dentro dos limites do tabuleiro (0 a 8 para um Sudoku 9x9).
    """
    return (SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num) % GRID_SIZE

def shuffle(samp: range) -> list:
    """ Usa a função sample do módulo random para retornar uma lista embaralhada de uma sequência fornecida (samp) """
    return sample(samp, len(samp))

def create_grid(sub_grid: int) -> list[list]:
    """ Cria tabuleiro 9x9 preenchido com números aleatoriamente """
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]

def remove_numbers(grid: list[list]):
    """ Transforma números em zero aleatoriamente no tabuleiro """
    num_of_cells = GRID_SIZE * GRID_SIZE
    divisor = randint(5,7)
    empties = num_of_cells * 3 // divisor # 7 é o nível mais fácil e 4 o mais difícil
    filled = num_of_cells - empties
    for i in sample(range(num_of_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0

    return divisor, filled

class Grid:
    def __init__(self, pygame, font):
        self.cell_size = 80
        self.num_x_offset = 29
        self.num_y_offset = 20
        self.line_coordinates = create_line_coordinates(self.cell_size)
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid) # cria uma cópia antes de remover os números para o tabuleiro aleatório
        self.win = False
        self.time_solution = 0
        self.is_solving = False
        self.is_backtracking = False
        self.is_user_grid = False
        self.selected_cell = None
        self.divisor, self.filled = remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()

        self.game_font = font

        self.selection = SelectNumber(pygame, self.game_font)
        self.selection_btn_game = SelectGame(pygame, self.game_font)

    def restart(self) -> None:
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        self.win = False
        self.time_solution = 0
        self.is_solving = False
        self.is_backtracking = False
        self.is_user_grid = False
        self.selected_cell = None
        self.divisor, self.filled = remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()

    def create_empty_grid(self) -> None:
        """ Inicializa um tabuleiro vazio """
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.occupied_cell_coordinates = []
        self.__test_grid = deepcopy(self.grid)

    def check_grids(self):
        """ Verifica de todas as células preencidas são válidas """
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != self.__test_grid[y][x]:
                    return False
        return True

    def is_cell_preoccupied(self, x: int, y: int) -> bool:
        """ Checa células não jogáveis - inicializadas ou já ocupadas """
        for cell in self.occupied_cell_coordinates:
            if x == cell[1] and y == cell[0]: # x é coluna e y é linha
                return True
        return False

    def get_mouse_click(self, x: int, y: int):
        if x <= 720: # dentro do tamanho do tabuleiro
            grid_x, grid_y = x // 80, y // 80
            if not self.is_cell_preoccupied(grid_x, grid_y) or self.is_user_grid:
                self.set_cell(grid_x, grid_y, self.selection.selected_number)
            
        elif y >= 440 and x >= 720: 
            self.selection.button_clicked(x, y)
            if self.check_grids() and not self.is_user_grid:
                self.win = True
        btn_game = self.selection_btn_game.button_clicked(x, y)
        if btn_game == 0:
            self.restart()
        elif btn_game == 1:
            self.divisor = ""
            self.filled = 0
            self.time_solution = 0
            self.is_user_grid = True
            self.create_empty_grid()
        elif btn_game == 2:
            self.time_solution = 0
            self.is_solving = False
            self.is_backtracking = False
            for y in range(9):
                for x in range(9):
                    if (y, x) not in self.occupied_cell_coordinates:
                        self.set_cell(x, y, 0)
        elif btn_game == 3:
            self.is_solving = True
            if self.is_user_grid:
                self.occupied_cell_coordinates = self.pre_occupied_cells()
            begin = time.time()
            solution = SolverAStar(self.grid)
            if solution.solve():
                solved_board = solution.get_solution()
                for y in range(9):
                    for x in range(9):
                        if self.get_cell(x, y) == 0:
                            if (y, x) not in self.occupied_cell_coordinates:
                                self.set_cell(x, y, solved_board[y][x])
            else:
                print("sem solução")
            end = time.time()
            self.time_solution = end - begin
            return self.is_solving
        elif btn_game == 4:
            self.is_backtracking = True
            self.is_solving = False
            if self.is_user_grid:
                self.occupied_cell_coordinates = self.pre_occupied_cells()
            begin = time.time()
            solver_back = Backtracking(self.grid)
            if solver_back.solve_backtracking():
                for y in range(9):
                    for x in range(9):
                        if self.get_cell(x, y) == 0:
                            if (y, x) not in self.occupied_cell_coordinates:
                                self.set_cell(x, y, solver_back.board[y][x])
            else:
                print("sem solução")
            end = time.time()
            self.time_solution = end - begin
            return self.is_backtracking

    def pre_occupied_cells(self) -> list[tuple]:
        """" Coleta as coordenadas y, x para todas as células inicializadas ou já ocupadas """
        occupied_cell_coordinates = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x, y) != 0:
                    occupied_cell_coordinates.append((y, x)) # primeiro a linha, depois a coluna: y, x
        return occupied_cell_coordinates

    def __draw_lines(self, pygame, surface) -> None:
        """ Desenha as linhas de divisão do tabuleiro """
        for index, point in enumerate(self.line_coordinates):
            if index == 2 or index == 5 or index == 10 or index == 13:
                pygame.draw.line(surface, self.selection.color_normal, point[0], point[1])
            else:
                pygame.draw.line(surface, self.selection.color_gray, point[0], point[1])

    def __draw_numbers(self, surface)  -> None:
        """ Escreve os números no tabuleiro """
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x, y) != 0:
                    if (y, x) in self.occupied_cell_coordinates:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, self.selection.color_black)
                    elif self.is_solving:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, self.selection.color_purple)
                    elif self.is_backtracking:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, self.selection.color_blue)
                    else:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, self.selection.color_selected)

                    if self.get_cell(x, y) != self.__test_grid[y][x] and not self.is_solving and not self.is_backtracking and not self.is_user_grid: # self.grid[y][x] != self.__test_grid[y][x]
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, self.selection.color_red)

                    surface.blit(text_surface, (x * self.cell_size + self.num_x_offset, y * self.cell_size + self.num_y_offset))

    def draw_all(self, pygame, surface):
        self.__draw_lines(pygame, surface)
        self.__draw_numbers(surface)
        self.selection.draw(pygame, surface)
        self.selection_btn_game.draw(pygame, surface)

    def get_cell(self, x: int, y: int) -> int:
        """ Obtém o valor de uma célula na coordenada y, x """
        return self.grid[y][x]
    
    def set_cell(self, x: int, y: int, value: int) -> int:
        """ Define o valor de uma célula na coordenada y, x """
        self.grid[y][x] = value

    def select_cell(self, x, y) -> None:
        """ Seleciona uma célula no tabuleiro """
        self.selected_cell = (x, y)

    def insert_number(self, number) -> None:
        """ Insere um número na célula selecionada """
        if self.selected_cell:
            x, y = self.selected_cell
            self.grid[y][x] = number