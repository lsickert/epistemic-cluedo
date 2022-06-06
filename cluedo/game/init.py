"""this module contains functions needed to initialize a game run"""
from typing import Tuple

import random
import cluedo.game.helper as helper
import copy
import itertools


def create_resource_sets(num_characters: int = 6, num_weapons: int = 6, num_rooms: int = 9) -> tuple:
    """creates the set of characters, weapons and rooms that will be used in a game"""
    characters = _get_id_list(helper.get_characters())
    weapons = _get_id_list(helper.get_weapons())
    rooms = _get_id_list(helper.get_rooms())

    random.shuffle(characters)
    random.shuffle(weapons)
    random.shuffle(rooms)

    del characters[num_characters:]
    del weapons[num_weapons:]
    del rooms[num_rooms:]

    return characters, weapons, rooms


def create_card_deck(character_list: list, weapon_list: list, room_list: list) -> Tuple[tuple, list]:
    """
    create the deck of playing cards.

    Returns:
    goal_deck: a tuple of one character, weapon and room to be used as the set to find in the game
    clue_deck: a list with all remaining cards in random order
    """
    characters = copy.deepcopy(character_list)
    weapons = copy.deepcopy(weapon_list)
    rooms = copy.deepcopy(room_list)

    goal_deck = characters.pop(), weapons.pop(), rooms.pop()
    clue_deck = characters + weapons + rooms

    random.shuffle(clue_deck)

    return goal_deck, clue_deck


def get_card_combinations(characters: list, weapons: list, rooms: list) -> list:
    """return the number of card combinations that are possible in a game"""

    comb_list = itertools.product(characters, weapons, rooms)
    return list(comb_list)


def _get_id_list(l: list) -> list:
    """return a list with only the id values of a specification resource"""
    id_list = []
    for e in l:
        id_list.append(e["id"])

    return id_list
