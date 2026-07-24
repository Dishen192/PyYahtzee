import gui
import scoring
import scorecard
import constants
import random

# Handles dice creation, rolling and interaction

roll_left_label = gui.Label(text="Rolls left: 3",font="Comic Sans MS", font_size=28, x=530, y=805, bold=True)
dice = []
dice_label = []

def create_dice():
    """
    Creates the five dice and their labels
    """
    for i in range(5):
        die = gui.Button(constants.die_start_x+(i*(constants.die_size+constants.die_gap)), 795, width=constants.die_size, height=constants.die_size, border_radius=10)
        label = gui.Label(constants.die_start_x+(i*(constants.die_size+constants.die_gap))-4, 759, text="", font_size=90, obj=die, center_to_object=False)
        die.held = False
        die.value = 0
        die.oc = die.color
        die.hc = gui.darken(die.color)
        dice.append(die)
        dice_label.append(label)

# The "Roll" button used for rolling the dice and its label
roll_btn = gui.Button(290, 870, width=100, height=50, border_radius=10)
roll_label = gui.Label(text="Roll", font="Comic Sans MS",bold=True, obj=roll_btn, font_size=36, center_to_object=True)


def roll_die():
    """
    Handles the rolling of the dice while ignoring the held dice
    """
    rolls = []
    die_values = []
    for i in range(5):
        roll = random.randint(1, 6)
        rolls.append(roll)
    for i, die in enumerate(dice):
        if not die.held:
            dice_label[i].set_text(constants.die_symbols[rolls[i]-1])
            dice[i].value = rolls[i]

    if constants.roll_no==1:
        roll_btn.disabled=True

    constants.roll_no-=1
    roll_left_label.set_text(f"Rolls left: {constants.roll_no}")
    for die in dice:
        die_values.append(die.value)
    
    scoring.calc_score(die_values)


def hold_die(indx):
    """
    Lets the player hold dice to not roll 
    """
    curr_die = dice[indx]
    if curr_die.held == True:
        curr_die.held = False
        curr_die.color = dice[indx].oc
    else:
        curr_die.held = True
        curr_die.color = dice[indx].hc

def draw(screen):
    for die in dice:
        die.draw(screen)
    
    for lbl in dice_label:
        lbl.draw(screen)
    
    roll_btn.draw(screen)
    roll_label.draw(screen)
    roll_left_label.draw(screen)

# Handle events(Button clicks)
def events(event):
    for i, die in enumerate(dice):
        die.on_click(event, func=lambda i=i: hold_die(i))
    roll_btn.on_click(event, func=roll_die)
    for btn in scorecard.current_player.buttons:
        btn.on_click(event, func=lambda btn=btn: scoring.set_score(btn.name, btn))