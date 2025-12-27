from random import random

class Recipe:
    def __init__(self, id, ingredients, chance, output):
        self.id = id
        self.ingredients = ingredients
        self.chance = chance
        self.output = output
    
    def can_craft(self, inventory):
        """
        Compares a users inventory to a recipe to determine if they have enough
        ingredients.

        Parameters:
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
        ingredients = self.ingredients

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
    
    def craft(self, inventory, item_list, id):
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
            (bool): True for successful crafting, false for failure
        """

        # Store ingredients from the recipe
        ingredients = self.ingredients

        # Loop through each ingredient and remove it from the user's inventory
        for key, value in ingredients.items():
            inventory.remove_item(item_list[key], value)
        
        # Roll a random number to compare to crafting chance
        roll = random()

        # If roll exceeds the crafting chance, crafting failed. Return early.
        if roll >= self.chance / 100:
            return False
        
        # If roll was within crafting chance, add item to user's inventory.
        inventory.add_item(item_list[id], self.output)
        return True