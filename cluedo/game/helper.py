"""This module contains various helper functions that are used throughout the rest of the game modules."""

import random
import json

_game_resources = None


def throw_single_dice():
    """Returns a random number from 1-6 to simulate a dice throw."""
    return random.randint(1, 6)


def throw_double_dice():
    """Adds two random numbers from 1-6 together to simulate a throw with two dices."""
    d1 = throw_single_dice()
    d2 = throw_single_dice()

    return d1 + d2


def _load_resources() -> None:
    """loads the game resource specifications"""
    global _game_resources
    with open("../resources/resources.json", encoding="utf8") as f:
        _game_resources = json.loads(f)


def get_resources() -> dict:
    """returns the full game resource specifications"""

    if _game_resources is None:
        _load_resources()

    return _game_resources


def get_characters() -> list:
    """returns the character specifications"""

    if _game_resources is None:
        _load_resources()

    return _game_resources["characters"]


def get_weapons() -> list:
    "returns the weapon specifications"
    if _game_resources is None:
        _load_resources()

    return _game_resources["weapons"]


def get_rooms() -> list:
    """returns the room specifications"""
    if _game_resources is None:
        _load_resources()

    return _game_resources["rooms"]
