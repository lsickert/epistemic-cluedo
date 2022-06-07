"""epistemic-cluedo main module"""
import cluedo.game.core as game

if __name__ == "__main__":

    game.start_game(num_players=3, num_characters=5, num_weapons=5, num_rooms=5)
