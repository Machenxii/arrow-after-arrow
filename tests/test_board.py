"""对核心路径判断进行自动化测试。"""

import unittest

from arrow_game import Arrow, Board


class BoardPathTest(unittest.TestCase):
    def test_clear_arrow_can_leave_board(self):
        arrow = Arrow(2, 4, "right")
        self.assertTrue(Board([arrow]).is_path_clear(arrow))

    def test_blocked_arrow_cannot_leave_board(self):
        arrow = Arrow(2, 0, "right")
        blocker = Arrow(2, 3, "up")
        self.assertFalse(Board([arrow, blocker]).is_path_clear(arrow))

    def test_all_four_directions_at_edge(self):
        arrows = [
            Arrow(0, 2, "up"),
            Arrow(4, 2, "down"),
            Arrow(2, 0, "left"),
            Arrow(2, 4, "right"),
        ]
        board = Board(arrows)
        for arrow in arrows:
            with self.subTest(direction=arrow.direction):
                self.assertTrue(board.is_path_clear(arrow))

    def test_remove_changes_board_state(self):
        arrow = Arrow(1, 1, "up")
        board = Board([arrow])
        board.remove(arrow)
        self.assertEqual(board.arrows, [])


if __name__ == "__main__":
    unittest.main()
