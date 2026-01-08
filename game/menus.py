# menus.py
import time
import msvcrt
from ui.screens import travelling_screen, clear_screen, check_terminal_size, display_inventory
from ui.colors import UI_COLORS as uic
from ui.format import mins_seconds
from game.progression import buy_upgrade
from paths import BALANCE_SAVE
from game.save_manager import save_wallet
import json

HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
TOP_LEFT_CURSOR = "\033[H"

# === SELECTIONS ===
def recieve_menu_key(locked=False):
    """ Reads keyboard input and returns a matching menu action """

    # Check if a key was pressed
    if not msvcrt.kbhit() and locked == False:
        return None

    # Recieve a key from the user
    key = msvcrt.getch()

    # ARROW KEYS
    if key == b'\xe0':
        key = msvcrt.getch()
        return {
            b'H': 'UP',
            b'P': 'DOWN',
            b'K': 'RIGHT',
            b'M': 'LEFT',
        }.get(key)

    # NORMAL KEYS
    key = key.lower()
    return {
        b'w': 'UP',
        b's': 'DOWN',
        b'a': 'LEFT',
        b'd': 'RIGHT',
        b'\r': 'SELECT' # ENTER
    }.get(key)

# ===== Mining Menus =====

def mineshaft_menu(mineshaft, player, item_list, upgrades_save):
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
    inventory = player.inventory
    wallet = player.wallet
    selected = 0
    first_display = True
    while True:
        check_terminal_size(40)
        divider_length = 40
        cooldown = mineshaft.cooldown

        # ===== Actions =====
        selections = [
            "Mine",
            "Purchase Upgrades",
            "Return to Mining Menu"
        ]

        # Check if user has made an input, map it if so
        key = recieve_menu_key()
        option = None
        if key == 'UP':
            selected -= 1
        elif key == "DOWN":
            selected += 1
        elif key in ("SELECT", "LEFT", "RIGHT"):
            # Map user selection
            option = selections[selected]
        
        # Ensure selection stays in range
        selected = max(0, min(selected, (len(selections) - 1)))

        # Refresh menu on key press or first time the menu is displayed
        if key or first_display:
            first_display = False
            clear_screen()
            # ===== Title =====
            print(f"{uic['bold']}{uic[mineshaft.color]}===== {mineshaft.name.upper()} ===== {uic['reset']}")
            print()
            # ===== Cooldown =====
            if cooldown.remaining() <= 0:
                print(f"{uic['off_white']}Cooldown: (Ready){uic['reset']}")
            else:
                print(f"{uic['off_white']}Cooldown: ({mins_seconds(cooldown.remaining())}){uic['reset']}")
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
            if loot_table:
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
                    print(f"    {chr(8226)} {uic['grey']}{uic['italic']}"
                          f"{upgrade['description']}{uic['reset']}")
                    print(f"    {chr(8226)} {uic['off_white']}{uic['bold']}{upgrade['features']}{uic['reset']}")
                    print(f"    {chr(8226)} {uic['off_white']}Cost: {uic['yellow']}{upgrade['cost']}{uic['reset']}")
                    print()
            
            # Display all options based on selection
            for i, selection in enumerate(selections):
                # Format the user's current selection
                if i == selected:
                    prefix = f">".ljust(4)
                else:
                    prefix = "".ljust(4)
                
                print(f"{uic['pink']}{prefix}{uic['reset']}{uic['off_white']}"
                    f"{selection}{uic['reset']}")
            
            # Return to mining menu
            if option == 'Return to Mining Menu':
                travelling_screen("The Mine", uic['warm_brown'])
                break

            # ===== Mine =====
            elif option == 'Mine':
                # Check if any drops are unlocked, continue if not
                if not loot_table:
                    clear_screen()
                    message = "No drops are currently unlocked."
                    for char in message:
                        print(f"{uic['italic']}{uic['grey']}{char}{uic['reset']}", flush=True, end="")
                        time.sleep(0.07)
                    print()
                    time.sleep(1)
                    first_display = True
                    clear_screen()
                    continue

                # Check if cooldown is ready, mine if so.
                if cooldown.trigger():
                    clear_screen()
                    print(f"{uic['off_white']}Mining{uic['reset']}", end="", flush=True)
                    for i in range(3):
                        time.sleep(0.33)
                        print(f"{uic['off_white']}.{uic['reset']}", end="", flush=True)
                    print()

                    # Complete the mine() action and store the result
                    result = mineshaft.mine(inventory, item_list, loot_table)
                    for item, amount in result.items():
                        print(f"You recieved {item.rarity.color}{item.name}{uic['reset']} x{amount}", flush=True)
                        time.sleep(1)
                    clear_screen()
                    first_display = True
                    continue

                # If cooldown is not ready, let the user know
                else:
                    clear_screen()
                    message = "Cooldown is not ready."
                    for char in message:
                        print(f"{uic['italic']}{uic['grey']}{char}{uic['reset']}", flush=True, end="")
                        time.sleep(0.07)
                    print()
                    time.sleep(1)
                    first_display = True
                    clear_screen()
                    continue

            # ===== Buy Upgrades =====
            elif option == 'Purchase Upgrades':
                clear_screen()
                upgrade_selected = 0
                while True:
                    clear_screen()
                    print()
                    print(f"{uic['bold']}{uic['orange']}===== Available Upgrades ===== {uic['reset']}")
                    
                    # Determine available selections
                    upgrade_selections = []
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
                            upgrade_selections.append((id, upgrade))
                    
                    # Add the exit option
                    upgrade_selections.append(0)
                    
                    # Print each option with an arrow beside the current selection
                    for i, selection in enumerate(upgrade_selections):
                        # Format the user's current selection
                        if i == upgrade_selected:
                            prefix = f">".ljust(4)
                        else:
                            prefix = "".ljust(4)

                        if selection != 0:
                            # Print upgrade name, description, features and cost
                            upgrade = selection[1]
                            print(f"{uic['pink']}{prefix}{uic['reset']}{uic['bold']}"
                                  f"{upgrade['label']}{uic['reset']}")
                            print(f"      {chr(8226)} {uic['grey']}{uic['italic']}{upgrade['description']}{uic['reset']}")
                            print(f"      {chr(8226)} {uic['off_white']}{uic['bold']}{upgrade['features']}{uic['reset']}")
                            print(f"      {chr(8226)} {uic['off_white']}{uic['bold']}Cost: {uic['reset']}"
                                  f"{uic['yellow']}{upgrade['cost']}{uic['reset']}")
                            print()
                        
                        else:
                            print(f"{uic['bold']}{prefix}Return to "
                                f"{uic[mineshaft.color]}{mineshaft.name}"
                                f"{uic['reset']}")
                            print()

                    # Recieve an input from a user, locked so that menu only
                    # updates on key press
                    key = recieve_menu_key(locked=True)

                    # Map user input
                    if key == 'UP':
                        upgrade_selected -= 1      
                        upgrade_selected = max(0, min(upgrade_selected, (len(upgrade_selections) - 1)))
                        continue
                    elif key == "DOWN":
                        upgrade_selected += 1
                        upgrade_selected = max(0, min(upgrade_selected, (len(upgrade_selections) - 1)))
                        continue
                    # If user chose to select, map their selection
                    elif key in ("SELECT", "LEFT", "RIGHT"):
                        upgrade_selection = upgrade_selections[upgrade_selected]
                        
                        # Return to the mine when user specifies
                        if upgrade_selection == 0:
                            clear_screen()
                            first_display = True
                            break
                        
                        # Define required placeholders based on upgrade selection
                        upgrade_id = upgrade_selection[0]
                        upgrade_object = upgrade_selection[1]
                        upgrade_cost = upgrade_object['cost']

                        # Buy item if user has enough coins
                        if not wallet.spend_coins(upgrade_cost):
                            # If not, let them know and recieve a new selection
                            clear_screen()
                            message = "You don't have enough coins!"
                            for char in message:
                                print(f"{uic['italic']}{uic['off_white']}{char}{uic['reset']}", end="", flush=True)
                                time.sleep(0.07)
                            clear_screen()
                            continue

                        # If user has all the required items, complete purchase.
                        owned_upgrades.append(upgrade_id)
                        buy_upgrade(mineshaft, upgrade_id, upgrades_save, item_list)
                        save_wallet(player, BALANCE_SAVE)
                        # Display sucessful purchase message
                        clear_screen()
                        upgrade_name = mineshaft.upgrades[upgrade_id]['label']
                        message = f"You have sucessfully purchased {upgrade_name}!"
                        for char in message:
                            print(f"{uic['bold']}{uic['neon_green']}{char}{uic['reset']}", end="", flush=True)
                            time.sleep(0.07)
                        clear_screen()
        # Check for input every 0.1 seconds
        time.sleep(0.1)

