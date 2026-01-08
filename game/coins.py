# coins.py

class Wallet():
    """
    A simple wallet system to track a player's coin balance.
    """
    def __init__(self, balance=0):
        self.balance = balance

    def add_coins(self, amount):
        """ 
        Adds a specified amount of coins to the wallet.

        Parameters:
            amount (int): The amount of coins to add.

        Returns:
            None 
        """
        self.balance += amount

    def spend_coins(self, amount):
        """ 
        Spends a specified amount of coins from the wallet.
        Parameters:
            amount (int): The amount of coins to spend.

        Returns:
            bool: True if the coins were spent successfully, False otherwise.
        """
        if amount > self.balance:
            return False
        self.balance -= amount
        return True
    
    def set_coins(self, amount):
        """ 
        Sets the balance to a specified value.
        Parameters:
            amount (int): The amount of coins to set the balance to.

        Returns:
            None
        """

        self.balance = amount
        return