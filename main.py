import pygame
import welt
import chars
import init
import sys

pygame.init()
pygame.font.init()
BG = pygame.image.load("menu/background.png")
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Erzjagd")


def get_font(size):  # gibt die benötigte Font-Größe an
    return pygame.font.Font("font/mana.ttf", size)


def reset_game():    # Setzt den Highscore auf 0 d.h das Game startet von vorne
    chars.highscore = 0


def play():     # Spiel-Loop
    while True:
        game = init.Game(1280, 720)                         # Hier bekommen die Objekte/Charaktere ihre Koordinaten
        player = chars.Player(game, 620, 360)
        mine = welt.Mine(game, 200, 200)
        depot = welt.Depot(game, 1000, 500)
        tankstelle = welt.Tankstelle(game, 1000, 200)
        helicopter = chars.Helicopter(game, 200, 500)
        base = welt.Basis(game, 200, 500)

        # Game loop
        while game.running:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            game.draw_background()                      # Alle Funktionen um das Spiel zum Laufen zu bringen
            game.draw_highscore()                       # Hier wird alles gezeichnet und die Funktionen ein gerufen
            mine.draw_mine()
            depot.draw_depot()
            tankstelle.draw_tankstelle()
            base.draw_basis()
            player.collect_erz(mine)
            player.deposit_erz(depot)
            player.refill_ausdauer(tankstelle)
            player.draw_ausdauer()
            player.draw_player()
            helicopter.draw_helicopter()
            mine.update_erz_counter()
            player.update_player()
            helicopter.chase(player)
            helicopter.steal(player, helicopter)
            helicopter.to_base(base)
            helicopter.update_animation()
            game.update_display()

            # Check, ob gewonnen oder Verloren
            if player.ausdauer <= 0:
                init.Game.draw_game_over(game)
                reset_game()
                break
            elif chars.highscore >= 4000:
                init.Game.draw_victory(game)
                reset_game()
                break
            elif chars.highscore <= -100:
                init.Game.draw_game_over(game)
                reset_game()
                break

        # Sobald das Spiel abgeschlossen ist, kehrt es zum Hauptmenü zurück
        pygame.time.delay(4000)  # Zeitintervall bevor es zum Menü geht
        break  # Damit es zum Hauptmenü geht und das Spiel abgebrochen wird
    pygame.display.update()


def options():              # Optionsmenü wird erstellt
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = init.Button(image=None, pos=(640, 460),
                                   text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():            # Hauptmenü wird erstellt
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = init.Button(image=pygame.image.load("menu/play_rect.png"), pos=(640, 250),
                                  text_input="PLAY", font=get_font(75), base_color="White", hovering_color="green")
        OPTIONS_BUTTON = init.Button(image=pygame.image.load("menu/options_rect.png"), pos=(640, 400),
                                     text_input="OPTIONS", font=get_font(75), base_color="White",
                                     hovering_color="green")
        QUIT_BUTTON = init.Button(image=pygame.image.load("menu/quit_rect.png"), pos=(640, 550),
                                  text_input="QUIT", font=get_font(75), base_color="White", hovering_color="green")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:        # Wenn Mauszeiger auf Button kommt, dann ...
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# Hauptmenü startet als erstes
main_menu()
