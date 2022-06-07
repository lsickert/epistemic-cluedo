"""This module contains the core game functionality"""

import cluedo.game.init as init
import cluedo.logic_checker.kripke_model as kripke
import cluedo.game.player as player_class

def start_game(num_players: int = 6, num_characters: int = 6, num_weapons: int = 6, num_rooms: int = 9):

    characters, weapons, rooms = init.create_resource_sets(num_characters, num_weapons, num_rooms)

    goal_deck, clue_deck = init.create_card_deck(characters, weapons, rooms)

    possible_worlds = init.get_card_combinations(characters, weapons, rooms)

    base_model = kripke.create_kripke_model(possible_worlds, num_players)

    players = {}

    hand_cards = _split_hand_cards(num_players, clue_deck)

    for player in range(num_players):
        players[str(player+1)] = player_class.Player((player+1), hand_cards[player], base_model)

    print("done")


def _split_hand_cards(num_players: int, clue_deck: list) -> list:
    c = len(clue_deck) // num_players
    r = len(clue_deck) % num_players
    return [clue_deck[p * c + min(p,r):(p+1) * c + min(p+1,r)] for p in range(num_players)]
