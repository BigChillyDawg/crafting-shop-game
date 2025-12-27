# item.py

import json
from game.rarity import Rarity

# Item class, holds a name and other traits for ease of use across numerous games.
class Item:
    def __init__(self, id, name, category, rarity, stackable, traits):
        self.id = id
        self.name = name
        self.category = category
        self.rarity = rarity
        self.stackable = stackable
        self.traits = traits