# menus.py
import time
from ui.screens import travelling_screen, invalid_input_screen, clear_screen
from ui.colors import UI_COLORS as uic
from ui.format import mins_seconds
from game.progression import buy_upgrade
import json


# ===== Mining Menus =====

def mineshaft_menu(mineshaft, inventory, item_list, upgrades_save):
    """
    Displays an individual mineshafts menu. Displaying features such as its
    upgrades, cooldown and drop rates.
    
    mineshaft (object): A Mineshaft() object that the user has entered
    inventory (object): A player Inventory()
    item_list (dict): A dictionary mapping item IDs to Item() objects
    upgrades_data (object): A valid Path() object to a JSON file containing
                                upgrade information.
    upgrades_save (object): A valid Path() object to a JSON file containing
                            save info of upgrades a player has unlocked.

    Returns:
        None
    """
    while True:
        divider_length = 40
        cooldown = mineshaft.cooldown
        # ===== Title =====
        print()
        print(f"{uic['bold']}{uic[mineshaft.color]}===== {mineshaft.name.upper()} ===== {uic['reset']}")
        print()
        # ===== Cooldown =====
        print(f"Cooldown: {mins_seconds(cooldown.remaining())}")
        print()
        # ====== DROPS =====
        print("-" * divider_length)
        print("DROPS")
        print("-" * divider_length)

        # Sum total drop weights, create a loot table using weightings
        loot_table = {}
        total_weight = 0
        for drop, value in mineshaft.drops.items():
            if value["unlocked"] == True:
                total_weight += value["weight"]
                loot_table[drop] = total_weight

        # Display drops and drop rates from the loot table, sorted by rarity
        for drop in sorted(loot_table, key=lambda d: mineshaft.drops[d]['weight'], reverse=True):
            item = item_list[drop]
            print(f"{item.rarity.color}{item.name:<20}{uic['reset']}{(mineshaft.drops[drop]['weight'] / total_weight * 100):.2f}%")
        print("\n")

        # ===== UPGRADES =====
        print("-" * divider_length)
        print("UPGRADES")
        print("-" * divider_length)

        # Owned upgrades
        if upgrades_save.exists():
            with upgrades_save.open('r') as f:
                owned_upgrades = json.load(f)['owned']
        else:
            owned_upgrades = []

        check = chr(10003)
        # Display owned upgrades to the user
        for id, upgrade in mineshaft.upgrades.items():
            if id in owned_upgrades:
                print(f"[{uic['neon_green']}{check}{uic['reset']}] {uic['bold']}{upgrade['label']}{uic['reset']}")
                print(f"    {uic['grey']}{chr(8226)}{uic['italic']}{upgrade['description']}{uic['reset']}")
                print(f"    {uic['off_white']}{uic['bold']}{upgrade['features']}{uic['reset']}")
                print()

        # Display available upgrades to the user, ensure none are locked
        for id, upgrade in mineshaft.upgrades.items():
            # Check if the requirements for the upgrade are met
            locked = False
            for requirement in upgrade['requires']:
                if requirement not in owned_upgrades:
                    locked = True
                    break
            # If requirements aren't met, move onto the next upgrade
            if locked == True:
                continue
            if id not in owned_upgrades:
                print(f"[] {uic['bold']}{upgrade['label']}{uic['reset']}")
                print(f"    {chr(8226)} {uic['grey']}{uic['italic']}{upgrade['description']}{uic['reset']}")
                print(f"    {chr(8226)} {uic['off_white']}{uic['bold']}{upgrade['features']}{uic['reset']}")
                print(f"    {chr(8226)} {uic['off_white']}Cost:{uic['reset']}")
                for item, amount in upgrade['cost'].items():
                    print(" " * 6, end="")
                    print(f"{uic['pink']}- {uic['reset']}", end="")
                    print(f"{uic['off_white']}{item_list[item].name}{uic['reset']} {amount}x")
                    print()
        
        # ===== Actions =====
        print()
        print("1) Mine")
        print("2) Purchase Upgrades")
        print("0) Return to Mining Menu")
        user_input = input(">> ")
        
        # Handle invalid inputs
        if user_input not in ['0', '1', '2']:
            invalid_input_screen()
            clear_screen()
            continue
        
        # Return to mining menu
        if user_input == '0':
            clear_screen()
            travelling_screen("The Mine", uic['warm_brown'])
            break

        # ===== Mine =====
        if user_input == '1':
            if cooldown.trigger():
                print(f"Mining", end="", flush=True)
                for i in range(3):
                    time.sleep(0.33)
                    print(".", end="", flush=True)
                print()

                # Complete the mine() action and store the result
                result = mineshaft.mine(inventory, item_list, loot_table)
                for item, amount in result.items():
                    print(f"You recieved {item.rarity.color}{item.name}{uic['reset']} x{amount}")
                    print(("=" * 40), flush=True)
                    time.sleep(0.75)
                cooldown.reset()
                continue
            else:
                print("Not ready yet.")
                continue

        # ===== Buy Upgrades =====
        if user_input == '2':
            while True:
                print()
                print(f"{uic['bold']}{uic['orange']}===== Available Upgrades ===== {uic['reset']}")
                # Display available upgrades and their cost, along with an index 
                index_map = {}
                i = 0
                for id, upgrade in mineshaft.upgrades.items():
                    # Check if the requirements for the upgrade are met
                    locked = False
                    for requirement in upgrade['requires']:
                        if requirement not in owned_upgrades:
                            locked = True
                            break
                    # If requirements aren't met, move onto the next upgrade
                    if locked == True:
                        continue
                    # If user doesn't already own the upgrade, add it to the list
                    if id not in owned_upgrades:
                        i += 1
                        index_map[str(i)] = id
                        index = f"{i})".ljust(4)
                        print(f"{index}{uic['bold']}{upgrade['label']}{uic['reset']}")
                        print(f"    {chr(8226)}{uic['grey']}{uic['italic']}{upgrade['description']}{uic['reset']}")
                        print(f"    {chr(8226)}{uic['off_white']}{uic['bold']}{upgrade['features']}{uic['reset']}")
                        print(f"    {chr(8226)}Cost:")
                        for item, amount in upgrade['cost'].items():
                            print(" " * 6, end="")
                            print(f"{uic['pink']}- {uic['reset']}", end="")
                            print(f"{uic['off_white']}{item_list[item].name}{uic['reset']} {amount}x")
                            print()
                print("0) Return to Mineshaft")
                print()

                # ===== Upgrade Actions =====

                
                print("Enter the number of the upgrade you wish to purchase")
                upgrade_choice = input(">> ")

                # Return to Mineshaft menu when specified
                if upgrade_choice == '0':
                    break

                # Handle invalid inputs
                if upgrade_choice not in index_map:
                    invalid_input_screen()
                    continue

                # Attempt to buy upgrade user specified
                upgrade_id = index_map[upgrade_choice]
                upgrade_cost = mineshaft.upgrades[upgrade_id]['cost']

                # Compare user inventory to each item to check affordability.
                affordable = True
                for id, amount in upgrade_cost.items():
                    if (item_list[id] in inventory.items and inventory.items[item_list[id]] < amount) \
                        or item_list[id] not in inventory.items:
                        # If user didn't have enough of a required item
                        # let them know and flag affordability
                        print()
                        message = "You don't have enough items!"
                        for char in message:
                            print(f"{uic['italic']}{uic['off_white']}{char}{uic['reset']}", end="", flush=True)
                            time.sleep(0.07)
                        print()
                        affordable = False
                        break

                # Check if user had all required items.
                if affordable == False:
                    continue

                # If user has all the required items, complete purchase.
                owned_upgrades.append(upgrade_id)
                buy_upgrade(mineshaft, upgrade_id, inventory, item_list, upgrades_save)
                # Display sucessful purchase message
                upgrade_name = mineshaft.upgrades[upgrade_id]['label']
                message = f"You have sucessfully purchased {upgrade_name}!"
                for char in message:
                    print(f"{uic['bold']}{uic['neon_green']}{char}{uic['reset']}", end="", flush=True)
                    time.sleep(0.07)
                clear_screen()

