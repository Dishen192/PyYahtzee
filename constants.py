import gui

# All the common variables accessed by programs throughout the project

# Score chart related variables
row_name = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "Chance", "Three of a kind", "Four of a kind", "Full house", "Small straight", "Large straight", "Yahtzee"]
row_symbols = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "Chance", "■ ■ ■", "● ● ● ●", "◆ ◆ ◆ ● ●", "■ ◆ ● ▲ ▲", "■ ◆ ● ▲ ★", "★ ★ ★ ★ ★"]

# Variables used in setting scores
chosen = False
scores = [25, 30, 40, 50]

# Game state and player related variables
no_of_players = 2
game_over = False
game_started = False

# Background colour assigned to each player
backgrounds = [gui.hex_to_rgb("#A78BFA"), gui.hex_to_rgb("#E5989B"), gui.hex_to_rgb("#84A98C"), gui.hex_to_rgb("#7EA8BE")]

# Scorecard column colour for each player
table_backgrounds = ["#6D5BAE", "#B96A74", "#5F7D67", "#5A7B8F"]

# The unicode die symbols for the dice
die_symbols = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

# Dice related variables
roll_no = 3
die_start_x = 170
die_size = 60
die_gap = 10