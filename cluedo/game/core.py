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
        
    print("setup for game is done")
    game_run(players)


def _split_hand_cards(num_players: int, clue_deck: list) -> list:

    c = len(clue_deck) // num_players
    r = len(clue_deck) % num_players
    return [clue_deck[p * c + min(p,r):(p+1) * c + min(p+1,r)] for p in range(num_players)]

def game_run(player_list):

    for player in player_list:
        suggestion = player_list[str(player)].make_suggestion()
        print("player " + player + " suggests:")
        print(suggestion)

        i = 1
        while i < len(player_list): # This loop and if statement make it such that the next opponent is checked for cards,
            opponent = int(player) + i   # rather than 3 checking -> [1-2-4-5-6], we have 3 checking -> [4-5-6-1-2].
            if opponent > len(player_list):
                opponent = opponent - len(player_list)

            print("hand cards " + str(opponent))
            print(player_list[str(opponent)].hand_cards)
            
            i += 1
