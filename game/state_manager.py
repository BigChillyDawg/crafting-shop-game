def update_drops(object):
    """
    Loops through an objects upgrades and unlocks any purchased drops.

    Parameters:
        object (object): A valid object containing drops

    Returns:
        None
    """
    # Loop through each upgrade an object has
    for upgrade in object.upgrades.values():
        # Check if the upgrade is owned and if it contains new drops
        if upgrade["new_drops"] and upgrade["owned"]:
            # Loop through each new drop and set its status to unlocked
            for drop in upgrade["new_drops"]:
                object.drops[drop]["unlocked"] = True