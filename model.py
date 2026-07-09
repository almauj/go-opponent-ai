import numpy as np 

class GoEngine:

    def __init__(self, size=9):
        self.size=size

        # 0 = empty, 1 = black, -1 = white
        self.board = np.zeros((size, size), dtype=int)
        self.current_player = 1

    def get_neighbors(self, row, col):
        """ Checks boundaries and opponents.

            Args: row=row, col=column

            Returns: Neighbors - List of valid (r, c) tuples directly around current given position.
        """

        neighbors = []

        directions = [(1,0), (0,1), (-1,0), (0,-1)]

        for drows, dcols in directions:
            r = row + drows
            c = col + dcols

            if (0 <= r < self.size) and (0 <= c < self.size):
                neighbors.append((r,c))
        
        return neighbors
        # print(neighbors)

    def find_group(self, start_row, start_column):
        """ Finds all stones of the same color vertically or horizontally.

            Args: start_row, start_column  - starting position

            Return: Group - set of coordinates/positions with row and column values
        """

        color = self.board[start_row][start_column]

        # empty spaces
        if color == 0:
            return set()
        
        group = set()
        queue = [(start_row, start_column)]

        while queue:
            curr_r, curr_c = queue.pop(0)

            if (curr_r, curr_c) not in group:
                group.add((curr_r, curr_c))

                neighbors = self.get_neighbors(curr_r, curr_c)

                for n_row, n_col in neighbors:
                    if (n_row, n_col) not in group and self.board[n_row][n_col] == color:
                        queue.append((n_row, n_col)) 
                        
        
        return group
    
    def count_liberties(self, group):
        """Counts liberties, unique empty spaces that touch the group, based on the given group/position. 

            Args: group - a set of positions/coordinates

            Return: Number of liberties found.
        """

        liberties = set()

        for (row, col) in group:
            neighbors = self.get_neighbors(row, col)

            for (n_row, n_col) in neighbors:

                if (n_row, n_col) not in liberties and self.board[n_row][n_col] == 0:
                    liberties.add((n_row, n_col))

        return len(liberties)
    
    def take_turn(self, row, col):
        """Executes a move and handles turns (player switching)

            Args: row, col - the position for desired move

            Returns: true - for valid moves
                    false - for invalid moves
        """

        # checks if position is empty
        if self.board[row][col] != 0:
            return False
        
        # placement of stone
        self.board[row][col] = self.current_player

        # ----- capturing opponent's stone(s) -----
        new_neighbors = self.get_neighbors(row, col)

        opponent = -self.current_player

        for (n_row, n_col) in new_neighbors:
            if self.board[n_row][n_col] == opponent:

                opponent_group = self.find_group(n_row, n_col)

                if self.count_liberties(opponent_group) == 0:

                    for (o_row, o_col) in opponent_group:
                        
                        self.board[o_row][o_col] = 0
                pass


        # ---- illegal move -----
        player_group = self.find_group(row, col)

        if self.count_liberties(player_group) == 0:
            self.board[row][col] = 0
            return False
                
        # opponent switching

        self.current_player = -self.current_player
        return True


    

