# save_manager.py

import json
from game.mineshaft import Mineshaft
from game.recipe import Recipe
from game.rarity import Rarity
from game.item import Item
from game.cooldown import Cooldown

# ===== Game State Functions =====

def load_cooldowns(filepath, registry):
    """
    Loads saved cooldown data from a JSON file and applies it to the given
    registry.

    Parameters:
        filepath (object): A valid Path() object to a JSON file containing
                           cooldown data.
        registry (dict): A dictionary mapping ID's to objects.
    
    Returns:
        None
    """
    # Load saved cooldowns if they exist
    if filepath.exists():
        with filepath.open('r') as f:
            cooldown_json = json.load(f)
    else:
        cooldown_json = {}

    # Update last used for each mineshaft with a saved cooldown
    for id, last_time in cooldown_json.items():
        registry[id].cooldown.last_used = last_time

def save_cooldowns(filepath, registry):
    """
    Saves cooldown state data for a given registry to a JSON file. Stores
    object ID's as keys and their corresponding cooldown last-used timestamps
    as values.
    
    Parameters:
        filepath (object): A valid Path() object to a JSON file used to store
                           cooldown data.
        registry (dict): A dictionary mapping ID's to objects containing
                         a Cooldown() instance.
    
    Returns:
        None
    """

    cooldowns = {}

    # Loop through a registry to find each cooldown's last use
    for id, object in registry.items():
        cooldowns[id] = object.cooldown.last_used

    # Save the final list of cooldowns to the registry.
    with filepath.open('w') as f:
        json.dump(cooldowns, f)


#  ===== Inventory Functions =====

def load_inventory(inventory, item_list, filepath):
        """
        Loads saved data from a JSON file to the inventory. Converts ID's to
        item objects.
        
        Parameters:
            inventory (object): A valid Inventory() object.
            item_list (dict): Dictionary mapping item ID's to item objects.
            filepath (object): A valid Path() object to a JSON file containing
                               inventory contents
        
        Returns:
            None
        """

        # Check if the file exists to prevent errors
        if not filepath.exists():
            return
        
        # Open inventory json file and load it into a dictionary.
        with filepath.open("r") as f:
            inventory_data = json.load(f)
        
        # Clear the items dictionary to prevent duplication
        inventory.items.clear()

        # Add saved items and their quantities to the inventory
        for key, value in inventory_data.items():
            inventory.items[item_list[key]] = value

def save_inventory(inventory, filepath):
    """
    Saves the contents of a users inventory to a JSON file.
    
    Parameters:
        inventory (object): A valid Inventory() object.
        filepath (object): A valid Path() object to a JSON file containing
                           inventory contents
        
    Returns:
        None
    """

    # Initialize and store ID's and quantities in a new dictionary.
    id_inventory = {}
    for key, value in inventory.items.items():
        id_inventory[key.id] = value

    # Save the new dictionary to a JSON file
    with filepath.open("w") as f:
        json.dump(id_inventory, f)

# ===== Mineshaft Functions =====

def load_mineshafts(mineshaft_data, cooldown_save):
    """ 
    Loads recipes from a JSON data file into a dictionary containing ID's
    as keys and mineshaft objects as values. Creates Mineshaft() objects
    using properties specified in the given file. Applies any unlocked
    upgrades to each mineshaft using apply_upgrades().
    
    Parameters:
        mineshaft_data (object): A valid Path() object to a JSON file
                                 containing mineshaft data.
        cooldown_save (object): A valid Path() object to a JSON file
                                containing saved cooldowns
        
    Returns:
        (dict): A dictionary containing id's as keys and mineshaft objects
                as values.
    """

    # Open the mineshaft data file and return parse it into a dictionary
    with mineshaft_data.open("r") as f:
        mineshaft_json = json.load(f)

    # Converts mineshaft data into valid Mineshaft() objects.
    # Stores ID's as keys and mineshaft objects as values.
    mineshaft_registry = {}
    for id, mineshaft in mineshaft_json.items():
        mineshaft_registry[id] = Mineshaft(id=id,
                                           name=mineshaft["name"],
                                           color=mineshaft["color"],
                                           drops=mineshaft["drops"],
                                           upgrades={}, 
                                           cooldown=Cooldown(mineshaft["cooldown"]))

    load_cooldowns(cooldown_save, mineshaft_registry)

    return mineshaft_registry

# ===== Recipe Functions =====
def load_recipes(filepath):
    """ 
    Loads recipes from a JSON data file into a dictionary containing ID's
    as keys and recipe objects as values. Creates Recipe() objects using 
    properties specified in the given file.
    
    Parameters:
        filepath (object): A valid Path() object to a JSON file containing 
                           recipes.
    
    Returns:
        (dict): A dictionary containing id's as keys and recipes as values.
    """

    # Open the json data file and return parse it into a dictionary
    with filepath.open("r") as f:
        recipe_json = json.load(f)


    recipe_registry = {}
    # Converts item data into valid item objects.
    # Stores the items and their IDs and returns them as a dictionary.
    for id, recipe in recipe_json.items():
        recipe_registry[id] = Recipe(id, recipe["ingredients"], recipe["chance"], recipe["amount"])

    return recipe_registry

# ===== Item Functions =====
def load_items(filepath):
    """ 
    Loads items from a json data file into a dictionary containing item
    ID's as keys and item objects as values. Creates Item() objects using 
    properties specified in the given file.
    
    Parameters:
        filepath (object): A valid pathlib file path object.
    
    Returns:
        (dict): A dictionary containing id's as keys and items as values.
    """

    # Open the json data file and return parse it into a dictionary
    with filepath.open("r") as f:
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



