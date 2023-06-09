import pygame
import init

pygame.init()
pygame.font.init()
font = pygame.font.Font("font/mana.ttf", 20)


class Basis:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.image = pygame.image.load("world/base.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))

    def draw_basis(self):
        self.game.window.blit(self.image, (self.x, self.y))
        name_surface = font.render("Basis", True, (255, 255, 255))
        name_x = self.x + self.image.get_width() / 2 - name_surface.get_width() / 2
        self.game.window.blit(name_surface, (name_x, self.y - 30))


class Tankstelle:

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.image = pygame.image.load("world/tankstelle.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 4), int(self.image.get_height() * 4)))

    def draw_tankstelle(self):
        self.game.window.blit(self.image, (self.x, self.y))
        name_surface = font.render("Tankstelle", True, (255, 255, 255))
        name_x = self.x + self.image.get_width() / 2 - name_surface.get_width() / 2
        self.game.window.blit(name_surface, (name_x, self.y - 30))


class Mine:

    MAX_ERZ_COUNT = 10
    ERZ_PRODUCTION_RATE = 0.1

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.image = pygame.image.load("world/mine.png").convert_alpha()
        self.erzCounter = 0
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 3), int(self.image.get_height() * 3)))

    def update_erz_counter(self):
        self.erzCounter += self.ERZ_PRODUCTION_RATE / init.Game.FPS
        if self.erzCounter > self.MAX_ERZ_COUNT:
            self.erzCounter = self.MAX_ERZ_COUNT

    def draw_mine(self):
        self.game.window.blit(self.image, (self.x, self.y))
        barWidth = 50
        barHeight = 10
        barFillWidth = int(self.erzCounter / self.MAX_ERZ_COUNT * barWidth)
        barRect = pygame.Rect(self.x, self.y - barHeight - 2, barWidth, barHeight)
        fillRect = pygame.Rect(self.x, self.y - barHeight - 2, barFillWidth, barHeight)
        pygame.draw.rect(self.game.window, (0, 255, 0), fillRect)
        pygame.draw.rect(self.game.window, (255, 255, 255), barRect, 1)
        name_surface = font.render("Mine", True, (255, 255, 255))
        name_x = self.x + self.image.get_width() / 2 - name_surface.get_width() / 2
        self.game.window.blit(name_surface, (name_x, self.y - 30))


class Depot:

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.image = pygame.image.load("world/depot.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 4), int(self.image.get_height() * 4)))

    def draw_depot(self):
        self.game.window.blit(self.image, (self.x, self.y))
        name_surface = font.render("Depot", True, (255, 255, 255))
        name_x = self.x + self.image.get_width() / 2 - name_surface.get_width() / 2
        self.game.window.blit(name_surface, (name_x, self.y - 30))
