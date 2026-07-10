
import sqlite3 as sq
from datetime import datetime 

DB_NAME = "go_analytics.db"

def init_db():
    """Creates database if not exists"""
    conn = sq.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_history (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            board_size INTEGER,
            winner TEXT,
            total_moves INTEGER,
            bot_stones INTEGER,
            player_stones INTEGER,
            bot_captures INTEGER,
            player_captures INTEGER,
            final_board_img BLOB
            )
         """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bot_traits (
            id INTEGER REFERENCES game_history(game_id),
            aggression REAL,
            defense REAL,
            venture REAL
            )
        """)
    
    cursor.execute("SELECT COUNT(*) FROM bot_traits")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO bot_traits (id, aggression, defense, venture) VALUES (0, 8.0, 5.0, 1.5)")

    conn.commit()
    conn.close()

def get_bot_traits():
    """Retrieves current traits for bot"""
    conn = sq.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT aggression, defense, venture FROM bot_traits ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row if row else (8.0, 5.0, 1.5)

def log_game(board_size, winner, total_moves, bot_stones, player_stones, bot_captures, player_captures, image_bytes):
    """ Logs a new row of data from a completed game to the database and updates bot's traits dynamically.
    """
    conn = sq.connect(DB_NAME)
    cursor = conn.cursor()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = "INSERT INTO game_history (timestamp, board_size, winner, total_moves, bot_stones, player_stones, bot_captures, player_captures, final_board_img) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (current_time, board_size, winner, total_moves, bot_stones, player_stones, bot_captures, player_captures, image_bytes))

    new_game_id = cursor.lastrowid

    # ---- Bot Trait Adjustmant ----
    cursor.execute("SELECT aggression, defense, venture FROM bot_traits ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        curr_agg, curr_def, curr_ven = row
    else:
        curr_agg, curr_def, curr_ven = (8.0, 5.0, 1.5)
    
    if winner.lower() == 'player':
        if player_captures > bot_captures:
            curr_def += 0.1 
            curr_ven += 0.5
        else: 
            curr_agg += 0.1
            curr_ven += 0.3
    else:
        curr_agg = max(1.0, curr_agg - 0.1)
        curr_def = max(1.0, curr_def - 0.1)
        curr_ven = max(0.5, curr_ven - 0.1)

    cursor.execute("INSERT INTO bot_traits (id, aggression, defense, venture) VALUES (?, ?, ?, ?)", (new_game_id, curr_agg, curr_def, curr_ven))
    print(f"Bot adapted behavior - {winner} Win. Personality is now -> Aggression = {curr_agg}, Defense = {curr_def}, Venture = {curr_ven}")

    conn.commit()
    conn.close()
    print("Game data and final board image were successfully logged into database.")
    return new_game_id
