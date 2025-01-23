# fsww55838@gmail.com - github - @FunkeGoodVibe

import unittest
from src.game_of_life import cell_survives_underpopulation, count_neighbours

class TestUnderpopulation(unittest.TestCase):
    def test_zero_neighbours(self):
        test_screen = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
        target_is_alive = cell_survives_underpopulation(test_screen, 1, 1)
        self.assertFalse(target_is_alive)

    def test_one_neighbour_0(self):
        test_screen = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
        target_is_alive = cell_survives_underpopulation(test_screen, 1, 1)
        self.assertFalse(target_is_alive)

    def test_two_neighbours_0_1(self):
        test_screen = [
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
        target_is_alive = cell_survives_underpopulation(test_screen, 1, 1)
        self.assertTrue(target_is_alive)

    def test_two_neighbours_0_2(self):
        test_screen = [
            [1, 0, 1],
            [0, 1, 0],
            [0, 0, 0],
        ]
        target_is_alive = cell_survives_underpopulation(test_screen, 1, 1)
        self.assertTrue(target_is_alive)

    def test_two_neighbours_0_8(self):
        test_screen = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ]
        target_is_alive = cell_survives_underpopulation(test_screen, 1, 1)
        self.assertTrue(target_is_alive)

class TestCountNeighbours(unittest.TestCase):
    def test_zero_neighbours_dead_cell(self):
        test_screen = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.assertTrue(count_neighbours(test_screen, 1, 1) == 0)

    def test_zero_neighbours_live_cell(self):
        test_screen = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
        self.assertTrue(count_neighbours(test_screen, 1, 1) == 0)

    def test_one_neighbours_0_live_cell(self):
        test_screen = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
        self.assertTrue(count_neighbours(test_screen, 1, 1) == 1)


    def test_one_neighbours_1_0_live_cell(self):
        test_screen = [
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
        self.assertTrue(count_neighbours(test_screen, 1, 1) == 2)