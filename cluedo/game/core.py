"""This module contains the core game functionality"""

import cluedo.game.init as init
import cluedo.logic_checker.kripke_model as kripke
import cluedo.game.player as player_class
from tqdm import tqdm

def start_game(num_players: int = 6, num_characters: int = 6, num_weapons: int = 6, num_rooms: int = 9):
    pbar = tqdm(desc= "Starting game setup", total=(num_players*2 + num_players*num_players + 5))

    pbar.set_description("Create resources")
    pbar.update(1)
    characters, weapons, rooms = init.create_resource_sets(
        num_characters, num_weapons, num_rooms)

    pbar.set_description("Create card deck")
    pbar.update(1)
    goal_deck, clue_deck = init.create_card_deck(characters, weapons, rooms)

    pbar.set_description("Calculate possible card combinations")
    pbar.update(1)
    possible_worlds = init.get_card_combinations(characters, weapons, rooms)

    pbar.set_description("Create baseline Kripke model")
    pbar.update(1)
    base_model = kripke.create_multi_kripke_model(possible_worlds, num_players)

    players = {}

    pbar.set_description("Split hand cards between players")
    pbar.update(1)
    hand_cards = _split_hand_cards(num_players, clue_deck)

    # initialize players
    for player in range(num_players):
        pbar.set_description(f"Create player {str(player+1)}")
        pbar.update(1)
        players[str(player+1)] = player_class.Player((player+1), hand_cards[player], base_model, characters, weapons, rooms)

    # build the hand card models of the other players for each player
    for player in players.values():
        pbar.set_description(f"Create hand card knowledge for player {str(player.player_id)}")
        pbar.update(1)
        num_hand_cards = len(player.hand_cards)

        remaining_clues = clue_deck.copy()

        for card in player.hand_cards:
            remaining_clues.remove(card)

        for other_player in players.values():
            pbar.set_description(f"Create hand card knowledge for player {str(player.player_id)} about player {str(other_player.player_id)}")
            pbar.update(1)
            if not other_player.player_id == player.player_id:
                other_player.build_hand_cards_model(player.player_id, num_hand_cards, remaining_clues)

    pbar.close()

    print("setup for game is done")
    game_round(players)


def game_round(player_list):

    for player in player_list:
        suggestion = player_list[str(player)].make_suggestion()
        print("player " + player + " suggests:")
        print(suggestion)

        i = 1
        # This loop and if statement make it such that the next opponent is checked for cards,
        while i < len(player_list):
            # rather than 3 checking -> [1-2-4-5-6], we have 3 checking -> [4-5-6-1-2].
            opponent = int(player) + i
            if opponent > len(player_list):
                opponent = opponent - len(player_list)

            print("matching hand cards player " + str(opponent))
            print(player_list[str(opponent)].check_hand_cards(suggestion))

            i += 1


def _split_hand_cards(num_players: int, clue_deck: list) -> list:

    c = len(clue_deck) // num_players
    r = len(clue_deck) % num_players
    return [clue_deck[p * c + min(p, r):(p+1) * c + min(p+1, r)] for p in range(num_players)]
