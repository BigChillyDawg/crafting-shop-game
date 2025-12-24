# main.py

import item
from inventory import Inventory

# Parse the list of items from the json data
item_list = item.load_items("items.json")

# Initialize an inventory object for the user
inv = Inventory()
# Load in the user's inventory from their previous sessions
inv.load_inventory(item_list)

while True:
    # Display menu to the user and recieve an input
    print("-" * 100)
    print("Please enter an item to add to your inventory!")
    print("Enter display to show your inventory")
    user_input = input(">> ")

    # If user enters 0, exit the program
    if user_input == "0":
        break

    # Display the user's inventory if they enter display
    if user_input.lower() == "display":
        # If user's inventory is empty, let them know
        if not inv.inventory_contents():
            print("Inventory is empty!")
            continue

        # Print the name of each item object in the user's inventory and
        # display quantities
        for key, value in inv.inventory_contents().items():
            print(f"{key.name}: {value}")
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