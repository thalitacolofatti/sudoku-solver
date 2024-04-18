import pygame as pg
import math
from solverAstar import Solver, BoardState

# Cores
preto = (0, 0, 0)
vermelho = (255, 64, 131)
verde = (64, 255, 134)
lilas_claro = (212, 175, 250)
lilas = (164, 74, 255)
branco = (255, 255, 255)
cinza = (237, 237, 237)

# Setup da tela do Jogo
window = pg.display.set_mode((1000, 700))

# Inicializando fonte
pg.font.init()
# Escolhendo uma fonte e tamanho
fonte = pg.font.SysFont("Roboto", 50, bold=True)

tabuleiro_data = [['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                  ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                  ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                  ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                  ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                  ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                  ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                  ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                  ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n']]

jogo_data = [['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
             ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
             ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
             ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
             ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
             ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
             ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
             ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
             ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n']]

escondendo_numeros = True
tabuleiro_preenchido = True
click_last_status = False
click_position_x = -1
click_position_y = -1
numero = 0

def Tabuleiro_Hover(window, mouse_position_x, mouse_position_y):
    quadrado = 66.7
    ajuste = 50
    x = (math.ceil((mouse_position_x - ajuste) / quadrado) - 1)
    y = (math.ceil((mouse_position_y - ajuste) / quadrado) - 1)
    pg.draw.rect(window, branco, (0, 0, 1000, 700))
    if x >= 0 and x <= 8 and y >= 0 and y <= 8:
        pg.draw.rect(window, lilas_claro, ((ajuste + x * quadrado, ajuste + y * quadrado, quadrado, quadrado)))

def Celula_Selecionada(window, mouse_position_x, mouse_position_y, click_last_status, click, x, y):
    quadrado = 66.7
    ajuste = 50
    if click_last_status == True and click == True:
        x = (math.ceil((mouse_position_x - ajuste) / quadrado) - 1)
        y = (math.ceil((mouse_position_y - ajuste) / quadrado) - 1)
    if x >= 0 and x <= 8 and y >= 0 and y <= 8:
        pg.draw.rect(window, lilas, ((ajuste + x * quadrado, ajuste + y * quadrado, quadrado, quadrado)))
    return x, y

def Tabuleiro(window):
    pg.draw.rect(window, preto, (50, 50, 600, 600), 6)
    pg.draw.rect(window, preto, (50, 250, 600, 200), 6)
    pg.draw.rect(window, preto, (250, 50, 200, 600), 6)
    pg.draw.rect(window, preto, (50, 117, 600, 67), 2)
    pg.draw.rect(window, preto, (50, 317, 600, 67), 2)
    pg.draw.rect(window, preto, (50, 517, 600, 67), 2)
    pg.draw.rect(window, preto, (117, 50, 67, 600), 2)
    pg.draw.rect(window, preto, (317, 50, 67, 600), 2)
    pg.draw.rect(window, preto, (517, 50, 67, 600), 2)

def Button_AI_Solver(window):
    pg.draw.rect(window, lilas, (700, 200, 250, 100))
    palavra_f = fonte.render('AI Solver', True, preto)
    window.blit(palavra_f, (725, 225))

def Button_Blank_Board(window):
    pg.draw.rect(window, cinza, (700, 350, 250, 100))
    palavra_f = fonte.render('Blank', True, preto)
    window.blit(palavra_f, (735, 375))

def Quadrante_Selecionado(tabuleiro_data, x, y):
    quadrante = []
    if x >= 0 and x <= 2 and y >= 0 and y <= 2:
        quadrante.extend([tabuleiro_data[0][0], tabuleiro_data[0][1], tabuleiro_data[0][2],
                          tabuleiro_data[1][0], tabuleiro_data[1][1], tabuleiro_data[1][2],
                          tabuleiro_data[2][0], tabuleiro_data[2][1], tabuleiro_data[2][2]])
    elif x >= 3 and x <= 5 and y >= 0 and y <= 2:
        quadrante.extend([tabuleiro_data[0][3], tabuleiro_data[0][4], tabuleiro_data[0][5],
                          tabuleiro_data[1][3], tabuleiro_data[1][4], tabuleiro_data[1][5],
                          tabuleiro_data[2][3], tabuleiro_data[2][4], tabuleiro_data[2][5]])
    elif x >= 6 and x <= 8 and y >= 0 and y <= 2:
        quadrante.extend([tabuleiro_data[0][6], tabuleiro_data[0][7], tabuleiro_data[0][8],
                          tabuleiro_data[1][6], tabuleiro_data[1][7], tabuleiro_data[1][8],
                          tabuleiro_data[2][6], tabuleiro_data[2][7], tabuleiro_data[2][8]])
    elif x >= 0 and x <= 2 and y >= 3 and y <= 5:
        quadrante.extend([tabuleiro_data[3][0], tabuleiro_data[3][1], tabuleiro_data[3][2],
                          tabuleiro_data[4][0], tabuleiro_data[4][1], tabuleiro_data[4][2],
                          tabuleiro_data[5][0], tabuleiro_data[5][1], tabuleiro_data[5][2]])
    elif x >= 3 and x <= 5 and y >= 3 and y <= 5:
        quadrante.extend([tabuleiro_data[3][3], tabuleiro_data[3][4], tabuleiro_data[3][5],
                          tabuleiro_data[4][3], tabuleiro_data[4][4], tabuleiro_data[4][5],
                          tabuleiro_data[5][3], tabuleiro_data[5][4], tabuleiro_data[5][5]])
    elif x >= 6 and x <= 8 and y >= 3 and y <= 5:
        quadrante.extend([tabuleiro_data[3][6], tabuleiro_data[3][7], tabuleiro_data[3][8],
                          tabuleiro_data[4][6], tabuleiro_data[4][7], tabuleiro_data[4][8],
                          tabuleiro_data[5][6], tabuleiro_data[5][7], tabuleiro_data[5][8]])
    elif x >= 0 and x <= 2 and y >= 6 and y <= 8:
        quadrante.extend([tabuleiro_data[6][0], tabuleiro_data[6][1], tabuleiro_data[6][2],
                          tabuleiro_data[7][0], tabuleiro_data[7][1], tabuleiro_data[7][2],
                          tabuleiro_data[8][0], tabuleiro_data[8][1], tabuleiro_data[8][2]])
    elif x >= 3 and x <= 5 and y >= 6 and y <= 8:
        quadrante.extend([tabuleiro_data[6][3], tabuleiro_data[6][4], tabuleiro_data[6][5],
                          tabuleiro_data[7][3], tabuleiro_data[7][4], tabuleiro_data[7][5],
                          tabuleiro_data[8][3], tabuleiro_data[8][4], tabuleiro_data[8][5]])
    elif x >= 6 and x <= 8 and y >= 6 and y <= 8:
        quadrante.extend([tabuleiro_data[6][6], tabuleiro_data[6][7], tabuleiro_data[6][8],
                          tabuleiro_data[7][6], tabuleiro_data[7][7], tabuleiro_data[7][8],
                          tabuleiro_data[8][6], tabuleiro_data[8][7], tabuleiro_data[8][8]])
    return quadrante

def Reiniciando_Tabuleiro_Data(tabuleiro_data):
    tabuleiro_data = [['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                      ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                      ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                      ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                      ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                      ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                      ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                      ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
                      ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n']]
    return tabuleiro_data

def Escrevendo_Numeros(window, jogo_data):
    quadrado = 66.7
    ajuste = 67
    for nn in range(9):
        for n in range(9):
            if jogo_data[nn][n] != 'n':
                palavra = fonte.render(str(jogo_data[nn][n]), True, preto)
                window.blit(palavra, (ajuste + n * quadrado, ajuste - 9 + nn * quadrado))

def Digitando_Numero(numero):
    try:
        numero = int(numero[1])
    except:
        numero = int(numero)
    return numero

def Numero_Digitado(window, tabuleiro_data, jogo_data, click_position_x, click_position_y, numero):
    x = click_position_x
    y = click_position_y
    if x >= 0 and x <= 8 and y >= 0 and y <= 8 and tabuleiro_data[y][x] != numero and jogo_data[y][x] == 'n' and numero != 0:
        jogo_data[y][x] = numero
        # print("Tabuleiro Check teste: ", tabuleiro_data)
        # print("Jogo Check: ", jogo_data)
        # print("X Check: ", x)
        # print("Y Check: ", y)
        # print("numero Check: ", numero)
        numero = 0
    return jogo_data, numero

def Copiar_Tabuleiro_Com_Numeros_Escondidos(tabuleiro_data, jogo_data):
    copia_tabuleiro = []
    # print("copiatab.tabul: ", tabuleiro_data)
    # print("copiatab.jog: ", jogo_data)
    for i in range(9):
        linha = []
        for j in range(9):
            if jogo_data[i][j] == 'n':
                linha.append(0)  # Substituir número escondido por zero
            else:
                linha.append(jogo_data[i][j])  # Manter o número original
        copia_tabuleiro.append(linha)
    
    # print("copiatab: ", copia_tabuleiro)
    return copia_tabuleiro

def Sudoku_Solver(copia_tabuleiro):
    start = BoardState(copia_tabuleiro)
    solver = Solver(start)
    solution = solver.solve()
    solver.validate_solution(solution)
    return solution

def Click_Button_AI_Solver(window, mouse_position_x, mouse_position_y, click_last_status, click, tabuleiro_data, jogo_data):
    quadrado = 66.7
    ajuste = 50
    x = mouse_position_x
    y = mouse_position_y 
    if x >= 700 and x <= 950 and y >= 200 and y <= 300 and click_last_status == False and click == True:
        # Cria uma cópia do tabuleiro com os números escondidos substituídos por zeros
        tabuleiro_para_resolver = Copiar_Tabuleiro_Com_Numeros_Escondidos(tabuleiro_data, jogo_data)
        # Chama a função de resolver Sudoku
        solucao = Sudoku_Solver(tabuleiro_para_resolver)
        if solucao:
            # Atualiza o jogo com os números resolvidos
            for i in range(9):
                for j in range(9):
                    # Obtém o valor da célula da solução diretamente da propriedade da BoardState
                    jogo_data[i][j] = solucao.board[i][j]
    return jogo_data

def Tabuleiro_Blank(tabuleiro_data):
    """Inicializa o tabuleiro com zeros."""
    for i in range(9):
        for j in range(9):
            tabuleiro_data[i][j] = 'n'
    return tabuleiro_data

def Criar_tabuleiro_vazio():
    """Cria um novo tabuleiro vazio."""
    tabuleiro_data = [[0 for _ in range(9)] for _ in range(9)]
    return tabuleiro_data

def Click_Button_Blank(window, mouse_position_x, mouse_position_y, click_last_status, click, tabuleiro_preenchido, escondendo_numeros, tabuleiro_data, jogo_data):
    x = mouse_position_x
    y = mouse_position_y
    if x >= 700 and x <= 950 and y >= 350 and y <= 450 and click_last_status == False and click == True:
        tabuleiro_preenchido = False
        escondendo_numeros = True
        tabuleiro_data = Tabuleiro_Blank(tabuleiro_data)

        jogo_data = Reiniciando_Tabuleiro_Data(jogo_data)

    return tabuleiro_preenchido, escondendo_numeros, tabuleiro_data, jogo_data

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            numero = pg.key.name(event.key)

    # Declarando variavel da posição do mouse
    mouse = pg.mouse.get_pos()
    mouse_position_x = mouse[0]
    mouse_position_y = mouse[1]

    # Declarando variavel do click do mouse
    click = pg.mouse.get_pressed()

    # Jogo
    Tabuleiro_Hover(window, mouse_position_x, mouse_position_y)
    click_position_x, click_position_y = Celula_Selecionada(window, mouse_position_x, mouse_position_y, click_last_status, click[0], click_position_x, click_position_y)
    Tabuleiro(window)
    Button_AI_Solver(window)
    Button_Blank_Board(window)

    tabuleiro_preenchido, escondendo_numeros, tabuleiro_data, jogo_data = Click_Button_Blank(window, mouse_position_x, mouse_position_y, click_last_status, click[0], tabuleiro_preenchido, escondendo_numeros, tabuleiro_data, jogo_data)
    Escrevendo_Numeros(window, jogo_data)
    numero = Digitando_Numero(numero)
    jogo_data, numero = Numero_Digitado(window, tabuleiro_data, jogo_data, click_position_x, click_position_y, numero)

    # Se o botão AI Solver for clicado
    jogo_data = Click_Button_AI_Solver(window, mouse_position_x, mouse_position_y, click_last_status, click[0], tabuleiro_data, jogo_data)
    
    # Click Last Status
    if click[0] == True:
        click_last_status = True
    else:
        click_last_status = False

    pg.display.update()