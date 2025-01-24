from dataclasses import dataclass

@dataclass
class Coordinate:
    row: int
    col: int

    def __add__(self, other):
        return Coordinate(self.row+other.row, self.col+other.col)

# game board is used to isolate the game functionality from the board and screen implementation
# a future user interface can read the baord's state to udpate the interface, or inherit from this 
class GameBoard:
    def __init__(self, rows: int = 0, cols: int = 0, live_cells: list[Coordinate] = []) -> None:
        self._rows = rows
        self._cols = cols
        self._board = [[0 for col in range cols] for row in range rows]
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

    def _is_inside_board(self, coordinate: Coordinate) -> bool:
        return (coordinate.row < self._rows and
                coordinate.row >= 0 and
                coordinate.col < self._cols and
                coordinate.col >= 0)
    
    def _set_cell_state(self, coordinate: Coordinate, alive: bool) -> None:
        if self._is_inside_board(coordinate):
            self._board[coordinate.row][coordinate.col] = 1 if alive else 0

    # returns true if alive, false if dead 
    def get_cell_state_at_pos(self, coordinate: Coordinate) -> bool:
        if self._is_inside_board(coordinate):
            return self._board[coordinate.row][coordinate.col] == 1
        return False

    def get_cell_state_at_pos(self, row: int, col: int) -> bool:
        coordinate = Coordinate(row, col)
        return self.get_cell_state_at_pos(coordinate)
    
    def print_board(self) -> None:
        print("GAME OF LIFE BOARD")
        for row in self._board:
            print(row)
