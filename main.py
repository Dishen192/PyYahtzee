import pygame
pygame.init()

import constants
import gui
import menu
import scoring

# Program flow:
# Menu -> Initialise game -> Main game loop

# Define window sizes
menu_size = (400, 500)
game_size = (830, 930)

screen = pygame.display.set_mode(menu_size)
pygame.display.set_caption("Yahtzee")

clock = pygame.time.Clock()
menu_running =  True
game_running = True

# Menu mode handles the menu window
def menu_mode():
    global screen
    global game_running
    global menu_running

    while menu_running:
        screen.fill(gui.hex_to_rgb("#D4C6F4"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                game_running = False
            menu.events(event)

        if constants.game_started:
            #Quit and reopen window to center window to screen
            pygame.display.quit()
            pygame.display.init()
            
            screen = pygame.display.set_mode(game_size)
            game_running=True
            menu_running=False
        else:
            menu.draw(screen)

        # Updates the game screen at 60 fps
        pygame.display.flip()
        clock.tick(60) # --> Change the 60 to your desired fps

# Game mode handles the game window
def game_mode():
    global screen
    global game_running

    import scorecard
    scorecard.create_players()
    scorecard.create_table(constants.no_of_players)

    import dice
    dice.create_dice()

    import turn
    turn.create_total_labels()

    while game_running:
        if not constants.game_over:
            if scoring.check_win():
                turn.end_game()

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                dice.events(event)
        
        screen.fill(scorecard.current_player.background)
        dice.draw(screen)
        scorecard.draw(screen)
        turn.draw(screen)

        # Updates the game screen at 60 fps
        pygame.display.flip()
        clock.tick(60) # --> Change the 60 to your desired fps

menu_mode()
game_mode()

pygame.quit()