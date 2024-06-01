import pygame as pg
import random
import math
import time
from solverAstar import Solver, BoardState
# from randomBoard import

# Cores
preto = (0, 0, 0)
vermelho = (255, 64, 131)
verde = (64, 255, 134)
lilas_claro = (212, 175, 250)
lilas = (164, 74, 255)
branco = (255, 255, 255)
cinza = (237, 237, 237)

# Setup da tela do Jogo
window = pg.display.set_mode((1000, 800))

# Inicializando fonte
pg.font.init()
# Escolhendo uma fonte e tamanho
fonte = pg.font.SysFont("Roboto", 50, bold=True)
fontep = pg.font.SysFont("Roboto", 34, bold=True)

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
    pg.draw.rect(window, branco, (0, 0, 1000, 800))
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

def Button_Random(window):
    pg.draw.rect(window, verde, (700, 50, 250, 100))
    palavra_f = fontep.render('Jogo Aleatório', True, preto)
    window.blit(palavra_f, (715, 80))

# blank
def Button_Blank_Board(window):
    pg.draw.rect(window, cinza, (700, 200, 250, 100))
    palavra_f = fontep.render('Tabuleiro Vazio', True, preto)
    window.blit(palavra_f, (710, 230))

def Button_Astar_Solver(window):
    pg.draw.rect(window, lilas, (700, 350, 250, 100))
    palavra_f = fontep.render('Solução A*', True, preto)
    window.blit(palavra_f, (735, 380))

def Linha_Escolhida(tabuleiro_data, y):
    linha_sorteada = tabuleiro_data[y]
    return linha_sorteada

def Coluna_Escolhida(tabuleiro_data, x):
    coluna_sorteada = []
    for n in range(8):
        coluna_sorteada.append(tabuleiro_data[n][x])
    return coluna_sorteada

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

def Preenchendo_Quadrantes(tabuleiro_data, x2, y2):
    quadrante_preenchido = True
    loop = 0
    try_count = 0
    numero = 1
    while quadrante_preenchido == True:
        x = random.randint(x2, x2 + 2)
        y = random.randint(y2, y2 + 2)
        linha_sorteada = Linha_Escolhida(tabuleiro_data, y)
        coluna_sorteada = Coluna_Escolhida(tabuleiro_data, x)
        quadrante = Quadrante_Selecionado(tabuleiro_data, x, y)
        if tabuleiro_data[y][x] == 'n' and numero not in linha_sorteada and numero not in coluna_sorteada and numero not in quadrante:
            tabuleiro_data[y][x] = numero
            numero += 1
        loop += 1
        if loop == 50:
            tabuleiro_data[y2][x2] = 'n'
            tabuleiro_data[y2][x2 + 1] = 'n'
            tabuleiro_data[y2][x2 + 2] = 'n'
            tabuleiro_data[y2 + 1][x2] = 'n'
            tabuleiro_data[y2 + 1][x2 + 1] = 'n'
            tabuleiro_data[y2 + 1][x2 + 2] = 'n'
            tabuleiro_data[y2 + 2][x2] = 'n'
            tabuleiro_data[y2 + 2][x2 + 1] = 'n'
            tabuleiro_data[y2 + 2][x2 + 2] = 'n'
            loop = 0
            numero = 1
            try_count += 1
        if try_count == 10:
            break
        count = 0
        for n in range(9):
            if quadrante[n] != 'n':
                count += 1
        if count == 9:
            quadrante_preenchido = False
    return tabuleiro_data

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

