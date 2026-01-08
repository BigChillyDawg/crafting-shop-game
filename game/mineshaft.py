from random import uniform
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
        self.base_cooldown_duration = cooldown.duration

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
            (dict): A dictionary of Item() objects and acquired amounts.
        """

        # Initialize a dictionary to store final mining rewards
        rewards = {}
        reward = None
        # Return an empty dict of rewards if no loot table is provided.
        if not loot_table:
            return rewards
        # Creates a roll multiplied by the highest value in the loot table.
        # Returns the corresponding item within the loot table's range.
        # Ex: {"item1": 20, "item2": 30}. A roll of 25 returns item2.
        roll = uniform(0, max(loot_table.values()))
        for drop, weight in loot_table.items():
            if roll > weight:
                continue
            reward = drop
            break

        # Check if a reward was found, if not, return the empty dictionary.
        # This shouldn't happen, but is there just in case.
        if reward is None:
            return rewards

        # Establish the amount of the reward the user received from mining.
        # Upgrades can be added here later to increase the amount.
        amount = self.drops[reward]["amount"]

        # Add the item and specified amount to the user's inventory
        inventory.add_item(item_list[reward], amount)

        # Save the item and received amount to the rewards dictionary.
        rewards[item_list[reward]] = amount

        return rewards


