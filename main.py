# main.py

import item
import recipe
from inventory import Inventory
import crafting
import json

# Parse required JSON data
item_list = item.load_items("items.json")
recipes = recipe.load_recipes("recipes.json")

# Initialize an inventory object for the user
inv = Inventory()
# Load in the user's inventory from their previous sessions
inv.load_inventory(item_list)

while True:
    # Colors for use in menu
    GREY = "\033[90m"
    RESET = "\033[0m"\
    
    # Display menu to the user and recieve an input
    inv.display_inventory()
    print()
    print(f"{GREY}=== Choose Option ==={RESET}")
    print("1) Crafting Menu")
    print("0) Save and Exit")
    user_input = input(">> ")

    # Check for invalid inputs
    if user_input not in ['0', '1']:
        print("Invalid input!")
        continue

    # If user enters 0, exit the program
    if user_input == "0":
        break

    # Enter crafting menu when user specifies
    if user_input.lower() == "1":
        crafting.crafting_menu(inv, recipes, item_list)

# Save the inventory contents for next program instance
inv.save_inventory()
print("Your game has been saved. Thank you for playing!")