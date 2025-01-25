from game_board import GameBoard, Pos

def count_neighbours(board: GameBoard, pos: Pos) -> bool:
    count = 0
    for neibour_pos in [
        Pos(-1, -1), Pos(-1, 0), Pos(-1, 1),
        Pos(0, -1),              Pos(0, 1),
        Pos(1, -1),  Pos(1, 0),  Pos(1, 1),
    ]:
        target_coorinate = pos + neibour_pos
        if board.get_cell_state_at_pos(target_coorinate):
            count += 1
    return count

def cell_survives_underpopulation(board: GameBoard, pos: Pos) -> bool:
    return count_neighbours(board, pos) >= 2

def cell_survives_overpopulation(board: GameBoard, pos: Pos) -> bool:
    return count_neighbours(board, pos) <= 3

def main():
    test_board = GameBoard(5, 5, [Pos(2, 2)])
    test_board.print()

if __name__ == "__main__":
    main()