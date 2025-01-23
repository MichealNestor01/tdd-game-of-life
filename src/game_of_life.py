# rules

# inital implementation of underpopulation rule
def cell_survives_underpopulation(screen: list[list[int]], r: int, c: int) -> bool:
    if screen[r-1][c-1] == 1 and screen[r-1][c] == 1:
        return True
    if screen[r-1][c-1] == 1 and screen[r-1][c+1] == 1:
        return True
    if screen[r-1][c-1] == 1 and screen[r+1][c+1] == 1:
        return True
    return False

# refactor after count neighbours has been implemented and tested
# def cell_survives_underpopulation(screen: list[list[int]], r: int, c: int) -> bool:
#     return count_neighbours(screen, r, c) >= 2

def count_neighbours(screen: list[list[int]], r: int, c: int) -> bool:
    count = 0
    for row_offset in range(-1, 2):
        for col_offset in range(-1, 2):
            if (screen[r+row_offset][c+col_offset] == 1 and
                not (row_offset == 0 and col_offset == 0)):
                count += 1
    return count

# setup functions:

def show_screen(screen_array: list[list[int]]) -> None:
    for row in screen_array:
        print(row)

def main():
    test_screen = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    show_screen(test_screen)

if __name__ == "__main__":
    main()