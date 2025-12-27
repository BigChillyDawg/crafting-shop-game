# menus.py
import time
from ui.colors import UI_COLORS as uic

# ===== Mining Menus =====
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