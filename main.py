"""epistemic-cluedo main module"""

# import sleep
from time import sleep


from gui.game import *

if __name__ == "__main__":
    # infinite loop
    game = Game()
    from gui.view import *
    view = View(game)
    state = State.MOVING
    while not game.over:
        for event in pg.event.get():
            # print("event")

            if event.type == pg.QUIT :
                pg.quit()
                quit()
               
                # map.rolled_dice(random.randint(1, 6), random.randint(1, 6))
            
            # if event.type == pg.MOUSEBUTTONDOWN:
        sleep(0.05)
        state = game.turn(state)
        if state == State.END_TURN:
            sleep(1)
        view.repaint()
        #     if event.type == pg.KEYDOWN:
        #         if event.key == pg.K_UP:
        #             map.player_moved((0,-1))
        #         if event.key == pg.K_DOWN:
        #             map.player_moved((0,1))
        #         if event.key == pg.K_LEFT:
        #             map.player_moved((-1,0))
        #         if event.key == pg.K_RIGHT:
        #             map.player_moved((1,0))
        #         if event.key == pg.K_RETURN:
        #             map.provide_cards(['1', '2', '3', '4', '5', '6'])

        # game.turn()
            
pg.quit()