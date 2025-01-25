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

def cell_meets_reproduction_requirements(board: GameBoard, pos: Pos) -> bool:
    return count_neighbours(board, pos) == 3

def perform_game_step_iteration(board: GameBoard) -> GameBoard:
    new_board = board.deepCopy()
    for row in range(board.get_rows()):
        for col in range(board.get_cols()):
            curr_cell_pos = Pos(row, col)
            if board.get_cell_state_at_pos(curr_cell_pos): # alive
                if not (cell_survives_underpopulation(board, curr_cell_pos) and 
                        cell_survives_overpopulation(board, curr_cell_pos)):
                    new_board.set_cell_state(curr_cell_pos, False)
            elif cell_meets_reproduction_requirements(board, curr_cell_pos): #dead
                new_board.set_cell_state(curr_cell_pos, True)
    return new_board

def main():
    print("Welcome to the game of life")
    rows = int(input("enter screen rows: "))
    cols = int(input("enter screen cols: "))
    board  = GameBoard(rows, cols)
    board.print()
    print("Available commands:")
    print("- Send a list of coordinates to toggle state: (1,2), (3,5), (3,3)")
    print("- Continue to next itteration: just submit enter")
    print("- Close program: x")
    while True:
        action = input("Enter a command: ")
        if action == "x":
            return
        elif action == "":
            board = perform_game_step_iteration(board)
            board.print()
        elif "(" in action:
            try:
                coordinates = action.split("(")
                print(coordinates)
                cells_to_toggle = []
                for coord in coordinates:
                    if "," in coord:
                        print(coord)
                        row = int(coord.split(",")[0])
                        col = int(coord.split(",")[1].split(")")[0])
                        cells_to_toggle.append(Pos(row, col))
                for cell in cells_to_toggle:
                    board.set_cell_state(cell, not board.get_cell_state_at_pos(cell))
                board.print()
            except:
                print(f"coordinates were not formatted correctly, format like this: (1,2), (3,5), (3,3)")
        else:
            print(f"command '{action}' is not recognsied :(")
            
if __name__ == "__main__":
    main()