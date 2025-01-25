from dataclasses import dataclass

@dataclass
class Pos:
    row: int
    col: int

    def __add__(self, other: 'Pos'):
        return Pos(self.row+other.row, self.col+other.col)

# game board is used to isolate the game functionality from the board and screen implementation
# a future user interface can read the baord's state to udpate the interface, or inherit from this 
class GameBoard:
    def __init__(self, rows: int = 0, cols: int = 0, live_cells: list[Pos] = []) -> None:
        self._rows = rows
        self._cols = cols
        self._board = [[0 for _ in range(cols)] for _ in range(rows)]
        for live_cell in live_cells:
            if self._is_inside_board(live_cell):
                self._set_cell_state(live_cell, True)

    def __eq__(self, other: 'GameBoard') -> bool:
        if self._rows != other._rows:
            return False
        if self._cols != other._cols:
            return False
        for row in range(self._rows):
            for col in range(self._cols):
                if self._board[row][col] != other._board[row][col]:
                    return False
        return True

    def _is_inside_board(self, Pos: Pos) -> bool:
        return (Pos.row < self._rows and
                Pos.row >= 0 and
                Pos.col < self._cols and
                Pos.col >= 0)
    
    def _set_cell_state(self, Pos: Pos, alive: bool) -> None:
        if self._is_inside_board(Pos):
            self._board[Pos.row][Pos.col] = 1 if alive else 0

    # returns true if alive, false if dead or off the board
    def get_cell_state_at_pos(self, Pos: Pos) -> bool:
        if self._is_inside_board(Pos):
            return self._board[Pos.row][Pos.col] == 1
        return False

    def clear(self) -> None:
        self._board = [[0 for _ in range(self._cols)] for _ in range(self._rows)]
    
    def print(self) -> None:
        print("GAME OF LIFE BOARD")
        for row in self._board:
            print(row)
