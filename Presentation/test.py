import random
import pygame as pg 

from load_rooms import  *

# activate the pg library .
# initiate pg and give permission
# to use pg's functionality.
pg.init()

# INIT
DICE_FONT = pg.font.SysFont('Arial', 75)
CARD_FONT = pg.font.SysFont('Arial', 40)
START_POS = {1: (10, 0), 2: (13, 0), 3: (23, 14), 4: (14, 23), 5: (9, 23), 6: (0, 13)}
PLAYER_COLORS = {1: pg.Color("green"),
                 2: pg.Color("blue"), 
                 3: pg.Color("yellow"), 
                 4: pg.Color('red'), 
                 5: pg.Color('white'), 
                 6: pg.Color('purple')
}

ROOMS = load_rooms()
print(ROOMS)

# define the RGB value
# for white colour
white = (255, 255, 255)
grey = (60,60,60)
black = (0,0,0)

# assigning values to WIDTH and HEIGHT variable
WIDTH = 1900
HEIGHT = 1000

# create the display surface object
# of specific dimension..e(WIDTH, HEIGHT).
sc = pg.display.set_mode((WIDTH, HEIGHT ))
pg.display.update()

# set the pg window name
pg.display.set_caption('Cluedo')


class Map:
    def __init__(self, screen, nr_players):
        self.sc = screen
        self.nr_players = nr_players
        self.image = pg.image.load("./map.jpg")
        
        self.sc.blit(self.image, (0, 0))
        
        self.dice_1 = ""
        self.dice_2 = ""
        self.player_steps = 0
        self.cards = []
        self.player_pos = {i: START_POS[i] for i in range(1, nr_players + 1)}


    def provide_cards(self, cards):
        self.cards = cards


    def rolled_dice(self, dice_1, dice_2):
        self.dice_1 = str(dice_1)
        self.dice_2 = str(dice_2)
        self.player_steps = dice_1 + dice_2
    

    # def new_player_location 
     
    def player_moved(self, direction, player = 1):
        if self.player_steps == 0:
            return

        door = self.player_pos[player] in DOOR_LOCATIONS
        new_loc = [self.player_pos[player][0], self.player_pos[player][1]]
        cur_room = ROOMS[new_loc[0]][new_loc[1]]
        if cur_room != "corridor":
            self.__move_from_room(player, direction, cur_room)

        new_loc[0] += direction[0]
        new_loc[1] += direction[1]

        room_type = ROOMS[new_loc[0]][new_loc[1]]
        if not door and room_type != 'corridor':
            return
        if door and room_type != 'corridor':
            self.player_steps = 0
            self.player_pos[player] = ROOM_PLACEMENT[room_type]
            return

        self.player_steps -= 1
        self.player_pos[player] = tuple(new_loc)


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
        for player, pos in self.player_pos.items():
            pg.draw.circle(sc, pg.Color('black'), (34*pos[0] + 15, 34*pos[1] + 15), 14)
            pg.draw.circle(sc, PLAYER_COLORS[player], (34*pos[0] + 15, 34*pos[1] + 15), 12)
       

    def repaint(self):
        self.sc.blit(self.image, (0, 0))
        self.__draw_dice(25, 850, self.dice_1)
        self.__draw_dice(150, 850, self.dice_2)
        self.__disp_players()
        sc.blit(CARD_FONT.render("Your Cards", True, black), (900, 25))
        for idx, card in enumerate(self.cards[::2]):
            sc.blit(CARD_FONT.render(card, True, black), (900, 75 + idx * 40))
        for idx, card in enumerate(self.cards[1::2]):
            sc.blit(CARD_FONT.render(card, True, black), (1300, 75 + idx * 40))
        pg.display.update()

def main(nr_players:int  = 6):
    # infinite loop
    map = Map(sc, nr_players)
    while True :

        # completely fill the surface object
        # with white colour
        sc.fill(grey)

        # iterate over the list of Event objects
        # that was returned by pg.event.get() method.
        for event in pg.event.get():

            # if event object type is QUIT
            # then quitting the pg
            # and program both.
            if event.type == pg.QUIT :

                # deactivates the pg library
                pg.quit()

                # quit the program.
                quit()
               
            if event.type == pg.MOUSEBUTTONDOWN:
                map.rolled_dice(random.randint(1, 6), random.randint(1, 6))
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    map.player_moved((0,-1))
                if event.key == pg.K_DOWN:
                    map.player_moved((0,1))
                if event.key == pg.K_LEFT:
                    map.player_moved((-1,0))
                if event.key == pg.K_RIGHT:
                    map.player_moved((1,0))
                if event.key == pg.K_RETURN:
                    map.provide_cards(['1', '2', '3', '4', '5', '6'])


            # # Draws the surface object to the screen.
            map.repaint()
            # pg.display.update()


if __name__=="__main__":
    main(5)