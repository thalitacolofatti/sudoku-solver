from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
from tabuleiro import Grid

# posiciona a janela do jogo na tela do dispositivo (acima, esquerda)
environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (180, 80) # no exemplo (400,100)

# cria a superfície da janela e muda o título da janela
surface = pg.display.set_mode((1080, 720)) # no exemplo (1200,900) logo as celulas serao de 80x80 e nao 100x100
pg.display.set_caption('Solucionador Sudoku')

# sons
pg.mixer.init()

effect_button = pg.mixer.Sound('sudoku-solver/sounds/button.mp3')
effect_clean = pg.mixer.Sound('sudoku-solver/sounds/clean.mp3')
effect_set = pg.mixer.Sound('sudoku-solver/sounds/set.mp3')
effect_solve = pg.mixer.Sound('sudoku-solver/sounds/solution.mp3')
effect_button.set_volume(0.5)
effect_clean.set_volume(0.5)
effect_set.set_volume(0.5)
effect_solve.set_volume(0.5)
play_win = True

# fontes
pg.font.init()
game_font = pg.font.SysFont('inkfree', 34, bold=True)
game_font_g = pg.font.SysFont('inkfree', 60, bold=True)
game_font_p = pg.font.SysFont('inkfree', 20)

grid = Grid(pg, game_font)
running = True

# parte das cores
lightgray = (237, 237, 237)
purple = (80, 15, 145)
darkgray = (56, 56, 56)

# loop do jogo
while running:
    # verifica eventos de entrada
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN and not grid.win:
            if pg.mouse.get_pressed()[0]: # verifica se o botão esquerdo foi pressionado
                pos = pg.mouse.get_pos()
                grid.get_mouse_click(pos[0], pos[1])
                # cada som toca dependendo da posição do clique do mouse
                if (pos[0] <= 720 and pos[1] <= 720) or (786 <= pos[0] <= 1013 and 440 <= pos[1] <= 680):
                    effect_button.play()
                elif 770 <= pos[0] <= 1030: 
                    if 40 <= pos[1] <= 145:
                        effect_set.play()
                    elif 150 <= pos[1] <= 200:
                        effect_clean.play()
                    elif 205 <= pos[1] <= 310:
                        effect_solve.play()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and grid.win:
                grid.win = False

    #pinta de cinza a superfície da janela
    surface.fill(lightgray)

    # desenha o tabuleiro
    grid.draw_all(pg, surface)

    if grid.filled > 0:
        if grid.divisor == 5:
            level = "Nível Difícil"
        elif grid.divisor == 6:
            level = "Nível Intermediário"
        elif grid.divisor == 7:
            level = "Nível Fácil"
        level_surface = game_font_p.render(level, False, darkgray)
        surface.blit(level_surface, (790, 340))
        occupied_num_surface = game_font_p.render((str(grid.filled) + " números preenchidos"), False, darkgray)
        surface.blit(occupied_num_surface, (790, 370))
    else:
        msg_surface = game_font_p.render(("Insira os números no tabuleiro"), False, darkgray)
        surface.blit(msg_surface, (765, 340))

    if grid.time_solution > 0:
        time_solution_surface = game_font_p.render((f"{grid.time_solution:.4f}" + "s para solucionar"), False, darkgray) 
        surface.blit(time_solution_surface, (790, 400))

    if grid.win:
        pg.draw.rect(surface, lightgray, (220, 310, 280, 120), border_radius=20)
        won_surface = game_font_g.render("Vitória!", False, purple)
        surface.blit(won_surface, (264, 320))
        space_surface = game_font_p.render("Aperte espaço para continuar", False, darkgray)
        surface.blit(space_surface, (234, 390))
        if play_win:
            effect_solve.play()
            play_win = False

    # atualiza a superfície da janela
    pg.display.flip()