def mining_menu(player, mineshafts, item_list, upgrades_save):
    """
    Displays mining menu to the user. Determines the shaft the user would
    like to mine in and processes any actions they'd like to take.

    Parameters:
        player (object): A valid Player() object
        mineshafts (dict): A dictionary containing the mineshafts registry
        item_list (dict): A dictionary containing the item registry
    
    Returns:
        None
    """

    # Display the travelling animation
    travelling_screen("The Mine", uic['warm_brown'])

    # Hide the cursor
    print(HIDE_CURSOR, end="")
    # Initialize user selection
    selected = 0
    last_draw = 0
    while True:
        check_terminal_size(20)
        # Move cursor to top left
        print(TOP_LEFT_CURSOR, end="")
        # Check if the user pressed a key and recieve it if so
        key = recieve_menu_key()

        # Establish available selections for the user
        selections = []
        for mineshaft in mineshafts.values():
            selections.append(mineshaft)
        
        # Add the exit option
        selections.append(0)

        # Map user input
        if key == 'UP':
            selected -= 1
        elif key == "DOWN":
            selected += 1
        # If user chose to select, map their selection
        elif key in ("SELECT", "LEFT", "RIGHT"):
            # Map user selection
            mineshaft = selections[selected]

            # Leave mining area if user chose to exit
            if mineshaft == 0:
                travelling_screen("The Workshop", uic["arcane_purple"])
                break

            # Display travelling animation
            travelling_screen(mineshaft.name, uic[mineshaft.color])

            # Display mineshaft menu
            mineshaft_menu(mineshaft, player, item_list, upgrades_save)

        # Ensure selection stays in range
        selected = max(0, min(selected, (len(selections) - 1)))

        # Display menu on key press or every 0.25 seconds
        if key or last_draw + 0.25 <= time.time():
            print(f"\n{uic['bold']}{uic['warm_brown']}=== MINING ==={uic['reset']}\n")

            # Display all options based on selection
            for i, selection in enumerate(selections):
                # Format the user's current selection
                if i == selected:
                    prefix = f">".ljust(4)
                else:
                    prefix = "".ljust(4)

                # If selection is not the exit option, display formatted name
                if selection != 0:
                    color = uic[selection.color]
                    # Establish remaining cooldown
                    if selection.cooldown.remaining() > 0:
                        remaining_cooldown = mins_seconds(selection.cooldown.remaining())
                    else:
                        remaining_cooldown = "Ready"
                    
                    # Display mineshaft name
                    print(f"{uic['pink']}{prefix}{uic['reset']}{uic['bold']}{color}"
                        f"{selection.name:<20}{uic['reset']}({uic['off_white']}"
                        f"{remaining_cooldown}{uic['reset']})")
                    print()
                # Display exit option when necessary 
                else:
                    print(f"{uic['pink']}{prefix}{uic['reset']}{uic['bold']}"
                        f"{uic['off_white']}Exit{uic['reset']}")
                    print()
            # Reset the timer
            last_draw = time.time()
    # Make the cursor visible again
    print(SHOW_CURSOR, end="")
    return
    

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

    clear_screen()
    print(HIDE_CURSOR, end="")
    # Display crafting menu and recieve valid input from the user
    NAME_WIDTH = 20
    selected = 0
    first_display = True
    while True:
        # Initialize placeholders for craftable items and their indexes
        craftables = []
        # Loop through the users inventory to determine what they can craft
        for id, recipe in recipes.items():
            if recipe.can_craft(inventory):
                craftables.append(id)
        
        # Add the exit option
        craftables.append(0)

        # Check for an input from the user
        key = recieve_menu_key()
        if key == 'UP':
            selected -= 1
        elif key == "DOWN":
            selected += 1
        elif key in ("SELECT", "LEFT", "RIGHT"):
            # If user chose to exit, return
            if craftables[selected] == 0:
                travelling_screen("The Workshop", uic["arcane_purple"])
                break

            # Craft the user's desired recipe.
            recipe_final = recipes[craftables[selected]]
            success = recipe_final.craft(inventory, item_list, recipe_final.id)

            # Display the crafting animation. Let the user know if crafting succeeded or failed.
            clear_screen()
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
                print(f"{uic['italic']}{uic['grey']}Ingredients have been lost!"
                      f"{uic['reset']}", flush=True)

            time.sleep(0.75)
            clear_screen()
            # Prompt the user for another input
            first_display = True
            continue

        # Ensure selection stays in range
        selected = max(0, min(selected, (len(craftables) - 1)))
        
        # Display menu on key press or on first display
        if key or first_display:
            check_terminal_size(40)
            clear_screen()
            first_display = False
            # Title
            print(f"\n{uic['bold']}{uic['orange']}=== AVAILABLE RECIPES ==={uic['reset']}\n")

            # Display formatted recipes and ingredients to the user
            for i, recipe in enumerate(craftables):
                # Place cursor arrow beside selected recipe
                if i == selected:
                    prefix = f">".ljust(4)
                else:
                    prefix = "".ljust(4)

                if recipe != 0:
                    # Display formatted recipe name and success rate
                    recipe_color = item_list[recipe].rarity.color
                    print(f"{uic['pink']}{prefix}{uic['reset']}{uic['bold']}"
                        f"{recipe_color}{item_list[recipe].name} {uic['reset']}"
                        f"({recipes[recipe].chance}% success rate)"
                        )

                    # Display individual ingredients and amounts
                    for ingredient, amount in recipes[recipe].ingredients.items():
                        ing_color = item_list[ingredient].rarity.color
                        print(f"{'':<6}{uic['grey']}-{uic['reset']} {ing_color}"
                            f"{item_list[ingredient].name:<{NAME_WIDTH}}"
                            f"{uic['reset']} x{amount}")
                    print()
                # Display exit option    
                else:
                    print(f"{uic['pink']}{prefix}{uic['reset']}{uic['off_white']}"
                          f"Return to {uic['arcane_purple']}The Workshop"
                          f"{uic['reset']}")
                    print()
        time.sleep(0.1)
    print(SHOW_CURSOR, end="")
    return
        