def Gabarito_do_Tabuleiro(tabuleiro_data, tabuleiro_preenchido):
    while tabuleiro_preenchido == True:
        # Quadrante 1
        tabuleiro_data = Preenchendo_Quadrantes(tabuleiro_data, 0, 0)
        # Quadrante 2
        tabuleiro_data = Preenchendo_Quadrantes(tabuleiro_data, 3, 0)
        # Quadrante 3
        tabuleiro_data = Preenchendo_Quadrantes(tabuleiro_data, 6, 0)
        # Quadrante 4
        tabuleiro_data = Preenchendo_Quadrantes(tabuleiro_data, 0, 3)
        # Quadrante 7
        tabuleiro_data = Preenchendo_Quadrantes(tabuleiro_data, 0, 6)
        # Quadrante 5
        tabuleiro_data = Preenchendo_Quadrantes(tabuleiro_data, 3, 3)
        # Quadrante 8
        tabuleiro_data = Preenchendo_Quadrantes(tabuleiro_data, 3, 6)
        # Quadrante 6
        tabuleiro_data = Preenchendo_Quadrantes(tabuleiro_data, 6, 3)
        # Quadrante 9
        tabuleiro_data = Preenchendo_Quadrantes(tabuleiro_data, 6, 6)
        for nn in range(9):
            for n in range(9):
                if tabuleiro_data[nn][n] == 'n':
                    tabuleiro_data = Reiniciando_Tabuleiro_Data(tabuleiro_data)
        count = 0
        for nn in range(9):
            for n in range(9):
                if tabuleiro_data[nn][n] != 'n':
                    count += 1
        if count == 81:
            tabuleiro_preenchido = False
    return tabuleiro_data, tabuleiro_preenchido

# blank
# def Tabuleiro_Blank(tabuleiro_data):
#     #Inicializa o tabuleiro com zeros.
#     for i in range(9):
#         for j in range(9):
#             tabuleiro_data[i][j] = 'n'
#     return tabuleiro_data

# def Criar_tabuleiro_vazio():
#     #Cria um novo tabuleiro vazio.
#     tabuleiro_data = [[0 for _ in range(9)] for _ in range(9)]
#     return tabuleiro_data

def Escondendo_Numeros(tabuleiro_data, jogo_data, escondendo_numeros):
    if escondendo_numeros == True:
        numeros_aparentes = random.randint(25,54)
        print("Quantidade de números aparentes: ", numeros_aparentes )
        for n in range(numeros_aparentes):
            sorteando_numero = True
            while sorteando_numero == True:
                x = random.randint(0, 8)
                y = random.randint(0, 8)
                if jogo_data[y][x] == 'n':
                    jogo_data[y][x] = tabuleiro_data[y][x]
                    sorteando_numero = False
        escondendo_numeros = False
    return jogo_data, escondendo_numeros

def Escrevendo_Numeros(window, jogo_data):
    quadrado = 66.7
    ajuste = 67
    for nn in range(9):
        for n in range(9):
            if jogo_data[nn][n] != 'n':
                palavra = fonte.render(str(jogo_data[nn][n]), True, preto)
                window.blit(palavra, (ajuste + n * quadrado, ajuste - 9 + nn * quadrado))
                if jogo_data[nn][n] == 'X':
                    palavra = fonte.render(str(jogo_data[nn][n]), True, vermelho)
                    window.blit(palavra, (ajuste + n * quadrado, ajuste - 9 + nn * quadrado))

def Digitando_Numero(numero):
    try:
        numero = int(numero[1])
    except:
        numero = int(numero)
    return numero

