import pygame

pygame.init()
pygame.font.init()
font = pygame.font.Font("font\mana.ttf", 20)
highscore = 0


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
        text = font.render("Highscore: " + str(highscore), True, (0, 0, 0))
        self.window.blit(text, (900, 30))

    def draw_game_over(self):
        self.window.fill((0, 0, 0))
        text_surface = self.font.render("Game Over", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
        self.window.blit(text_surface, text_rect)
        pygame.display.update()

    def draw_victory(self):
        self.window.fill((0, 0, 0))
        text_surface = self.font.render("Gewonnen", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
        self.window.blit(text_surface, text_rect)
        pygame.display.update()


class Button():
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
