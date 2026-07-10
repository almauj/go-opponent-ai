
import random as rd
import numpy as np

class HeuristicBot:
    def __init__(self, color=-1):
        self.color = color

    def evaluate_move(self, board, row, col, engine):
        """Calculates numerical weight for specified empty cell.

            Args: 
                - board - the entire board layout
                - row, col - the specific empty cell
                - engine - the game engine

            Returns: 
                scores - logical weights
        """

        score = 0
        opponent = -self.color
        neighbors = engine.get_neighbors(row,col)

        # local scoring
        for n_row, n_col in neighbors:
            neighbor_tile = board[n_row][n_col]
            if neighbor_tile == 1:
                score += getattr(self, 'aggression_weight', 8.0)
            elif neighbor_tile == self.color:
                score += getattr(self, 'defense_weight', 5.0)
        
        # venture scoring
        center = engine.size // 2 
        distance_from_center = abs(row - center) + abs(col - center)
        closeness_to_center = 8 - distance_from_center

        venture_coefficient = getattr(self, 'venture_weight', 1.5)
        score += closeness_to_center * venture_coefficient

        return score
    
    def get_move(self, engine):
        """Selects best move position according to scores.

            Args: engine - game engine

            Returns: random choice between best moves based on entire board
        
        """

        board = engine.board
        best_score = -1000
        best_moves = []

        for r in range(engine.size):
            for c in range(engine.size):
                if board[r][c] == 0: # empty space
                    if engine.is_legal_move(r, c, self.color):
                        move_score = self.evaluate_move(board, r, c, engine)

                        if move_score > best_score:
                            best_score = move_score
                            best_moves.clear()
                            best_moves.append((r, c))

                        elif move_score == best_score:
                            best_moves.append((r, c))

                        else:
                            pass

        return rd.choice(best_moves) if best_moves else None