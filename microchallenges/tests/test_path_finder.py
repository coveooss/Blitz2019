import unittest

from challenges.pathfinder.pathfinder import find_solution
from challenges.pathfinder.pathfinder import generate_problem


class TestPathFinderTests(unittest.TestCase):
    def test_multiple_path_same_weigth(self):
        weigth = find_solution([
            [0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0]
        ])

        self.assertEqual(weigth, 9)

    def test_multiple_path_same_weigth_2(self):
        weigth = find_solution([
            [0, 1, 5, 1, 1, 1],
            [9, 1, 1, 1, 1, 1],
            [9, 1, 1, 1, 1, 1],
            [9, 1, 1, 1, 1, 1],
            [1, 9, 1, 8, 1, 1],
            [1, 9, 1, 1, 1, 0]
        ])

        self.assertEqual(weigth, 9)

    def test_verticalline_path(self):
        weigth = find_solution([
            [0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1]
        ])

        self.assertEqual(weigth, 4)

    def test_line_path(self):
        weigth = find_solution([
            [1,  0,  3, 22, 10, 143],
            [12, 5,  5,  3, 14,  11],
            [4, 11,  3, 12,  4,   1],
            [5,  5, 10, 13,  5,   1],
            [5,  7,  9, 17,  1,   1],
            [1,  5, 12,  1,  0,   1]
        ])

        self.assertEqual(weigth, 31)

    def test_problem_generation(self):
        problems = generate_problem(15)[0]
        self.assertGreaterEqual(len(problems), 15)


if __name__ == '__main__':
    unittest.main()
