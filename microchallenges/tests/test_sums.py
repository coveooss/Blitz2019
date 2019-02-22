import unittest

from challenges.subsetsum.subsetsum import compute_answer_for_array


class TestSumsChallengeTests(unittest.TestCase):
    def test_simple_problem(self):
        possible = compute_answer_for_array([1, 2, 3], 5)
        self.assertTrue(possible)

    def test_impossible_problem(self):
        possible = compute_answer_for_array([1, 2, 3], 7)
        self.assertFalse(possible)

        possible = compute_answer_for_array([1, 2, 3, 10], 7)
        self.assertFalse(possible)

        possible = compute_answer_for_array([0], 7)
        self.assertFalse(possible)

    def test_duplicate_number(self):
        possible = compute_answer_for_array([1, 3, 3], 6)
        self.assertTrue(possible)

        possible = compute_answer_for_array([1, 1, 1, 1, 1, 1], 6)
        self.assertTrue(possible)

    def test_solution_with_self(self):
        possible = compute_answer_for_array([1, 3, 6], 6)
        self.assertTrue(possible)

    def test_multiple_solution(self):
        possible = compute_answer_for_array([1, 3, 3, 6, 6], 6)
        self.assertTrue(possible)


if __name__ == '__main__':
    unittest.main()
