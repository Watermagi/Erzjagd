import pygame
import math
import chars

pygame.init()
pygame.font.init()
font = pygame.font.Font("font\mana.ttf", 20)
highscore = 0
stolen = 0


def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.inventory = 0
        self.max_inventory = 20
        self.image = pygame.image.load("chars/spieler.png")
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))
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
        self.ausdauer = 100
        self.ausdauer_decrease_rate = 0.01

    def draw_inventory_bar(self):
        # Berechnet den aktuellen Erzstand des Spielers als Bruchteil des maximalen Inventarplatzes
        currentCount = self.inventory
        fracCount = currentCount / self.max_inventory
        pygame.draw.rect(self.game.window, (255, 255, 255), pygame.Rect(80, 20, 200, 20))
        pygame.draw.rect(self.game.window, (0, 255, 0), pygame.Rect(80, 20, int(200 * fracCount), 20))
        text = font.render("Erz: {}/{}".format(currentCount, self.max_inventory), True, (0, 0, 0))
        self.game.window.blit(text, (80, 50))

    def draw_player(self):
        player_image = self.image.subsurface(
            pygame.Rect(self.animations[self.currentAnimation][self.currentFrame][0] * 32,
                        self.animations[self.currentAnimation][self.currentFrame][1] * 32, 32, 32))
        self.game.window.blit(player_image, (self.x, self.y))
        name_surface = font.render("LKW", True, (0, 0, 255))
        name_x = self.x + player_image.get_width() / 2 - name_surface.get_width() / 2
        self.game.window.blit(name_surface, (name_x, self.y - 25))

    def update_player(self):
        movement = pygame.Vector2(0, 0)
        self.draw_inventory_bar()

        if pygame.key.get_pressed()[pygame.K_d]:
            movement.x += 0.5
            self.currentAnimation = "right"
        if pygame.key.get_pressed()[pygame.K_a]:
            movement.x -= 0.5
            self.currentAnimation = "left"
        if pygame.key.get_pressed()[pygame.K_w]:
            movement.y -= 0.5
            self.currentAnimation = "up"
        if pygame.key.get_pressed()[pygame.K_s]:
            movement.y += 0.5
            self.currentAnimation = "down"

        if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s] or \
                pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]:
            self.ausdauer -= self.ausdauer_decrease_rate

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

    def collect_erz(self, mine):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
            mine_rect = pygame.Rect(mine.x, mine.y, mine.image.get_width(), mine.image.get_height())
            if player_rect.colliderect(mine_rect) and distance(self.x, self.y, mine.x, mine.y) < 30:
                numOres = mine.erzCounter
                if numOres > 0:
                    space_available = self.max_inventory - self.inventory
                    ores_to_collect = min(numOres, space_available)  # Collect only up to the available space
                    ores_to_collect = int(ores_to_collect)
                    self.inventory += ores_to_collect
                    mine.erzCounter -= ores_to_collect

    def deposit_erz(self, depot):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
            depot_rect = pygame.Rect(depot.x, depot.y, depot.image.get_width(), depot.image.get_height())
            if player_rect.colliderect(depot_rect) and distance(self.x, self.y, depot.x, depot.y) < 40:
                chars.highscore += self.inventory * 100
                self.inventory = 0

    def refill_ausdauer(self, tankstelle):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
            tankstelle_rect = pygame.Rect(tankstelle.x, tankstelle.y, tankstelle.image.get_width(),
                                          tankstelle.image.get_height())
            if player_rect.colliderect(tankstelle_rect) and distance(self.x, self.y, tankstelle.x,
                                                                     tankstelle.y) < 50:
                self.ausdauer = 100

    def draw_ausdauer(self):
        pygame.draw.rect(self.game.window, (255, 0, 0), (500, 20, 100, 20))
        pygame.draw.rect(self.game.window, (0, 255, 0), (500, 20, self.ausdauer, 20))
        text = font.render("Ausdauer: {}".format(self.ausdauer - (self.ausdauer % 1)), True, (0, 0, 0))
        self.game.window.blit(text, (500, 50))


