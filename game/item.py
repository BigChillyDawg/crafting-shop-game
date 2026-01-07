# item.py

import json
from game.rarity import Rarity

class Item:
    """
    A class representing an item in the game. Each item has an ID, name,
    category, rarity, stackability, and traits. Integrates with the inventory,
    mineshaft, and other game based systems.
    """
    def __init__(self, id, name, category, rarity, stackable, traits, price=0):
        self.id = id
        self.name = name
        self.category = category
        self.rarity = rarity
        self.stackable = stackable
        self.traits = traits
        self.price = price