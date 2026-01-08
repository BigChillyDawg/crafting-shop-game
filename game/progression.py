from copy import deepcopy
from json import load, dump

# === Helper function to deal with drop changes with upgrades === 
def update_upgrades(object, item_list):
    """
    Loops through an objects upgrades and unlocks any purchased drops, modifies
    drop rates based on owned upgrades, and applies any cooldown changes.

    Parameters:
        object (object): A valid object containing drops
        item_list (dict): A registry mapping item ID's to item objects

    Returns:
        None
    """
    # Reset drops to base state
    object.drops = deepcopy(object.base_drops)

    # Reset cooldown to base cooldown
    object.cooldown.duration = object.base_cooldown_duration

    # Loop through each upgrade an object has
    for upgrade in object.upgrades.values():
        # Check if the upgrade is owned.
        if not upgrade["owned"]:
            continue
        # New Drops 
        if upgrade["new_drops"]:
            # Loop through each new drop and set its status to unlocked
            for drop in upgrade["new_drops"]:
                object.drops[drop]["unlocked"] = True

        # Drop Modifiers
        if upgrade["drop_modifier"]:
            for drop, multiplier in upgrade["drop_modifier"].items():
                # Multiply each drop by the required modifier
                if drop in object.drops and "weight" in object.drops[drop]:
                    object.drops[drop]["weight"] = object.drops[drop]["weight"] * multiplier

        # Rarity Modifiers
        if upgrade["rarity_modifier"]:
            # Loop through each rarity and corresponding multiplier
            for rarity, multiplier in upgrade["rarity_modifier"].items():
                # Loop through each drop the mineshaft has
                for id, drop in object.drops.items():
                    # Check if the drop matches the corresponding rarity
                    # Apply multiplier if so
                    if item_list[id].rarity.label.lower() == rarity:   
                        drop['weight'] = drop['weight'] * multiplier

        # Cooldown Modifier
        if upgrade["cooldown_modifier"] != "none":
            # Update cooldown duration based on modifier
            object.cooldown.duration = (object.cooldown.duration * 
                                       (1 - upgrade["cooldown_modifier"]))

def buy_upgrade(object, upgrade_id, upgrades_save, item_list):
    """ 
    Applies an upgrade and deducts funds or items required to purchase it from
    a user's inventory.
    
    Parameters:
        object (object): A valid object to apply the upgrade to.
        upgrade_id (str): The ID of a corresponding upgrade
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

    # Handle any drop changes due to the upgrade
    update_upgrades(object, item_list)

def load_upgrades(registry, upgrades_data, upgrades_save, item_list):
    """
    Applies upgrade ownership states to each object in a given registry 
    from a JSON file. Determines if an upgrade is owned or still locked 
    using save data and applies a boolean value accordingly. Main use  
    is to load upgrades on initial launch.

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
        update_upgrades(object, item_list)