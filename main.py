# main.py

import item
from inventory import Inventory
import crafting
import json

# Parse required JSON data
item_list = item.load_items("items.json")
with open("recipes.json", "r") as f:
    recipes = json.load(f)

# Initialize an inventory object for the user
inv = Inventory()
# Load in the user's inventory from their previous sessions
inv.load_inventory(item_list)

while True:
    # Display menu to the user and recieve an input
    print("-" * 100)
    print("Please enter an item to add to your inventory!")
    print("Enter display to show your inventory")
    print("Enter 'C' for crafting!")
    user_input = input(">> ")

    # If user enters 0, exit the program
    if user_input == "0":
        break

    if user_input.lower() == "c":
        desired_recipe = crafting.crafting_menu()
        craftable = crafting.can_craft(recipes[desired_recipe], inv)
        if not craftable:
            print("You do not have enough items to craft this recipe!")
        else:
            crafting.craft(recipes[desired_recipe], inv, item_list, desired_recipe)
        continue

    # Display the user's inventory if they enter display
    if user_input.lower() == "display":
        # If user's inventory is empty, let them know
        if not inv.inventory_contents():
            print("Inventory is empty!")
            continue
        
        # Print inventory title
        print("\033[1;90m==== INVENTORY ====\033[0m")
        
        # Loop through inventory to display items to user
        for key, value in inv.inventory_contents().items():
            # Match rarities to text colors
            match key.rarity:
                case "uncommon":
                    color = "\033[32m"
                case "rare":
                    color = "\033[94m"
                case "epic":
                    color = "\033[95m"
                case "legendary":
                    color = "\033[93m"
                case _:
                    color = "\033[90m"
            
            # Print item and quanitity formatted with colour
            print(f"{color}{key.name}\033[0m: {value}")
        continue
    
    # Handles cases where user enters an invalid input
    if user_input not in item_list:
        print("Item doesn't exist")
        continue

    # Define the current item from list of item data
    # Increment the amount of their items by one and 
    # display the increment to the terminal
    current_item = item_list[user_input]
    inv.add_item(current_item, 1)
    print(f"1 {current_item.name.lower()} has been added to your inventory!")

# Save the inventory contents for next program instance
inv.save_inventory()