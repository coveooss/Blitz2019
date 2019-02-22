import unittest

from challenges.water.water import solve_water
from challenges.water.water import generate_problem


class TestWaterChallengeTests(unittest.TestCase):
    def test_staircase_right(self):
        water = solve_water([5, 4, 3, 2, 1])

        self.assertEqual(water, 0)

    def test_staircase_left(self):
        water = solve_water([1, 2, 3, 4, 5])

        self.assertEqual(water, 0)

    def test_flat(self):
        water = solve_water([0, 0, 0, 0])

        self.assertEqual(water, 0)

    def test_one_pond(self):
        water = solve_water([4, 3, 2, 4])

        self.assertEqual(water, 3)

    def test_multiple_ponds(self):
        water = solve_water([4, 3, 2, 4, 1, 3, 2, 1, 2])

        self.assertEqual(water, 6)

    def test_multiple_ponds_with_greater_left_max(self):
        water = solve_water([5, 3, 2, 4, 1, 3, 2, 1, 2])

        self.assertEqual(water, 6)

    def test_multiple_ponds_with_greater_right_max(self):
        water = solve_water([4, 3, 2, 4, 1, 3, 2, 1, 6])

        self.assertEqual(water, 12)

    def test_multiple_ponds_with_greater_middle_max(self):
        water = solve_water([4, 3, 2, 9, 1, 3, 2, 1, 2])

        self.assertEqual(water, 6)

    def test_multiple_ponds_with_end_in_staircase(self):
        water = solve_water([4, 3, 2, 3, 1, 3, 2, 1, 0])

        self.assertEqual(water, 3)

    def test_multiple_ponds_with_beginning_in_staircase(self):
        water = solve_water([0, 1, 3, 2, 3, 1, 3])

        self.assertEqual(water, 3)

    def test_w_shape(self):
        water = solve_water([5, 4, 3, 0, 3, 0, 3, 4, 5])

        self.assertEqual(water, 18)

    def test_should_generate_expected_amount_of_problems(self):
        problems = generate_problem(15)[0]
        self.assertGreaterEqual(len(problems), 15)


if __name__ == '__main__':
    unittest.main()