def Checando_Numero_Digitado(window, tabuleiro_data, jogo_data, click_position_x, click_position_y, numero):
    x = click_position_x
    y = click_position_y
    if x >= 0 and x <= 8 and y >= 0 and y <= 8 and tabuleiro_data[y][x] == numero and jogo_data[y][x] == 'n' and numero != 0:
        jogo_data[y][x] = numero
        print("Tabuleiro Check1 teste: ", tabuleiro_data)
        print("Jogo Check1: ", jogo_data)
        print("X Check1: ", x)
        print("Y Check1: ", y)
        print("numero Check1: ", numero)
        numero = 0
    if x >= 0 and x <= 8 and y >= 0 and y <= 8 and tabuleiro_data[y][x] == numero and jogo_data[y][x] == numero and numero != 0:
        print("pass")
        pass
    if x >= 0 and x <= 8 and y >= 0 and y <= 8 and tabuleiro_data[y][x] != numero and jogo_data[y][x] == 'n' and numero != 0:
        jogo_data[y][x] = 'X'
        print("Tabuleiro Check3 teste: ", tabuleiro_data)
        print("Jogo Check3: ", jogo_data)
        print("X Check3: ", x)
        print("Y Check3: ", y)
        print("numero Check3: ", numero)
        numero = 0
    if x >= 0 and x <= 8 and y >= 0 and y <= 8 and tabuleiro_data[y][x] == numero and jogo_data[y][x] == 'X' and numero != 0:
        jogo_data[y][x] = numero
        print("Tabuleiro Check4 teste: ", tabuleiro_data)
        print("Jogo Check4: ", jogo_data)
        print("X Check4: ", x)
        print("Y Check4: ", y)
        print("numero Check4: ", numero)
        numero = 0
    return jogo_data, numero

# blank
# def Numero_Digitado(window, tabuleiro_data, jogo_data, click_position_x, click_position_y, numero):
#     x = click_position_x
#     y = click_position_y
#     if x >= 0 and x <= 8 and y >= 0 and y <= 8 and tabuleiro_data[y][x] != numero and jogo_data[y][x] == 'n' and numero != 0:
#         jogo_data[y][x] = numero
#         print("Tabuleiro Checkout teste: ", tabuleiro_data)
#         print("Jogo Checkout: ", jogo_data)
#         print("X Checkout: ", x)
#         print("Y Checkout: ", y)
#         print("numero Checkout: ", numero)
#         numero = 0
#     return jogo_data, numero

def Copiar_Tabuleiro_Com_Numeros_Escondidos(tabuleiro_data, jogo_data):
    copia_tabuleiro = []
    for i in range(9):
        linha = []
        for j in range(9):
            if jogo_data[i][j] == 'n':
                linha.append(0)  # Substituir número escondido por zero
            else:
                linha.append(tabuleiro_data[i][j])  # Manter o número original
        copia_tabuleiro.append(linha)
    return copia_tabuleiro

def Sudoku_SolverAstar(copia_tabuleiro):
    start = BoardState(copia_tabuleiro)
    solver = Solver(start)
    solution = solver.solve()
    solver.validate_solution(solution)
    print(solution)
    return solution

def Click_Button_Random(mouse_position_x, mouse_position_y, click_last_status, click, tabuleiro_preenchido, escondendo_numeros, tabuleiro_data, jogo_data):
    x = mouse_position_x
    y = mouse_position_y
    if x >= 700 and x <= 950 and y >= 50 and y <= 150 and click_last_status == False and click == True:
        tabuleiro_preenchido = True
        escondendo_numeros = True
        tabuleiro_data = Reiniciando_Tabuleiro_Data(tabuleiro_data)
        jogo_data = Reiniciando_Tabuleiro_Data(jogo_data)
    return tabuleiro_preenchido, escondendo_numeros, tabuleiro_data, jogo_data

# blank
# def Click_Button_Blank(window, mouse_position_x, mouse_position_y, click_last_status, click, tabuleiro_preenchido, escondendo_numeros, tabuleiro_data, jogo_data):
#     x = mouse_position_x
#     y = mouse_position_y
#     if x >= 700 and x <= 950 and y >= 200 and y <= 300 and click_last_status == False and click == True:
#         tabuleiro_preenchido = False
#         escondendo_numeros = True
#         tabuleiro_data = Tabuleiro_Blank(tabuleiro_data)
#         jogo_data = Reiniciando_Tabuleiro_Data(jogo_data)
#     return tabuleiro_preenchido, escondendo_numeros, tabuleiro_data, jogo_data

