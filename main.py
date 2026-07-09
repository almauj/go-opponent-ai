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
    pos_count = CELL_SIZE

    while pos_count < BOARD_SIZE:
        pg.draw.line(screen, BLACK, (pos_count, CELL_SIZE), (0, BOARD_SIZE), 1) # vertical
        pg.draw.line(screen, BLACK, (0, BOARD_SIZE), (pos_count, CELL_SIZE), 1) # horizontal

        pos_count += CELL_SIZE

    
    # stones
    for i in range(0, engine.size):
        for j in range(0, engine.size):
            cell = engine.board[i][j]

            if cell == 1:
                pg.draw.circle(screen, BLACK, (i, j), 10) # draw black
            elif cell == -1:
                pg.draw.circle(screen, WHITE, (i, j), 10) # draw white
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

            row, col = 0
            matrix_x = mouse_x // CELL_SIZE
            matrix_y = mouse_y // CELL_SIZE

            row += matrix_x
            col += matrix_y

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