# ===== Inventory Menus =====
def inventory_menu(player):
    """
    Displays the inventory menu to the user. Shows their current inventory
    contents and options to choose from.

    Parameters:
        player (object): A valid Player() object

    Returns:
        str: The user's selected menu option
    """

    clear_screen()
    # Initialize required placeholders
    selections = [
            "Crafting",
            "Mining",
            "Shop",
            "Save and Exit"
        ]
    selected = 0
    first_display = True
    print(HIDE_CURSOR, end="")

    while True:
        check_terminal_size(40)
         # Check if user has made an input, map it if so
        key = recieve_menu_key()
        if key == 'UP':
            selected -= 1
        elif key == "DOWN":
            selected += 1
        elif key in ("SELECT", "LEFT", "RIGHT"):
            # Map user selection
            print(SHOW_CURSOR, end="")
            return selections[selected]
        # Ensure selection stays in range
        selected = max(0, min(selected, (len(selections) - 1)))
        
        # Display menu on key press or first display
        if key or first_display:
            first_display = False 
            clear_screen()

            display_inventory(player.inventory)
            print()
            print(f"{uic['bold']}{uic['yellow']}Coins: {uic['reset']}"
                  f"{uic['yellow']}{player.wallet.balance}{uic['reset']}")
            print()
            print(f"{uic['grey']}=== Choose Option ==={uic['reset']}")
            print()
            # Display all options based on selection
            for i, selection in enumerate(selections):
                # Format the user's current selection
                if i == selected:
                    prefix = f">".ljust(4)
                else:
                    prefix = "".ljust(4)
                
                print(f"{uic['pink']}{prefix}{uic['reset']}{uic['off_white']}"
                        f"{selection}{uic['reset']}")
            
