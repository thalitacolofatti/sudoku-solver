
black = (0, 0, 0)
blue = (74, 160, 247)
darkgray = (56, 56, 56)
gray = (186, 186, 186)
green = (0, 224, 93)
lilac = (175, 104, 247)
lightgray = (237, 237, 237)
purple = (80, 15, 145)
red = (209, 36, 93)

class SelectNumber:
    def __init__(self, pygame, font):
        self.pygame = pygame
        self.btn_w = 70 # largura do botão
        self.btn_h = 70 # altura do botão
        self.game_font = font
        self.selected_number = 0

        self.color_black = black
        self.color_blue = blue
        self.color_gray = gray
        self.color_lightgray = lightgray
        self.color_lilac = lilac
        self.color_normal = darkgray
        self.color_purple = purple
        self.color_red = red
        self.color_selected = green
        
        self.btn_positions = [(785, 450), (865, 450), (945, 450),
                              (785, 530), (865, 530), (945, 530),
                              (785, 610), (865, 610), (945, 610)]
        
    def draw(self, pygame, surface):
        for index, pos in enumerate(self.btn_positions):
            pygame.draw.rect(surface, self.color_normal, [pos[0], pos[1], self.btn_w, self.btn_h], width=2, border_radius=10)

            # verifica se o mouse está passando por cima (hover)
            if self.button_hover(pos):
                pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.btn_w, self.btn_h], width=2, border_radius=10)
                text_surface = self.game_font.render(str(index + 1), False, self.color_selected)
            else:
                text_surface = self.game_font.render(str(index + 1), False, self.color_black)
            
            # verifica se um numero foi selecionado, depois desenha em verde
            if self.selected_number > 0:
                if self.selected_number - 1 == index:
                    pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.btn_w, self.btn_h], width=2, border_radius=10)
                    text_surface = self.game_font.render(str(index + 1), False, self.color_selected)
            
            surface.blit(text_surface, (pos[0] + 23, pos[1] + 15))

    def button_clicked(self, mouse_x: int, mouse_y: int) -> None:
        for index, pos in enumerate(self.btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                self.selected_number = index + 1
    
    def button_hover(self, pos: tuple) -> bool:
        # verifica se o mouse está passando por cima de um botão
        mouse_pos = self.pygame.mouse.get_pos()
        if self.on_button(mouse_pos[0], mouse_pos[1], pos):
            return True

    def on_button(self, mouse_x: int, mouse_y: int, pos: tuple) -> bool:
        # verifica se o ponteiro do mouse está dentro da área de um botão 
        return pos[0] < mouse_x < pos [0] + self.btn_w and pos[1] < mouse_y < pos[1] + self.btn_h

class SelectGame:
    def __init__(self, pygame, font):
        self.pygame = pygame
        self.btn_w = 260
        self.btn_h = 50
        self.game_font = font

        self.btn_positions = [(770, 40), (770, 95), (770, 150), (770, 205), (770, 260)]

    def draw(self, pygame, surface):
        for index, pos in enumerate(self.btn_positions):
            if index == 0:
                pygame.draw.rect(surface, green, (pos[0], pos[1], self.btn_w, self.btn_h), border_radius=10)
                surface.blit(self.game_font.render(str("Jogo Aleatório"), False, black), (pos[0]+ 24, pos[1] + 5))
            elif index == 1:
                pygame.draw.rect(surface, gray, (pos[0], pos[1], self.btn_w, self.btn_h), border_radius=10)
                surface.blit(self.game_font.render(str("Inserir tabuleiro"), False, black), (pos[0] + 8, pos[1]+ 5))
            elif index == 2:
                pygame.draw.rect(surface, red, (pos[0], pos[1], self.btn_w, self.btn_h), border_radius=10)
                surface.blit(self.game_font.render(str("Limpar"), False, black), (pos[0] + 74, pos[1] + 5))
            elif index == 3:
                pygame.draw.rect(surface, lilac, (pos[0], pos[1], self.btn_w, self.btn_h), border_radius=10)
                surface.blit(self.game_font.render(str("Solução A*"), False, black), (pos[0] + 54, pos[1] + 5))
            elif index == 4:
                pygame.draw.rect(surface, blue, (pos[0], pos[1], self.btn_w, self.btn_h), border_radius=10)
                surface.blit(self.game_font.render(str("Backtracking"), False, black), (pos[0] + 24, pos[1] + 5))

    def button_clicked(self, mouse_x: int, mouse_y: int):
        for index, pos in enumerate(self.btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                if index == 0:
                    btn_clicked = 0
                elif index == 1:
                    btn_clicked = 1
                elif index == 2:
                    btn_clicked = 2
                elif index == 3:
                    btn_clicked = 3
                elif index == 4:
                    btn_clicked = 4
                return btn_clicked

    
    def on_button(self, mouse_x: int, mouse_y: int, pos: tuple) -> bool:
        # verifica se o ponteiro do mouse está dentro da área de um botão 
        return pos[0] < mouse_x < pos [0] + self.btn_w and pos[1] < mouse_y < pos[1] + self.btn_h