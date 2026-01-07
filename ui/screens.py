# screens.py

from ui.colors import UI_COLORS as uic
from game.rarity import Rarity
import time
import msvcrt
import os
import shutil

def clear_screen():
    """ Clears the terminal screen """
    os.system('cls' if os.name == 'nt' else 'clear')

def check_terminal_size(rows):
    """ Ensures the terminal meets a given amount of rows """
    while shutil.get_terminal_size().lines < rows:
        clear_screen()
        print("Your terminal is currently too small for gameplay!")
        print("Please increase the amount of rows, press a key when ready.")
        msvcrt.getch()
        clear_screen()
        if shutil.get_terminal_size().lines < rows:
            print("Terminal is still too small, try again please!", flush=True)
            time.sleep(1)
            clear_screen()


def welcome_screen():
    """
    Displays an animated welcome screen to the user.
    """
    clear_screen()
    
    welcome = "Welcome to "

    # Print characters 1 at a time
    for char in welcome:
        print(char, end="", flush=True)
        time.sleep(0.05)
    
    title1 = "ARCANE"
    title2 = "WORKSHOP!"

    # Repeat the process for both titles with a space in between
    for char in title1:
        print(f"{uic['bold']}{uic['arcane_purple']}{char}{uic['reset']}", end="", flush=True)
        time.sleep(0.05)

    print(" ", end="")

    for char in title2:
        print(f"{uic['bold']}{uic['warm_brown']}{char}{uic['reset']}", end="", flush=True)
        time.sleep(0.05)
    print()
    time.sleep(0.75)

    # Wait for an input from the user before moving on
    input_message = "Press any key to continue..."
    for char in input_message:
        print(f"{uic['italic']}{uic['grey']}{char}{uic['reset']}", end="", flush=True)
        time.sleep(0.05)
    print()
    msvcrt.getch()

def display_inventory(inventory):
    """Prints color coded inventory contents to the terminal. """
    
    # Print inventory title
    print(f"{uic['orange']}===== INVENTORY ====={uic['reset']}")

    if not inventory.items:
        print("(Empty)")

    # Loop through inventory to display items from common to legendary
    for r in Rarity:
        for key, value in inventory.items.items():
            if key.rarity == r:
                # Print each item and quanitity formatted with color
                print(f"{key.rarity.color}{key.name}{uic['reset']} {value}x")

    return

def travelling_screen(location, color):
    """
    Displays an animated screen to a location with a specified color

    Parameters:
        location (str): The name of the location being travelled to
        color (str): Color code for the name of the location

    Returns:
        None
    """
    clear_screen()
    travelling = "Travelling to "

    for char in travelling:
        print(char, end="", flush=True)
        time.sleep(0.07)
    
    for char in location:
        print(f"{uic['bold']}{color}{char}{uic['reset']}", end="", flush=True)
        time.sleep(0.07)

    for char in '...':
        print(char, end="", flush=True)
        time.sleep(0.2)
    clear_screen()

def invalid_input_screen():
    """ Displays an invalid input screen. """

    clear_screen()
    invalid = "Invalid input!"
    
    for char in invalid:
        print(f"{uic['bold']}{uic['grey']}{char}{uic['reset']}", end="", flush=True)
        time.sleep(0.07)
    
    time.sleep(0.2)
    clear_screen()
