"""contains the player class"""
import copy
from enum import Enum
import cluedo.logic_checker.formulas as formulas
import cluedo.logic_checker.kripke_model as kripke
import random
import itertools
import gui.helper as helper
from gui.load_rooms import DISPLAY_COLOR, FULLMAP, ROOM_PLACEMENT, STARTING_LOCATIONS
from gui.pathfinding import find_paths
from gui.view import View

class State(Enum):
    MOVING = 1
    SUGGESTING = 2
    END_TURN = 3


class Player:
    """all functions and properties of an individual player"""

    def __init__(self, player_id: int, hand_cards: list, goal_model, all_cards, higher_order: int, color: str) -> None:
        self.player_id = player_id
        self.hand_cards = hand_cards
        self.goal_model = copy.deepcopy(goal_model)
        self.all_characters = all_cards["characters"]
        self.all_weapons = all_cards["weapons"]
        self.all_rooms = all_cards["rooms"]
        self.hand_card_models = {}
        self.own_hand_card_model = None
        self.controllable = higher_order > 0
        self.higher_order = higher_order
        self.color = color
        self.disp_color = DISPLAY_COLOR[color]
        self.location = STARTING_LOCATIONS[color]
        self.latest_suggestion = None
        self.steps_left = 0
        self.start_of_turn = True
        self.last_room = None

        self._update_model_with_hand_cards()

        print(f"Player {player_id} has the following cards: {hand_cards}")


    def set_location(self, x, y):
        self.location = (x, y)

    def move(self):
        """
        Move to the specified room, or leave empty for 'choice' to let the player decide based on 'random' parameter.
        If the `random` parameter is set to true, then the player will move to a random room, otherwise move to the room with the highest information gain.
        """
        print(f"{self.color} moves from {self.location} to {self.path}")
        self.location = self.path[0]
        self.path = self.path[1:]
        self.makes_step()

        return self.location

    def make_suggestion(self, options = []):
        """
        Make a suggestion based of own model.
        If the `random` parameter is set to true, a random suggestion will be returned, otherwise the properties with the highest information gain are returned.
        """
        # if self.controllable:
        #     return self._user_control()

        # if self.higher_order >= 0 and not random_sugg:
        if True:
            characters = []
            weapons = []
            rooms = []
            # print(options)
            for world in self.goal_model.worlds:
                for idx, prop in enumerate(world.assignment):
                    if idx == 0:
                        characters.append(prop)

                    if idx == 1:
                        weapons.append(prop)

                    if idx == 2:
                        if prop in options and options != []:
                            rooms.append(prop)
            
            if rooms == []:
                for world in self.goal_model.worlds:
                    rooms.append(list(world.assignment)[2])
                

            suggestion = []
            suggestion.append(max(characters, key=characters.count))
            suggestion.append(max(weapons, key=weapons.count))
            suggestion.append(max(rooms, key=rooms.count))
            self.latest_suggestion = suggestion
            return suggestion

    def threw_dice(self, amount):
        self.steps_left = amount
    

    def prepare_turn(self):
        x, y = self.location
        paths = find_paths(x, y)
        for k, v in paths.items():
            print(f"towards {k}")
            print(v)
        dice = helper.throw_double_dice()
        self.steps_left = dice
        options = [k for k,v in paths.items() if len(v) < self.steps_left]
        suggestion = self.make_suggestion(options)
        self.path = paths[suggestion[2]]
        if self.location in ROOM_PLACEMENT.values():
            self.path = self.path[1:]


    def turn(self):
        x, y = self.location
        if self.start_of_turn:
            print("Prepping turn")
            self.prepare_turn()
            self.start_of_turn = False
            self.move()
            return State.MOVING
        
        if self.steps_left > 0 and FULLMAP[x][y] == 'corridor':
            print("moving")
            self.move()
            if FULLMAP[self.location[0]][self.location[1]] != 'corridor':
                self.steps_left = 0
                self.start_of_turn = True
                return State.SUGGESTING
            if self.steps_left == 0:
                self.start_of_turn = True
                return State.END_TURN
            return State.MOVING
        self.start_of_turn = True
        return State.END_TURN

    def makes_step(self):
        self.steps_left -= 1
        if FULLMAP[self.location[0]][self.location[1]] != 'corridor':
            self.steps_left = 0

        return self.steps_left > 0

    def opponent_has_card(self, player_id, card):
        pass

    def opponent_does_not_have_cards(self, player_id: str, cards: list):
        pass

    def opponent_has_one_of_cards(self, player_id, cards):
        pass

    def check_own_hand_cards(self, suggestion, opponent: str, use_knowledge: bool = None):
        """checks if the player has one of the suggested cards in his own hand cards
        If the parameter `use_knowledge` is set, the player will try to return a card the other agent already knows
        """
        temp_sugg = set(suggestion)
        possible_matches = [
            card for card in self.hand_cards if card in temp_sugg]

        if len(possible_matches) > 0:
            random.shuffle(possible_matches)

            if len(possible_matches) > 1 and (self.higher_order >= 2 or use_knowledge):
                for match in possible_matches:
                    if formulas.agent_knows_has_specific_card(match, opponent).semantic(self.own_hand_card_model, "w1"):
                        # we do not need to update model, since the opponent will not gain any new knowledge here
                        return match

            self.update_own_hand_cards_model(possible_matches[0], opponent)

            return possible_matches[0]

        return possible_matches

    def check_other_hand_cards(self):
        """Check the hand card models of all other players if it is known that they have a specific card and update the own goal model to exclude that card"""

        if self.higher_order >= 1:
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

