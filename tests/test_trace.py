import unittest
import json

import os
import uuid

import xmlrunner

from game.constants import MOVE
from game.game import Trace, Game
from game.quoridor import Board, Agent
from game.trace import load_trace

PLAYER_1 = 0
PLAYER_2 = 1

REPLAY_FILENAME_ROOT = "test"


##TODO: Test pour des gigagame (> 4Gb)
class TestTrace(unittest.TestCase):

    def setUp(self):
        self.replay_file_name = "./" + REPLAY_FILENAME_ROOT + str(uuid.uuid4()) + ".json"

    def tearDown(self):
        os.remove(self.replay_file_name)

    def test_export_json(self):
        board = Board()
        trace = Trace(board, [None, None])
        trace.add_action(1, (MOVE, 7, 4), 1.0)
        with open(self.replay_file_name, "w") as file:
            trace.write(file)
        with open(self.replay_file_name, "r") as file:
            content = file.readline()
            self.assertNotEqual(content, "")

    def test_export_and_load(self):
        initial_board = Board()
        trace = Trace(initial_board, [None, None])
        trace.add_action(1, (MOVE, 7, 4), 1.0)
        with open(self.replay_file_name, "w") as file:
            trace.write(file)
        with open(self.replay_file_name, "r") as file2:
            loaded_trace = load_trace(file2)
            initial_loaded_game = loaded_trace.get_initial_board()
            (player, action, t) = loaded_trace.actions[0]
            pre_move_board = initial_loaded_game.clone()
            first_move_loaded_game = initial_loaded_game.play_action(action, player)
            self.assertEqual(pre_move_board.pawns[1], (8,4))
            self.assertEqual(first_move_loaded_game.pawns[1], (7,4))

    def test_replay_without_winner(self):
        initial_board = Board()
        trace = Trace(initial_board, [None, None])
        with open(self.replay_file_name, "w") as file:
            trace.write(file)
        with open(self.replay_file_name, "r") as file:
            replay = json.load(file)
            self.assertEqual(replay['winner'], 0)

    def test_replay_with_player1_winner(self):
        initial_board = Board()
        initial_board.move_pawn((8,4), PLAYER_1)
        initial_board.move_pawn((7,4), PLAYER_2)
        game = Game([Agent(), Agent()], initial_board)
        game.play()
        with open(self.replay_file_name, "w") as file:
            game.trace.write(file)
        with open(self.replay_file_name, "r") as file:
            replay = json.load(file)
            self.assertEqual(replay['winner'], 0)

    def test_replay_with_player2_winner(self):
        initial_board = Board()
        initial_board.move_pawn((1, 4), PLAYER_1)
        initial_board.move_pawn((0, 4), PLAYER_2)
        game = Game([Agent(), Agent()], initial_board)
        game.play()
        with open(self.replay_file_name, "w") as file:
            game.trace.write(file)
        with open(self.replay_file_name, "r") as file:
            replay = json.load(file)
            self.assertEqual(replay['winner'], 1)


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)
