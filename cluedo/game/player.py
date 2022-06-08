"""contains the player class"""
import copy
import cluedo.logic_checker.formulas as formulas
import cluedo.logic_checker.kripke_model as kripke
import random

class Player:
    """all functions and properties of an individual player"""

    def __init__(self, player_id: int, hand_cards: list, base_model) -> None:
        self.player_id = player_id
        self.hand_cards = hand_cards
        self.goal_model = copy.deepcopy(base_model)

        self.update_model_with_hand_cards()

    def update_model_with_hand_cards(self):
        
        for card in self.hand_cards:
            formula = formulas.not_has_specific_card(card)

            self.goal_model = kripke.update_kripke_model(self.goal_model, formula)
        

    def make_suggestion(self):
        """Random suggestion based of own model"""

        random_world_id = random.randint(1, len(self.goal_model.worlds))

        suggestion = []  
        for prop in self.goal_model.worlds[random_world_id].assignment:
            suggestion.append(prop)

        return suggestion

        
