"""This module contains various helper functions that are used throughout the rest of the game modules."""

import random

def throw_single_dice():
    """Returns a random number from 1-6 to simulate a dice throw."""
    return random.randint(1,6)

def throw_double_dice():
    """Adds two random numbers from 1-6 together to simulate a throw with two dices."""
    d1 = throw_single_dice()
    d2 = throw_single_dice()

    return d1 + d2
