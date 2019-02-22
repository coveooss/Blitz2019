import unittest
import xmlrunner

from game.constants import PLAYER_1, PLAYER_2, PLAYER_3, PLAYER_4, MOVE, WALL_H, WALL_V
from game.board import InvalidPlayerCountError, Board


class TestBoard2Players(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_create_board_from_another_one(self):
        self.board.move_pawn((1, 1), PLAYER_1)
        self.board.move_pawn((2, 2), PLAYER_2)
        self.board.add_wall((3, 3), is_horiz=True, player=PLAYER_1)
        self.board.add_wall((4, 4), is_horiz=False, player=PLAYER_1)
        self.board.add_wall((5, 5), is_horiz=True, player=PLAYER_2)
        self.board.add_wall((6, 6), is_horiz=False, player=PLAYER_2)

        board2 = Board(self.board, len(self.board.pawns))

        self.assertEqual(2, len(board2.pawns))
        self.assertEqual(self.board.pawns, board2.pawns)
        self.assertEqual(2, len(board2.goals))
        self.assertEqual(self.board.goals, board2.goals)
        self.assertEqual(2, len(board2.player_walls))
        self.assertEqual(self.board.player_walls, board2.player_walls)
        self.assertEqual(self.board.verti_walls, board2.verti_walls)
        self.assertEqual(self.board.horiz_walls, board2.horiz_walls)

    def test_create_board_from_another_one_with_custom_starting_walls(self):
        board = Board(player_count=2, starting_walls=[3, 8])

        board2 = Board(board, len(board.pawns))

        self.assertEqual(2, len(board2.pawns))
        self.assertEqual(board.pawns, board2.pawns)
        self.assertEqual(2, len(board2.goals))
        self.assertEqual(board.goals, board2.goals)
        self.assertEqual(2, len(board2.player_walls))
        self.assertEqual(board.player_walls, board2.player_walls)
        self.assertEqual(board.verti_walls, board2.verti_walls)
        self.assertEqual(board.horiz_walls, board2.horiz_walls)

    def test_start_position(self):
        self.assertEqual((0, 4), self.board.pawns[PLAYER_1])
        self.assertEqual((8, 4), self.board.pawns[PLAYER_2])

    def test_should_not_allow_3_players(self):
        self.assertRaises(InvalidPlayerCountError, Board, None, 3)

    def test_should_not_allow_more_than_4_players(self):
        self.assertRaises(InvalidPlayerCountError, Board, None, 5)

    def test_can_move_here_works_for_all_players(self):
        self.assertTrue(self.board.can_move_here(0, 5, PLAYER_1))
        self.assertTrue(self.board.can_move_here(8, 5, PLAYER_2))

    def test_can_move_here_allow_moves_around(self):
        self.board.move_pawn((1,4), PLAYER_1)
        self.assertTrue(self.board.can_move_here(0, 4, PLAYER_1)) #up
        self.assertTrue(self.board.can_move_here(1, 3, PLAYER_1)) #left
        self.assertTrue(self.board.can_move_here(1, 5, PLAYER_1)) #right
        self.assertTrue(self.board.can_move_here(2, 4, PLAYER_1)) #down

    def test_can_move_here_disallow_move_on_yourself(self):
        self.assertFalse(self.board.can_move_here(0, 4, PLAYER_1))

    def test_can_move_here_disallow_diagonal_move(self):
        self.board.move_pawn((1, 4), PLAYER_1)
        self.assertFalse(self.board.can_move_here(2, 5, PLAYER_1))
        self.assertFalse(self.board.can_move_here(0, 5, PLAYER_1))
        self.assertFalse(self.board.can_move_here(2, 3, PLAYER_1))
        self.assertFalse(self.board.can_move_here(0, 3, PLAYER_1))

    def test_get_legal_pawn_moves(self):
        self.board.move_pawn((1,4), PLAYER_1)
        expected_moves = [(MOVE, 2, 4), (MOVE, 0, 4), (MOVE, 1, 5), (MOVE, 1, 3)]
        moves = self.board.get_legal_pawn_moves(PLAYER_1)
        self.assertEqual(expected_moves, moves)

    def test_get_legal_pawn_moves_with_player2_close(self):
        self.board.move_pawn((1,4), PLAYER_1)
        self.board.move_pawn((1,5), PLAYER_2)
        expected_moves = [(MOVE, 2, 4), (MOVE, 0, 4), (MOVE, 1, 3), (MOVE, 1, 6)] #Jump baby
        moves = self.board.get_legal_pawn_moves(PLAYER_1)
        self.assertEqual(expected_moves, moves)

    def test_get_legal_pawn_moves_with_player1_close(self):
        self.board.move_pawn((1,4), PLAYER_2)
        self.board.move_pawn((1,5), PLAYER_1)
        expected_moves = [(MOVE, 2, 4), (MOVE, 0, 4), (MOVE, 1, 3), (MOVE, 1, 6)] #Jump baby
        moves = self.board.get_legal_pawn_moves(PLAYER_2)
        self.assertEqual(expected_moves, moves)

    def test_get_legal_pawn_moves_with_wall(self):
        self.board.move_pawn((4, 4), PLAYER_1)
        self.board.add_wall((4, 3), is_horiz=False, player=PLAYER_1)
        expected_moves = [(MOVE, 5, 4), (MOVE, 3, 4), (MOVE, 4, 5)]
        moves = self.board.get_legal_pawn_moves(PLAYER_1)
        self.assertEqual(expected_moves, moves)

    def test_is_finished_at_start(self):
        self.assertFalse(self.board.is_finished())

    def test_is_finished_at_mid_game(self):
        self.board.move_pawn((3, 4), PLAYER_1)
        self.board.move_pawn((4, 4), PLAYER_2)
        self.assertFalse(self.board.is_finished())

    def test_is_finished_player_1(self):
        self.board.move_pawn((8, 4), PLAYER_1)
        self.assertTrue(self.board.is_finished())

    def test_is_finished_player_2(self):
        self.board.move_pawn((0, 4), PLAYER_2)
        self.assertTrue(self.board.is_finished())

    def test_wall_count_at_start(self):
        self.assertEqual(10, self.board.player_walls[PLAYER_1])
        self.assertEqual(10, self.board.player_walls[PLAYER_2])

    def test_move_on_other_paws_disallowed(self):
        for i in range(0, 2):
            for j in range(0, 2):
                with self.subTest(i=i, j=j):
                    self.board.move_pawn((4, 4), i)
                    self.assertFalse(self.board.can_move_here(4, 4, j))

    def test_min_steps_before_victory_at_victory_player_1(self):
        self.board.move_pawn((8, 0), PLAYER_1)
        self.assertEqual(0, self.board.get_min_steps_before_victory(PLAYER_1))

    def test_min_steps_before_victory_at_victory_player_2(self):
        self.board.move_pawn((0, 8), PLAYER_2)
        self.assertEqual(0, self.board.get_min_steps_before_victory(PLAYER_2))

    def test_min_steps_before_victory_at_start(self):
        for i in range(0, 2):
            with self.subTest(i=i):
                self.assertEqual(8, self.board.get_min_steps_before_victory(i))

    def test_clone(self):
        board2 = self.board.clone()
        self.assertEqual(self.board.pawns, board2.pawns)
        self.assertEqual(self.board.goals, board2.goals)
        self.assertEqual(self.board.player_walls, board2.player_walls)

    def test_paths_exist(self):
        #Build a cell
        for i in range(3, 6):
            self.board.horiz_walls.append((3, i))
            self.board.horiz_walls.append((5, i))
            self.board.verti_walls.append((i, 3))
            self.board.verti_walls.append((i, 5))

        #shove both player in it
        for i in range(0, 2):
            new_board = self.board.clone()
            with self.subTest(i=i):
                new_board.move_pawn((4,4), i)
                #watch them cry
                self.assertFalse(new_board.paths_exist)

    def test_is_action_valid_isnt_when_stepping_on_someone_elses_toes(self):
        self.board.move_pawn((4,3), PLAYER_1)
        self.board.move_pawn((4,4), PLAYER_2)
        self.assertFalse(self.board.is_action_valid((MOVE, 4, 4), PLAYER_1))
        self.assertFalse(self.board.is_action_valid((MOVE, 4, 3), PLAYER_2))

    def test_is_action_valid_isnt_when_moving_somewhere_random(self):
        self.board.move_pawn((4, 3), PLAYER_1)
        self.board.move_pawn((4, 4), PLAYER_2)
        self.assertFalse(self.board.is_action_valid((MOVE, 1, 1), PLAYER_1))
        self.assertFalse(self.board.is_action_valid((MOVE, 2, 2), PLAYER_2))

    def test_is_action_valid_is_when_moving_properly(self):
        self.board.move_pawn((1, 1), PLAYER_1)
        self.board.move_pawn((2, 2), PLAYER_2)
        self.assertTrue(self.board.is_action_valid((MOVE, 1, 2), PLAYER_1))
        self.assertTrue(self.board.is_action_valid((MOVE, 2, 3), PLAYER_2))

    def test_get_score_player_1_win(self):
        self.board.move_pawn((8, 0), PLAYER_1)
        self.board.move_pawn((8, 4), PLAYER_2)
        self.assertEqual(50, self.board.get_score(PLAYER_1))
        self.assertEqual(42, self.board.get_score(PLAYER_2))

    def test_get_score_player_2_win(self):
        self.board.move_pawn((0, 4), PLAYER_1)
        self.board.move_pawn((0, 0), PLAYER_2)
        self.assertEqual(42, self.board.get_score(PLAYER_1))
        self.assertEqual(50, self.board.get_score(PLAYER_2))

    def test_get_score_player_both_same_distance(self):
        self.board.move_pawn((4, 4), PLAYER_1)
        self.board.move_pawn((4, 3), PLAYER_2)
        self.assertEqual(46, self.board.get_score(PLAYER_1))
        self.assertEqual(46, self.board.get_score(PLAYER_2))

    def test_get_scores_should_order_player_by_score(self):
        self.board.move_pawn((4,4), PLAYER_1)
        self.board.move_pawn((8,4), PLAYER_2)
        player_score = self.board.get_scores()
        self.assertEqual(PLAYER_1, player_score[0][0])
        self.assertEqual(PLAYER_2, player_score[1][0])

    def test_get_scores_should_order_player_by_score_with_player_2_winning(self):
        self.board.move_pawn((0,4), PLAYER_1)
        self.board.move_pawn((4,4), PLAYER_2)
        player_score = self.board.get_scores()
        self.assertEqual(PLAYER_2, player_score[0][0])
        self.assertEqual(PLAYER_1, player_score[1][0])

    def test_get_scores_walls_should_be_tiebreaker(self):
        self.board.move_pawn((4,4), PLAYER_1)
        self.board.move_pawn((4,3), PLAYER_2)
        self.board.player_walls[PLAYER_1] = 8
        self.board.player_walls[PLAYER_2] = 2
        player_score = self.board.get_scores()
        self.assertEqual(PLAYER_1, player_score[0][0])
        self.assertEqual(PLAYER_2, player_score[1][0])

    def test_get_scores_walls_should_not_be_considered_without_tie(self):
        self.board.move_pawn((4,4), PLAYER_1)
        self.board.move_pawn((1,3), PLAYER_2)
        self.board.player_walls[PLAYER_1] = 8
        self.board.player_walls[PLAYER_2] = 2
        player_score = self.board.get_scores()
        self.assertEqual(PLAYER_2, player_score[0][0])
        self.assertEqual(PLAYER_1, player_score[1][0])

    def test_should_support_starting_wall_specification(self):
        player1_wall_count = 3
        player2_wall_count = 14
        board = Board(player_count=2, starting_walls=[player1_wall_count, player2_wall_count])
        self.assertEqual(player1_wall_count, board.player_walls[0])
        self.assertEqual(player2_wall_count, board.player_walls[1])


class TestBoard4Players(unittest.TestCase):
    def setUp(self):
        self.board = Board(player_count=4)

    def test_create_board_from_another_one(self):
        self.board.move_pawn((0, 1), PLAYER_1)
        self.board.move_pawn((0, 2), PLAYER_2)
        self.board.move_pawn((0, 2), PLAYER_3)
        self.board.move_pawn((0, 2), PLAYER_4)
        self.board.add_wall((1, 1), is_horiz=True, player=PLAYER_1)
        self.board.add_wall((1, 2), is_horiz=True, player=PLAYER_2)
        self.board.add_wall((1, 3), is_horiz=True, player=PLAYER_3)
        self.board.add_wall((1, 4), is_horiz=True, player=PLAYER_4)
        self.board.add_wall((2, 1), is_horiz=False, player=PLAYER_1)
        self.board.add_wall((3, 1), is_horiz=False, player=PLAYER_2)
        self.board.add_wall((4, 1), is_horiz=False, player=PLAYER_3)
        self.board.add_wall((5, 1), is_horiz=False, player=PLAYER_4)

        board2 = Board(self.board, len(self.board.pawns))

        self.assertEqual(4, len(board2.pawns))
        self.assertEqual(self.board.pawns, board2.pawns)
        self.assertEqual(4, len(board2.goals))
        self.assertEqual(self.board.goals, board2.goals)
        self.assertEqual(4, len(board2.player_walls))
        self.assertEqual(self.board.player_walls, board2.player_walls)
        self.assertEqual(self.board.verti_walls, board2.verti_walls)
        self.assertEqual(self.board.horiz_walls, board2.horiz_walls)

    def test_create_board_from_another_one_with_custom_starting_walls(self):
        board = Board(player_count=4, starting_walls=[1,2,3,5])

        board2 = Board(board, len(board.pawns))

        self.assertEqual(4, len(board2.pawns))
        self.assertEqual(board.pawns, board2.pawns)
        self.assertEqual(4, len(board2.goals))
        self.assertEqual(board.goals, board2.goals)
        self.assertEqual(4, len(board2.player_walls))
        self.assertEqual(board.player_walls, board2.player_walls)
        self.assertEqual(board.verti_walls, board2.verti_walls)
        self.assertEqual(board.horiz_walls, board2.horiz_walls)

    def test_start_position(self):
        self.assertEqual((0, 4), self.board.pawns[PLAYER_1])
        self.assertEqual((4, 8), self.board.pawns[PLAYER_2])
        self.assertEqual((8, 4), self.board.pawns[PLAYER_3])
        self.assertEqual((4, 0), self.board.pawns[PLAYER_4])

    def test_can_move_here_works_for_all_players(self):
        self.assertTrue(self.board.can_move_here(0, 5, PLAYER_1))
        self.assertTrue(self.board.can_move_here(4, 7, PLAYER_2))
        self.assertTrue(self.board.can_move_here(8, 5, PLAYER_3))
        self.assertTrue(self.board.can_move_here(4, 1, PLAYER_4))

    def test_can_move_here_allow_moves_around(self):
        self.board.move_pawn((4,1), PLAYER_4)
        self.assertTrue(self.board.can_move_here(4, 2, PLAYER_4)) #up
        self.assertTrue(self.board.can_move_here(3, 1, PLAYER_4)) #left
        self.assertTrue(self.board.can_move_here(5, 1, PLAYER_4)) #right
        self.assertTrue(self.board.can_move_here(4, 0, PLAYER_4)) #down

    def test_can_move_here_disallow_move_on_yourself(self):
        self.assertFalse(self.board.can_move_here(8, 4, PLAYER_3))

    def test_can_move_here_disallow_diagonal_move(self):
        self.board.move_pawn((4, 4), PLAYER_3)
        self.assertFalse(self.board.can_move_here(5, 5, PLAYER_3))
        self.assertFalse(self.board.can_move_here(3, 3, PLAYER_3))
        self.assertFalse(self.board.can_move_here(3, 5, PLAYER_3))
        self.assertFalse(self.board.can_move_here(5, 3, PLAYER_3))

    def test_get_legal_pawn_moves_with_wall(self):
        self.board.move_pawn((4,4), PLAYER_4)
        self.board.add_wall((4, 3), is_horiz=False, player=PLAYER_4)
        expected_moves = [(MOVE, 5, 4), (MOVE, 3, 4), (MOVE, 4, 5)]
        moves = self.board.get_legal_pawn_moves(PLAYER_4)
        self.assertEqual(expected_moves, moves)

    def test_get_legal_pawn_moves_with_all_players_close(self):
        self.board.move_pawn((4, 4), PLAYER_1)
        self.board.move_pawn((3, 4), PLAYER_2)
        self.board.move_pawn((5, 4), PLAYER_3)
        self.board.move_pawn((4, 3), PLAYER_4)
        expected_moves = [(MOVE, 4, 5), (MOVE, 6, 4), (MOVE, 2, 4), (MOVE, 4, 2)] # Jump baby
        moves = self.board.get_legal_pawn_moves(PLAYER_1)
        self.assertEqual(expected_moves, moves)

    def test_get_legal_pawn_moves(self):
        self.board.move_pawn((4,4), PLAYER_3)
        expected_moves = [(MOVE, 5, 4), (MOVE, 3, 4), (MOVE, 4, 5), (MOVE, 4, 3)]
        moves = self.board.get_legal_pawn_moves(PLAYER_3)
        self.assertEqual(expected_moves, moves)

    def test_is_finished_at_start(self):
        self.assertFalse(self.board.is_finished())

    def test_is_finished_at_mid_game(self):
        self.board.move_pawn((3, 4), PLAYER_1)
        self.board.move_pawn((4, 4), PLAYER_2)
        self.board.move_pawn((4, 3), PLAYER_3)
        self.board.move_pawn((2, 4), PLAYER_4)
        self.assertFalse(self.board.is_finished())

    def test_is_finished_player_1(self):
        self.board.move_pawn((8, 4), PLAYER_1)
        self.assertFalse(self.board.is_finished())

    def test_is_finished_player_2(self):
        self.board.move_pawn((4, 0), PLAYER_2)
        self.assertFalse(self.board.is_finished())

    def test_is_finished_player_3(self):
        self.board.move_pawn((0, 4), PLAYER_3)
        self.assertFalse(self.board.is_finished())

    def test_is_finished_player_4(self):
        self.board.move_pawn((4, 8), PLAYER_4)
        self.assertFalse(self.board.is_finished())

    def test_is_finished_half_of_the_players(self):
        self.board.move_pawn((8, 4), PLAYER_1)
        self.board.move_pawn((0, 4), PLAYER_3)
        self.assertFalse(self.board.is_finished())

    def test_is_finished_all_but_one_players(self):
        self.board.move_pawn((8, 4), PLAYER_1)
        self.board.move_pawn((4, 0), PLAYER_2)
        self.board.move_pawn((0, 4), PLAYER_3)
        self.assertTrue(self.board.is_finished())

    def test_wall_count_at_start(self):
        self.assertEqual(5, self.board.player_walls[PLAYER_1])
        self.assertEqual(5, self.board.player_walls[PLAYER_2])
        self.assertEqual(5, self.board.player_walls[PLAYER_3])
        self.assertEqual(5, self.board.player_walls[PLAYER_4])

    def test_move_on_other_paws_disallowed(self):
        for i in range(0, 4):
            for j in range(0, 4):
                with self.subTest(i=i, j=j):
                    self.board.move_pawn((4, 4), i)
                    self.assertFalse(self.board.can_move_here(4, 4, j))

    def test_min_steps_before_victory_at_victory_player_1(self):
        self.board.move_pawn((8, 5), PLAYER_1)
        self.assertEqual(0, self.board.get_min_steps_before_victory(PLAYER_1))

    def test_min_steps_before_victory_at_victory_player_2(self):
        self.board.move_pawn((1, 0), PLAYER_2)
        self.assertEqual(0, self.board.get_min_steps_before_victory(PLAYER_2))

    def test_min_steps_before_victory_at_victory_player_3(self):
        self.board.move_pawn((0, 2), PLAYER_3)
        self.assertEqual(0, self.board.get_min_steps_before_victory(PLAYER_3))

    def test_min_steps_before_victory_at_victory_player_4(self):
        self.board.move_pawn((2, 8), PLAYER_4)
        self.assertEqual(0, self.board.get_min_steps_before_victory(PLAYER_4))

    def test_is_legal_pawn_move_move_on_the_side(self):
        self.assertTrue(self.board.is_legal_pawn_move(PLAYER_2, (4, 1), (5, 0)))

    def test_min_steps_before_victory_at_start(self):
        for i in range(0, 4):
            with self.subTest(i=i):
                self.assertEqual(8, self.board.get_min_steps_before_victory(i))

    def test_clone(self):
        board2 = self.board.clone()
        self.assertEqual(self.board.pawns, board2.pawns)
        self.assertEqual(self.board.goals, board2.goals)
        self.assertEqual(self.board.player_walls, board2.player_walls)

    def test_paths_exist(self):
        # Build a cell
        for i in range(3, 6):
            self.board.horiz_walls.append((3, i))
            self.board.horiz_walls.append((5, i))
            self.board.verti_walls.append((i, 3))
            self.board.verti_walls.append((i, 5))

        for i in range(0, 4):
            new_board = self.board.clone()
            with self.subTest(i=i):
                new_board.move_pawn((4, 4), i)
                self.assertFalse(new_board.paths_exist)

    def test_is_action_valid_isnt_when_stepping_on_someone_elses_toes(self):
        self.board.move_pawn((4, 1), PLAYER_1)
        self.board.move_pawn((4, 2), PLAYER_2)
        self.board.move_pawn((4, 3), PLAYER_3)
        self.board.move_pawn((4, 4), PLAYER_4)
        self.assertFalse(self.board.is_action_valid((MOVE, 4, 2), PLAYER_1))
        self.assertFalse(self.board.is_action_valid((MOVE, 4, 3), PLAYER_2))
        self.assertFalse(self.board.is_action_valid((MOVE, 4, 4), PLAYER_3))
        self.assertFalse(self.board.is_action_valid((MOVE, 4, 3), PLAYER_4))

    def test_is_action_valid_isnt_when_moving_somewhere_random(self):
        self.board.move_pawn((0, 1), PLAYER_1)
        self.board.move_pawn((0, 2), PLAYER_2)
        self.board.move_pawn((0, 3), PLAYER_3)
        self.board.move_pawn((0, 4), PLAYER_4)
        self.assertFalse(self.board.is_action_valid((MOVE, 8, 1), PLAYER_1))
        self.assertFalse(self.board.is_action_valid((MOVE, 8, 2), PLAYER_2))
        self.assertFalse(self.board.is_action_valid((MOVE, 8, 3), PLAYER_3))
        self.assertFalse(self.board.is_action_valid((MOVE, 8, 4), PLAYER_4))

    def test_is_action_valid_is_when_moving_properly(self):
        self.board.move_pawn((1, 1), PLAYER_1)
        self.board.move_pawn((2, 2), PLAYER_2)
        self.board.move_pawn((3, 3), PLAYER_3)
        self.board.move_pawn((4, 4), PLAYER_4)
        self.assertTrue(self.board.is_action_valid((MOVE, 1, 2), PLAYER_1))
        self.assertTrue(self.board.is_action_valid((MOVE, 2, 3), PLAYER_2))
        self.assertTrue(self.board.is_action_valid((MOVE, 3, 4), PLAYER_3))
        self.assertTrue(self.board.is_action_valid((MOVE, 4, 5), PLAYER_4))

    def test_get_score_player_1_win(self):
        self.board.move_pawn((8, 0), PLAYER_1)
        self.board.move_pawn((4, 8), PLAYER_2)
        self.board.move_pawn((8, 1), PLAYER_3)
        self.board.move_pawn((0, 0), PLAYER_4)
        self.assertEqual(50, self.board.get_score(PLAYER_1))
        self.assertEqual(42, self.board.get_score(PLAYER_2))
        self.assertEqual(42, self.board.get_score(PLAYER_3))
        self.assertEqual(42, self.board.get_score(PLAYER_4))

    def test_get_score_player_2_win(self):
        self.board.move_pawn((0, 0), PLAYER_1)
        self.board.move_pawn((8, 0), PLAYER_2)
        self.board.move_pawn((8, 1), PLAYER_3)
        self.board.move_pawn((1, 0), PLAYER_4)
        self.assertEqual(42, self.board.get_score(PLAYER_1))
        self.assertEqual(50, self.board.get_score(PLAYER_2))
        self.assertEqual(42, self.board.get_score(PLAYER_3))
        self.assertEqual(42, self.board.get_score(PLAYER_4))

    def test_get_score_player_3_win(self):
        self.board.move_pawn((0, 7), PLAYER_1)
        self.board.move_pawn((4, 8), PLAYER_2)
        self.board.move_pawn((0, 3), PLAYER_3)
        self.board.move_pawn((2, 0), PLAYER_4)
        self.assertEqual(42, self.board.get_score(PLAYER_1))
        self.assertEqual(42, self.board.get_score(PLAYER_2))
        self.assertEqual(50, self.board.get_score(PLAYER_3))
        self.assertEqual(42, self.board.get_score(PLAYER_4))

    def test_get_score_player_4_win(self):
        self.board.move_pawn((0, 3), PLAYER_1)
        self.board.move_pawn((7, 8), PLAYER_2)
        self.board.move_pawn((8, 1), PLAYER_3)
        self.board.move_pawn((4, 8), PLAYER_4)
        self.assertEqual(42, self.board.get_score(PLAYER_1))
        self.assertEqual(42, self.board.get_score(PLAYER_2))
        self.assertEqual(42, self.board.get_score(PLAYER_3))
        self.assertEqual(50, self.board.get_score(PLAYER_4))

    def test_get_score_player_all_same_distance(self):
        self.board.move_pawn((4, 4), PLAYER_1)
        self.board.move_pawn((3, 4), PLAYER_2)
        self.board.move_pawn((4, 3), PLAYER_3)
        self.board.move_pawn((4, 3), PLAYER_4)
        self.assertEqual(46, self.board.get_score(PLAYER_1))
        self.assertEqual(46, self.board.get_score(PLAYER_2))
        self.assertEqual(46, self.board.get_score(PLAYER_3))
        self.assertEqual(46, self.board.get_score(PLAYER_4))

    def test_get_scores_should_order_player_by_score(self):
        self.board.move_pawn((8, 0), PLAYER_1)
        self.board.move_pawn((4, 1), PLAYER_2)
        self.board.move_pawn((3, 6), PLAYER_3)
        self.board.move_pawn((4, 4), PLAYER_4)
        player_score = self.board.get_scores()
        self.assertEqual(PLAYER_1, player_score[0][0])
        self.assertEqual(PLAYER_2, player_score[1][0])
        self.assertEqual(PLAYER_3, player_score[2][0])
        self.assertEqual(PLAYER_4, player_score[3][0])

    def test_get_scores_should_order_player_by_score_with_player_2_winning(self):
        self.board.move_pawn((7, 1), PLAYER_1)
        self.board.move_pawn((4, 0), PLAYER_2)
        self.board.move_pawn((3, 6), PLAYER_3)
        self.board.move_pawn((4, 4), PLAYER_4)
        player_score = self.board.get_scores()
        self.assertEqual(PLAYER_2, player_score[0][0])
        self.assertEqual(PLAYER_1, player_score[1][0])
        self.assertEqual(PLAYER_3, player_score[2][0])
        self.assertEqual(PLAYER_4, player_score[3][0])

    def test_get_scores_should_order_player_by_score_with_player_3_winning(self):
        self.board.move_pawn((7, 1), PLAYER_1)
        self.board.move_pawn((4, 2), PLAYER_2)
        self.board.move_pawn((0, 8), PLAYER_3)
        self.board.move_pawn((4, 4), PLAYER_4)
        player_score = self.board.get_scores()
        self.assertEqual(PLAYER_3, player_score[0][0])
        self.assertEqual(PLAYER_1, player_score[1][0])
        self.assertEqual(PLAYER_2, player_score[2][0])
        self.assertEqual(PLAYER_4, player_score[3][0])

    def test_get_scores_should_order_player_by_score_with_player_4_winning(self):
        self.board.move_pawn((3, 1), PLAYER_1)
        self.board.move_pawn((4, 2), PLAYER_2)
        self.board.move_pawn((3, 6), PLAYER_3)
        self.board.move_pawn((4, 8), PLAYER_4)
        player_score = self.board.get_scores()
        self.assertEqual(PLAYER_4, player_score[0][0])
        self.assertEqual(PLAYER_2, player_score[1][0])
        self.assertEqual(PLAYER_3, player_score[2][0])
        self.assertEqual(PLAYER_1, player_score[3][0])

    def test_get_scores_walls_should_be_tiebreaker(self):
        self.board.move_pawn((4, 4), PLAYER_1)
        self.board.move_pawn((3, 4), PLAYER_2)
        self.board.move_pawn((4, 3), PLAYER_3)
        self.board.move_pawn((4, 3), PLAYER_4)
        self.board.player_walls[PLAYER_1] = 9
        self.board.player_walls[PLAYER_2] = 8
        self.board.player_walls[PLAYER_3] = 7
        self.board.player_walls[PLAYER_4] = 6
        player_score = self.board.get_scores()
        self.assertEqual(PLAYER_1, player_score[0][0])
        self.assertEqual(PLAYER_2, player_score[1][0])
        self.assertEqual(PLAYER_3, player_score[2][0])
        self.assertEqual(PLAYER_4, player_score[3][0])

    def test_get_scores_walls_should_be_tiebreaker_with_player_3_winning(self):
        self.board.move_pawn((4, 4), PLAYER_1)
        self.board.move_pawn((3, 4), PLAYER_2)
        self.board.move_pawn((4, 3), PLAYER_3)
        self.board.move_pawn((4, 3), PLAYER_4)
        self.board.player_walls[PLAYER_1] = 8
        self.board.player_walls[PLAYER_2] = 7
        self.board.player_walls[PLAYER_3] = 9
        self.board.player_walls[PLAYER_4] = 5
        player_score = self.board.get_scores()
        self.assertEqual(PLAYER_3, player_score[0][0])
        self.assertEqual(PLAYER_1, player_score[1][0])
        self.assertEqual(PLAYER_2, player_score[2][0])
        self.assertEqual(PLAYER_4, player_score[3][0])

    def test_get_scores_walls_should_not_be_considered_without_tie(self):
        self.board.move_pawn((0, 7), PLAYER_1)
        self.board.move_pawn((4, 8), PLAYER_2)
        self.board.move_pawn((0, 3), PLAYER_3)
        self.board.move_pawn((2, 0), PLAYER_4)
        self.board.player_walls[PLAYER_1] = 8
        self.board.player_walls[PLAYER_2] = 4
        self.board.player_walls[PLAYER_3] = 2
        self.board.player_walls[PLAYER_4] = 6
        player_score = self.board.get_scores()
        self.assertEqual(PLAYER_3, player_score[0][0])
        self.assertEqual(PLAYER_1, player_score[1][0])
        self.assertEqual(PLAYER_4, player_score[2][0])
        self.assertEqual(PLAYER_2, player_score[3][0])

    def test_get_scores_last_player_should_be_priorised_in_case_of_tie_with_points_and_walls(self):
        self.board.move_pawn((0, 7), PLAYER_1)
        self.board.move_pawn((4, 8), PLAYER_2)
        self.board.move_pawn((0, 3), PLAYER_3)
        self.board.move_pawn((2, 0), PLAYER_4)
        self.board.player_walls[PLAYER_1] = 8
        self.board.player_walls[PLAYER_2] = 8
        self.board.player_walls[PLAYER_3] = 2
        self.board.player_walls[PLAYER_4] = 8
        player_score = self.board.get_scores()
        self.assertEqual(PLAYER_3, player_score[0][0])
        self.assertEqual(PLAYER_4, player_score[1][0])
        self.assertEqual(PLAYER_2, player_score[2][0])
        self.assertEqual(PLAYER_1, player_score[3][0])

    def test_should_support_starting_wall_specification(self):
        player1_wall_count = 3
        player2_wall_count = 14
        player3_wall_count = 15
        player4_wall_count = 92
        board = Board(player_count=4, starting_walls=[player1_wall_count, player2_wall_count, player3_wall_count, player4_wall_count])
        self.assertEqual(player1_wall_count, board.player_walls[0])
        self.assertEqual(player2_wall_count, board.player_walls[1])
        self.assertEqual(player3_wall_count, board.player_walls[2])
        self.assertEqual(player4_wall_count, board.player_walls[3])


class TestBoardRules(unittest.TestCase):
    def setUp(self):
        self.board2 = Board(player_count=2)

    def test_is_action_valid_should_return_false_if_no_wall_left(self):
        self.board2.player_walls = [0, 0, 0, 0]

        self.assertFalse(self.board2.is_action_valid((WALL_H, 1, 1), PLAYER_1))
        self.assertFalse(self.board2.is_action_valid((WALL_H, 1, 1), PLAYER_2))
        self.assertFalse(self.board2.is_action_valid((WALL_H, 1, 1), PLAYER_3))
        self.assertFalse(self.board2.is_action_valid((WALL_H, 1, 1), PLAYER_4))


class TestBoardBasics(unittest.TestCase):



    def setUp(self):
        self.board2 = Board(player_count=2)

    def test_play_action_add_vertical_wall(self):
        self.board2.play_action((WALL_V, 0, 0), PLAYER_1)
        self.assertEqual(self.board2.player_walls[PLAYER_1], 9)
        self.assertEqual(len(self.board2.verti_walls), 1)


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)
