"""
    player.py
    ---------

    This module contains the Player class that represents game characters.
"""

__author__ = "Reindert-Jan Ekker"


class Player:
    """
    The Player class represents the characters in the game.
    """

    def __init__(self, name, weapon):
        self.name = name
        self.weapon = weapon
        self.health = 100

    def take_hit(self, damage):
        self.health -= damage
        return self.health

    @property
    def is_alive(self):
        """True if :attr:`health` is larger than 0, False otherwise"""
        return self.health > 0

    def __str__(self):
        return "Player {} has {} health and brings his {} to the fight".format(
            self.name, self.health, type(self.weapon).__name__
        )
