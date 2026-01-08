# main.py

import paths
# ===== Game imports =====
import game.save_manager as save_manager
import game.progression as progression
import game.menus as menus
from game.inventory import Inventory
from game.player import Player
from game.coins import Wallet

# ===== UI Imports =====
from ui.colors import UI_COLORS
from ui.screens import welcome_screen, clear_screen

# Parse required JSON data
item_list = save_manager.load_items(paths.ITEM_FILE)
recipes = save_manager.load_recipes(paths.RECIPES_FILE)
mineshafts = save_manager.load_mineshafts(paths.MINESHAFTS_FILE, paths.MINESHAFT_COOLDOWNS)

# Initialize player data
player = Player(Inventory(), Wallet())
inv = player.inventory
save_manager.load_inventory(inv, item_list, paths.INVENTORY_SAVE)
save_manager.load_wallet(player, paths.BALANCE_SAVE)

# Load any purchased upgrades
progression.load_upgrades(mineshafts, paths.UPGRADES_FILE, paths.UPGRADES_SAVE)

# Colors for use in menu
GREY = UI_COLORS["grey"]
RESET = UI_COLORS["reset"]

# Display Welcome Message
welcome_screen()

while True:
    # Display menu to the user and recieve an input
    user_input =menus.inventory_menu(player)

    # Save and exit when user specifies
    if user_input == "Save and Exit":
        break

    # Enter crafting menu when user specifies
    if user_input == "Crafting":
        menus.crafting_menu(inv, recipes, item_list)

    # Enter mining menu when user specifies
    if user_input == "Mining":
        menus.mining_menu(player, mineshafts, item_list, paths.UPGRADES_SAVE)
    
    # Enter shop menu when user specifies
    if user_input == "Shop":
        menus.shop_menu(player, item_list)

# Save the inventory contents for next program instance
save_manager.save_inventory(inv, paths.INVENTORY_SAVE)
save_manager.save_cooldowns(paths.MINESHAFT_COOLDOWNS, mineshafts)
save_manager.save_wallet(player, paths.BALANCE_SAVE)
clear_screen()
print("Your game has been saved. Thank you for playing!")