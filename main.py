import pygame
import welt
import chars
import init
import sys

pygame.init()
pygame.font.init()


def initialize_game():
    pygame.init()
    game = init.Game
    clock = pygame.time.Clock()
    player = chars.Player(game, 400, 400)
    mine = welt.Mine(game, 200, 200)
    depot = welt.Depot(game, 1000, 500)
    tankstelle = welt.Tankstelle(game, 1000, 200)
    helicopter = chars.Helicopter(game, 200, 600)
    base = welt.Basis(game, 200, 600)

    # Überprüfung auf Klicks während des Menüs
    while game.running and game.start_menu:
        clock.tick(game.FPS)

        # Update display
        game.update_display()

        # Draw buttons and check for clicks
        if init.play_button.draw(game.window):
            game.start_game()
        elif init.quit_button.draw(game.window):
            pygame.quit()
            sys.exit()

        # Update game objects
        mine.draw_mine()
        depot.draw_depot()
        tankstelle.draw_tankstelle()
        base.draw_basis()
        mine.update_erz_counter()
        player.draw_player()
        player.update_player()
        helicopter.chase(player)
        helicopter.update_animation()
        player.collect_erz(mine)
        player.deposit_erz(depot)
        player.refill_ausdauer(tankstelle)
        player.draw_ausdauer()
        helicopter.draw_helicopter()
        helicopter.update_animation()

        pygame.display.update()

        # Check if Victory or Game Over
        if player.ausdauer <= 0:
            init.Game.draw_game_over(game)
        elif player.highscore >= 1000:
            init.Game.draw_victory(game)

    pygame.quit()
    sys.exit()


# Start the game
initialize_game()
