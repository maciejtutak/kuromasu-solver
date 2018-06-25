import unittest

from kuromasu import Kuromasu



class KuromasuPrepTest(unittest.TestCase):
    """Check basic class methods and helpers."""
    BOARD = [
        ['0', '0', '2'],
        ['4', '0', '0'],
        ['0', '0', '0'],
    ]

    BOARD_PADDED = [
        ['x', 'x', 'x', 'x', 'x'],
        ['x', '0', '0', '2', 'x'],
        ['x', '4', '0', '0', 'x'],
        ['x', '0', '0', '0', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
    ]
     
    game = Kuromasu(BOARD)

    def test_init(self):
        self.assertIsInstance(
            self.game,
            Kuromasu,
        )

    def test_str(self):
        self.assertEqual(
            self.game.__str__(),
            '0 0 2\n4 0 0\n0 0 0',
        )

    def test_create_padding(self):
        self.game.create_padding()

        self.assertEqual(
            self.game.board,
            self.BOARD_PADDED,
        )
    
class KuromasuSolvedTest(unittest.TestCase):
    """Check if is_solved succeeds."""
    BOARD_SOLVED = [
        ['x', 'x', 'x', 'x', 'x'],
        ['x', '0', '#', '2', 'x'],
        ['x', '4', '0', '0', 'x'],
        ['x', '#', '0', '#', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
    ]

    game = Kuromasu(BOARD_SOLVED)

    def test_is_solved(self):
        self.assertTrue(self.game.is_solved())

    def test_check_white_cells_visible_from_numbers(self):
        self.assertTrue(self.game.check_white_cells_visible_from_numbers())

    def test_get_number_cells(self):
        self.assertEqual(
            self.game.get_number_cells(),
            [(1, 3), (2, 1)],
        )

    def test_count_white_cells_visible_from_number(self):
        self.assertEqual(
            self.game.count_white_cells_visible_from_number((2, 1)),
            4,
        )

    def test_check_all_white_cells_accessible(self):
        self.assertTrue(self.game.check_all_white_cells_accessible())


    def test_get_first_white_cell(self):
        self.assertEqual(
            self.game.get_first_white_cell(),
            (1, 1),
        )

    def test_get_neighboring_white_cells(self):
        self.assertEqual(
            self.game.get_neighboring_white_cells((2, 1)),
            [(1, 1), (2, 2)],
        )

    def test_count_cells_total(self):
        self.assertEqual(
            self.game.count_cells_total(),
            9,
        )

    def test_count_black_cells_total(self):
        self.assertEqual(
            self.game.count_black_cells_total(),
            3,
        )

    def test_check_black_cells_separate(self):
        self.assertTrue(self.game.check_black_cells_separate())

    def test_get_black_cells(self):
        self.assertTrue(
            self.game.get_black_cells(),
            [(1, 2), (3, 1), (3, 3)],
        )

class KuromasuFailedTest(unittest.TestCase):
    """Check if is_solved fails."""
    BOARD_FAILED = [
        ['x', 'x', 'x', 'x', 'x'],
        ['x', '0', '0', '2', 'x'],
        ['x', '4', '0', '#', 'x'],
        ['x', '#', '#', '0', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
    ]
    
    game = Kuromasu(BOARD_FAILED)

    def test_is_solved_fail(self):
        self.assertFalse(self.game.is_solved())

    def test_check_white_cells_visible_from_numbers_fail(self):
        self.assertFalse(self.game.check_white_cells_visible_from_numbers())

    def test_count_white_cells_visible_from_number_fail(self):
        self.assertNotEqual(
            self.game.count_white_cells_visible_from_number((2, 1)),
            4,
        )

    def test_check_all_white_cells_accessible_fail(self):
        self.assertFalse(self.game.check_all_white_cells_accessible())

    def test_get_neighboring_white_cells_fail(self):
        self.assertNotEqual(
            self.game.get_neighboring_white_cells((2, 1)),
            [(1, 1), (2, 2), (3, 1)],
        )

    def test_check_black_cells_separate_fail(self):
        self.assertFalse(self.game.check_black_cells_separate())


class KuromasuStatesTest(unittest.TestCase):
    """Check if get_new_states generates states correctly."""
    BOARD_S0 = [
        ['x', 'x', 'x', 'x', 'x'],
        ['x', '0', '#', '2', 'x'],
        ['x', '4', '0', '0', 'x'],
        ['x', '0', '0', '0', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
    ]

    BOARD_S1 = [
        ['x', 'x', 'x', 'x', 'x'],
        ['x', '#', '#', '2', 'x'],
        ['x', '4', '0', '0', 'x'],
        ['x', '0', '0', '0', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
    ]

    BOARD_S2 = [
        ['x', 'x', 'x', 'x', 'x'],
        ['x', '0', '#', '2', 'x'],
        ['x', '4', '#', '0', 'x'],
        ['x', '0', '0', '0', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
    ]
    
    BOARD_S3 = [
        ['x', 'x', 'x', 'x', 'x'],
        ['x', '0', '#', '2', 'x'],
        ['x', '4', '0', '#', 'x'],
        ['x', '0', '0', '0', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
    ]

    BOARD_S4 = [
        ['x', 'x', 'x', 'x', 'x'],
        ['x', '0', '#', '2', 'x'],
        ['x', '4', '0', '0', 'x'],
        ['x', '#', '0', '0', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
    ]

    BOARD_S5 = [
        ['x', 'x', 'x', 'x', 'x'],
        ['x', '0', '#', '2', 'x'],
        ['x', '4', '0', '0', 'x'],
        ['x', '0', '#', '0', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
    ]

    BOARD_S6 = [
        ['x', 'x', 'x', 'x', 'x'],
        ['x', '0', '#', '2', 'x'],
        ['x', '4', '0', '0', 'x'],
        ['x', '0', '0', '#', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
    ]

    game_1 = Kuromasu(BOARD_S0)

    def test_get_new_states_1(self):
        self.assertEqual(
            self.game_1.get_new_states(),
            [ 
                Kuromasu(self.BOARD_S1, self.game_1),
                Kuromasu(self.BOARD_S2, self.game_1),
                Kuromasu(self.BOARD_S3, self.game_1),
                Kuromasu(self.BOARD_S4, self.game_1),
                Kuromasu(self.BOARD_S5, self.game_1),
                Kuromasu(self.BOARD_S6, self.game_1),
            ]
        )

    game_2 = Kuromasu(BOARD_S2)
    
    def test_get_new_states_2(self):
        self.assertEqual(
            len(self.game_2.get_new_states()),
            5,
        )
    
    BOARD_SX = [
        ['x', 'x', 'x', 'x', 'x'],
        ['x', '0', '#', '2', 'x'],
        ['x', '4', '#', '#', 'x'],
        ['x', '#', '#', '#', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
    ]
    
    game_3 = Kuromasu(BOARD_SX)

    def test_get_new_states_3(self):
        self.assertEqual(
            len(self.game_3.get_new_states()),
            1,
        )

    game_4 = Kuromasu(BOARD_S6)

    def test_h_1(self):
        self.assertEqual(
            self.game_4.h(),
            1,
        )

    def test_h_2(self):
        self.assertEqual(
            self.game_1.h(),
            2,
        )

if __name__ == "__main__":
    unittest.main()
