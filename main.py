import pygame
import welt
import chars
import init
import sys

pygame.init()
pygame.font.init()
BG = pygame.image.load("menu/Background.png")
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Erzjagd")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font/mana.ttf", size)


def play():
    while True:
        game = init.Game(1280, 720)
        clock = pygame.time.Clock()
        player = chars.Player(game, 400, 400)
        mine = welt.Mine(game, 200, 200)
        depot = welt.Depot(game, 1000, 500)
        tankstelle = welt.Tankstelle(game, 1000, 200)
        helicopter = chars.Helicopter(game, 200, 600)
        base = welt.Basis(game, 200, 600)

        # Game loop
        while game.running:
            clock.tick(game.FPS)
            game.update_display()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update game objects
            mine.update()
            depot.update()
            tankstelle.update()
            base.update()
            player.update()
            helicopter.chase(player)
            helicopter.update_animation()

            # Draw game objects
            game.draw_display()
            mine.draw_mine()
            depot.draw_depot()
            tankstelle.draw_tankstelle()
            base.draw_basis()
            player.draw_player()
            player.draw_ausdauer()
            helicopter.draw_helicopter()

            pygame.display.update()

            # Check if Victory or Game Over
            if player.ausdauer <= 0:
                init.Game.draw_game_over(game)
                break  # Exit the game loop and go back to the main menu
            elif player.highscore >= 1000:
                init.Game.draw_victory(game)
                break  # Exit the game loop and go back to the main menu

        # Continue to the main menu after the game is finished
        pygame.time.delay(2000)  # Delay for 2 seconds before going back to the main menu
        break  # Exit the play function and go back to the main menu



def options():
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


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = init.Button(image=pygame.image.load("menu/Play Rect.png"), pos=(640, 250),
                                  text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = init.Button(image=pygame.image.load("menu/Options Rect.png"), pos=(640, 400),
                                     text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4",
                                     hovering_color="White")
        QUIT_BUTTON = init.Button(image=pygame.image.load("menu/Quit Rect.png"), pos=(640, 550),
                                  text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# Start the game
main_menu()
