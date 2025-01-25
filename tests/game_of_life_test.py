# fsww55838@gmail.com - github - @FunkeGoodVibe
import unittest
import copy
import itertools
from src.game_board import GameBoard, Pos
from src.game_of_life import cell_survives_underpopulation, cell_survives_overpopulation, dead_cell_lives_by_reproduction, count_neighbours

class TestGameOfLifeBase(unittest.TestCase):
    def setUp(self):
        self.target = Pos(1, 1)
        self.board = GameBoard(3, 3, [self.target])
        self.rel_neighbour_positions = [
            Pos(-1, -1), Pos(-1, 0), Pos(-1, 1),
            Pos(0, -1),              Pos(0, 1),
            Pos(1, -1),  Pos(1, 0),  Pos(1, 1),
        ]

    # neighbour positions are given relative to the target, eg above would be (-1, 0)
    def _setNeighbours(self, relative_neibours: list[Pos]) -> None:
        for neighbour in relative_neibours:
            self.board._set_cell_state(self.target+neighbour, True)
    
    # gets possible combinations of neighbour positions relative to the target, can be used for an exauhstive test
    def _getAllRelNeighbourPositionNeighbourCombinations(self) -> list[list[Pos]]:
        combinations = []
        for combination_length in range(len(self.rel_neighbour_positions)+1):
            for neighbour_combination in itertools.combinations(self.rel_neighbour_positions, combination_length):
                combinations.append(neighbour_combination)
        return combinations

class TestCountNeighbours(TestGameOfLifeBase):
    def test_zero_neighbours_dead_cell(self):
        # deactivate the target for this test
        self.board._set_cell_state(self.target, False)
        self.assertEqual(count_neighbours(self.board, self.target), 0)

    def test_zero_neighbours_live_cell(self):
        self.assertEqual(count_neighbours(self.board, self.target), 0)

    def test_one_neighbours_0_live_cell(self):
        self._setNeighbours([Pos(-1, -1)])
        self.assertEqual(count_neighbours(self.board, self.target), 1)

    def test_one_neighbours_0_1_live_cell(self):
        self._setNeighbours([Pos(-1, -1), Pos(-1, 0)])
        self.assertEqual(count_neighbours(self.board, self.target), 2)

    def test_catch_all(self):
        for neighbours_to_set_alive in self._getAllRelNeighbourPositionNeighbourCombinations():
            self.board.clear()
            self._setNeighbours(neighbours_to_set_alive)
            self.assertEqual(count_neighbours(self.board, self.target), len(neighbours_to_set_alive), f"target dead, neighbours alive = {neighbours_to_set_alive}, board = {self.board._board}")
            self.board._set_cell_state(self.target, True)
            self.assertEqual(count_neighbours(self.board, self.target), len(neighbours_to_set_alive), f"target alive, neighbours alive  = {neighbours_to_set_alive}, board = {self.board._board}")

class TestUnderpopulation(TestGameOfLifeBase):        
    def test_zero_neighbours(self):
        self.assertFalse(cell_survives_underpopulation(self.board, self.target))

    def test_one_neighbour_0(self):
        self._setNeighbours([Pos(-1, -1)])
        self.assertFalse(cell_survives_underpopulation(self.board, self.target))

    def test_two_neighbours_0_1(self):
        self._setNeighbours([Pos(-1, -1), Pos(-1, 0)])
        self.assertTrue(cell_survives_underpopulation(self.board, self.target))

    def test_two_neighbours_0_2(self):
        self._setNeighbours([Pos(-1, -1), Pos(-1, 1)])
        self.assertTrue(cell_survives_underpopulation(self.board, self.target))

    def test_two_neighbours_0_8(self):
        self._setNeighbours([Pos(-1, -1), Pos(1, 1)])
        self.assertTrue(cell_survives_underpopulation(self.board, self.target))
    
    def test_three_neighbours_0_1_7(self):
        self._setNeighbours([Pos(-1, -1), Pos(-1, 0), Pos(1, 0)])
        self.assertTrue(cell_survives_underpopulation(self.board, self.target))

    def test_catch_all(self):
        for neighbours_to_set_alive in self._getAllRelNeighbourPositionNeighbourCombinations():
            self.board.clear()
            self.board._set_cell_state(self.target, True)
            self._setNeighbours(neighbours_to_set_alive)
            if len(neighbours_to_set_alive) >= 2:
                self.assertTrue(cell_survives_underpopulation(self.board, self.target))
            else:
                self.assertFalse(cell_survives_underpopulation(self.board, self.target))

class TestOverpopulation(TestGameOfLifeBase):
    def test_zero_neighbours(self):
        self.assertTrue(cell_survives_overpopulation(self.board, self.target))
    
    def test_one_neighbour_0(self):
        self._setNeighbours([Pos(-1, -1)])
        self.assertTrue(cell_survives_overpopulation(self.board, self.target))

    def test_four_neighbours_0_1_2_3(self):
        self._setNeighbours([Pos(-1, -1), Pos(-1, 0), Pos(-1, 1), Pos(0, -1)])
        self.assertFalse(cell_survives_overpopulation(self.board, self.target))

    def test_five_neighbours_0_1_2_3(self):
        self._setNeighbours([Pos(-1, -1), Pos(-1, 0), Pos(-1, 1), Pos(0, -1), Pos(1, 1)])
        self.assertFalse(cell_survives_overpopulation(self.board, self.target))

    def test_catch_all(self):
        for neighbours_to_set_alive in self._getAllRelNeighbourPositionNeighbourCombinations():
            self.board.clear()
            self.board._set_cell_state(self.target, True)
            self._setNeighbours(neighbours_to_set_alive)
            if len(neighbours_to_set_alive) <= 3:
                self.assertTrue(cell_survives_overpopulation(self.board, self.target))
            else:
                self.assertFalse(cell_survives_overpopulation(self.board, self.target))
