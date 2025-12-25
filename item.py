# item.py

import json
from rarity import Rarity

# Item class, holds a name and other traits for ease of use across numerous games.
class Item:
    def __init__(self, id, name, category, rarity, stackable, traits):
        self.id = id
        self.name = name
        self.category = category
        self.rarity = rarity
        self.stackable = stackable
        self.traits = traits

def load_items(filename):
    """ 
    Loads items from a json data file into a dictionary containing item
    ID's as keys and item objects as values. Creates Item() objects using 
    properties specified in the given file.
    
    Parameters:
        filename (str): The name of a json file to pull data from.
    
    Returns:
        (dict): A dictionary containing id's as keys and items as values.
    """

    # Open the json data file and return parse it into a dictionary
    with open(filename, "r") as f:
        item_json = json.load(f)

    # Map rarity strings to rarity objects
    rarity_map = {
        "common": Rarity.COMMON,
        "uncommon": Rarity.UNCOMMON,
        "rare": Rarity.RARE,
        "epic": Rarity.EPIC,
        "legendary": Rarity.LEGENDARY
    }

    item_registry = {}
    # Converts item data into valid item objects.
    # Stores the items and their IDs and returns them as a dictionary.
    for id, item_data in item_json.items():
        item_registry[id] = Item(id, item_data["name"], item_data["category"], rarity_map[item_data["rarity"]], item_data["stackable"], item_data["traits"])

    return item_registry