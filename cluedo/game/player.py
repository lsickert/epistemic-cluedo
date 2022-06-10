"""contains the player class"""
import copy
import cluedo.logic_checker.formulas as formulas
import cluedo.logic_checker.kripke_model as kripke
import random
import itertools


class Player:
    """all functions and properties of an individual player"""

    def __init__(self, player_id: int, hand_cards: list, base_model, all_characters: list, all_weapons: list, all_rooms: list) -> None:
        self.player_id = player_id
        self.hand_cards = hand_cards
        self.goal_model = copy.deepcopy(base_model)
        self.all_characters = all_characters
        self.all_weapons = all_weapons
        self.all_rooms = all_rooms
        self.hand_card_models = {}

        self._update_model_with_hand_cards()

    def make_suggestion(self):
        """Random suggestion based of own model"""

        random_world_id = random.randint(0, len(self.goal_model.worlds)-1)

        suggestion = []
        for prop in self.goal_model.worlds[random_world_id].assignment:
            suggestion.append(prop)

        return suggestion

    def check_hand_cards(self, suggestion):
        """checks if the player has one of the suggested cards in his own hand cards"""
        temp_sugg = set(suggestion)
        possible_matches = [
            card for card in self.hand_cards if card in temp_sugg]

        if len(possible_matches) > 0:
            random.shuffle(possible_matches)

            return possible_matches[0]

        else:
            return possible_matches

    def build_hand_cards_model(self, player_id: str, num_hand_cards: int, possible_cards: list):

        combinations = itertools.combinations(possible_cards, num_hand_cards)

        self.hand_card_models[str(player_id)] = kripke.create_single_kripke_model(
            combinations)

    def _update_model_with_hand_cards(self):

        for card in self.hand_cards:
            formula = formulas.not_has_specific_card(card)

            self.goal_model = kripke.update_kripke_model(
                self.goal_model, formula)
