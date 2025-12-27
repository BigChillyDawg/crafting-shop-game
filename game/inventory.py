# inventory.py
import json
import game.rarity as rarity
from ui.colors import UI_COLORS

class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item, quantity):
        """ 
        Adds an item to the user's inventory wuth a specified quanitity.
        
        Parameters:
            item (object): The item object to be added to the inventory.
            quantity (int): The amount of the item to be added.

        Returns:
            None
        """

        # If quantity is negative, raise an error.
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # If item is already in inventory, increment its quantity.
        # If not, add the item to the inventory with the specified quantity.
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    def remove_item(self, item, quantity):
        """ 
        Removes a specified quanitity of an item from the users inventory.
        Raises an error if the item isn't found, or if the quanitity exceeds
        the amount of given item in the inventory.
        
        Parameters:
            item (object): The item object to be added to the inventory.
            quantity (int): The amount of the item to be added.

        Returns:
            None
        """

        # Checks if the item is in the inventory, if the quanitity doesn't
        # exceed the amount of items in the inventory, and if the given 
        # quanitity is non negative. Raises errors if conditions aren't met.
        if item not in self.items:
            raise KeyError(f"Item '{item.name}' not found in inventory")
        if quantity > self.items[item]:
            raise ValueError(f"Not enough '{item.name}' available")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # Removes the quantity of items from the inventory
        self.items[item] -= quantity

        # If quanitity is 0, remove the item from the inventory
        if self.items[item] == 0:
            del self.items[item]
        
    def inventory_contents(self):
        """ Returns a copy of the inventory's contents. """
        items = self.items.copy()
        return items
            