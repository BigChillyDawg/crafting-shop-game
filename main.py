# main.py

import paths
# ===== Game imports =====
import game.save_manager as save_manager
import game.state_manager as state_manager
import game.progression as progression
import game.menus as menus
from game.inventory import Inventory

# ===== UI Imports =====
from ui.colors import UI_COLORS
from ui.screens import welcome_screen, display_inventory

# Parse required JSON data
item_list = save_manager.load_items(paths.ITEM_FILE)
recipes = save_manager.load_recipes(paths.RECIPES_FILE)
mineshafts = save_manager.load_mineshafts(paths.MINESHAFTS_FILE)

# Initialize an empty inventory and load contents from save data
inv = Inventory()
save_manager.load_inventory(inv, item_list, paths.INVENTORY_SAVE)

# Load any purchased upgrades
progression.apply_upgrades(mineshafts, paths.UPGRADES_FILE, paths.UPGRADES_SAVE)
for mineshaft in mineshafts.values():
    state_manager.update_drops(mineshaft)

# Colors for use in menu
GREY = UI_COLORS["grey"]
RESET = UI_COLORS["reset"]

# Display Welcome Message
welcome_screen()

while True:
    # Display menu to the user and recieve an input
    print()
    print("=" * 40)
    display_inventory(inv)
    print()
    print(f"{GREY}=== Choose Option ==={RESET}")
    print("1) Crafting")
    print("2) Mining")
    print("0) Save and Exit")
    user_input = input(">> ")

    # Check for invalid inputs
    if user_input not in ['0', '1', '2']:
        print("Invalid input!")
        continue

    # If user enters 0, exit the program
    if user_input == "0":
        break

    # Enter crafting menu when user specifies
    if user_input == "1":
        menus.crafting_menu(inv, recipes, item_list)

    # Enter mining menu when user specifies
    if user_input == "2":
        menus.mining_menu(inv, mineshafts, item_list, paths.UPGRADES_FILE, paths.UPGRADES_SAVE)

# Save the inventory contents for next program instance
save_manager.save_inventory(inv, paths.INVENTORY_SAVE)
print("Your game has been saved. Thank you for playing!")