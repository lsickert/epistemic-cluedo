"""contains the player class"""
import copy
import cluedo.logic_checker.formulas as formulas
import cluedo.logic_checker.kripke_model as kripke
import random
import itertools


class Player:
    """all functions and properties of an individual player"""

    def __init__(self, player_id: int, hand_cards: list, base_model, all_characters: list, all_weapons: list, all_rooms: list, controllable: bool = True) -> None:
        self.player_id = player_id
        self.hand_cards = hand_cards
        self.goal_model = copy.deepcopy(base_model)
        self.all_characters = all_characters
        self.all_weapons = all_weapons
        self.all_rooms = all_rooms
        self.hand_card_models = {}
        self.controllable = controllable

        self._update_model_with_hand_cards()

        print(f"Player {player_id} has the following cards: {hand_cards}")

    def make_suggestion(self, random_sugg=True):
        """
        Make a suggestion based of own model.
        If the `random` parameter is set to true, a random suggestion will be returned, otherwise the properties with the highest information gain are returned.
        """
        if self.controllable:
            return self._user_control()

        if random_sugg:
            random_world_id = random.randint(0, len(self.goal_model.worlds)-1)

            suggestion = []
            for prop in self.goal_model.worlds[random_world_id].assignment:
                suggestion.append(prop)
            
            return suggestion

        characters = []
        weapons = []
        rooms = []
        for world in self.goal_model.worlds:
            for idx, prop in enumerate(world.assignment):
                if idx == 0:
                    characters.append(prop)

                if idx == 1:
                    weapons.append(prop)

                if idx == 2:
                    rooms.append(prop)

        suggestion = []
        suggestion.append(max(characters, key=characters.count))
        suggestion.append(max(weapons, key=weapons.count))
        suggestion.append(max(rooms, key=rooms.count))

        return suggestion

    def check_own_hand_cards(self, suggestion):
        """checks if the player has one of the suggested cards in his own hand cards"""
        temp_sugg = set(suggestion)
        possible_matches = [
            card for card in self.hand_cards if card in temp_sugg]

        if len(possible_matches) > 0:
            random.shuffle(possible_matches)

            return possible_matches[0]

        return possible_matches

    def check_other_hand_cards(self):
        """Check the hand card models of all other players if it is known that they have a specific card and update the own goal model to exclude that card"""

        possible_values = set()

        for world in self.goal_model.worlds:
            for prop in world.assignment:
                possible_values.add(prop)

        for model in self.hand_card_models.values():
            for prop in possible_values:
                # we only need to check the first world since all worlds are connected in a S5 model
                knows_hand_card = formulas.knows_has_specific_card(
                    prop).semantic(model, model.worlds[0].name)

                if knows_hand_card:
                    self.update_goal_model(
                        formulas.not_has_specific_card(prop))

    def check_winning_possibility(self):
        """checks if the player has a possibility of winning the game, meaning that there is only one world left in his goal model"""

        num_possible_worlds = len(self.goal_model.worlds)

        if num_possible_worlds == 1:
            accusation = []
            for prop in self.goal_model.worlds[0].assignment:
                accusation.append(prop)
            return accusation
        else:
            return []

    def build_hand_cards_model(self, player_id: str, num_hand_cards: int, possible_cards: list):

        combinations = itertools.combinations(possible_cards, num_hand_cards)

        self.hand_card_models[str(player_id)] = kripke.create_single_kripke_model(
            combinations)

    def update_hand_cards_model(self, player_id: str, formula):

        self.hand_card_models[str(player_id)] = kripke.update_kripke_model(
            self.hand_card_models[str(player_id)], formula)

    def update_goal_model(self, formula):

        self.goal_model = kripke.update_kripke_model(self.goal_model, formula)

    def _update_model_with_hand_cards(self):

        for card in self.hand_cards:
            formula = formulas.not_has_specific_card(card)

            self.goal_model = kripke.update_kripke_model(
                self.goal_model, formula)

    def _user_control(self):
        possibilities = []
        for x in self.goal_model.worlds:
            for y in x.assignment:
                if y not in possibilities:
                    possibilities.append(y)

        suggestion = []
        characters = [x for x in possibilities if x in self.all_characters]
        suggestion.append(self.__prompt(characters, "character"))
        weapons = [x for x in possibilities if x in self.all_weapons]
        suggestion.append(self.__prompt(weapons, "weapon"))
        rooms = [x for x in possibilities if x in self.all_rooms]
        suggestion.append(self.__prompt(rooms, "room"))
        return suggestion

    def __prompt(self, options, card_type):
        space_in_between = 15
        string = ""
        for idx, option in enumerate(options):
            string += f"{idx}: {option}"
            for _ in range(space_in_between - len(string) % space_in_between):
                string += " "
        print(string)
        return options[int(input(f"Choose a {card_type}: "))]
