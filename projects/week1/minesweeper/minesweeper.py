import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def __repr__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge represelntation given the fact that
        a cell is known to be a mine.
        """
        for sentence_cell in list(self.cells):
            if sentence_cell == cell:
                #print(f"{cell} is a mine removed from sencent count--  ")
                self.cells.remove(sentence_cell)
                self.count -=1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        for sentence_cell in list(self.cells):
            if sentence_cell == cell:
                #print("safe cell removed from sentence ")
                self.cells.remove(sentence_cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1)
        self.moves_made.add(cell)

        # 2)
        self.mark_safe(cell)

        # 3)
        neighbor_cells = set() # undetermined neighbor cells
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if 0 <= i < self.height and 0 <= j < self.width:
                    active_cell = (i,j)
                    if active_cell in self.safes:
                        continue
                    elif active_cell in self.mines:
                        count -=1
                    else: # undetermined yet
                        neighbor_cells.add(active_cell)
        self.knowledge.append(Sentence(neighbor_cells,count))

        changes_maded = True

        while changes_maded:
            #print(self.knowledge)
            changes_maded = False

            # 4)
            for sentence in list(self.knowledge):
                if not len(sentence.cells):
                    self.knowledge.remove(sentence)
            
                k_safes = sentence.known_safes();
                if k_safes:
                    changes_maded = True
                    self.knowledge.remove(sentence)
                    for cell_ in list(k_safes):
                        self.mark_safe(cell_)

                k_mines = sentence.known_mines();
                if k_mines:
                    changes_maded = True
                    self.knowledge.remove(sentence)
                    for cell_ in list(k_mines):
                        self.mark_mine(cell_)
            

            # 5)
            for sentence_out in list(self.knowledge):
                for sentence_in in list(self.knowledge):
                    if sentence_in == sentence_out:
                        continue
                    else:
                        if( len(sentence_in.cells) > len(sentence_out.cells) ): 
                            sentence_in,sentence_out = sentence_out,sentence_in
                        if sentence_in.cells.issubset(sentence_out.cells) :
                            new_sentence = Sentence(sentence_out.cells.difference(sentence_in.cells),sentence_out.count-sentence_in.count)
                            if new_sentence.cells and new_sentence not in self.knowledge:
                                changes_maded = True
                                self.knowledge.append(new_sentence)
            

        
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe_cell in self.safes:
            if safe_cell not in self.moves_made:
                return safe_cell
        return None        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        init_pos = (random.randrange(self.height),random.randrange(self.height))
        if init_pos not in self.moves_made and init_pos not in self.mines:
            return init_pos
        
        current_pos = ((init_pos[0]+1)%self.height,(init_pos[1]+1)%self.width)
        while current_pos != init_pos:
            if current_pos not in self.moves_made and current_pos not in self.mines:
                return current_pos
            current_pos = ((current_pos[0]+1)%self.height,(current_pos[1]+1)%self.width)
        return None

