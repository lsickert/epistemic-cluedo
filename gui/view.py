import random
from cv2 import circle
import pygame as pg 

from gui.load_rooms import  *
from gui.helper import throw_double_dice

from time import sleep

# activate the pg library .
# initiate pg and give permission
# to use pg's functionality.

START_POS = {1: (10, 0), 2: (13, 0), 3: (23, 14), 4: (14, 23), 5: (9, 23), 6: (0, 13)}
PLAYER_COLORS = {1: pg.Color("green"),
                 2: pg.Color("blue"), 
                 3: pg.Color("yellow"), 
                 4: pg.Color('red'), 
                 5: pg.Color('white'), 
                 6: pg.Color('purple')
}

DICE_FONT = None
CARD_FONT = None
sc = None
def initialize():
    pg.init()

    global DICE_FONT
    global CARD_FONT
    global sc
    # INIT
    DICE_FONT = pg.font.SysFont('Arial', 75)
    CARD_FONT = pg.font.SysFont('Arial', 40)
    # create the display surface object
    # of specific dimension..e(WIDTH, HEIGHT).
    sc = pg.display.set_mode((WIDTH, HEIGHT ))
    sc.fill(grey)


# set the pg window name
pg.display.set_caption('Cluedo')

ROOMS = load_rooms()

# define the RGB value
# for white colour
white = (255, 255, 255)
grey = (40,40,40)
black = (0,0,0)

# assigning values to WIDTH and HEIGHT variable
WIDTH = 1900
HEIGHT = 1000



class View:
    INSTANCE = None
    def __init__(self, game):
        View.INSTANCE = self
        self.game = game
        self.image = pg.image.load("./resources/map.jpg")
        self.dice_1 = ""
        self.dice_2 = ""
        self.player_steps = 0
        self.cards = []
        initialize()
        self.repaint()


    def provide_cards(self, cards):
        self.cards = cards


    def throw_dice(self):
        self.dice = throw_double_dice()
        self.dice_1 = str(self.dice[0])
        self.dice_2 = str(self.dice[1])
        return self.dice[0] + self.dice[1]
    

    # def new_player_location 
     
    def player_moved(self, direction):
        player = 0
        if self.player_steps == 0:
            return

        door = self.player_pos[player] in DOOR_LOCATIONS
        new_loc = [self.player_pos[player][0], self.player_pos[player][1]]
        cur_room = ROOMS[new_loc[0]][new_loc[1]]
        if cur_room != "corridor":
            self.__move_from_room(player, direction, cur_room)

        new_loc[0] += direction[0]
        new_loc[1] += direction[1]
        print(new_loc)

        if (new_loc[0], new_loc[1]) in SPECIAL_PATHWAYS:
            new_loc = list(SPECIAL_PATHWAYS[(new_loc[0], new_loc[1])])

        if not new_loc[0] in ROOMS or not new_loc[1] in ROOMS[new_loc[0]]:
            return

        room_type = ROOMS[new_loc[0]][new_loc[1]]
        if not door and room_type != 'corridor':
            return
        if door and room_type != 'corridor':
            self.player_steps = 0
            self.player_pos[player] = ROOM_PLACEMENT[room_type]
            return

        self.player_steps -= 1
        self.player_pos[player] = tuple(new_loc)
    

    def repaint(self):
        sc.fill(grey)
        sc.blit(self.image, (0, 0))
        self.__draw_dice(25, 850, self.dice_1)
        self.__draw_dice(150, 850, self.dice_2)
        self.__disp_players()
        color = pg.Color(self.game.players[0].disp_color)
        sc.blit(CARD_FONT.render("Your Cards", True, color), (900, 25))
        for idx, card in enumerate(self.game.players[0].hand_cards[::2]):
            sc.blit(CARD_FONT.render(card, True, color), (900, 75 + idx * 40))
        for idx, card in enumerate(self.game.players[0].hand_cards[1::2]):
            sc.blit(CARD_FONT.render(card, True, color), (1300, 75 + idx * 40))

        if self.game.latest_suggestion is not None:
            color = self.game.suggester.disp_color
            sc.blit(CARD_FONT.render(f"Latest suggestion by {self.game.suggester.color}", True, pg.Color(color)), (900, 175 + idx * 40))
            idx += 1
            sc.blit(CARD_FONT.render(self.game.latest_suggestion[0], True, pg.Color(color)), (900, 175 + idx * 40))
            idx += 1
            sc.blit(CARD_FONT.render(self.game.latest_suggestion[1], True, pg.Color(color)), (900, 175 + idx * 40))
            idx += 1
            sc.blit(CARD_FONT.render(self.game.latest_suggestion[2], True, pg.Color(color)), (900, 175 + idx * 40))
        

        sc.blit(CARD_FONT.render("Goal Deck", True, white), (900, 800))
        for idx, card in enumerate(self.game.goal_deck):
            sc.blit(CARD_FONT.render(card, True, white), (900, 850 + idx * 40))


        pg.display.update()


    def __move_from_room(self, player, direction, cur_room):
        options = [loc for loc, room in DOOR_LOCATIONS.items() if room == cur_room]
        self.player_steps -= 1
        if direction[0] == 0:
            if direction[1] == 1:
                # Return position with highest second entry
                self.player_pos[player] = max(options, key=lambda x: x[1])
            else:
                self.player_pos[player] = min(options, key=lambda x: x[1])
        if direction[1] == 0:
            if direction[0] == 1:
                # Return position with highest second entry
                self.player_pos[player] = max(options, key=lambda x: x[0])
            else:
                self.player_pos[player] = min(options, key=lambda x: x[0])


    def __draw_dice(self, x, y, roll):
        dice = pg.Rect(x, y, 100, 100)
        sc.fill(pg.Color('white'), dice)
        if self.dice_1 == "" or self.dice_2 == "":
            return
        self.dice_1 = int(self.dice_1)
        self.dice_2 = int(self.dice_2)
        # top left
        if roll in [2,3,4,5,6]:
            pg.draw.circle(sc, pg.Color('black'), (x + 25, y + 25), 7)
            pg.draw.circle(sc, pg.Color('black'), (x + 75, y + 75), 7)
        # top right
        if roll in [4,5,6]:
            pg.draw.circle(sc, pg.Color('black'), (x + 75, y + 25), 7)
            pg.draw.circle(sc, pg.Color('black'), (x + 25, y + 75), 7)
        # middle
        if roll in [1,3,5]:
            pg.draw.circle(sc, pg.Color('black'), (x + 50, y + 50), 7)
        # middle left
        if roll == 6:
            pg.draw.circle(sc, pg.Color('black'), (x + 25, y + 50), 7)
            pg.draw.circle(sc, pg.Color('black'), (x + 75, y + 50), 7)
    

    def __disp_players(self) -> None:
        for player in self.game.players:
            pos = player.location
            pg.draw.circle(sc, pg.Color('black'), (34*pos[0] + 15, 34*pos[1] + 15), 14)
            pg.draw.circle(sc, pg.Color(player.disp_color), (34*pos[0] + 15, 34*pos[1] + 15), 12)
    

    @staticmethod
    def update():
        View.INSTANCE.repaint()

       