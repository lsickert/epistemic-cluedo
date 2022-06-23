"""This module contains functions to create the individual formulas used in the game."""

from lib2to3.pgen2.token import AT
from mlsolver.formula import *


def character_weapon_room_and(character: str, weapon: str, room: str):
    """Formula to check for (character AND weapon AND room)"""
    return And(Atom(character), And(Atom(weapon), Atom(room)))


def character_weapon_room_or(character: str, weapon: str, room: str):
    """Formula to check (character OR weapon OR room)"""
    return Or(Atom(character), Or(Atom(weapon), Atom(room)))


def not_character_weapon_room_and(character: str, weapon: str, room: str):
    """Formula to check NOT(character AND weapon AND room)"""
    return Not(And(Atom(character), And(Atom(weapon), Atom(room))))


def has_specific_card(card: str):
    """Formula to check that a player has a specific card"""
    return Atom(card)


def not_has_specific_card(card: str):
    """Formula to check that a player does not have a specific card"""
    return Not(Atom(card))

def knows_has_specific_card(card: str):
    """Formula to check if a player knows about having a specific cards"""
    return Box(Atom(card))

def knows_not_has_specific_card(card: str):
    """Formula to check if a player knows about having a specific cards"""
    return Box(Not(Atom(card)))

# def not_character_weapon_room_or(character: str, weapon: str, room: str):
#     """Formula to check NOT(character OR weapon OR room)"""
#     return Not(Or(Atom(character),Or(Atom(weapon), Atom(room))))
