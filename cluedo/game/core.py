"""This module contains the core game functionality"""

import cluedo.game.init as init
import cluedo.logic_checker.kripke_model as kripke


def start_game(num_players: int = 6):

    characters, weapons, rooms = init.create_resource_sets()

    goal_deck, clue_deck = init.create_card_deck(characters, weapons, rooms)

    possible_worlds = init.get_card_combinations(characters, weapons, rooms)

    model = kripke.create_kripke_model(possible_worlds, num_players)

