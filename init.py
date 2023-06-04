import pygame
import sys

pygame.init()
pygame.font.init()


class Game():
    FPS = 60

    def __init__(self, title, screenWidth, screenHeight):
        self.running = True
        self.window = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption(title)
        self.background = pygame.image.load("world/land.png").convert_alpha()
        self.font = pygame.font.Font("font\mana.ttf", 30)

    def update_display(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.running = False
        pygame.display.update()

    def draw_background(self):
        self.window.fill((255, 255, 255))
        self.window.blit(self.background, (0, 0))

    def draw_highscore(self):
        text = font.render("Highscore: " + str(highscore), True, (0, 0, 0))
        self.window.blit(text, (900, 30))

class Button:
    def __init__(self, x, y, image, action, scale):
        self.action = action
        self.image = pygame.image.load(image)
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            if mouse_clicked:
                self.clicked = True
        else:
            self.clicked = False

        return self.clicked


play_button = Button(400, 350, "menu/play_button.png", Game.start_game, 0.2)
quit_button = Button(400, 500, "menu/quit_button.png", Game.quit_game, 0.2)
