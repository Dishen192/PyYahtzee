import constants

class Player:
    """
    Stores all information related to a single player,
    including scores, available options, buttons, labels
    and UI properties.
    """
    def __init__(self, name):
        self.name = name
        self.available_values = {name: 0 for name in constants.row_name}
        self.scored_values = {name: 0 for name in constants.row_name}
        self.options = {name: False for name in constants.row_name}
        self.scored = {name: False for name in constants.row_name}
        self.background = "#123456"
        self.buttons = []
        self.label = []
        self.total = 0
        self.yahtzee_bonus = 0
        self.upper_bonus = 0