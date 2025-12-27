from enum import IntEnum
from ui.colors import UI_COLORS

class Rarity(IntEnum):
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