

from gui.helper import *
from gui.init import *
import gui.logic_checker.kripke_model as kripke
import gui.logic_checker.formulas as formulas
from gui.player import Player, State
from gui.view import View

NR_CHARACTERS = 6
NR_ROOMS = 6
NR_WEAPONS = 7 

CHARACTERS = get_characters()
ROOMS = get_rooms()
WEAPONS = get_weapons()

PLAYERS = [-1, 0, 1, 2]
LIST_OF_COLORS = ["scarlett", "green", "mustard", "plum", "peacock", "white"]

class Game:
    def __init__(self):
        self.characters, self.weapons, self.rooms = create_resource_sets()
        self.all_cards = {"characters": self.characters, "weapons": self.weapons, "rooms": self.rooms}

        characters = self.characters
        weapons = self.weapons
        rooms = self.rooms
        self.goal_deck, self.clue_deck = create_card_deck(characters, weapons, rooms)
        possible_worlds = self.possible_worlds = get_card_combinations(characters, weapons, rooms)
        self.base_model = kripke.create_multi_kripke_model(possible_worlds, len(PLAYERS))

        self.latest_suggestion = None
        self.suggester = None

        self.__init_players()
        self.over = False


    def turn(self, state):
        player = self.players[0]
        print(f"{player.color}'s turn")
        if state == State.SUGGESTING:
            self.make_suggestion(player.latest_suggestion)
            self.players = self.players[1:] + [self.players[0]]
            return State.MOVING

        if state == State.END_TURN:
            self.players = self.players[1:] + [self.players[0]]
            self.players[0].prepare_turn()
            return State.MOVING


        player = self.players[0]
        state = player.turn()
        return state


    def make_suggestion(self, suggestion):
        self.latest_suggestion = suggestion
        self.suggester = self.players[0]
        suggestee = suggestion[0]
        for player in self.players:
            if player.color == suggestee:
                player.set_location(self.suggester.location[0] , self.suggester.location[1])
        View.update()
        
        print(f"{self.players[0].color} makes suggestion {suggestion}")
        print(f"With goal deck {self.goal_deck}")
        for player in self.players[1:]:
            matches = [card for card in player.hand_cards if card in suggestion]
            if len(matches) != 0:
                print(f"{player.color} shows {matches[0]}")
                self.opponent_shows_card(self.players[0], player, matches[0], suggestion)
                break
            else:
                print(f"{player.color} has no card")
                self.opponent_has_no_card(player, suggestion)
        
        for sug in suggestion:
            if sug not in self.goal_deck:
                return
        print("SUGGESTION WAS RIGHT!")
        self.over = True
                    

    def opponent_shows_card(self, player, opponent, card, suggestion):
        player.update_goal_model(formulas.not_has_specific_card(card))
        player.update_hand_cards_model(opponent.player_id, formulas.has_specific_card(card))

        for other_player in self.players[1:]:
            if not other_player.player_id == opponent.player_id:
                if other_player.higher_order >= 0:
                    other_player.update_goal_model(formulas.not_character_weapon_room_and(
                        suggestion[0], suggestion[1], suggestion[2]))

                if other_player.higher_order >= 1:
                    other_player.update_hand_cards_model(opponent.player_id, formulas.character_weapon_room_or(
                        suggestion[0], suggestion[1], suggestion[2]))

    def opponent_has_no_card(self, opponent, suggestion):
        for player in self.players:
            if player != opponent:
                player.update_hand_cards_model(opponent.player_id, formulas.not_character_weapon_room_and(
                    suggestion[0], suggestion[1], suggestion[2]))

    def __init_players(self):
        players = []
        hand_cards = _split_hand_cards(len(PLAYERS), self.clue_deck)
        for player, order in enumerate(PLAYERS):
            color = LIST_OF_COLORS[player]
            players.append(Player(player, hand_cards[player], self.base_model, self.all_cards, order, color))

        # build the hand card models of the other players for each player
        for player in players:
            player.build_own_hand_cards_model(len(PLAYERS))
            num_hand_cards = len(player.hand_cards)
            remaining_clues = self.clue_deck.copy() + list(self.goal_deck)

            for card in player.hand_cards:
                remaining_clues.remove(card)
            for other_player in players:
                if not other_player.player_id == player.player_id:
                    player.build_hand_cards_model(
                        other_player.player_id, num_hand_cards, remaining_clues)

        self.players = players


def _split_hand_cards(num_players: int, clue_deck: list) -> list:
    c = len(clue_deck) // num_players
    r = len(clue_deck) % num_players
    return [clue_deck[p * c + min(p, r):(p+1) * c + min(p+1, r)] for p in range(num_players)]
