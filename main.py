import pygame as pg
import numpy as np
import subprocess
import sys 
import io

from model import GoEngine
from database import init_db, log_game, get_bot_traits
from bot import HeuristicBot


# constant configurations
BOARD_SIZE = 9
CELL_SIZE = 54
BOARD_VIEW_SIZE = 540
SIDEBAR_SIZE = 180
WINDOW_WIDTH = BOARD_VIEW_SIZE + SIDEBAR_SIZE
WINDOW_HEIGHT = BOARD_VIEW_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TAN = (220, 179, 92)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)

# initialize db files locally
init_db()

# pygame initializations 
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Go Opponent Model")

pg.mixer.music.load('assets/background.mp3')
pg.mixer.music.set_volume(0.5) 
pg.mixer.music.play(-1)
font = pg.font.SysFont("Arial", 20)

pass_rect = pg.Rect(BOARD_VIEW_SIZE + 20, 150, 140, 45)
resign_rect = pg.Rect(BOARD_VIEW_SIZE + 20, 220, 140, 45)

clock = pg.time.Clock()

# engine model instance
engine = GoEngine(size=BOARD_SIZE)

# bot configurations
bot_agg, bot_def, bot_ven = get_bot_traits()
bot = HeuristicBot(color=-1)
bot.aggression_weight = bot_agg 
bot.defense_weight = bot_def
bot.venture_weight = bot_ven

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

    pg.draw.rect(screen, GRAY, (BOARD_VIEW_SIZE, 0, SIDEBAR_SIZE, WINDOW_HEIGHT))
    pg.draw.line(screen, BLACK, (BOARD_VIEW_SIZE, 0), (BOARD_VIEW_SIZE, WINDOW_HEIGHT), 3)


    # render capture score metrics text fields 
    txt_p_caps = font.render(f"Your Caps: {engine.player_captures}", True, BLACK)
    txt_b_caps = font.render(f"Bot Caps: {engine.bot_captures}", True, BLACK)
    screen.blit(txt_p_caps, (BOARD_VIEW_SIZE + 20, 40))
    screen.blit(txt_b_caps, (BOARD_VIEW_SIZE + 20, 80))

    # interactive action button styles
    pg.draw.rect(screen, DARK_GRAY, pass_rect, 0, 5)
    pg.draw.rect(screen, DARK_GRAY, resign_rect, 0, 5)
    screen.blit(font.render("Pass Turn", True, WHITE), (BOARD_VIEW_SIZE + 45, 160))
    screen.blit(font.render("Resign", True, WHITE), (BOARD_VIEW_SIZE + 55, 230))

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

    
            


# ---- game loop ----
running = True
total_moves_played = 0
force_quit_no_log = False


while running:
    if engine.is_board_full():
        print("No available moves. Ending game.")
        running = False
        break

    # --- Bot Turn ----
    if engine.current_player == -1 and running:
        pg.time.wait(400) # rest delay
        bot_choice = bot.get_move(engine)
        if bot_choice:
            b_row, b_col = bot_choice
            if engine.take_turn(b_row, b_col):
                total_moves_played += 1
                print(f"Bot placed stone at: {bot_choice}")
        else:
            # force skip if no moves available
            print("Bot has no legal moves left.")
            engine.current_player = 1


    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False
            force_quit_no_log = True


        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()

            row = round((mouse_x - CELL_SIZE) / CELL_SIZE)
            col = round((mouse_y - CELL_SIZE) / CELL_SIZE)

            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                move_successful = engine.take_turn(row, col)
                if move_successful:
                    total_moves_played += 1
                    print(f"Move successful! Stone placed at ({row}, {col})")
                else:
                    print("Illegal move attempted. Try again.")

            elif pass_rect.collidepoint((mouse_x, mouse_y)) and engine.current_player == 1:
                print("You passed your turn.")
                engine.current_player = -1
            elif resign_rect.collidepoint((mouse_x, mouse_y)):
                print("You resigned. Bot wins!")
                running = False
                break

    
    # rendering 
    draw_board()
    pg.display.flip()
    clock.tick(60)

pg.quit()

# --- post game data pipeline
if not force_quit_no_log:
    final_player_stones = int(np.sum(engine.board == 1))
    final_bot_stones = int(np.sum(engine.board == -1))
    game_winner = 'Player' if final_player_stones > final_bot_stones else 'Bot'

    # extract board pixels and pixel conversion to bytes
    board_rect = pg.Rect(0, 0, BOARD_VIEW_SIZE, WINDOW_HEIGHT)
    board_surface = screen.subsurface(board_rect)

    img_buffer = io.BytesIO()
    pg.image.save(board_surface, img_buffer, "png") # saves to RAM buffer
    raw_png_bytes = img_buffer.getvalue()
    img_buffer.close()

    # data pipeline
    log_game (
        board_size=BOARD_SIZE,
        winner=game_winner,
        total_moves=total_moves_played,
        bot_stones=final_bot_stones,
        player_stones=final_player_stones,
        bot_captures=engine.bot_captures,
        player_captures=engine.player_captures,
        image_bytes=raw_png_bytes
        )
    

    print("Launching Streamlit performance dashboard...")
    subprocess.Popen(["streamlit", "run", "dashboard.py"])

sys.exit()