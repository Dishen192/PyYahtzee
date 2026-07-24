import gui
import player
import constants

# This file contains everything related to drawing the chart and the labels for the scores

# List containing every Player object in the current game.
players = []

# 1D lists storing the row labels and their background boxes
row_label = []
row_boxes = []

# 2D lists storing every score button and label
# player_buttons[player][row]
# player_labels[player][row]
player_buttons = []
player_labels = []

# Create the table box on the right side of the window
total_box = gui.Box(570, 175, width=250, height=180, border_radius=10, color="#3F3A5B")


def create_players():
    """
    Creates the required number of players
    based on the menu selection
    """
    global players
    global current_player

    players = [player.Player(f"Player {i+1}") for i in range(constants.no_of_players)]
    current_player = players[0]
    for i, pla in enumerate(players):
        pla.background = constants.backgrounds[i]


def create_row_names(i):
    """
    Creates the labels displaying the
    Yahtzee scoring categories.
    """
    global row_label

    row_box = gui.Box(10, 7+(i*60), width=180, height=55, border_radius=10)
    row_lbl = gui.Label(text=constants.row_symbols[i], font_size=30 if i>=7 else 36, obj=row_box, center_to_object=True, bold=True)

    row_boxes.append(row_box)
    row_label.append(row_lbl)


def create_row(i, j):
    """
    Creates a single button of the chart 
    """
    global row_label

    btn = gui.Button(196+(i*85), 7+(j*60), width=80, height=55, border_radius=10, color=constants.table_backgrounds[i])
    lbl = gui.Label(text="", font="Comic Sans MS", font_size=34, obj=btn, center_to_object=True, bold=True, color="#FFFFFF")
    btn.name = constants.row_name[j]
    lbl.name = constants.row_name[j]
    btn.player = players[i]

    return btn, lbl

def draw(screen):
    for box in row_boxes:
        box.draw(screen)

    total_box.draw(screen)

    for label in row_label:
        label.draw(screen)
    
    for player in player_buttons:
        for btn in player:
            btn.draw(screen)
    
    for player in player_labels:
        for label in player:
            label.draw(screen)


def create_table(no_of_players):
    """
    Draw the chart on the window 
    """
    for i in range(13):        
        create_row_names(i)

    for i in range(no_of_players):
        buttons = []
        labels = []
        for j in range(13):
            btn, lbl = create_row(i, j)
            buttons.append(btn)
            labels.append(lbl)
        player_buttons.append(buttons)
        player_labels.append(labels)

    for i, pla in enumerate(players):
        pla.buttons = player_buttons[i]
        pla.label = player_labels[i]
