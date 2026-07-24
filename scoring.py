import scorecard
import constants
import turn

# Implements the Yahtzee scoring rules and score calculation

# Handles the Three of a kind case
def three_of_a_kind(die_values):
    count = 0
    for i in range(1, 7):
        for val in die_values:
            if val==i:
                count+=1
        if count>=3:
            return True
        count = 0
    return False

# Handles the Four of a kind case
def four_of_a_kind(die_values):
    count = 0
    for i in range(1, 7):
        for val in die_values:
            if val==i:
                count+=1
        if count>=4:
            return True
        count = 0
    return False

# Handles the full house case
def full_house(die_values):
    counts = {}
    for val in die_values:
        if val not in counts:
            counts[val] = 1
        else:
            counts[val] += 1
        
    return sorted(counts.values()) == [2, 3]

# Handles the Small straight case
def small_straight(die_values):
    prev_val = 0
    count = 0
    max_count = 0
    die_values = list(set(die_values))
    die_values.sort()

    for i, val in enumerate(die_values):
        if i != 0:
            if val-prev_val == 1:
                count+=1
                max_count = max(max_count, count)
            else:
                count=0
        prev_val = val
    
    return max_count>=3

# Handles the Large straight case
def large_straight(die_values):
    prev_val = 0
    count = 0

    die_values = list(set(die_values))
    die_values.sort()

    for i, val in enumerate(die_values):
        if i != 0:
            if val-prev_val == 1:
                count+=1
            else:
                count=0
                break
        prev_val = val
    
    return count>=4

# Handles the Yahtzee case
def yahtzee(die_values):
    return all(val == die_values[0] for val in die_values)

# Handles the chance case
def chance(die_values):
    return True

"""
Joker rule: Let's say a player rolls a yahtzee, if this is their first yahtzee they get 50 points
If the player gets more than one yahtzee they get a bonus of 100 points but they must score in the number they've rolled
Eg: If a player has already scored a yahtzee and they roll five "6"s, they get 100 points but must score 30 in the sixes box
But if the player has already scored there then they get to score in any of --> Full house, Small straight, or Large straight
even though it isn't a valid Full house, Small straight or large straight
"""
def joker_rule(die_values):
    """
    Handles the joker rule of Yahtzee
    """
    die_value = die_values[0]
    for name in constants.row_name:
        scorecard.current_player.available_values[name] = 0
        scorecard.current_player.options[name] = False
    if scorecard.current_player.scored[constants.row_name[die_value-1]]:
        for name in constants.row_name[:6]:
            if not scorecard.current_player.scored[name]:
                scorecard.current_player.available_values[name] = 0
                scorecard.current_player.options[name] = True
        for name in constants.row_name[6:9]:
            if not scorecard.current_player.scored[name]:
                scorecard.current_player.available_values[name] = die_value*5
                scorecard.current_player.options[name] = True
        for i, name in enumerate(constants.row_name[9:12]):
            if not scorecard.current_player.scored[name]:
                scorecard.current_player.available_values[name] = constants.scores[i]
                scorecard.current_player.options[name] = True
    else:
        scorecard.current_player.available_values[constants.row_name[die_value-1]] = die_value*5
        scorecard.current_player.options[constants.row_name[die_value-1]] = True


# List of functions to call while calculating scores
func_list = [chance, three_of_a_kind, four_of_a_kind, full_house, small_straight, large_straight, yahtzee]


def display_values():
    """
    Displays the values for every available Yahtzee category
    """
    for lbl in scorecard.current_player.label:
        if not scorecard.current_player.scored[lbl.name]:
            lbl.set_text(text=str(scorecard.current_player.available_values[lbl.name]))


def calc_score(die_values):
    """
    Calculates the score for every Yahtzee category
    based on the current dice values.
    """
    scorecard.current_player.available_values = {name: 0 for name in constants.row_name}
    scorecard.current_player.options = {name: False for name in constants.row_name}

    for val in die_values:
        for i in range(6):
            if val == (i+1):
                scorecard.current_player.available_values[constants.row_name[i]]+=(i+1)
                scorecard.current_player.options[constants.row_name[i]] = True

    for i, func in enumerate(func_list):
        if func(die_values):
            scorecard.current_player.options[constants.row_name[i+6]] = True
            if i<3:
                scorecard.current_player.available_values[constants.row_name[i+6]] = sum(die_values)
            elif i>=3 and i<6:
                scorecard.current_player.available_values[constants.row_name[i+6]] = constants.scores[i-3]
            else:
                if scorecard.current_player.scored["Yahtzee"] and scorecard.current_player.scored_values["Yahtzee"]==50:
                    scorecard.current_player.yahtzee_bonus+=1
                    joker_rule(die_values)
                else:
                    scorecard.current_player.available_values[constants.row_name[i+6]] = constants.scores[i-3]
    
    display_values()

# Sets the score of the current player once they choose the category in which to score
def set_score(choice, btn):
    """
    Records the chosen score, updates the scorecard,
    recalculates totals and bonuses, and advances
    the game to the next player's turn.
    """
    global no_of_players

    scorecard.current_player.scored_values[choice] = scorecard.current_player.available_values[choice]
    scorecard.current_player.label[constants.row_name.index(choice)].set_text(text=str(scorecard.current_player.available_values[choice]))
    scorecard.current_player.scored[choice]=True
    btn.disabled = True
    
    scorecard.current_player.total = sum(scorecard.current_player.scored_values.values())+(scorecard.current_player.yahtzee_bonus*100)

    for i, label in enumerate(turn.player_total_labels):
        label.set_text(f"{scorecard.players[i].name} Total: {scorecard.players[i].total}")

    scorecard.current_player.available_values = {name: 0 for name in constants.row_name}

    for lbl in scorecard.current_player.label:
        if not scorecard.current_player.scored[lbl.name]:
            lbl.set_text(text="")

    constants.chosen = True
    turn.switch_player()
    turn.start_new_turn()

# Checks which player has won the game
def check_win():
    """
    Checks if every category for every player is scored
    and returns True if condition satisfied
    """
    check = False

    for player in scorecard.players:
        for btn in player.buttons:
            if btn.disabled:
                check=True
            else:
                check=False
                return False
    
    return check
