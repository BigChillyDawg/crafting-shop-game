# item.py

import json

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
    Loads items from the items.json data file into a dictionary.
    
    Parameters:
        filename (str): The name of a json file to pull data from.
    
    Returns:
        (dict): A dictionary of item data from a json file.
    """

    # Open the json data file and return parse it into a dictionary
    with open(filename, "r") as f:
        item_json = json.load(f)

    item_registry = {}
    
    for id, item_data in item_json.items():
        item_registry[id] = Item(id, item_data["name"], item_data["category"], item_data["rarity"], item_data["stackable"], item_data["traits"])

    return item_registry
    
    
# def get_item(item, items):
#     """ Takes an item as an input and returns a valid Item object to be used
#     throughout the program. Matches the specific properties of each item from
#     the items.json data file.

#     Parameters:
#         item (str): The unique string identifier of an item
    
#     Returns:
#         item (object): An item object with properties outlined in the JSON
#                        data file.
#         items (dict): A dictionary of item data parsed from items.json
    
#     """

#     # Checks if an item is in the list of available items
#     if item not in items:
#         raise KeyError("Item doesn't exist.")
    
#     # Recieve item data from the JSON list of data
#     item_data = items[item]

#     # Returns an Item() object with matching properties
#     return Item(item, item_data["name"], item_data["category"], item_data["rarity"], item_data["stackable"], item_data["traits"])