# ===== Shop Menu =====
def shop_menu(player, item_list):
    """
    Displays the shop menu to the user. Allows them to buy and sell items.

    Parameters:
        player (object): A valid Player() object
        item_list (dict): A dictionary containing the item registry.

    Returns:
        None
    """

    clear_screen()
    print(HIDE_CURSOR, end="")
    # Initialize required placeholders
    first_display = True
    selected = 0

    # Define available selections
    selections = []
    for item in item_list.values():
        selections.append(item)

    # Sort selections by rarity
    selections = sorted(selections, key=lambda x: x.rarity.value)

    # Exit option
    selections.append(0) 
    
    while True:
        check_terminal_size(40)
         # Check if user has made an input, map it if so
        key = recieve_menu_key()
        if key == 'UP':
            selected -= 1
        elif key == "DOWN":
            selected += 1
        elif key in ("SELECT", "LEFT", "RIGHT"):
            # Map user selection
            selection = selections[selected]

            # Exit shop if user specifies
            if selection == 0:
                travelling_screen("The Workshop", uic["arcane_purple"])
                break

            # Process buying an item
            buy_sell_menu(selection, player)
            first_display = True
            print(HIDE_CURSOR, end="")
            continue
            
        # Ensure selection stays in range
        selected = max(0, min(selected, (len(selections) - 1)))
        
        # Display menu on key press or first display
        if key or first_display:
            first_display = False 
            clear_screen()

            print(f"{uic['bold']}{uic['dark_green']}===== SHOP ====="
                  f"{uic['reset']}")
            print()
            print(f"{uic['bold']}{uic['yellow']}Coins: {uic['reset']}"
                  f"{uic['yellow']}{player.wallet.balance}{uic['reset']}")
            print()
            print(f"{'Buy':>27}{'|':>4}{'Sell':>7}")

            # Display all options based on selection
            for i, selection in enumerate(selections):
                
                # Format the user's current selection
                if i == selected:
                    prefix = f">".ljust(4)
                else:
                    prefix = "".ljust(4)

                if selection != 0:
                    price = selection.price
                    print(f"{uic['pink']}{prefix}{uic['reset']}"
                        f"{selection.rarity.color}"
                        f"{selection.name:<20}{uic['reset']}"
                        f"{uic['yellow']}{(price * 2):<6}{uic['reset']}"
                        f"{'|':<4}{uic['yellow']}{(price)}{uic['reset']}")
                else:
                    print()
                    print(f"{uic['pink']}{prefix}{uic['reset']}"
                          f"{uic['bold']}{uic['off_white']}Return to {uic['reset']}"
                          f"{uic['arcane_purple']}The Workshop{uic['reset']}")
                
        time.sleep(0.1)
    
    print(SHOW_CURSOR, end="")

