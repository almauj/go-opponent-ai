# Go ML Model: An Adaptive Heuristic Go Engine

A full-stack 2D Go game implementation and data logging pipeline built entirely from scratch in Python—no LLM APIs required. This project features an automated, rule-validated bot opponent that dynamically adjusts how it plays based on our matches, saving everything to a local SQLite database and visualizing stats on a custom Streamlit dashboard.

---

## The Story Behind the Project

For a while now, I’ve really wanted to learn the ancient game of Go. But the apps I had usually had a lot of ads and limited rounds, which I thought was kind of lame. So! I decided to build the game myself with an opponent that learns alongside me. However, since I'm already learning agentic frameworks, I wanted to build this model without LLM APIs and apply my knowledge of reinforcement learning.

At first I thought it would not be that complicated especially with simple graphics, but it was definitely a challenging project that pushed me to think through complex logic and solve tough problems. To help me figure out the architecture and get over some learning curves, I utilized AI to act as a senior software engineer and mentor.

It is super important to emphasize that **this project was not a copy-paste job**. While my AI mentor gave me large chunks of theoretical guidance and structural templates, the logic behind the decisions, the bug fixes, and the upgrades were entirely my own. I designed and built this system out of passion and curiosity for both the game and the code, and it’s something I am incredibly proud of. :)

---

## How It Works

* **The Engine (`model.py`)**: The brain of the game rules. Built on top of NumPy arrays, it enforces liberties, handles connected stone groups (using a flood-fill algorithm), and calculates clean captures.
* **The Interface (`main.py`)**: Built with Pygame. It handles the wooden 2D board rendering, background music, and translates mouse clicks into exact grid coordinates.
* **The Opponent (`bot.py`)**: A heuristic-driven bot that scores every empty spot on a scorecard to decide where to drop White stones.
* **The Data Pipeline (`database.py` & `dashboard.py`)**: A local SQLite warehouse that pairs up with a browser-based Streamlit dashboard to show my progress over time.

---

## Struggles, Debugging, and Breakthroughs

Here are the three biggest bugs I ran into, what was causing them, and how I fixed them:

### 1. The Color Desynchronization Trap

* **The Bug:** The bot would randomly freeze, refuse to place stones, and suddenly swap player colors—forcing me to play as White and breaking the whole turn counter.
* **The Cause:** I had initialized the bot to think it was playing as Black (`color=1`) while the main game loop expected it to play as White (`-1`). Because of this, the bot would pick moves that were perfectly legal for Black, but completely illegal/suicide for White. The engine rejected the move, but the loop accidentally passed the turn anyway without a stone being placed, trapping the game in a deadlock.
* **The Fix:** I synchronized the colors. I updated `main.py` so the bot initialized as `-1` and refactored `bot.py` to evaluate the board dynamically based on a relative opponent pointer (`opponent = -self.color`).

### 2. The Suicide Move Filter

* **The Bug:** The bot only scanned for empty squares. It would routinely pick the highest-scoring spot on its scorecard, only for the engine to reject it because it was an illegal suicide move, causing the game turns to get out of sync.
* **The Cause:** The bot didn't have a way to "preview" whether a move was actually legal before trying to play it on the live board.
* **The Fix:** I created a concept called a **Single Source of Truth**. I added an `is_legal_move(row, col, player)` function inside the `GoEngine`. Now, before the bot scores an empty square, it asks the engine: *"Is this move suicide?"* If the engine says yes, the bot skips it entirely, completely preventing rule violations.

### 3. Pygame's Window Lifecycle Crash

* **The Bug:** I wanted to take a screenshot of the final board state at the end of each match and save it directly into the SQLite database as a binary `BLOB` asset (perfect for training a machine learning model later). But whenever the bot resigned or the game ended, it threw a `pygame.error: Surface is not initialized` crash.
* **The Cause:** The game loop was hitting a `break` statement that instantly called `pg.quit()`. This completely destroyed the window out of the computer's memory a fraction of a millisecond before the database script could crop the screen.
* **The Fix:** I rewrote the ending into a clean **Game Over State Handler**. When a resignation happens, the loop stays alive but sets a `game_over = True` flag. The script captures the board screenshot using an in-memory `io.BytesIO()` buffer and saves it to SQL **while the screen is wide open**. Only when I click the "Quit & Dashboard" button does the program safely shut down.

---

## A Bot That Grows With Me

To make sure we both learn together, I programmed a bidirectional learning loop into the database:

* The bot tracks three personality traits: `aggression`, `defense`, and `venture` (which uses **Manhattan Distance math** to force the bot to stop clustering and explore the open center of the board).
* **If I win:** The database automatically increases the bot's traits by `+0.1`, making it slightly tougher the next day.
* **If the bot wins:** It dials back its parameters by `-0.1`, easing up its playstyle so I have room to breathe, learn, and catch up.

---

## How to Run the Game

### Install Dependencies

```bash
pip install pygame numpy streamlit pandas 
```

### 1. Play a Match

Run the main script to play on a 9x9 board. Left-click to place Black stones. Use the right sidebar to Pass or Resign. The bot will also automatically resign if it runs out of legal moves or determines defeat is inevitable.

```bash
python main.py
```

### 2. Open the Dashboard

When the game ends, the sidebar will update with a **Quit** button. Clicking it safely logs your data, takes a final screenshot, closes the game, and automatically boots up your browser dashboard to show your win rate, capture trends, and your last played board!

```bash
streamlit run dashboard.py
```

---

## Future Upgrades

I will admit there is still lots of room for improvement as far as integrating more of the rules of Go and strategies that come with it. But as I get better, I plan to keep upgrading this project:

* **Enhanced Declustering**: While the bot improved its moves with my initial attempt to decluster, it still clusters toward the center, so I will be doing more research to see different ways to resolve this.
* **Computer Vision**: Train a Convolutional Neural Network (CNN) directly on the final board image BLOBs saved in my database to recognize winning board shapes.
* **Go Strategy Mapping**: Build coordinate checkers into the analytics engine to log advanced shapes (like *Kosumi*, *Nobi*, or opening *Joseki* patterns).
* **Look-Ahead Search (MCTS)**: Upgrade the bot with a Monte Carlo Tree Search so it can simulate future moves 3 steps ahead instead of just reacting to its immediate turn.

As of 07/2026, my next immediate steps will be to resolve the 'Ko' rule enforcement and the clustering state of the Go Bot. 
