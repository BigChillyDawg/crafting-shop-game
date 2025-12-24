# crafting.py
# Contains functions necessary to the crafting system

import random

def crafting_menu():
    """
    Displays crafting menu to the user. Determines the recipe the user would
    like to craft and returns it's ID as a string.

    Parameters:
        None
    
    Returns:
        (str): ID of a recipe the user would like to craft.
    """

    # Display crafting menu to user:
    print("--- CRAFTING MODE ---")

    # TEMPORARY CRAFTING SYSTEM:
    print("Enter the item you'd like to craft: ")
    return input(">> ")

    # LATER CRAFTING SYSTEM:

    # Recieve ingredients

    # Display available recipes and amounts

    # Recieve a recipe from the user

    # Return the recipe

def can_craft(recipe, inventory):
    """
    Compares a users inventory to a recipe to determine if they have enough
    ingredients.

    Parameters:
        recipe (dict): A dictionary containing crafting information
        inventory (object): A valid Inventory() object

    Returns:
        (bool): True when an inventory contains the amount of items 
                required for a given recipe.                      
    """

    # Get the contents of the users inventory
    contents_raw = inventory.inventory_contents()
    contents = {}
    
    # Convert item objects to ID's for simplicity
    for key, value in contents_raw.items():
        contents[key.id] = value

    # Store ingredients from the recipe
    ingredients = recipe["ingredients"]

    # Check if required ingredients are in the inventory
    for item in ingredients:
        if item not in contents:
            return False
        
    # Check if there are enough of each ingredient in the inventory
    for item in ingredients:
        if ingredients[item] > contents[item]:
            return False
        
    # Return true when all conditions have been met
    return True
        
def craft(recipe, inventory, item_list, id):
    """
    Use ingredients in given inventory to craft a new item. Deduct required
    items from the user's inventory, and add the product to the user's 
    inventory if crafting was sucessful.
    
    Parameters:
        recipe (dict): A dictionary containing crafting information
        inventory (object): A valid Inventory() object
        item_list (dict): A registry mapping item ID's to respective objects.
        id (str): item ID of the crafting output
    
    Returns:
        None
    """

    # Store ingredients from the recipe
    ingredients = recipe["ingredients"]

    # Loop through each ingredient and remove it from the user's inventory
    for key, value in ingredients.items():
        inventory.remove_item(item_list[key], value)
    
    # Roll a random number, compare it to crafting chance
    roll = random.random() * 100

    # If roll exceeds the crafting chance, crafting failed. Return early.
    if roll >= recipe["chance"]:
        print("Crafting failed!")
        return
    
    # If roll was within crafting chance, add item to user's inventory.
    inventory.add_item(item_list[id], recipe["amount"])
    print(f"You have sucessfully crafted {item_list[id].name}")