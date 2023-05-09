import pygame
import math
pygame.init()
pygame.font.init()
font = pygame.font.Font("font\mana.ttf", 20)
highscore = 0

# Spieldefinition
# ------------------------------------------------------------------------------------------------------------------ #

class Game():
    FPS = 60

    def __init__(self, title, screenWidth, screenHeight):
        self.running = True
        self.window = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption(title)
        self.background = pygame.image.load("land.png").convert_alpha()
        self.font = pygame.font.Font("font\mana.ttf", 30)

    def updateDisplay(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.running = False
        pygame.display.update()

    def drawBackground(self):
        self.window.fill((255, 255, 255))
        self.window.blit(self.background, (0, 0))

    def drawHighscore(self):
        text = font.render("Highscore: " + str(highscore), True, (255, 255, 255))
        self.window.blit(text, (900, 30))

# Mine
# ------------------------------------------------------------------------------------------------------------------ #

class Mine():
    MAX_ERZ_COUNT = 10
    ERZ_PRODUCTION_RATE = 0.1

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.image = pygame.image.load("mine.png").convert_alpha()
        self.erzCounter = 0
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 3), int(self.image.get_height() * 3)))

    def updateErzCounter(self):
        self.erzCounter += self.ERZ_PRODUCTION_RATE / Game.FPS
        if self.erzCounter > self.MAX_ERZ_COUNT:
            self.erzCounter = self.MAX_ERZ_COUNT

    def drawMine(self):
        self.game.window.blit(self.image, (self.x, self.y))
        # Balken zeichnen
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


# Depot
# ------------------------------------------------------------------------------------------------------------------ #