def Click_Button_Astar_Solver(window, mouse_position_x, mouse_position_y, click_last_status, click, tabuleiro_data, jogo_data):
    quadrado = 66.7
    ajuste = 50
    x = mouse_position_x
    y = mouse_position_y 
    if x >= 700 and x <= 950 and y >= 350 and y <= 450 and click_last_status == False and click == True:
        inicio = time.time()
        
        # Cria uma cópia do tabuleiro com os números escondidos substituídos por zeros
        tabuleiro_para_resolver = Copiar_Tabuleiro_Com_Numeros_Escondidos(tabuleiro_data, jogo_data)
        print("Tabuleiro p resolver: ", tabuleiro_para_resolver)
        quantidade_zeros = sum(row.count(0) for row in tabuleiro_para_resolver) # para verificar se é um tabuleiro com solução única - mínimo 17 numeros
        if quantidade_zeros >=64:
            print("Esse tabuleiro não pode ser resolvido, favor inserir mais números")
        else:
            # Chama a função de resolver Sudoku
            solucao = Sudoku_SolverAstar(tabuleiro_para_resolver)
            if solucao:
                # Atualiza o jogo com os números resolvidos
                for i in range(9): # linha
                    for j in range(9): # coluna
                        # Obtém o valor da célula da solução diretamente da propriedade da BoardState
                        print("Antes: ", jogo_data[i][j], "linha: ", i, "coluna: ", j)
                        print("Board: ", solucao.board[i][j], i, j)
                        jogo_data[i][j] = solucao.board[i][j]
                        # testes
                        # if jogo_data[i][j] not in tabuleiro_para_resolver[i][j]:
                        #     palavra = fonte.render(str(jogo_data[i][j]), True, lilas)
                        #     window.blit(palavra, (ajuste + j * quadrado, ajuste - 9 + i * quadrado))
                        """
                        if (i, j) not in tabuleiro_para_resolver:
                        # Célula não inicial, defina a cor da solução
                            pg.draw.rect(window, lilas_claro, ((ajuste + j * quadrado, ajuste - 9 + i * quadrado, quadrado, quadrado)))
                        else:
                        # Célula inicial, mantenha a cor original
                            pg.draw.rect(window, branco, ((ajuste + j * quadrado, ajuste - 9 + i * quadrado, quadrado, quadrado)))
                        Arrumar para ou os quadrados preenchidos ficarem lilas ou os números, essa lógica não funcionou! 
                        """
            fim = time.time()
            tempo = fim -inicio
            print(f"Tempo de execução: {tempo} segundos")
    return jogo_data

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
    Button_Random(window)
    Button_Blank_Board(window)
    Button_Astar_Solver(window)
    # random
    tabuleiro_data, tabuleiro_preenchido = Gabarito_do_Tabuleiro(tabuleiro_data, tabuleiro_preenchido)
    jogo_data, escondendo_numeros = Escondendo_Numeros(tabuleiro_data, jogo_data, escondendo_numeros)
    Escrevendo_Numeros(window, jogo_data)
    numero = Digitando_Numero(numero)
    # blank jogo_data, numero = Numero_Digitado(window, tabuleiro_data, jogo_data, click_position_x, click_position_y, numero)
    # random
    jogo_data, numero = Checando_Numero_Digitado(window, tabuleiro_data, jogo_data, click_position_x, click_position_y, numero)

    # Blank
    # tabuleiro_preenchido, escondendo_numeros, tabuleiro_data, jogo_data = Click_Button_Blank(window, mouse_position_x, mouse_position_y, click_last_status, click[0], tabuleiro_preenchido, escondendo_numeros, tabuleiro_data, jogo_data)

    # random
    tabuleiro_preenchido, escondendo_numeros, tabuleiro_data, jogo_data= Click_Button_Random(mouse_position_x, mouse_position_y, click_last_status, click[0], tabuleiro_preenchido, escondendo_numeros, tabuleiro_data, jogo_data)

    # Se o botão AI Solver for clicado
    jogo_data = Click_Button_Astar_Solver(window, mouse_position_x, mouse_position_y, click_last_status, click[0], tabuleiro_data, jogo_data)

    # Click Last Status
    if click[0] == True:
        click_last_status = True
    else:
        click_last_status = False

    pg.display.update()