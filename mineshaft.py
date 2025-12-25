from random import random
import json
import time
from colors import UI_COLORS as uic

class Mineshaft:
    def __init__(self, id, name, color, drops):
        self.id = id
        self.name = name
        self.color = color
        self.drops = drops

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

        # Sum the total weights, create a loot table using weightings
        loot_table = {}
        total_weight = 0
        for drop, value in self.drops.items():
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
 


  
def load_mineshafts(filename):
    """ 
    Loads recipes from a JSON data file into a dictionary containing ID's
    as keys and mineshaft objects as values. Creates Mineshaft() objects
    using properties specified in the given file.
    
    Parameters:
        filename (str): The name of a json file to pull data from.
    
    Returns:
        (dict): A dictionary containing id's as keys and mineshaft objects
                as values.
    """

    # Open the json data file and return parse it into a dictionary
    with open(filename, "r") as f:
        mineshaft_json = json.load(f)

    # Converts mineshaft data into valid Mineshaft() objects.
    # Stores ID's as keys and mineshaft objects as values.
    mineshaft_registry = {}
    for id, mineshaft in mineshaft_json.items():
        mineshaft_registry[id] = Mineshaft(id, mineshaft["name"], mineshaft["color"], mineshaft["drops"])

    return mineshaft_registry

def mining_menu(inventory, mineshafts, item_list):
    """
    Displays mining menu to the user. Determines the shaft the user would
    like to mine in and processes any actions they'd like to take.

    Parameters:
        inventory (object): A valid inventory object
        mineshafts (dict): A dictionary containing the mineshafts registry
        item_list (dict): A dictionary containing the item registry
    
    Returns:
        None
    """
    while True:
        index_map = {}
        print(f"\n{uic['bold']}{uic['warm_brown']}=== MINING ==={uic['reset']}\n")

        # Display formatted mineshafts to the user
        for i, mineshaft in enumerate(mineshafts.values(), start=1):
            # Format the index and spacing that comes before each mineshaft
            index = f"{i})".ljust(4)

            # Match indexes to mineshafts and store them in index_map
            index_map[str(i)] = mineshaft

            # Display formatted mineshaft name
            color = uic[mineshaft.color]
            print(f"{uic['bold']}{index}{color}{mineshaft.name}{uic['reset']}")

            # Display drops, up to three total
            i = 0
            print("    Drops: ", end="")
            for drop in mineshaft.drops:
                # If there are more than three drops, display ... to imply more
                if i == 3:
                    print("... |", end="")
                    break
                item = item_list[drop]
                print(f"{item.rarity.color}{item.name}{uic['reset']} | ", end="")
            print("\n")
    
        # Display exit option
        final_index = f"0)".ljust(4)
        print(f"{uic['bold']}{final_index}Exit{uic['reset']}")
        print()

        # Recieve valid input from user
        print("Enter a shaft number to mine")
        user_input = input(">> ")

        # Leave mining area when user chooses to exit
        if user_input.lower() == '0':
            break

        # Handle invalid inputs
        if user_input not in index_map:
            print("Invalid input! Please try again")
            continue

        # Map the selected index to a Mineshaft() object
        mineshaft = index_map[user_input]

        # We are assuming entering an index automatically mines for now

        # Display mining animation

        print()
        print("=" * 40)
        print(f"You have entered {uic['bold']}"
              f"{uic[mineshaft.color]}{mineshaft.name}{uic['reset']}"
              f"", flush=True)
        time.sleep(0.5)
        print(f"Mining", end="", flush=True)
        for i in range(3):
            time.sleep(0.33)
            print(".", end="", flush=True)
        print()

        # Complete the mine() action and store the result
        result = mineshaft.mine(inventory, item_list)
        for item, amount in result.items():
            print(f"You recieved {item.rarity.color}{item.name}{uic['reset']} x{amount}")
            print(("=" * 40), flush=True)
            time.sleep(0.75)

        # FUTURE:
        # Display mineshafts menu
        # mineshaft.menu()

        

