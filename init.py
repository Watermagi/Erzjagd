import pygame
import chars

pygame.init()
pygame.font.init()
font = pygame.font.Font("font\mana.ttf", 30)


class Game:
    FPS = 60

    def __init__(self, screenWidth, screenHeight):
        self.running = True
        self.window = pygame.display.set_mode((screenWidth, screenHeight))
        self.background = pygame.image.load("world/land.png").convert_alpha()
        self.font = pygame.font.Font("font\mana.ttf", 30)

    def update_display(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        pygame.display.update()

    def draw_background(self):
        self.window.fill((255, 255, 255))
        self.window.blit(self.background, (0, 0))

    def draw_highscore(self):
        text = font.render("Highscore: " + str(chars.highscore), True, (0, 0, 0))
        self.window.blit(text, (900, 30))

    def draw_game_over(self):
        self.window.fill((0, 0, 0))
        game_over_text = "Game Over"
        highscore_text = "Highscore: " + str(chars.highscore)
        erze_gestohlen_text = "Raube erlitten: " + str(chars.stolen)

        game_over_surface = self.font.render(game_over_text, True, (255, 255, 255))
        highscore_surface = self.font.render(highscore_text, True, (255, 255, 255))
        erze_gestohlen_surface = self.font.render(erze_gestohlen_text, True, (255, 255, 255))

        game_over_rect = game_over_surface.get_rect(
            center=(self.window.get_width() // 2, self.window.get_height() // 2 - 40))
        highscore_rect = highscore_surface.get_rect(
            center=(self.window.get_width() // 2, self.window.get_height() // 2))
        erze_gestohlen_rect = erze_gestohlen_surface.get_rect(
            center=(self.window.get_width() // 2, self.window.get_height() // 2 + 40))

        self.window.blit(game_over_surface, game_over_rect)
        self.window.blit(highscore_surface, highscore_rect)
        self.window.blit(erze_gestohlen_surface, erze_gestohlen_rect)
        pygame.display.update()

    def draw_victory(self):
        self.window.fill((0, 0, 0))
        victory_text = "Gewonnen!"
        highscore_text = "Highscore: " + str(chars.highscore)
        erze_gestohlen_text = "Raube erlitten: " + str(int(chars.stolen))

        victory_surface = self.font.render(victory_text, True, (255, 255, 255))
        highscore_surface = self.font.render(highscore_text, True, (255, 255, 255))
        erze_gestohlen_surface = self.font.render(erze_gestohlen_text, True, (255, 255, 255))

        victory_rect = victory_surface.get_rect(
            center=(self.window.get_width() // 2, self.window.get_height() // 2 - 40))
        highscore_rect = highscore_surface.get_rect(
            center=(self.window.get_width() // 2, self.window.get_height() // 2))
        erze_gestohlen_rect = erze_gestohlen_surface.get_rect(
            center=(self.window.get_width() // 2, self.window.get_height() // 2 + 40))

        self.window.blit(victory_surface, victory_rect)
        self.window.blit(highscore_surface, highscore_rect)
        self.window.blit(erze_gestohlen_surface, erze_gestohlen_rect)
        pygame.display.update()


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
