# fsww55838@gmail.com - github - @FunkeGoodVibe
import unittest
import copy
import itertools
from src.game_board import GameBoard, Pos
from src.game_of_life import cell_survives_underpopulation, cell_survives_overpopulation, cell_meets_reproduction_requirements, count_neighbours, perform_game_step_iteration

class TestGameOfLifeRuleBase(unittest.TestCase):
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
            self.board.set_cell_state(self.target+neighbour, True)
    
    # gets possible combinations of neighbour positions relative to the target, can be used for an exauhstive test
    def _getAllRelNeighbourPositionNeighbourCombinations(self) -> list[list[Pos]]:
        combinations = []
        for combination_length in range(len(self.rel_neighbour_positions)+1):
            for neighbour_combination in itertools.combinations(self.rel_neighbour_positions, combination_length):
                combinations.append(neighbour_combination)
        return combinations

class TestCountNeighbours(TestGameOfLifeRuleBase):
    def test_zero_neighbours_dead_cell(self):
        # deactivate the target for this test
        self.board.set_cell_state(self.target, False)
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
            self.board.set_cell_state(self.target, True)
            self.assertEqual(count_neighbours(self.board, self.target), len(neighbours_to_set_alive), f"target alive, neighbours alive  = {neighbours_to_set_alive}, board = {self.board._board}")

class TestUnderpopulation(TestGameOfLifeRuleBase):        
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
            self.board.set_cell_state(self.target, True)
            self._setNeighbours(neighbours_to_set_alive)
            if len(neighbours_to_set_alive) >= 2:
                self.assertTrue(cell_survives_underpopulation(self.board, self.target))
            else:
                self.assertFalse(cell_survives_underpopulation(self.board, self.target))

class TestOverpopulation(TestGameOfLifeRuleBase):
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
            self.board.set_cell_state(self.target, True)
            self._setNeighbours(neighbours_to_set_alive)
            if len(neighbours_to_set_alive) <= 3:
                self.assertTrue(cell_survives_overpopulation(self.board, self.target))
            else:
                self.assertFalse(cell_survives_overpopulation(self.board, self.target))

class TestReproduction(TestGameOfLifeRuleBase):
    def test_zero_neighbours(self):
        self.assertFalse(cell_meets_reproduction_requirements(self.board, self.target))

    def test_one_neighbour_0(self):
        self._setNeighbours([Pos(-1, -1)])
        self.assertFalse(cell_meets_reproduction_requirements(self.board, self.target))

    def test_three_neighbours_0_1_2_3(self):
        self._setNeighbours([Pos(-1, -1), Pos(-1, 0), Pos(-1, 1)])
        self.assertTrue(cell_meets_reproduction_requirements(self.board, self.target))

    def test_five_neighbours_0_1_2_3(self):
        self._setNeighbours([Pos(-1, -1), Pos(-1, 0), Pos(-1, 1), Pos(0, -1), Pos(1, 1)])
        self.assertFalse(cell_meets_reproduction_requirements(self.board, self.target))

    def test_catch_all(self):
        for neighbours_to_set_alive in self._getAllRelNeighbourPositionNeighbourCombinations():
            self.board.clear()
            self.board.set_cell_state(self.target, True)
            self._setNeighbours(neighbours_to_set_alive)
            if len(neighbours_to_set_alive) == 3:
                self.assertTrue(cell_meets_reproduction_requirements(self.board, self.target))
            else:
                self.assertFalse(cell_meets_reproduction_requirements(self.board, self.target))

class TestGameStepIteration(unittest.TestCase):
    def _compare_board_to_target_pattern(self, board: GameBoard, pattern: list[Pos]) -> None:
        # validates that the board matches the pattern given (a list of cells which should be alive)
        for row in range(5):
            for col in range(5):
                target = Pos(row, col)
                if target in pattern:
                    self.assertTrue(board.get_cell_state_at_pos(target), f"cell {row, col} should be alive")
                else:
                    self.assertFalse(board.get_cell_state_at_pos(target), f"cell {row, col} should be dead")

    def test_single_cell_dies(self):
        cell_pos = Pos(2, 2)
        board_before = GameBoard(5, 5, [cell_pos])
        board_after = perform_game_step_iteration(board_before)
        cell_is_alive = board_after.get_cell_state_at_pos(cell_pos)
        self.assertFalse(cell_is_alive)
        
    def test_block_pattern(self):
        # The block pattern is a pattern that does not grow or die https://conwaylife.com/wiki/Block
        cell_positions = [
            Pos(1, 1), Pos(1, 2), 
            Pos(2, 1), Pos(2, 2), 
        ]
        board_before = GameBoard(5, 5, cell_positions)
        board_after = perform_game_step_iteration(board_before)
        self._compare_board_to_target_pattern(board_after, cell_positions)

    def test_blinker_pattern(self):
        # pattern that oscillates: https://conwaylife.com/wiki/Blinker
        # it oscilates between the two patterns seen here
        cell_position_vertical = [
            Pos(2, 2),
            Pos(3, 2),
            Pos(4, 2)
        ]
        cell_position_horizontal = [
            Pos(3, 1), Pos(3, 2), Pos(3, 3)
        ]
        patterns = [cell_position_vertical, cell_position_horizontal]
        for starting_index in range(2):
            starting_pattern = patterns[starting_index]
            target_pattern = patterns[1-starting_index]
            board_before = GameBoard(5, 5, starting_pattern)
            board_before.print()
            board_after = perform_game_step_iteration(board_before)
            board_after.print()
            self._compare_board_to_target_pattern(board_after, target_pattern)

    def test_glider_pattern(self):
        # pattern that moves down the screen indefinitely: https://conwaylife.com/wiki/Glider
        glider_pos_one = [
                       Pos(1, 2),
                                  Pos(2, 3),
            Pos(3, 1), Pos(3, 2), Pos(3, 3)
        ]
        glider_pos_two = [

            Pos(2, 1),            Pos(2, 3),
                       Pos(3, 2), Pos(3, 3),
                       Pos(4, 2),      
        ]
        glider_pos_three = [
            
                                  Pos(2, 3),
            Pos(3, 1),            Pos(3, 3),
                       Pos(4, 2), Pos(4, 3)   
        ]
        glider_pos_four = [
             
                       Pos(2, 2),                 
                                  Pos(3, 3), Pos(3, 4),
                       Pos(4, 2), Pos(4, 3)   
        ]
        glider_pos_five = [
             
                                  Pos(2, 3),                 
                                             Pos(3, 4),
                       Pos(4, 2), Pos(4, 3), Pos(4, 4)   
        ]
        patterns = [glider_pos_one, glider_pos_two, glider_pos_three, glider_pos_four, glider_pos_five]
        for glider_iteration in range(4):
            starting_pattern = patterns[glider_iteration]
            target_pattern = patterns[glider_iteration+1]
            board_before = GameBoard(7, 7, starting_pattern)
            board_after = perform_game_step_iteration(board_before)
            self._compare_board_to_target_pattern(board_after, target_pattern)
