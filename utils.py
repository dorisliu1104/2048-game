import random
class Board:
    BOARD_SIZE = 4
    def __init__(self):
        self.board = [[None] * Board.BOARD_SIZE for _ in range(Board.BOARD_SIZE)]

    def get_cell(self, i, j):
        return self.board[i][j]
    
    def is_cell_empty(self, i, j):
        return not self.board[i][j]
    
    def set_cell(self, i, j, val):
        self.board[i][j] = val
    
    def swap(self, i1, j1, i2, j2):
        self.board[i1][j1], self.board[i2][j2] = self.board[i2][j2], self.board[i1][j1]
    
    def get_random_empty_cell(self):
        empty_cells = self._find_all_empty_cells()
        if not empty_cells:
            return None
        i = random.randint(0, len(empty_cells) - 1)
        return empty_cells[i]

    def _find_all_empty_cells(self):
        return [(i, j) for i in range(Board.BOARD_SIZE) for j in range(Board.BOARD_SIZE) if self.board[i][j] == None]

    def to_string(self):
        result = ''
        for l in self.board:
            result += str(l) + '\n'
        return result
    
    def flip_board(self):
        self.board = [l[::-1] for l in self.board]
        return self
    
    def transpose(self):
        self.board = [list(t) for t in list(zip(*self.board))]
        return self


class Game:
    DEFAULT_VAL = 2
    ALLOWED_DIRECTIONS = {'w', 'a', 's', 'd'}
    def __init__(self):
        self.board = Board()
        self._set_up_board()
        self._end = False

    def start(self):
        print(
            f'\n\nWelcome to Doris\' 2048 Game!!! Your initial board is: \n'
        )
        self.print_board()
    
        while not self._end:
            direction = self._get_user_input()
            if direction == 'w':
                self.board.transpose()
                self._move_left()
                self.board.transpose()
            elif direction == 'a':
                self._move_left()
            elif direction == 's':
                self.board.transpose().flip_board()
                self._move_left()
                self.board.transpose().flip_board()
            elif direction == 'd':
                self.board.flip_board()
                self._move_left()
                self.board.flip_board()
            if not self._set_random_cell():
                self._end = True 
                self._game_end_with_failure()
            self.print_board()
            
    def print_board(self):
        print(self.board.to_string())
    
    def _set_random_cell(self):
        p1 = self.board.get_random_empty_cell()
        if not p1:
            return False
        self.board.set_cell(*p1, Game.DEFAULT_VAL) 
        return True
    
    def _compress(self, row_num):
        for col_num in range(Board.BOARD_SIZE):
            pos = col_num
            while self.board.get_cell(row_num, pos) != None \
                and pos - 1 >= 0 and self.board.get_cell(row_num, pos - 1) == None:
                self.board.swap(row_num, pos, row_num, pos - 1)
                pos -= 1
    
    def _merge(self, row_num):
        for col_num in range(Board.BOARD_SIZE - 1):
            curr_cell = self.board.get_cell(row_num, col_num)
            if curr_cell != None \
                and self.board.get_cell(row_num, col_num + 1) == curr_cell:
                self.board.set_cell(row_num, col_num, curr_cell * 2)
                self.board.set_cell(row_num, col_num + 1, None)
    
    def _move_left(self):
        for row_num in range(Board.BOARD_SIZE):
            self._compress(row_num)
            self._merge(row_num)
            self._compress(row_num)
        

    def _set_up_board(self):
        self._set_random_cell()
        self._set_random_cell()
    
    def _get_user_input(self):
        direction = input('Enter the direction that you would like, followed by enter key. \nValid inputs: \'w\', \'a\', \'s\', or \'d\'\n\n'
        )
        while direction not in Game.ALLOWED_DIRECTIONS:
            direction = input("Invalid direction. Retry: \n\n")
        
        return direction
    
    def _game_end_with_success(self):
        pass

    def _game_end_with_failure(self):
        pass
    


