# Arcane Workshop

Learning how to work with data and classes while making a game!

---

## Core Gameplay Loop

1. Gather resources through mining
2. Craft items using probabilistic recipes
3. Crafting can succeed or fail (failure consumes ingredients)
4. Items have rarity tiers that affect presentation and progression
5. Unlock upgrades to expand available drops
6. Persist progress across sessions via save files

Risk and randomness are intentional and central to gameplay.

---

## Implemented Systems

Inventory
- Inventory class that can be used for multiple purposes
- Prevents invalid operations (negative quantities, missing items)
- add_item and remove_item functions
- JSON-based save/load support

Items and rarity
- Items objects that are loaded in using JSON data
- Really easy to create any item you'd like!
- Properties include:
  - ID
  - name
  - category
  - rarity
  - stackable flag
  - traits
- Rarity is implemented using Enum:
  - numeric tiering
  - color metadata for UI display

Crafting System
- Recipes defined in JSON
- Each recipe includes:
  - required ingredients
  - success chance
  - output quantity
- Crafting:
  - consumes ingredients
  - rolls against probability
- Only craftable recipes are shown to the player

Mining System:
- Multiple mineshafts defined via JSON
- Each mineshaft has:
  - weighted drop tables
  - unlockable drops
  - upgrade paths
- Mining uses cumulative-weight random rolls
- Drops are dynamically updated based on owned upgrades

Upgrade System:
- Upgrade system tied to specific mineshafts
- Upgrades:
  - unlock new drops
  - have prerequisite requirements
  - cost inventory items
- Upgrade ownership persists across sessions
- Applying upgrades dynamically modifies gameplay state

Menus and UI:
- Modular menu system (crafting, mining, upgrades)
- ANSI-colored terminal UI
- Only valid options are presented to the user
- Clear separation between UI logic and game systems

Save Data Handling:
- Inventory saved to JSON on exit
- Upgrade ownership saved independently
- Game state reconstructed on launch

---

Project is being designed to be easily portable and to
have structure that can be used across several games.

---
