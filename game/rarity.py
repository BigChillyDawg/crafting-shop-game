from enum import IntEnum
from ui.colors import UI_COLORS

class Rarity(IntEnum):
    """
    An Enum class representing item rarity levels.
    Each rarity level has an associated integer value, color, and label.
    """
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5

    @property
    def color(self):
        return UI_COLORS[self.name.lower()]
    
    @property
    def label(self):
        return self.name.capitalize()