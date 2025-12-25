# main.py

import item
import recipe
import crafting
import mineshaft
from colors import UI_COLORS
from inventory import Inventory
import json

# Parse required JSON data
item_list = item.load_items("items.json")
recipes = recipe.load_recipes("recipes.json")
mineshafts = mineshaft.load_mineshafts("mineshafts.json")

# Initialize an inventory object for the user
inv = Inventory()
# Load in the user's inventory from their previous sessions
inv.load_inventory(item_list)

# Colors for use in menu
GREY = UI_COLORS["grey"]
RESET = UI_COLORS["reset"]

while True:
    
    # Display menu to the user and recieve an input
    print()
    print("=" * 40)
    inv.display_inventory()
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
        crafting.crafting_menu(inv, recipes, item_list)

    # Enter mining menu when user specifies
    if user_input == "2":
        mineshaft.mining_menu(inv, mineshafts, item_list)

# Save the inventory contents for next program instance
inv.save_inventory()
print("Your game has been saved. Thank you for playing!")