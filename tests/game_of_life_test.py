# fsww55838@gmail.com - github - @FunkeGoodVibe
import unittest
from src.game_board import GameBoard, Pos
from src.game_of_life import cell_survives_underpopulation, count_neighbours

class TestGameOfLifeBase(unittest.TestCase):
    def setUp(self):
        self.target = Pos(1, 1)
        self.board = GameBoard(3, 3, [self.target])
    
    # neighbour positions are given relative to the target, eg above would be (-1, 0)
    def _setNeighbours(self, relative_neibours: list[Pos]) -> None:
        for neighbour in relative_neibours:
            self.board._set_cell_state(self.target+neighbour, True)

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