def mining_menu(inventory, mineshafts, item_list, upgrades_save):
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
            print()
    
        # Display exit option
        final_index = f"0)".ljust(4)
        print(f"{uic['bold']}{final_index}Exit{uic['reset']}")
        print()

        # Recieve valid input from user
        print(f"Enter the {uic['bold']}number{uic['reset']} of the shaft" 
              f" you wish to {uic['bold']}travel to!{uic['reset']}")
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

        # Display travelling animation
        travelling_screen(mineshaft.name, uic[mineshaft.color])
        
        # Display mineshaft menu

        mineshaft_menu(mineshaft, inventory, item_list, upgrades_save)

# ===== Crafting Menus =====
def crafting_menu(inventory, recipes, item_list):
    """
    Displays crafting menu to the user. Determines the recipe the user would
    like to craft and returns it's ID as a string.

    Parameters:
        inventory (object): A valid inventory object
        recipes (dict): A dictionary containing the recipe registry
        item_list (dict): A dictionary containing the item registry
    
    Returns:
        (Recipe): Recipe() object that the user would like to craft
    """

    # Display crafting menu and recieve valid input from the user
    NAME_WIDTH = 20  # controls alignment
    while True:
        # Initialize placeholders for craftable items and their indexes
        craftables = []
        index_map = {}
        # Loop through the users inventory to determine what they can craft
        for id, recipe in recipes.items():
            if recipe.can_craft(inventory):
                craftables.append(id)
        
        print(f"\n{uic['bold']}{uic['orange']}=== AVAILABLE RECIPES ==={uic['reset']}\n")

        # Display formatted recipes and ingredients to the user
        for i, recipe in enumerate(craftables, start=1):
            # Format the index and spacing that comes before each recipe
            index = f"{i})".ljust(4)

            # Match indexes to recipe objects and store them in index_map
            index_map[str(i)] = recipes[recipe]

            # Display recipe name and success rate
            recipe_color = item_list[recipe].rarity.color
            print(f"{uic['bold']}{index}{recipe_color}{item_list[recipe].name} {uic['reset']}"
                  f"({recipes[recipe].chance}% success rate)"
                  )

            # Display individual ingredients and amounts
            for ingredient, amount in recipes[recipe].ingredients.items():
                ing_color = item_list[ingredient].rarity.color
                print(f"    {uic['pink']}-{uic['reset']} {ing_color}"
                      f"{item_list[ingredient].name:<{NAME_WIDTH}}{uic['reset']} x{amount}"
                      )
            print()

        # Handle cases where no recipes are available
        if not craftables:
            print(f"{uic['italic']}{uic['grey']}No recipes available!{uic['reset']}\n")

        # Display exit option
        final_index = f"0)".ljust(4)
        print(f"{uic['bold']}{final_index}Exit{uic['reset']}")
        print()
        
        # Recieve valid input from user
        print("Please enter the number of the recipe you'd like to craft")
        user_input = input(">> ")

        # Leave crafting menu when user chooses to exit
        if user_input.lower() == '0':
            break

        if user_input not in index_map:
            print("Invalid input! Please try again")
            continue

        # Craft the user's desired recipe.
        recipe_final = index_map[user_input]
        success = recipe_final.craft(inventory, item_list, recipe_final.id)
        
        # Display the crafting animation. Let the user know if crafting succeeded or failed.
        print()
        print("=" * 40)
        print(f"{uic['bold']}{uic['orange']}Crafting Mode{uic['reset']}")
        print("Crafting", end="", flush=True)
        for i in range(3):
            time.sleep(0.5)
            print(".", end="", flush=True)
        if success:
            print(f"{uic['green']} success!{uic['reset']}", flush=True)
            time.sleep(0.5)
            item_name = item_list[recipe_final.id].name
            item_color = item_list[recipe_final.id].rarity.color
            print(f"{recipe_final.output}x {item_color}{item_name}{uic['reset']} has been added to your inventory", flush=True)
        else:
            print(f"{uic['red']} failed.{uic['reset']}", flush=True)
            time.sleep(0.5)
            print(f"Ingredients have been lost!", flush= True)
            
        print("=" * 40)
        time.sleep(0.75)
        # Prompt the user for another input
        continue
    # When user chooses to exit, return
    return