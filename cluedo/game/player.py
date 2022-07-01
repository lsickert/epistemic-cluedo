"""contains the player class"""
import copy
import cluedo.logic_checker.formulas as formulas
import cluedo.logic_checker.kripke_model as kripke
import random
import itertools
import cluedo.game.helper as helper

class Player:
    """all functions and properties of an individual player"""

    def __init__(self, player_id: int, hand_cards: list, base_model, all_characters: list, all_weapons: list, all_rooms: list, higher_order: int, color: str, controllable: bool = True) -> None:
        self.player_id = player_id
        self.hand_cards = hand_cards
        self.goal_model = copy.deepcopy(base_model)
        self.all_characters = all_characters
        self.all_weapons = all_weapons
        self.all_rooms = all_rooms
        self.hand_card_models = {}
        self.own_hand_card_model = None
        self.controllable = controllable
        self.higher_order = higher_order
        self.color = color
        self.location = None
        self.latest_suggestion = None

        self._update_model_with_hand_cards()

        print(f"Player {player_id} has the following cards: {hand_cards}")

    def move(self, suggestion, room = 'choice'):
        """
        Move to the specified room, or leave empty for 'choice' to let the player decide based on 'random' parameter.
        If the `random` parameter is set to true, then the player will move to a random room, otherwise move to the room with the highest information gain.
        """
        if room == 'choice':
            possible_rooms = helper.get_possible_rooms(self.location, self.color)
            self.location = suggestion[2] if suggestion[2] in possible_rooms else 'pathways'
        else:
            self.location = room    # Move to room

        return self.location

    def make_suggestion(self, random_sugg: bool = None):
        """
        Make a suggestion based of own model.
        If the `random` parameter is set to true, a random suggestion will be returned, otherwise the properties with the highest information gain are returned.
        """
        if self.controllable:
            return self._user_control()

        if self.higher_order > 0 and not random_sugg:
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
            self.latest_suggestion = suggestion
            return suggestion


        options = []
        for world in self.goal_model.worlds:
            if list(world.assignment)[2] in helper.get_possible_rooms(self.location):
                options.append(world)

        random_world = random.choice(options)

        suggestion = []
        for prop in random_world.assignment:
            suggestion.append(prop)
        self.latest_suggestion = suggestion
        return suggestion



    def check_own_hand_cards(self, suggestion, opponent: str, use_knowledge: bool = None):
        """checks if the player has one of the suggested cards in his own hand cards
        If the parameter `use_knowledge` is set, the player will try to return a card the other agent already knows
        """
        temp_sugg = set(suggestion)
        possible_matches = [
            card for card in self.hand_cards if card in temp_sugg]

        if not possible_matches:
            return None

        random.shuffle(possible_matches)
        if len(possible_matches) > 1 and (self.higher_order > 1 or use_knowledge):
            for match in possible_matches:
                if formulas.agent_knows_has_specific_card(match, opponent).semantic(self.own_hand_card_model, "w1"):
                    # we do not need to update model, since the opponent will not gain any new knowledge here
                    return match
        
        self.update_own_hand_cards_model(possible_matches[0], opponent)
        return possible_matches[0]


    def check_other_hand_cards(self):
        """Check the hand card models of all other players if it is known that they have a specific card and update the own goal model to exclude that card"""

        if self.higher_order > 0:
            possible_values = set()

            for world in self.goal_model.worlds:
                for prop in world.assignment:
                    possible_values.add(prop)

            for model in self.hand_card_models.values():
                for prop in possible_values:
                    # we only need to check the first world since all worlds are connected in a S5 model
                    try:
                        knows_hand_card = formulas.knows_has_specific_card(
                            prop).semantic(model, model.worlds[0].name)

                        if knows_hand_card:
                            self.update_goal_model(
                                formulas.not_has_specific_card(prop))
                    except IndexError:
                        print(model)
                        print(model.worlds)


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
        """Build a model for the knowledge about the hand cards of another player"""
        combinations = itertools.combinations(possible_cards, num_hand_cards)

        self.hand_card_models[str(player_id)] = kripke.create_single_kripke_model(
            combinations)

    def build_own_hand_cards_model(self, num_players: int):
        """Build a model for the knowledge about knowledge of other players about your hand cards"""
        # add full handcard knowledge and no handcard knowledge
        combinations = [tuple(self.hand_cards), tuple()]

        # add remaining card knowledge
        if len(self.hand_cards) > 1:
            for i in range(1, len(self.hand_cards)):

                combinations.extend(itertools.combinations(self.hand_cards, i))

        self.own_hand_card_model = kripke.create_multi_kripke_model(
            combinations, num_players, exclude_players=[int(self.player_id)])

    def update_hand_cards_model(self, player_id: str, formula):

        self.hand_card_models[str(player_id)] = kripke.update_kripke_model(
            self.hand_card_models[str(player_id)], formula)

    def update_goal_model(self, formula):

        self.goal_model = kripke.update_kripke_model(self.goal_model, formula)

    def update_own_hand_cards_model(self, match: str, opponent: str):

        remove_match_nodes = self.own_hand_card_model.nodes_not_follow_formula(
            formulas.has_specific_card(match))

        for node in remove_match_nodes:
            kripke.remove_agent_relations(
                self.own_hand_card_model, opponent, world_2=node, symmetric=True)

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
