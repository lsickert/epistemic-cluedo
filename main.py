"""epistemic-cluedo main module"""
import cluedo.game.core as game

if __name__ == "__main__":
    num_players = int(input("How many players? (default 3) "))
    controllable_players = int(input("How many controllable players? (default 1) "))
    num_characters = int(input("How many characters? (default 5) "))
    num_weapons = int(input("How many weapons? (default 5) "))
    num_rooms = int(input("How many rooms? (default 5) "))

    game.start_game(num_players, controllable_players, num_characters, num_weapons, num_rooms)
