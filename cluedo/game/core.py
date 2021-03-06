"""This module contains the core game functionality"""

import cluedo.game.init as init
import cluedo.logic_checker.kripke_model as kripke
import cluedo.logic_checker.formulas as formulas
import cluedo.game.player as player_class
from tqdm import tqdm
import random

def start_game(player_orders, controllable_players=1, num_characters: int = 6, num_weapons: int = 6, num_rooms: int = 9):

    num_players = len(player_orders)
    pbar = tqdm(desc="Starting game setup", total=(
        num_players*2 + num_players*num_players + 5))

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

    list_of_colors = ["scarlett", "green", "mustard", "plum", "peacock", "white"]

    # initialize players
    for player, order in enumerate(player_orders):
        pbar.set_description(f"Create player {str(player+1)}")
        pbar.update(1)
        color = random.choice(list_of_colors)   # Assign a color to each player, important for game rules and starting positions
        list_of_colors.remove(color)            # Remove color from list, such that each player has an unique color.
        players[str(player+1)] = player_class.Player((player+1), hand_cards[player],
                                                     base_model, characters, weapons, rooms, order, color, player < controllable_players)

    # build the hand card models of the other players for each player
    for player in players.values():
        pbar.set_description(
            f"Create hand card knowledge for player {str(player.player_id)}")
        pbar.update(1)

        player.build_own_hand_cards_model(num_players)

        num_hand_cards = len(player.hand_cards)

        remaining_clues = clue_deck.copy() + list(goal_deck)

        for card in player.hand_cards:
            remaining_clues.remove(card)

        for other_player in players.values():
            pbar.set_description(
                f"Create hand card knowledge for player {str(player.player_id)} about player {str(other_player.player_id)}")
            pbar.update(1)
            if not other_player.player_id == player.player_id:
                player.build_hand_cards_model(
                    other_player.player_id, num_hand_cards, remaining_clues)

    pbar.close()

    print("starting game")

    available_worlds = {}
    for player in players.values():
        if player.higher_order not in available_worlds:
            available_worlds[player.higher_order] = []
        available_worlds[player.higher_order] += [player.get_nr_available_worlds()]


    winner = None
    game_turn = 1
    while winner is None:
        print(f"Turn = {game_turn}")
        winner = game_round(players)
        game_turn += 1
        for player in players.values():
            available_worlds[player.higher_order] += [player.get_nr_available_worlds()]
    
    print(f"Winner is player {winner.player_id} of order {winner.higher_order} in turn {game_turn}")
    print(f"The winning suggestion was {winner.latest_suggestion} with goal deck {goal_deck}")

    return winner, available_worlds


def game_round(player_list) -> player_class.Player:
    for player in player_list.values():

        suggestion = player.make_suggestion()
        move = player.move(suggestion)
        print(f"player {player.player_id} moves to: {move}")

        if player.location == 'pathways':   # Players can not make a suggestion in the pathways between rooms.
            print(f"player {player.player_id} can not make a suggestion in the pathways between rooms.")
            continue

        print(f"player {player.player_id} suggests: {suggestion}")

        if move != suggestion[2]:               # If this ever comes up, then there is something that needs to be changed to the 
            print("illegal suggestion!!!")      # move or suggestion function, it has not happened yet, but until we hand this in
            return 0                            # this will tell us that this implementation works.

        for character in player_list.values():
            if character.color == suggestion[0]:
                move = character.move(suggestion)
                print(f"player {character.player_id} is moved to:")
                print(move)

        i = 1
        # This loop and if statement make it such that the next opponent is checked for cards,
        while i < len(player_list):
            # rather than 3 checking -> [1-2-4-5-6], we have 3 checking -> [4-5-6-1-2].
            opponent = int(player.player_id) + i
            if opponent > len(player_list):
                opponent = opponent - len(player_list)

            matching_card = player_list[str(
                opponent)].check_own_hand_cards(suggestion, str(player.player_id))
            print(
                f"matching hand cards player  {str(opponent)}: {matching_card}")

            # stop the round if a matching card is found
            if len(matching_card) > 0:
                # the suggesting player knows the specific card his opponent has
                player.update_goal_model(
                    formulas.not_has_specific_card(matching_card))

                player.update_hand_cards_model(
                    str(opponent), formulas.has_specific_card(matching_card))

                # every other player knows that the opponent has at least one of the three cards in his hand
                for other_player in player_list.values():

                    if other_player.player_id is not player.player_id and other_player.higher_order >= 1:
                        other_player.update_goal_model(formulas.not_character_weapon_room_and(
                            suggestion[0], suggestion[1], suggestion[2]))

                        if other_player.player_id is not opponent and other_player.higher_order >= 1:
                            other_player.update_hand_cards_model(str(opponent), formulas.character_weapon_room_or(
                                suggestion[0], suggestion[1], suggestion[2]))
                break
            else:
                # every player knows that this player does not have any of the three cards in his hand
                for inner_player in player_list.values():

                    if inner_player.player_id is not opponent and inner_player.higher_order >= 1:
                        inner_player.update_hand_cards_model(str(opponent), formulas.not_character_weapon_room_and(
                            suggestion[0], suggestion[1], suggestion[2]))

            i += 1
        else:
            # none of the other players has any of the cards of the suggestion, so we can safely assume that this sugggestion is correct
            return player

        # check if we can exclude any additional cards from the goal model since it is known by deduction that another player has them on their hand
        player.check_other_hand_cards()

        accusation = player.check_winning_possibility()

        if len(accusation) > 0:
            return player

    return None


def _split_hand_cards(num_players: int, clue_deck: list) -> list:
    c = len(clue_deck) // num_players
    r = len(clue_deck) % num_players
    return [clue_deck[p * c + min(p, r):(p+1) * c + min(p+1, r)] for p in range(num_players)]