def shop_history(history, item, player):
    """ 
    Helper function for buy_sell_menu(). Converts a list of shop history 
    data in the form of entrys to alist of color formatted strings relating 
    to user activity. 

    Parameters:
        history (list): List of entrys relating to user history in buy_sell_menu()
        item (object): Item() that the user is buying/selling
        player (object): The Player() interacting with the store
    
    Returns:
        None
    """

    if len(history) > 10:
        history = history[-10:]

    history_output = []
    
    for entry in history:
        action, amount, success = entry
        # === Successful Purchase ===
        if action == 'Buy' and success == True:
            history_output.append(f"{uic['off_white']}{amount}x "
            f"{item.rarity.color}{item.name}{uic['reset']} {uic['orange']}"
            f"sucessfully purchased for {uic['reset']}{uic['yellow']}"
            f"{amount * item.price * 2}{uic['reset']} {uic['green']}"
            f"coins.")
        # === Failed Purchase ===
        elif action == 'Buy' and success == False:
            history_output.append(f"{uic['off_white']}{amount}x "
            f"{item.rarity.color}{item.name}{uic['reset']} {uic['italic']}"
            f"{uic['grey']}requires {uic['reset']}{uic['yellow']}"
            f"{amount * item.price * 2}{uic['reset']}{uic['italic']}"
            f"{uic['grey']} more coins.{uic['reset']}")
        # === Successful Sale ===
        elif action == "Sell" and success == True:
            history_output.append(f"{uic['off_white']}{amount}x "
            f"{item.rarity.color}{item.name}{uic['reset']} {uic['green']}"
            f"sucessfully sold for {uic['reset']}{uic['yellow']}"
            f"{amount * item.price }{uic['reset']} {uic['green']}"
            f"coins.")
        # === Failed Sale ===
        elif action == "Sell" and success == False:
            # See how many items the user has, if none, set owned to 0.
            owned = player.inventory.items.get(item, 0)

            if owned == 0 and amount == 0:
                needed = 1
            elif owned == 0:
                needed = amount
            else:
                needed = amount - player.inventory.items[item]
            # Add the amount required to history
            history_output.append(f"{uic['off_white']}{needed}x "
            f"{uic['italic']}{uic['grey']}more {uic['reset']}"
            f"{item.rarity.color}{item.name}{uic['reset']} {uic['italic']}"
            f"{uic['grey']}required to sell.{uic['reset']}")
        
    return history_output

