"""epistemic-cluedo main module"""
import cluedo.game.core as game
import cluedo.game.helper as helper

import sys

def run_single_game(num_players, controllable_players, num_characters, num_weapons, num_rooms):
    winner, winner_suggestion, goal_deck, game_turn = game.start_game(num_players, controllable_players, num_characters, num_weapons, num_rooms)
    if winner_found:
        print(f"Player {winner.id} won in {game_turn} turns")
        print(f"Suggestion: {winner_suggestion}")
        print(f"Goal deck: {goal_deck}")
        return winner
    else:
        print("No winner found")

if __name__ == "__main__":
    if len(sys.argv) != 1:
        max_players = len(helper.get_characters())
        max_weapons = len(helper.get_weapons())
        max_rooms = len(helper.get_rooms())

        num_players = int(
            input(f"How many players? (default 3, max {max_players}) "))

        while num_players > max_players:
            num_players = int(
                input(f"Please choose at most {max_players} players! "))

        controllable_players = int(
            input("How many controllable players? (default 1, 0 for automatic game) "))

        while controllable_players > num_players:
            controllable_players = int(input(
                f"You cannot choose more controllable players than the maximal number of players. Please choose a number below {num_players}! "))

        num_characters = int(
            input(f"How many characters? (default 5, max {max_players}) "))

        while num_characters > max_players:
            num_characters = int(
                input(f"Please choose at most {max_players} characters! "))

        num_weapons = int(
            input(f"How many weapons? (default 5, max {max_weapons}) "))

        while num_weapons > max_weapons:
            num_weapons = int(
                input(f"Please choose at most {max_weapons} weapons! "))

        num_rooms = int(input(f"How many rooms? (default 5, max {max_rooms}) "))

        while num_rooms > max_rooms:
            num_rooms = int(input(f"Please choose at most {max_rooms} rooms! "))
           
        nr_of_games = 1

    else:
        num_players = 4
        controllable_players = 0
        num_characters = 7
        num_weapons = 7
        num_rooms = 7
        nr_of_games = 10

    for _ in range(nr_of_games):
        winner, winner_suggestion, goal_deck, game_turn = game.start_game(num_players, controllable_players,
                                                                          num_characters, num_weapons, num_rooms)
