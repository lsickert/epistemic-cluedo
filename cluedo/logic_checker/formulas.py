"""This module contains functions to create the individual formulas used in the game."""

from mlsolver.formula import *


def character_weapon_room_and(character: str, weapon: str, room: str) -> And:
    """Formula to check for (character AND weapon AND room)"""
    return And(Atom(character), And(Atom(weapon), Atom(room)))


def character_weapon_room_or(character: str, weapon: str, room: str) -> Or:
    """Formula to check (character OR weapon OR room)"""
    return Or(Atom(character), Or(Atom(weapon), Atom(room)))


def not_character_weapon_room_and(character: str, weapon: str, room: str) -> Not:
    """Formula to check NOT(character AND weapon AND room)"""
    return Not(And(Atom(character), And(Atom(weapon), Atom(room))))


def has_specific_card(card: str) -> Atom:
    """Formula to check that a player has a specific card"""
    return Atom(card)


def not_has_specific_card(card: str) -> Not:
    """Formula to check that a player does not have a specific card"""
    return Not(Atom(card))


def knows_has_specific_card(card: str) -> Box:
    """Formula to check if a player knows about having a specific cards.
    Only works in single-agent Kripke models, use `agent_knows_has_specific_card()` for multi-Kripke models
    """
    return Box(Atom(card))

def agent_knows_has_specific_card(card: str, agent: str) -> Box_a:
    """Formula to check if a player knows about having a specific cards.
    Only works in multi-agent Kripke models, use `knows_has_specific_card()` for single-Kripke models
    """
    return Box_a(agent, Atom(card))


def knows_not_has_specific_card(card: str) -> Box:
    """Formula to check if a player knows about not having a specific cards
    Only works in single-agent Kripke models, use `agent_knows_not_has_specific_card()` for multi-Kripke models
    """
    return Box(Not(Atom(card)))

def agent_knows_not_has_specific_card(card: str, agent: str) -> Box_a:
    """Formula to check if a player knows about not having a specific cards
    Only works in multi-agent Kripke models, use `knows_not_has_specific_card()` for single-Kripke models
    """
    return Box_a(agent, Not(Atom(card)))

def knows_character_weapon_room_or(character: str, weapon: str, room: str):
    """Formula to check if a player knows about either a character, weapon, or room
        Only works in single-agent Kripke models, use `agent_knows_character_weapon_room_or()` for multi-Kripke models
    """
    return Box(Or(Atom(character), Or(Atom(weapon), Atom(room))))

def agent_knows_character_weapon_room_or(character: str, weapon: str, room: str, agent: str):
    """Formula to check if a player knows about either a character, weapon, or room
        Only works in multi-agent Kripke models, use `knows_character_weapon_room_or()` for single-Kripke models
    """
    return Box_a(agent, Or(Atom(character), Or(Atom(weapon), Atom(room))))

# def not_character_weapon_room_or(character: str, weapon: str, room: str):
#     """Formula to check NOT(character OR weapon OR room)"""
#     return Not(Or(Atom(character),Or(Atom(weapon), Atom(room))))
