"""This module contains the core game functionality"""

import cluedo.game.init as init
import cluedo.logic_checker.kripke_model as kripke
from mlsolver.formula import *

def start_game(num_players: int = 6):

    characters, weapons, rooms = init.create_resource_sets()

    goal_deck, clue_deck = init.create_card_deck(characters, weapons, rooms)

    possible_worlds = init.get_card_combinations(characters, weapons, rooms)

    base_model = kripke.create_kripke_model(possible_worlds, num_players)

    # just for testing, this should return a model where only the goal world is present
    formula = And(Atom(goal_deck[0]),And(Atom(goal_deck[1]), Atom(goal_deck[2])))

    new_model = kripke.update_kripke_model(base_model,formula)

    print("done")

