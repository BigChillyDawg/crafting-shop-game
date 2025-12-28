from random import random
from ui.colors import UI_COLORS as uic

class Mineshaft:
    def __init__(self, id, name, color, drops, upgrades):
        self.id = id
        self.name = name
        self.color = color
        self.drops = drops
        self.upgrades = upgrades

    def mine(self, inventory, item_list):
        """
        Completes the mining action in the given mineshaft. Adds rewards
        to an inventory using specified weightings in the self.drops
        dictionary.
        
        Parameters:
            inventory (object): A valid Inventory() object
            item_list (dict): A dictionary containing the item registry.

        Returns:
            (dict): A dictionary of Item() objects and aquired amounts.
        """

        # Initialize a dictionary to store final mining rewards
        rewards = {}

        # Add new drops from upgrades
        

        # Sum the total weights, create a loot table using weightings
        loot_table = {}
        total_weight = 0
        for drop, value in self.drops.items():
            if value["unlocked"] == True:
                total_weight += value["weight"]
                loot_table[drop] = total_weight

        # Recieve a roll within the total weight range. Return the corresponding
        # item from the loot table.
        # Ex: {"item1": 20, "item2": 30}. Roll = 25 returns item2.
        roll = random() * total_weight
        for drop, range in loot_table.items():
            if roll > range:
                continue
            reward = drop
            break

        # Establish the amount of the reward the user recieved from mining.
        # Upgrades can be added here later to increase the amount.
        amount = self.drops[drop]["amount"]

        # Add the item and specified amount to the users inventory
        inventory.add_item(item_list[reward], amount)

        rewards[item_list[reward]] = amount

        return rewards
    
    # MOVE THIS FUNCTION TO MENUS
    def menu(self, inventory, item_list):
        while True: 
            print()
            print("=" * 40)
            print(f"You have entered {uic['bold']}"
                f"{uic[self.color]}{self.name}{uic['reset']}"
                f"", flush=True)
            
            # Display full list of drops and drop rate
            # Implement upgrades menu

            # 1) Mine
            # 2) Upgrades
            # 0) Exit

        

