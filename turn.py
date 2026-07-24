import scorecard
import constants
import dice
import gui

# This file contains everything that is needed for handling a player's turn

# Labels displaying each player's running total.
player_total_labels = []

# Creates all the players total labels and appends them to the players_total_labels list
def create_total_labels():
    for i, player in enumerate(scorecard.players):
        total_label = gui.Label(text=f"{player.name} Total: {player.total}", x=600, y=200+(i*30), bold=True, color="#FFFFFF")
        player_total_labels.append(total_label)

win_player_label = gui.Label(text = "", x = 600, y = 600, bold=True)


def switch_player():
    """
    Switches to the next player
    """
    player = scorecard.players.index(scorecard.current_player)
    scorecard.current_player = scorecard.players[0 if player==(constants.no_of_players-1) else player+1]

    constants.roll_no = 3
    dice.roll_btn.disabled=False


def start_new_turn():
    """ 
    Ends the current players turn and starts the next players turn 
    """
    constants.roll_no = 3
    dice.roll_left_label.set_text(f"Rolls left: {constants.roll_no}")

    for i, die in enumerate(dice.dice):
        die.held = False
        die.color = die.oc
        dice.dice_label[i].set_text("")


def end_game():
    """ 
    Ends the game and displays the winner
    """
    constants.game_over = True

    for player in scorecard.players:
        upper_total = sum(player.scored_values[pattern] for pattern in constants.row_name[:6])
        if upper_total>=63:
            player.total+=35
    
    for i, label in enumerate(player_total_labels):
        label.set_text(f"{scorecard.players[i].name} Total: {scorecard.players[i].total}")

    winner = max(scorecard.players, key=lambda p: p.total)
    win_player_label.set_text(f"{winner.name} wins!")

    dice.roll_btn.disabled = True

def draw(screen):
    win_player_label.draw(screen)
    for label in player_total_labels:
        label.draw(screen)