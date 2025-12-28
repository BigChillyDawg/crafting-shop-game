from json import load, dump

def buy_upgrade(object, upgrade_id, inventory, item_list, upgrades_save):
    """ 
    Applies an upgrade and deducts funds or items required to purchase it from
    a user's inventory.
    
    Parameters:
        object (object): A valid object to apply the upgrade to.
        upgrade (str): The ID of a corresponding upgrade
        inventory (object): An Inventory() object to deduct items from
        item_list (dict): A registry mapping item ID's to objects
        upgrades_save (object): A valid Path() object to a JSON file containing
                                save info of upgrades a player has unlocked.
    
    Returns:
        None
    """
    # Apply the upgrade to the object.
    object.upgrades[upgrade_id]["owned"] = True

    # Read the current save information on upgrades if it exists
    owned_upgrades = {"owned": []}
    if upgrades_save.exists():
        with upgrades_save.open("r") as f:
            owned_upgrades["owned"] = load(f)["owned"]

    # Add the upgrade to the owned list
    owned_upgrades["owned"].append(upgrade_id)

    # Save the upgrades data once more
    with upgrades_save.open("w") as f:
        dump(owned_upgrades, f)

    # Deduct the cost from the user's inventory
    for item, amount in object.upgrades[upgrade_id]["cost"].items():
        inventory.remove_item(item_list[item], amount)


def apply_upgrades(registry, upgrades_data, upgrades_save):
    """
    Applies upgrades to each item in a registry corresponding to an upgrades
    file. Determines if an upgrade is owned or still locked, and applies a
    boolean value accordingly. Can be used to update existing upgrades
    when an upgrade is purchased, or to load in upgrades on initial launch.

    Parameters:
        registry(dict): A valid registry mapping ID's to objects
        upgrades_data (object): A valid Path() object to a JSON file containing
                                upgrade information.
        upgrades_save (object): A valid Path() object to a JSON file containing
                                save info of upgrades a player has unlocked.

    Returns:
        None
    """
    # Parse upgrades content into a dictionary
    with upgrades_data.open("r") as f:
        upgrades_json = load(f)

    # Loops items in a registry and applies corresponding upgrades.
    # Adds a boolean value based on if an upgrade is owned or not.
    for id, object in registry.items():
        # Check if the current mineshaft has any upgrades
        if id in upgrades_json:
            # Check if the user has purchased any upgrades yet
            # Store their data in owned_upgrades if so
            if upgrades_save.exists():
                with upgrades_save.open("r") as f:
                    owned_upgrades = load(f)["owned"]
            # If not, set their owned upgrades to empty
            else:
                owned_upgrades = []

            # Look through each upgrade, check if the user owns it or not.
            # Save the condition as a boolean in each upgrade's dictionary.
            for upgrade in upgrades_json[id]:
                if upgrade in owned_upgrades:
                    upgrades_json[id][upgrade]["owned"] = True
                else:
                    upgrades_json[id][upgrade]["owned"] = False
            # Save the final list of upgrades
            upgrades = upgrades_json[id]

        # If there's no upgrades, set the dictionary to empty
        else:
            upgrades = {}

        # Update the object's upgrades.
        object.upgrades = upgrades