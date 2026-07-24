import gui
import constants

# Contains the UI and logic for the main menu

yahtzee_label = gui.Label(x=14, y=15, text="YAHTZEE", font="Comic Sans MS", font_size=78, smooth_edge=True, color="#3D2C5A", bold=True)
choose_label = gui.Label(x=20, y=130, text="Choose number of players", font="Comic Sans MS", font_size=30, smooth_edge=True, color="#5F5F6E", bold=True)

buttons = []
labels = []

# Create buttons for choosing number of players
for i in range(2, 5):
    btn = gui.Button(x=50, y=210+((i-2)*90), width=300, height=70, color="#FFFFFF", hover_color="#F2ECFA", border_radius=15, border_width=3, border_color="#863A4C")
    btn.player_no = i
    buttons.append(btn)

# Create labels for buttons
for i in range(2, 5):
    lbl = gui.Label(text=f"{i} PLAYERS", font="Comic Sans MS", font_size=46, smooth_edge=True, color="#863A4C", bold=True, obj=buttons[i-2], center_to_object=True)
    labels.append(lbl)


def draw(screen):
    yahtzee_label.draw(screen)
    choose_label.draw(screen)

    for btn in buttons:
        btn.draw(screen)

    for lbl in labels:
        lbl.draw(screen)

def select_no_of_players(btn):
    constants.no_of_players = btn.player_no
    constants.game_started = True

# Handles events(button clicks)
def events(event):
    for btn in buttons:
        btn.on_click(event, func=lambda btn=btn: select_no_of_players(btn))