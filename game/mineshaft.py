from random import random
from copy import deepcopy

class Mineshaft:
    """
    A class representing a mineshaft that can be mined for resources using the
    built-in mine() function.
    """
    def __init__(self, id, name, color, drops, upgrades, cooldown):
        self.id = id
        self.name = name
        self.color = color
        self.base_drops = deepcopy(drops)
        self.drops = deepcopy(drops)
        self.upgrades = upgrades
        self.cooldown = cooldown

    def mine(self, inventory, item_list, loot_table):
        """
        Completes the mining action in the given mineshaft. Adds rewards
        to an inventory using specified weightings in the self.drops
        dictionary.
        
        Parameters:
            inventory (object): A valid Inventory() object
            item_list (dict): A dictionary containing the item registry.
            loot_table (dict): A loot table calculated using current unlocked
                               drops and their weightings

        Returns:
            (dict): A dictionary of Item() objects and aquired amounts.
        """

        # Initialize a dictionary to store final mining rewards
        rewards = {}

        # Creates a roll multiplied by the highest value in the loot table.
        # Returns the corresponding item within the loot table's range.
        # Ex: {"item1": 20, "item2": 30}. A roll of 25 returns item2.
        roll = random() * next(reversed(loot_table.values()), None)
        for drop, range in loot_table.items():
            if roll > range:
                continue
            reward = drop
            break

        # Establish the amount of the reward the user recieved from mining.
        # Upgrades can be added here later to increase the amount.
        amount = self.drops[reward]["amount"]

        # Add the item and specified amount to the users inventory
        inventory.add_item(item_list[reward], amount)

        # Save the item and recieved amount to the rewards dictionary.
        rewards[item_list[reward]] = amount

        return rewards


