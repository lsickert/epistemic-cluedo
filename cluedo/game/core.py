"""This module contains the core game functionality"""

import cluedo.game.init as init
import cluedo.logic_checker.kripke_model as kripke
import cluedo.logic_checker.formulas as formulas
import cluedo.game.player as player_class
import random


def start_game(num_players: int = 6, controllable_players=1, num_characters: int = 6, num_weapons: int = 6, num_rooms: int = 9):
    print()
    characters, weapons, rooms = init.create_resource_sets(
        num_characters, num_weapons, num_rooms)

    goal_deck, clue_deck = init.create_card_deck(characters, weapons, rooms)

    possible_worlds = init.get_card_combinations(characters, weapons, rooms)

    base_model = kripke.create_multi_kripke_model(possible_worlds, num_players)

    players = {}

    hand_cards = _split_hand_cards(num_players, clue_deck)

    list_of_colors = ["scarlett", "green", "mustard", "plum", "peacock", "white"]

    # initialize players
    for player in range(num_players):
        color = random.choice(list_of_colors)   # Assign a color to each player, important for game rules and starting positions
        list_of_colors.remove(color)            # Remove color from list, such that each player has an unique color.
        players[str(player+1)] = player_class.Player((player+1), hand_cards[player],
                                                     base_model, characters, weapons, rooms, 2, color, player < controllable_players,)

    # build the hand card models of the other players for each player
    for player in players.values():
        print(f"initializing player {player.player_id}")

        player.build_own_hand_cards_model(num_players)

        num_hand_cards = len(player.hand_cards)

        remaining_clues = clue_deck.copy() + list(goal_deck)

        for card in player.hand_cards:
            remaining_clues.remove(card)

        for other_player in players.values():
            if not other_player.player_id == player.player_id:
                player.build_hand_cards_model(
                    other_player.player_id, num_hand_cards, remaining_clues)

    print("starting game")

    winner_found = False
    game_turn = 1
    while not winner_found:
        winner_found, winner, winner_suggestion = game_round(players)
        game_turn += 1

    return winner, winner_suggestion, goal_deck, game_turn


def game_round(player_list):

    for player in player_list.values():
        # Find suggestion and let agent move
        suggestion = _player_move(player)

        # Bring accused player to the accuser's location
        for character in player_list.values():
            if character.color == suggestion[0]:
                move = character.move(suggestion)
                print(f"player {character.player_id} is moved to:")
                print(move)

        # Check if next player has the cards
        winner_found, winner, winner_suggestion = _check_next_players(
            player_list, suggestion)

        if winner_found:
            return True, winner, winner_suggestion

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

                    if other_player.player_id is not player.player_id:
                        other_player.update_goal_model(formulas.not_character_weapon_room_and(
                            suggestion[0], suggestion[1], suggestion[2]))

                        if other_player.player_id is not opponent:
                            other_player.update_hand_cards_model(str(opponent), formulas.character_weapon_room_or(
                                suggestion[0], suggestion[1], suggestion[2]))
                break
            else:
                # every player knows that this player does not have any of the three cards in his hand
                for inner_player in player_list.values():

                    if inner_player.player_id is not opponent:
                        inner_player.update_hand_cards_model(str(opponent), formulas.not_character_weapon_room_and(
                            suggestion[0], suggestion[1], suggestion[2]))

            i += 1
        else:
            # none of the other players has any of the cards of the suggestion, so we can safely assume that this sugggestion is correct
            return True, player, suggestion

        # check if we can exclude any additional cards from the goal model since it is known by deduction that another player has them on their hand
        player.check_other_hand_cards()

        accusation = player.check_winning_possibility()

        if len(accusation) > 0:
            return True, player, accusation

    return False, None, None


def _check_next_players(suggestion, player_list, player):
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
            return opponent.player_id, matching_card[0]


def _player_move(player):
        suggestion = player.make_suggestion()
        move = player.move(suggestion)
        print(f"player {player.player_id} moves to: {move}")

        if player.location == 'pathways':   # Players can not make a suggestion in the pathways between rooms.
            print(f"player {player.player_id} can not make a suggestion in the pathways between rooms.")
            return None

        print(f"player {player.player_id} suggests: {suggestion}")

        if move != suggestion[2]:               # If this ever comes up, then there is something that needs to be changed to the 
            print("illegal suggestion!!!")      # move or suggestion function, it has not happened yet, but until we hand this in
            exit(0)                             # this will tell us that this implementation works.



def _split_hand_cards(num_players: int, clue_deck: list) -> list:
    c = len(clue_deck) // num_players
    r = len(clue_deck) % num_players
    return [clue_deck[p * c + min(p, r):(p+1) * c + min(p+1, r)] for p in range(num_players)]
