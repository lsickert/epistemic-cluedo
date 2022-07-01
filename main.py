"""epistemic-cluedo main module"""
from matplotlib.style import available
import cluedo.game.core as game
import cluedo.game.helper as helper
import random

import sys
from os import sep as s


def user_input():
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
    

    return num_players, controllable_players, num_characters, num_weapons, num_rooms



if __name__ == "__main__":
    if False:
        num_players, controllable_players, num_characters, num_weapons, num_rooms = user_input()
    else:
        # num_players = len(sys.argv) - 1
        players = [int(i) for i in sys.argv[1:]]
        controllable_players = 0
        if len(players) == 4:
            num_characters = 6
            num_weapons = 6
            num_rooms = 7
        elif len(players) == 6:
            num_characters = 6
            num_weapons = 7
            num_rooms = 8
        elif len(players) == 3:
            num_characters = 4
            num_weapons = 4
            num_rooms = 4
        else: exit(0)

    results = {}
    position_results = {}
    filename = ""
    for idx, player in enumerate(players):
        results[player] = 0
        position_results[idx + 1] = 0
        filename += str(player)

    with open(f"results{s}{filename}{s}run.txt", "w") as f:
        for idx in range(25):
            winner, available_worlds = game.start_game(players, controllable_players, num_characters, num_weapons, num_rooms)
            f.write(f"Player {winner.player_id} of order {winner.higher_order} wins\n")
            results[winner.higher_order] += 1
            position_results[winner.player_id] += 1

            for player, worlds in available_worlds.items():
                with open(f"results{s}{filename}{s}{player}.txt", "a") as f2:
                    for turn in worlds:
                        f2.write(f"{turn} ")
                    f2.write("\n")
        
        f.write(f"\n\nResults:\n")
        f.write(f"{results}\n")
        f.write(f"Position results:\n")
        f.write(f"{position_results}\n")





"""
4 players: 6 chars 6 weapons 7 rooms ->  19 total, 3 goal, 16 cards: 4 cards each
6 players: 6 chars 7 weapons 8 rooms ->  21 total, 3 goal, 18 cards: 3 cards each
6 players 
2 2 0 0     - 
2 2 1 1     - 
0 0 1 1     - 
2 2 1 1 0 0 - 3 min
"""