class Depot():

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.image = pygame.image.load("depot.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 4), int(self.image.get_height() * 4)))

    def drawDepot(self):
        self.game.window.blit(self.image, (self.x, self.y))
        name_surface = font.render("Depot", True, (255, 255, 255))
        name_x = self.x + self.image.get_width() / 2 - name_surface.get_width() / 2
        self.game.window.blit(name_surface, (name_x, self.y - 30))


# Tankstelle
# ------------------------------------------------------------------------------------------------------------------ #
class Tankstelle():

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.image = pygame.image.load("tankstelle.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 4), int(self.image.get_height() * 4)))

    def drawTankstelle(self):
        self.game.window.blit(self.image, (self.x, self.y))
        name_surface = font.render("Tankstelle", True, (255, 255, 255))
        name_x = self.x + self.image.get_width() / 2 - name_surface.get_width() / 2
        self.game.window.blit(name_surface, (name_x, self.y - 30))


# Spieler
# ------------------------------------------------------------------------------------------------------------------ #

class Player():
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.inventory = []
        self.max_inventory = 20
        self.highscore = 0
        self.image = pygame.image.load("spieler.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))
        self.animations = {
            "down": [(1, 1), (4, 1), (7, 1), (10, 1)],
            "up": [(1, 4), (4, 4), (7, 4), (10, 4)],
            "left": [(1, 7), (4, 7), (7, 7), (10, 7)],
            "right": [(1, 10), (4, 10), (7, 10), (10, 10)],
            "idle": [(1, 1), (4, 1)]
        }
        self.currentAnimation = "idle"
        self.currentFrame = 0
        self.animationDelay = 100
        self.delayCounter = 0
        self.name = "LKW"
        self.nameFont = pygame.font.SysFont("font\mana.ttf", 16)
        self.hunger = 200
        self.hunger_decrease_rate = 0.03

    def drawInventoryBar(self):
        # Berechnet den aktuellen Erzstand des Spielers als Bruchteil des maximalen Inventarplatzes
        currentCount = len(self.inventory)
        fracCount = currentCount / self.max_inventory

        # Zeichnet den Hintergrund des Balkendiagramms
        pygame.draw.rect(self.game.window, (255, 255, 255), pygame.Rect(80, 20, 200, 20))

        # Zeichnet den gefüllten Teil des Balkendiagramms
        pygame.draw.rect(self.game.window, (0, 255, 0), pygame.Rect(80, 20, int(200 * fracCount), 20))

        # Zeichnet den Text für den aktuellen Erzstand
        #font = pygame.font.SysFont("font\hello.ttf", 24)
        text = font.render("Erz: {}/{}".format(currentCount, self.max_inventory), True, (0, 0, 0))
        self.game.window.blit(text, (80, 50))

    def drawPlayer(self):
        player_image = self.image.subsurface(
            pygame.Rect(self.animations[self.currentAnimation][self.currentFrame][0] * 32,
                        self.animations[self.currentAnimation][self.currentFrame][1] * 32, 32, 32))
        self.game.window.blit(player_image, (self.x, self.y))
        # Draw the player's name above their head
        name_surface = font.render("LKW", True, (0, 0, 255))
        name_x = self.x + player_image.get_width() / 2 - name_surface.get_width() / 2
        self.game.window.blit(name_surface, (name_x, self.y - 25))

    def updatePlayer(self, mine):
        movement = pygame.Vector2(0, 0)
        self.drawInventoryBar()

        if (pygame.key.get_pressed()[pygame.K_RIGHT]):
            movement.x += 0.6
            self.currentAnimation = "right"
        if (pygame.key.get_pressed()[pygame.K_LEFT]):
            movement.x -= 0.6
            self.currentAnimation = "left"
        if (pygame.key.get_pressed()[pygame.K_UP]):
            movement.y -= 0.6
            self.currentAnimation = "up"
        if (pygame.key.get_pressed()[pygame.K_DOWN]):
            movement.y += 0.6
            self.currentAnimation = "down"

        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[
            pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.hunger -= self.hunger_decrease_rate

        if movement.length() > 0:
            movement.normalize_ip()
            movement *= 0.5
            new_x = self.x + movement.x
            new_y = self.y + movement.y
            if 90 <= new_x <= 1150:
                self.x = new_x
            if 90 <= new_y <= 640:
                self.y = new_y

            self.delayCounter += 1
            if self.delayCounter >= self.animationDelay:
                self.delayCounter = 0
                self.currentFrame += 1
                if self.currentFrame >= len(self.animations[self.currentAnimation]):
                    self.currentFrame = 0
        else:
            self.currentFrame = 0
            self.currentAnimation = "idle"


    def distance(self, x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    def collectErz(self, mine):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
            mine_rect = pygame.Rect(mine.x, mine.y, mine.image.get_width(), mine.image.get_height())
            if player_rect.colliderect(mine_rect) and self.distance(self.x, self.y, mine.x, mine.y) < 30:
                numOres = min(int(mine.erzCounter), 10)
                if numOres > 0:
                    if len(self.inventory) + numOres > self.max_inventory:
                        numOres = self.max_inventory - len(self.inventory)
                    mine.erzCounter -= numOres
                    self.inventory.extend([None] * numOres)
                if mine.erzCounter == 0:
                    self.game.game_over = True

    def depositErz(self, depot):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
            depot_rect = pygame.Rect(depot.x, depot.y, depot.image.get_width(), depot.image.get_height())
            if player_rect.colliderect(depot_rect) and self.distance(self.x, self.y, depot.x, depot.y) < 40:
                self.highscore += len(self.inventory) * 100
                global highscore
                highscore = max(highscore, self.highscore)
                self.inventory.clear()

    def refillHunger(self, tankstelle):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
            tankstelle_rect = pygame.Rect(tankstelle.x, tankstelle.y, tankstelle.image.get_width(),
                                          tankstelle.image.get_height())
            if player_rect.colliderect(tankstelle_rect) and self.distance(self.x, self.y, tankstelle.x,
                                                                          tankstelle.y) < 50:
                self.hunger = 200

    def drawHunger(self):
        pygame.draw.rect(game.window, (255, 0, 0), (500, 20, 200, 20))
        pygame.draw.rect(game.window, (0, 255, 0), (500, 20, self.hunger, 20))


# Helikopter
# ------------------------------------------------------------------------------------------------------------------ #

class Basis():
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.image = pygame.image.load("base.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))

    def drawBasis(self):
        self.game.window.blit(self.image, (self.x, self.y))
        name_surface = font.render("Basis", True, (255, 255, 255))
        name_x = self.x + self.image.get_width() / 2 - name_surface.get_width() / 2
        self.game.window.blit(name_surface, (name_x, self.y - 30))


# ------------------------------------------------------------------------------------------------------------------ #

game = Game("LKW-Spiel", 1280, 800)
player = Player(game, 400, 400)
mine = Mine(game, 200, 200)
depot = Depot(game, 1000, 500)
tankstelle = Tankstelle(game, 900, 200)
#helicopter = helicopter(game, 1000, 100)
base = Basis(game, 300, 570)

while(game.running):
    game.drawBackground()
    game.drawHighscore()
    mine.drawMine()
    depot.drawDepot()
    tankstelle.drawTankstelle()
    base.drawBasis()
    mine.updateErzCounter()
    player.drawPlayer()
    #helicopter.drawHelikopter()
    player.updatePlayer(mine)
    player.collectErz(mine)
    player.depositErz(depot)
    player.refillHunger(tankstelle)
    player.drawHunger()
    game.updateDisplay()

    if player.hunger <= 0:
        game.running = False
