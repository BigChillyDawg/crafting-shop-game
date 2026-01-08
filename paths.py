from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Main paths
DATA = ROOT / "data"
SAVE = ROOT / "save_data"

# Ensure save_data directory exists
SAVE.mkdir(parents=True, exist_ok=True)

# Cooldown directory
COOLDOWN_SAVE = SAVE / "cooldown_save"
COOLDOWN_SAVE.mkdir(parents=True, exist_ok=True)

# Save data
INVENTORY_SAVE = SAVE / "inventory.json"
UPGRADES_SAVE = SAVE / "owned_upgrades.json"
BALANCE_SAVE = SAVE / "balance.json"
MINESHAFT_COOLDOWNS = COOLDOWN_SAVE / "saved_cooldowns.json"

# Game data
ITEM_FILE = DATA / "items.json"
MINESHAFTS_FILE = DATA / "mineshafts.json"
RECIPES_FILE = DATA / "recipes.json"
UPGRADES_FILE = DATA / "upgrades.json"