class Helicopter:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.inventory = 0
        self.max_inventory = 5
        self.wait = 0
        self.image = pygame.image.load("chars/helicopter.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 2), int(self.image.get_height() * 2)))
        self.animations = {
            "down": [(0, 0), (1, 0), (2, 0), (3, 0)],
            "up": [(0, 1), (1, 1), (2, 1), (3, 1)],
            "left": [(0, 2), (1, 2), (2, 2), (3, 2)],
            "right": [(0, 3), (1, 3), (2, 3), (3, 3)],
            "idle": [(0, 0), (1, 0), (2, 0), (3, 0)]
        }
        self.currentAnimation = "idle"
        self.currentFrame = 0
        self.animationDelay = 100
        self.delayCounter = 0

    def chase(self, player):
        if self.inventory < self.max_inventory:
            if self.wait < 4:
                self.wait += 0.002
                return
            target_x = player.x
            target_y = player.y

            # Berechnen Sie die Richtung vom Helikopter zum Spieler
            direction_x = target_x - self.x
            direction_y = target_y - self.y

            direction_length = math.sqrt(direction_x ** 2 + direction_y ** 2)
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            # Bewegen Sie den Helikopter in Richtung des Spielers
            speed = 0.2
            self.x += direction_x * speed
            self.y += direction_y * speed

            # Aktualisieren Sie die Ausrichtung des Helikopters basierend auf der Richtung
            if abs(direction_x) > abs(direction_y):
                if direction_x > 0:
                    self.currentAnimation = "right"
                else:
                    self.currentAnimation = "left"
            else:
                if direction_y > 0:
                    self.currentAnimation = "down"
                else:
                    self.currentAnimation = "up"

    def steal(self, player, helicopter):
        player_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        helicopter_rect = pygame.Rect(helicopter.x, helicopter.y, helicopter.image.get_width(),
                                      helicopter.image.get_height())
        if helicopter_rect.colliderect(player_rect) and distance(self.x, self.y, player.x, player.y) < 30:
            if player.inventory >= 0:
                space_available = self.max_inventory - self.inventory
                ores_stolen = min(player.inventory, space_available)
                self.inventory += ores_stolen
                player.inventory -= ores_stolen
                chars.stolen += 1

    def to_base(self, base):
        if self.inventory == self.max_inventory:
            target_x = base.x
            target_y = base.y

            direction_x = target_x - self.x
            direction_y = target_y - self.y

            direction_length = math.sqrt(direction_x ** 2 + direction_y ** 2)
            if direction_length != 0:
                direction_x /= direction_length
                direction_y /= direction_length

            speed = 0.2
            self.x += direction_x * speed
            self.y += direction_y * speed

            if abs(direction_x) > abs(direction_y):
                if direction_x > 0:
                    self.currentAnimation = "right"
                else:
                    self.currentAnimation = "left"
            else:
                if direction_y > 0:
                    self.currentAnimation = "down"
                else:
                    self.currentAnimation = "up"
            if distance(self.x, self.y, base.x, base.y) < 5:
                chars.highscore -= self.inventory * 100
                self.inventory = 0
                self.wait = 0

    def draw_helicopter(self):
        player_image = self.image.subsurface(
            pygame.Rect(self.animations[self.currentAnimation][self.currentFrame][0] * 64,
                        self.animations[self.currentAnimation][self.currentFrame][1] * 64, 64, 64))
        self.game.window.blit(player_image, (self.x, self.y))

    def update_animation(self):
        self.delayCounter += 1
        if self.delayCounter >= self.animationDelay:
            self.delayCounter = 0
            self.currentFrame += 1
            if self.currentFrame >= len(self.animations[self.currentAnimation]):
                self.currentFrame = 0
