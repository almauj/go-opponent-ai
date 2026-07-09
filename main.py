import pygame as pg
import sys 
from model import GoEngine


# constant configurations
WINDOW_SIZE = 540
BOARD_SIZE = 9
CELL_SIZE = WINDOW_SIZE // (BOARD_SIZE + 1)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TAN = (220, 179, 92)

# pygame initializations 
pg.init()
screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pg.display.set_caption("Go Opponent Model")
clock = pg.time.Clock()

# engine model instance
engine = GoEngine(size=BOARD_SIZE)

def draw_board():
    """ Draws Game Grid and Stones. 

        Returns:
                - game grid with vertical and horizontal lines
                - stones -> 1=black, 0=empty, -1=white
    """

    # game board
    screen.fill(TAN)

    for i in range(BOARD_SIZE):
        offset = (i + 1) * CELL_SIZE
        pg.draw.line(screen, BLACK, (offset, CELL_SIZE), (offset, BOARD_SIZE * CELL_SIZE), 2) # vertical
        pg.draw.line(screen, BLACK, (CELL_SIZE, offset), (BOARD_SIZE * CELL_SIZE, offset), 2) # horizontal



    
    # stones

    for i in range(0, engine.size):
        for j in range(0, engine.size):
            cell = engine.board[i][j]
            pixel_x = (i + 1) * CELL_SIZE
            pixel_y = (j + 1) * CELL_SIZE

            if cell == 1:
                pg.draw.circle(screen, BLACK, (pixel_x, pixel_y), (CELL_SIZE // 2) - 2) # draw black
            elif cell == -1:
                pg.draw.circle(screen, WHITE, (pixel_x, pixel_y), (CELL_SIZE // 2) - 2) # draw white
            else:
                pass
            


# ---- game loop ----
running = True
while running:
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()

            row = round((mouse_x - CELL_SIZE) / CELL_SIZE)
            col = round((mouse_y - CELL_SIZE) / CELL_SIZE)

            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                move_successful = engine.take_turn(row, col)
                if move_successful:
                    print(f"Move successful! Stone placed at ({row}, {col})")
                else:
                    print("Illegal move attempted. Try again.")

    
    # rendering 
    draw_board()
    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()