def buy_sell_menu(item, player):
    """
    Displays the buy/sell menu for a specific item. Allows the user to
    purchase or sell the item.

    Parameters:
        item (object): A valid Item() object
        player (object): A valid Player() object

    Returns:
        None
    """

    inv = player.inventory
    wallet = player.wallet
    
    clear_screen()
    print(HIDE_CURSOR, end="")
    first_display = True
    selected = 0

    # Define available selections
    selections = [
        "Buy 1",
        "Buy 10",
        "Sell 1",
        "Sell 10",
        "Sell All",
        "Return to Shop"
    ]

    history = []

    check_terminal_size(40)

    while True:
         # Check if user has made an input, map it if so
        key = recieve_menu_key()
        if key == 'UP':
            selected -= 1
        elif key == "DOWN":
            selected += 1
        elif key in ("SELECT", "LEFT", "RIGHT"):
            # Map user selection
            option = selections[selected]

            # Return to shop if user specifies
            if option == "Return to Shop":
                clear_screen()
                first_display = True
                break

            # Process buying or selling the item
            # === Buying ===
            if option.startswith("Buy"):
                amount = int(option.split(" ")[1])
                cost = amount * item.price * 2
                # If player has enough coins, complete purchase
                if wallet.spend_coins(cost):
                    inv.add_item(item, amount)
                    # Add message to user's history
                    history.append(('Buy', amount, True))
                # If player doesn't have enough coins
                else: 
                    history.append(('Buy', amount, False))
                    pass
            # === Selling ===
            elif option.startswith("Sell") and option != "Sell All":
                amount = int(option.split(" ")[1])
                coins = amount * item.price
                # If player has enough items
                if inv.remove_item(item, amount):
                    # Add coins and remove the amount from users inventory ^
                    wallet.add_coins(coins)
                    history.append(('Sell', amount, True))
                # If player doesn't ahve enough items
                else:
                    history.append(('Sell', amount, False))
            elif option == "Sell All":
                # If user has more than 0 of the item
                if item in inv.items:
                    # Remove the items and add coins to users wallet
                    amount = inv.items[item]
                    coins = amount * item.price
                    inv.remove_item(item, amount)
                    wallet.add_coins(coins)
                    history.append(('Sell', amount, True))
                else:
                    amount = 0
                    history.append(('Sell', amount, False))
            
        # Ensure selection stays in range
        selected = max(0, min(selected, (len(selections) - 1)))
        
        # Display menu on key press or first display
        if key or first_display:
            first_display = False 
            clear_screen()

            history_display = shop_history(history, item, player)

            print(f"{uic['bold']}{uic['dark_green']}===== SHOP ====="
                  f"{uic['reset']}")
            print()
            print(f"{uic['bold']}{uic['yellow']}Coins: {uic['reset']}"
                  f"{uic['yellow']}{wallet.balance}{uic['reset']}")
            if item in inv.items:
                quantity = inv.items[item]
            else:
                quantity = 0
            print(f"{uic['bold']}{uic['orange']}Amount Owned: {uic['reset']}"
                  f"{uic['off_white']}{quantity}x{uic['reset']}")
            print()
            print(f"{uic['bold']}{uic['off_white']}Item: {uic['reset']}"
                  f"{item.rarity.color}{item.name}{uic['reset']}")
            print(f"{uic['bold']}{uic['off_white']}Sell Price: {uic['reset']}"
                  f"{uic['yellow']}{item.price}{uic['reset']} coins")
            print(f"{uic['bold']}{uic['off_white']}Buy Price: {uic['reset']}"
                  f"{uic['yellow']}{item.price * 2}{uic['reset']} coins")
            print()

            # Display all options based on selection
            for i, selection in enumerate(selections):
                # Format the user's current selection
                if i == selected:
                    prefix = f">".ljust(4)
                else:
                    prefix = "".ljust(4)

                print(f"{uic['pink']}{prefix}{uic['reset']}{uic['off_white']}"
                        f"{selection}{uic['reset']}")
                
            # Display current instance purchase history

            if history_display:
                print()
                for message in history_display:
                    print(message)
        time.sleep(0.1)


