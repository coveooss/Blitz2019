import socket
import unittest

from unittest.mock import MagicMock

import xmlrunner

from game.constants import WALL_H, MOVE
from game.game import Trace, Game, ConsoleViewer, TimeCreditExpiredError, HeadlessViewer
from game.quoridor import Board, Agent

PLAYER_1 = 0
PLAYER_2 = 1
PLAYER_3 = 2
PLAYER_4 = 3


class TestGameInit(unittest.TestCase):

    def test_should_support_being_sent_2_players(self):
        agents = [ConsoleViewer(), ConsoleViewer()]
        board = Board()
        viewer = None
        credits = [None, None]
        game = Game(agents, board, viewer, credits)

    def test_should_support_being_sent_3_players(self):
        agents = [ConsoleViewer(), ConsoleViewer(), ConsoleViewer()]
        board = Board()
        viewer = None
        credits = [None, None, None]
        game = Game(agents, board, viewer, credits)

    def test_should_support_being_sent_4_players(self):
        agents = [ConsoleViewer(), ConsoleViewer(), ConsoleViewer(), ConsoleViewer()]
        board = Board()
        viewer = None
        credits = [None, None, None, None]
        game = Game(agents, board, viewer, credits)

    def test_should_create_trace_with_player_names_when_2_are_supplied(self):
        agents = [ConsoleViewer(), ConsoleViewer()]
        board = Board()
        viewer = None
        credits = [None, None]
        player_names = ["Ding", "Dong"]  # Est effrayante
        game = Game(agents, board, viewer, credits, None, player_names)
        self.assertEqual(player_names, game.trace.player_names)

    def test_should_create_trace_with_player_names_when_4_are_supplied(self):
        agents = [ConsoleViewer(), ConsoleViewer(), ConsoleViewer(), ConsoleViewer()]
        board = Board()
        viewer = None
        credits = [None, None, None, None]
        player_names = ["CAESAR", "MARCVS", "AVRELIVS", "ANTONINVS"]
        game = Game(agents, board, viewer, credits, None, player_names)
        self.assertEqual(player_names, game.trace.player_names)


class TestGamePlay(unittest.TestCase):
    def setUp(self):
        credits = [None, None, None, None]
        self.agent1 = Agent()
        self.agent2 = Agent()
        self.agent3 = Agent()
        self.agent4 = Agent()
        self.agents = [self.agent1, self.agent2, self.agent3, self.agent4]
        for agent in self.agents:
            agent.initialize = MagicMock()
            agent.play = MagicMock()
        self.board2 = Board()
        self.board4 = Board(player_count=4)
        self.trace2 = Trace(self.board2, credits[0:2])
        self.trace2.set_winner = MagicMock()
        self.trace2.set_ranking = MagicMock()
        self.trace4 = Trace(self.board4, credits[0:4])
        self.trace4.set_winner = MagicMock()
        self.trace4.set_ranking = MagicMock()
        self.viewer = HeadlessViewer()
        self.viewer.finished = MagicMock()
        self.game2 = Game(self.agents[0:2], self.board2, self.viewer, credits[0:2], self.trace2)
        self.game4 = Game(self.agents[0:4], self.board4, self.viewer, credits[0:4], self.trace4)

    def test_play_with_2_players_should_call_initialize(self):
        self.board2.is_finished = MagicMock(return_value=True)
        self.game2.play()
        self.agent1.initialize.assert_called_with(self.board2, [0], None)
        self.agent2.initialize.assert_called_with(self.board2, [1], None)

    def test_play_with_2_players_should_play_while_not_finished(self):
        self.board2.is_finished = MagicMock(side_effect=[False, False, True])
        self.agent1.play = MagicMock(return_value=(WALL_H, 1, 2))
        self.agent2.play = MagicMock(return_value=(WALL_H, 2, 4))
        self.game2.play()
        self.agent1.play.assert_called_with(self.board2, 0, 1, None)
        self.agent2.play.assert_called_with(self.board2, 1, 2, None)

    def test_play_with_4_players_should_call_initialize(self):
        self.board4.is_finished = MagicMock(return_value=True)
        self.game4.play()
        self.agent1.initialize.assert_called_with(self.board4, [0], None)
        self.agent2.initialize.assert_called_with(self.board4, [1], None)
        self.agent3.initialize.assert_called_with(self.board4, [2], None)
        self.agent4.initialize.assert_called_with(self.board4, [3], None)

    def test_play_with_4_players_should_play_while_not_finished(self):
        self.board4.is_finished = MagicMock(side_effect=[False, False, False, False, True])
        self.agent1.play = MagicMock(return_value=(WALL_H, 1, 2))
        self.agent2.play = MagicMock(return_value=(WALL_H, 2, 4))
        self.agent3.play = MagicMock(return_value=(WALL_H, 3, 5))
        self.agent4.play = MagicMock(return_value=(WALL_H, 2, 4))
        self.game4.play()
        self.agent1.play.assert_called_with(self.board4, 0, 1, None)
        self.agent2.play.assert_called_with(self.board4, 1, 2, None)
        self.agent3.play.assert_called_with(self.board4, 2, 3, None)
        self.agent4.play.assert_called_with(self.board4, 3, 4, None)

    def test_play_with_2_players_should_correctly_set_the_winner(self):
        self.board2.is_finished = MagicMock(side_effect=[False, False, True])
        self.agent1.play = MagicMock(return_value=(WALL_H, 1, 2))
        self.agent2.play = MagicMock(return_value=(MOVE, 7, 4))
        self.game2.play()
        self.trace2.set_winner.assert_called_with(PLAYER_2, "")
        self.viewer.finished.assert_called_with(2, PLAYER_2, "")

    def test_play_with_4_players_should_correctly_set_the_winner(self):
        self.board4.is_finished = MagicMock(side_effect=[False, False, False, False, True])
        self.agent1.play = MagicMock(return_value=(WALL_H, 1, 2))
        self.agent2.play = MagicMock(return_value=(WALL_H, 5, 7))
        self.agent3.play = MagicMock(return_value=(MOVE, 7, 4))
        self.agent4.play = MagicMock(return_value=(WALL_H, 2, 2))
        self.game4.play()
        self.trace4.set_winner.assert_called_with(PLAYER_3, "")
        self.viewer.finished.assert_called_with(4, PLAYER_3, "")

    def test_play_should_reset_credits_every_turn(self):
        credits = [5.0, 3.0, 3.0, 3.0]
        trace4 = Trace(self.board4, credits[0:4])
        viewer = HeadlessViewer()
        game4 = Game(self.agents[0:4], self.board4, viewer, credits, trace4)
        self.board4.is_finished = MagicMock(side_effect=[False, False, False, False, False, True])
        self.agent1.play = MagicMock(return_value=[(WALL_H, 1, 2), (WALL_H, 3, 4)])
        self.agent2.play = MagicMock(return_value=(WALL_H, 5, 7))
        self.agent3.play = MagicMock(return_value=(MOVE, 7, 4))
        self.agent4.play = MagicMock(return_value=(WALL_H, 2, 2))
        game4.play()
        self.assertAlmostEqual(self.agent1.play.call_args[0][3], 5.0)

    def test_should_return_ranking_with_all_2_players(self):
        self.board2.is_finished = MagicMock(side_effect=[False, False, True])
        self.agent1.play = MagicMock(return_value=(WALL_H, 1, 2))
        self.agent2.play = MagicMock(return_value=(MOVE, 7, 4))
        self.game2.play()
        self.trace2.set_winner.assert_called_with(PLAYER_2, "")
        self.trace2.set_ranking.assert_called_with([PLAYER_2, PLAYER_1])
        self.viewer.finished.assert_called_with(2, PLAYER_2, "")

    def test_should_return_ranking_based_on_order_of_arrival_for_2_players(self):
        # They're both close to the victory but PLAYER_2 wins
        self.board2.move_pawn((6, 4), PLAYER_1)
        self.board2.move_pawn((1, 4), PLAYER_2)
        self.board2.players_on_goal = MagicMock(side_effect=[
            [False, False],
            [False, False],
            [False, True]])
        self.board2.is_finished = MagicMock(side_effect=[False, False, True])
        self.board2.is_player_on_goal = MagicMock(side_effect=[False, False, False, True])
        self.board2.get_scores = MagicMock(return_value=[(PLAYER_2, 50), (PLAYER_1, 49)])
        self.agent1.play = MagicMock(return_value=(MOVE, 7, 4))
        self.agent2.play = MagicMock(return_value=(MOVE, 0, 4))
        self.game2.play()
        self.trace2.set_winner.assert_called_with(PLAYER_2, "")
        self.trace2.set_ranking.assert_called_with([PLAYER_2, PLAYER_1])
        self.viewer.finished.assert_called_with(2, PLAYER_2, "")

    def test_should_return_ranking_based_on_order_of_arrival_for_2_players_with_disconnect(self):
        # They're both close to the victory but PLAYER_2 disconnect before reaching the end
        self.board2.move_pawn((6, 4), PLAYER_1)
        self.board2.move_pawn((1, 4), PLAYER_2)
        self.board2.players_on_goal = MagicMock(side_effect=[
            [False, False],
            [False, False],
            [False, False]])
        self.board2.is_finished = MagicMock(side_effect=[False, False, False])
        self.board2.is_player_on_goal = MagicMock(side_effect=[False, False, False])
        self.board2.get_scores = MagicMock(return_value=[(PLAYER_1, 50), (PLAYER_2, 49)])
        self.agent1.play = MagicMock(return_value=(MOVE, 7, 4))
        self.agent2.play = MagicMock(side_effect=[socket.timeout])
        self.game2.play()
        self.trace2.set_winner.assert_called_with(PLAYER_1, "Opponent's have been expelled.")
        self.trace2.set_ranking.assert_called_with([PLAYER_1, PLAYER_2])
        self.viewer.finished.assert_called_with(2, PLAYER_1, "Opponent's have been expelled.")

    def test_should_return_ranking_based_on_order_of_arrival_for_4_players(self):
        # set every player one step away from victory, PLAYER_1 finishes last
        self.board4.move_pawn((6, 4), PLAYER_1)
        self.board4.move_pawn((4, 1), PLAYER_2)
        self.board4.move_pawn((1, 4), PLAYER_3)
        self.board4.move_pawn((4, 7), PLAYER_4)

        self.board4.players_on_goal = MagicMock(side_effect=[
            [False, False, False, False],
            [False, False, False, False],
            [False, True, False, False],
            [False, True, True, False],
            [False, True, True, True]])
        self.board4.is_finished = MagicMock(side_effect=[False, False, False, False, True])
        self.board4.is_player_on_goal = MagicMock(side_effect=[False, False, False, True, False, True, False, True])
        self.board4.get_scores = MagicMock(
            return_value=[(PLAYER_2, 50), (PLAYER_3, 50), (PLAYER_4, 50), (PLAYER_1, 49)])
        self.agent1.play = MagicMock(return_value=(MOVE, 7, 4))  # rekt
        self.agent2.play = MagicMock(return_value=(MOVE, 4, 0))
        self.agent3.play = MagicMock(return_value=(MOVE, 0, 4))
        self.agent4.play = MagicMock(return_value=(MOVE, 4, 8))
        self.game4.play()
        self.trace4.set_winner.assert_called_with(PLAYER_2, "")  # first
        self.trace4.set_ranking.assert_called_with([PLAYER_2, PLAYER_3, PLAYER_4, PLAYER_1])  # order is VERY important
        self.viewer.finished.assert_called_with(4, PLAYER_2, "")

    def test_should_return_ranking_based_on_order_of_arrival_for_4_players_nonobstant_the_score_order(self):
        # set every player one step away from victory, PLAYER_1 finishes last
        self.board4.move_pawn((6, 4), PLAYER_1)
        self.board4.move_pawn((4, 1), PLAYER_2)
        self.board4.move_pawn((1, 4), PLAYER_3)
        self.board4.move_pawn((4, 7), PLAYER_4)

        self.board4.players_on_goal = MagicMock(side_effect=[
            [False, False, False, False],
            [False, False, False, False],
            [False, True, False, False],
            [False, True, True, False],
            [False, True, True, True]])
        self.board4.is_finished = MagicMock(side_effect=[False, False, False, False, True])
        self.board4.is_player_on_goal = MagicMock(side_effect=[False, False, False, True, False, True, False, True])
        self.board4.get_scores = MagicMock(
            return_value=[(PLAYER_4, 50), (PLAYER_3, 50), (PLAYER_2, 50), (PLAYER_1, 49)])
        self.agent1.play = MagicMock(return_value=(MOVE, 7, 4))  # rekt
        self.agent2.play = MagicMock(return_value=(MOVE, 4, 0))
        self.agent3.play = MagicMock(return_value=(MOVE, 0, 4))
        self.agent4.play = MagicMock(return_value=(MOVE, 4, 8))
        self.game4.play()
        self.trace4.set_winner.assert_called_with(PLAYER_2, "")  # first
        self.trace4.set_ranking.assert_called_with([PLAYER_2, PLAYER_3, PLAYER_4, PLAYER_1])  # order is VERY important
        self.viewer.finished.assert_called_with(4, PLAYER_2, "")

    def test_should_return_ranking_based_on_order_of_arrival_for_4_players_player_3_wins(self):
        # set every player one step away from victory, PLAYER_1 finishes last
        self.board4.move_pawn((6, 4), PLAYER_1)
        self.board4.move_pawn((4, 2), PLAYER_2)
        self.board4.move_pawn((1, 4), PLAYER_3)
        self.board4.move_pawn((4, 7), PLAYER_4)

        self.board4.players_on_goal = MagicMock(side_effect=[
            [False, False, False, False],
            [False, False, False, False],
            [False, False, False, False],
            [False, False, True, False],
            [False, False, True, True],
            [True, False, True, True]])

        self.board4.is_finished = MagicMock(side_effect=[False, False, False, False, False, True])
        self.board4.is_player_on_goal = MagicMock(
            side_effect=[False, False, False, False, False, True, False, True, False, True])
        self.board4.get_scores = MagicMock(
            return_value=[(PLAYER_2, 50), (PLAYER_3, 50), (PLAYER_4, 50), (PLAYER_1, 49)])
        self.agent1.play = MagicMock(side_effect=[(MOVE, 7, 4), (MOVE, 8, 4)])
        self.agent2.play = MagicMock(side_effect=[(MOVE, 4, 1), (MOVE, 4, 0)])  # rekt
        self.agent3.play = MagicMock(return_value=(MOVE, 0, 4))
        self.agent4.play = MagicMock(return_value=(MOVE, 4, 8))
        self.game4.play()
        self.trace4.set_winner.assert_called_with(PLAYER_3, "")  # first
        self.trace4.set_ranking.assert_called_with([PLAYER_3, PLAYER_4, PLAYER_1, PLAYER_2])  # order is VERY important
        self.viewer.finished.assert_called_with(5, PLAYER_3, "")

    def test_should_return_ranking_based_on_order_of_arrival_for_4_players_with_disconnections(self):
        # set every player one step away from victory, PLAYER_1 finishes last
        self.board4.move_pawn((6, 4), PLAYER_1)
        self.board4.move_pawn((4, 2), PLAYER_2)
        self.board4.move_pawn((1, 4), PLAYER_3)
        self.board4.move_pawn((4, 7), PLAYER_4)

        self.board4.players_on_goal = MagicMock(side_effect=[
            [False, False, False, False],
            [False, False, False, False],
            [False, False, False, False],
            [False, False, False, False],
            [False, False, True, False],
            [True, False, True, False],
            [True, False, True, False]])

        self.board4.is_finished = MagicMock(side_effect=[False, False, False, False, False, True])
        self.board4.is_player_on_goal = MagicMock(
            side_effect=[False, False, False, False, False, False, True, False, True])
        self.board4.get_scores = MagicMock(
            return_value=[(PLAYER_2, 50), (PLAYER_3, 50), (PLAYER_4, 50), (PLAYER_1, 49)])
        self.agent1.play = MagicMock(side_effect=[(MOVE, 7, 4), (MOVE, 8, 4)])
        self.agent2.play = MagicMock(side_effect=[(MOVE, 4, 1), (MOVE, 4, 0)])  # rekt
        self.agent3.play = MagicMock(side_effect=socket.timeout)
        self.agent4.play = MagicMock(return_value=(MOVE, 4, 8))
        self.game4.play()
        self.trace4.set_winner.assert_called_with(PLAYER_4, "")  # first
        self.trace4.set_ranking.assert_called_with([PLAYER_4, PLAYER_1, PLAYER_2, PLAYER_3])  # order is VERY important
        self.viewer.finished.assert_called_with(5, PLAYER_4, "")

    def test_should_not_poke_player_who_won(self):
        # set every player one step away from victory, PLAYER_1 finishes last
        self.board4.move_pawn((5, 4), PLAYER_1)
        self.board4.move_pawn((4, 3), PLAYER_2)
        self.board4.move_pawn((1, 4), PLAYER_3)
        self.board4.move_pawn((4, 7), PLAYER_4)

        self.board4.players_on_goal = MagicMock(side_effect=[
            [False, False, False, False],
            [False, False, False, False],
            [False, False, False, False],
            [False, False, True, False],
            [False, False, True, False],
            [False, False, True, True],
            [False, False, True, True],
            [False, False, True, True],
            [False, False, True, True],
            [False, False, True, True],
            [True, False, True, True]])
        self.board4.is_finished = MagicMock(
            side_effect=[False, False, False, False, False, False, False, False, False, True])
        self.board4.is_player_on_goal = MagicMock(
            side_effect=[False, False, False, False, False, True, False, True, False, False, False, False, True, True,
                         False, True])
        self.board4.get_scores = MagicMock(
            return_value=[(PLAYER_2, 50), (PLAYER_3, 50), (PLAYER_4, 50), (PLAYER_1, 49)])
        self.agent1.play = MagicMock(side_effect=[(MOVE, 6, 4), (MOVE, 7, 4), (MOVE, 8, 4)])
        self.agent2.play = MagicMock(side_effect=[(MOVE, 4, 2), (MOVE, 4, 1), (MOVE, 4, 0)])  # rekt
        self.agent3.play = MagicMock(side_effect=[(MOVE, 0, 4)])
        self.agent4.play = MagicMock(side_effect=[(MOVE, 4, 8)])
        self.game4.play()
        self.trace4.set_winner.assert_called_with(PLAYER_3, "")  # first
        self.trace4.set_ranking.assert_called_with([PLAYER_3, PLAYER_4, PLAYER_1, PLAYER_2])  # order is VERY important
        self.viewer.finished.assert_called_with(7, PLAYER_3, "")

    def test_should_not_infinite_loop_when_2_player_disconnect_and_2_players_are_done(self):
        # disconnect 2 players, make 2 other win
        self.board4.move_pawn((7, 4), PLAYER_1)  # win
        self.board4.move_pawn((4, 2), PLAYER_2)  # dc
        self.board4.move_pawn((1, 4), PLAYER_3)  # win
        self.board4.move_pawn((4, 7), PLAYER_4)  # dc

        self.board4.is_finished = MagicMock(return_value=False)
        self.board4.players_on_goal = MagicMock(
            side_effect=[[False, False, False, False], [True, False, False, False], [True, False, False, False],
                         [True, False, True, False], [True, False, True, False]])
        self.board4.is_player_on_goal = MagicMock(side_effect=[False, True, False, False, True, False])
        self.board4.get_scores = MagicMock(
            return_value=[(PLAYER_2, 50), (PLAYER_3, 50), (PLAYER_4, 50), (PLAYER_1, 49)])
        self.agent1.play = MagicMock(side_effect=[(MOVE, 8, 4)])  # win
        self.agent2.play = MagicMock(side_effect=socket.timeout)  # dc baby
        self.agent3.play = MagicMock(return_value=(MOVE, 0, 4))  # win
        self.agent4.play = MagicMock(side_effect=socket.timeout)  # dc baby
        self.game4.play()
        self.trace4.set_winner.assert_called_with(PLAYER_1, "")  # first
        self.trace4.set_ranking.assert_called_with([PLAYER_1, PLAYER_3, PLAYER_4, PLAYER_2])
        self.viewer.finished.assert_called_with(3, PLAYER_1, "")


class TestGameDisconnect2Players(unittest.TestCase):
    def setUp(self):
        credits = [None, None]
        self.agent1 = Agent()
        self.agent2 = Agent()
        agents = [self.agent1, self.agent2]
        for agent in agents:
            agent.initialize = MagicMock()
            agent.play = MagicMock()
        self.board2 = Board()
        self.trace2 = Trace(self.board2, credits[0:2])
        self.trace2.set_winner = MagicMock()
        self.trace2.set_ranking = MagicMock()
        self.board2.is_player_on_goal = MagicMock(return_value=False)
        self.viewer = HeadlessViewer()
        self.viewer.finished = MagicMock()
        self.game2 = Game(agents[0:2], self.board2, self.viewer, credits[0:2], self.trace2)

    def test_play_should_call_initialize_and_make_player2_win_on_player1_disconnect(self):
        self.agent1.initialize = MagicMock(side_effect=TimeCreditExpiredError)
        self.game2.play()
        self.agent1.initialize.assert_called_with(self.board2, [0], None)
        self.trace2.set_winner.assert_called_with(PLAYER_2, "Opponent's have been expelled.")

    def test_play_should_call_initialize_and_make_player1_win_on_player2_disconnect(self):
        self.agent2.initialize = MagicMock(side_effect=TimeCreditExpiredError)
        self.game2.play()
        self.agent1.initialize.assert_called_with(self.board2, [0], None)
        self.agent2.initialize.assert_called_with(self.board2, [1], None)
        self.trace2.set_winner.assert_called_with(PLAYER_1, "Opponent's have been expelled.")

    def test_play_should_call_play_and_make_player1_win_on_player2_disconnect(self):
        self.board2.is_finished = MagicMock(return_value=False)
        self.agent1.play = MagicMock(return_value=(WALL_H, 1, 2))
        self.agent2.play = MagicMock(side_effect=socket.timeout)
        self.game2.play()
        self.agent1.initialize.assert_called_with(self.board2, [0], None)
        self.agent2.initialize.assert_called_with(self.board2, [1], None)
        self.agent1.play.assert_called_with(self.board2, PLAYER_1, 1, None)
        self.agent2.play.assert_called_with(self.board2, PLAYER_2, 2, None)
        self.trace2.set_winner.assert_called_with(PLAYER_1, "Opponent's have been expelled.")

    def test_play_should_call_play_and_make_player2_win_on_player1_disconnect(self):
        self.board2.is_finished = MagicMock(return_value=False)
        self.agent1.play = MagicMock(side_effect=socket.timeout)
        self.game2.play()
        self.agent1.initialize.assert_called_with(self.board2, [0], None)
        self.agent2.initialize.assert_called_with(self.board2, [1], None)
        self.agent1.play.assert_called_with(self.board2, PLAYER_1, 1, None)
        self.trace2.set_winner.assert_called_with(PLAYER_2, "Opponent's have been expelled.")

    def test_should_return_ranking_with_player_2_when_player_1_disconnect(self):
        self.board2.is_finished = MagicMock(return_value=False)
        self.agent1.play = MagicMock(side_effect=socket.timeout)
        self.game2.play()
        self.agent1.initialize.assert_called_with(self.board2, [0], None)
        self.agent2.initialize.assert_called_with(self.board2, [1], None)
        self.agent1.play.assert_called_with(self.board2, PLAYER_1, 1, None)
        self.trace2.set_ranking.assert_called_with([PLAYER_2, PLAYER_1])

    def test_should_return_ranking_with_player_1_when_player_2_disconnect(self):
        self.board2.is_finished = MagicMock(return_value=False)
        self.agent1.play = MagicMock(return_value=(WALL_H, 1, 2))
        self.agent2.play = MagicMock(side_effect=socket.timeout)
        self.game2.play()
        self.agent1.initialize.assert_called_with(self.board2, [0], None)
        self.agent2.initialize.assert_called_with(self.board2, [1], None)
        self.agent1.play.assert_called_with(self.board2, PLAYER_1, 1, None)
        self.trace2.set_ranking.assert_called_with([PLAYER_1, PLAYER_2])

    def test_play_should_call_initialize_and_not_declare_a_winner_if_none_can_connect(self):
        self.agent1.initialize = MagicMock(side_effect=TimeCreditExpiredError)
        self.agent2.initialize = MagicMock(side_effect=TimeCreditExpiredError)
        self.board2.is_finished = MagicMock(return_value=True)
        self.game2.play()
        self.agent1.initialize.assert_called_with(self.board2, [PLAYER_1], None)
        self.agent2.initialize.assert_called_with(self.board2, [PLAYER_2], None)
        self.trace2.set_ranking.assert_called_with([PLAYER_2, PLAYER_1])


class TestGameDisconnect4Players(unittest.TestCase):
    def setUp(self):
        credits = [None, None, None, None]
        self.agent1 = Agent()
        self.agent2 = Agent()
        self.agent3 = Agent()
        self.agent4 = Agent()
        agents = [self.agent1, self.agent2, self.agent3, self.agent4]
        for agent in agents:
            agent.initialize = MagicMock()
            agent.play = MagicMock()
        self.board4 = Board(player_count=4)
        self.trace4 = Trace(self.board4, credits)
        self.trace4.set_winner = MagicMock()
        self.trace4.set_ranking = MagicMock()
        self.viewer = HeadlessViewer()
        self.viewer.finished = MagicMock()
        self.game4 = Game(agents, self.board4, self.viewer, credits, self.trace4)

    def test_play_should_call_initialize_and_not_leave_the_game_if_one_player_disconnect(self):
        self.agent2.initialize = MagicMock(side_effect=TimeCreditExpiredError)
        self.board4.is_finished = MagicMock(return_value=True)
        self.game4.play()
        self.agent1.initialize.assert_called_with(self.board4, [PLAYER_1], None)
        self.agent2.initialize.assert_called_with(self.board4, [PLAYER_2], None)
        self.agent3.initialize.assert_called_with(self.board4, [PLAYER_3], None)
        self.agent4.initialize.assert_called_with(self.board4, [PLAYER_4], None)

    def test_play_should_call_initialize_and_not_declare_a_winner_if_none_can_connect(self):
        self.agent1.initialize = MagicMock(side_effect=TimeCreditExpiredError)
        self.agent2.initialize = MagicMock(side_effect=TimeCreditExpiredError)
        self.agent3.initialize = MagicMock(side_effect=TimeCreditExpiredError)
        self.agent4.initialize = MagicMock(side_effect=TimeCreditExpiredError)
        self.board4.is_finished = MagicMock(return_value=True)
        self.game4.play()
        self.agent1.initialize.assert_called_with(self.board4, [PLAYER_1], None)
        self.agent2.initialize.assert_called_with(self.board4, [PLAYER_2], None)
        self.agent3.initialize.assert_called_with(self.board4, [PLAYER_3], None)
        self.agent4.initialize.assert_called_with(self.board4, [PLAYER_4], None)
        self.trace4.set_ranking.assert_called_with([PLAYER_4, PLAYER_3, PLAYER_2, PLAYER_1])

    def test_play_should_call_initialize_and_not_make_player_play_if_disconnected(self):
        self.agent3.initialize = MagicMock(side_effect=TimeCreditExpiredError)
        self.board4.is_finished = MagicMock(side_effect=[False, False, False, False, True])
        self.agent1.play = MagicMock(return_value=(WALL_H, 1, 2))
        self.agent2.play = MagicMock(return_value=(WALL_H, 2, 3))
        self.agent4.play = MagicMock(return_value=(WALL_H, 4, 5))
        self.game4.play()
        self.agent1.initialize.assert_called_with(self.board4, [PLAYER_1], None)
        self.agent2.initialize.assert_called_with(self.board4, [PLAYER_2], None)
        self.agent3.initialize.assert_called_with(self.board4, [PLAYER_3], None)
        self.agent4.initialize.assert_called_with(self.board4, [PLAYER_4], None)

        self.agent1.play.assert_called_with(self.board4, PLAYER_1, 1, None)
        self.agent2.play.assert_called_with(self.board4, PLAYER_2, 2, None)
        self.agent3.play.assert_not_called()
        self.agent4.play.assert_called_with(self.board4, PLAYER_4, 3, None)

    def test_play_should_call_play_while_there_are_connected_players(self):
        self.board4.is_finished = MagicMock(return_value=False)
        self.agent1.play = MagicMock(side_effect=[(WALL_H, 1, 1), (WALL_H, 1, 3), (WALL_H, 1, 5), socket.timeout])
        self.agent2.play = MagicMock(side_effect=[(WALL_H, 2, 1), socket.timeout])
        self.agent3.play = MagicMock(side_effect=[(WALL_H, 3, 1), (WALL_H, 3, 3), socket.timeout])
        self.agent4.play = MagicMock(side_effect=[(WALL_H, 4, 1), (WALL_H, 4, 3), (WALL_H, 4, 5), (WALL_H, 5, 1)])
        self.game4.play()
        self.agent1.initialize.assert_called_with(self.board4, [PLAYER_1], None)
        self.agent2.initialize.assert_called_with(self.board4, [PLAYER_2], None)
        self.agent3.initialize.assert_called_with(self.board4, [PLAYER_3], None)
        self.agent4.initialize.assert_called_with(self.board4, [PLAYER_4], None)

        round = 0
        self.assertEqual(self.agent1.play.call_args_list[round][0], (self.board4, PLAYER_1, 1, None))
        self.assertEqual(self.agent2.play.call_args_list[round][0], (self.board4, PLAYER_2, 2, None))
        self.assertEqual(self.agent3.play.call_args_list[round][0], (self.board4, PLAYER_3, 3, None))
        self.assertEqual(self.agent4.play.call_args_list[round][0], (self.board4, PLAYER_4, 4, None))

        round = 1
        self.assertEqual(self.agent1.play.call_args_list[round][0], (self.board4, PLAYER_1, 5, None))
        self.assertEqual(self.agent2.play.call_args_list[round][0], (self.board4, PLAYER_2, 6, None))
        self.assertEqual(self.agent3.play.call_args_list[round][0], (self.board4, PLAYER_3, 7, None))
        self.assertEqual(self.agent4.play.call_args_list[round][0], (self.board4, PLAYER_4, 8, None))

        round = 2
        self.assertEqual(self.agent1.play.call_args_list[round][0], (self.board4, PLAYER_1, 9, None))
        # self.assertEqual(self.agent2.play.call_args_list[round][0], (self.board4, PLAYER_2, 9, None))
        self.assertEqual(self.agent3.play.call_args_list[round][0], (self.board4, PLAYER_3, 10, None))
        self.assertEqual(self.agent4.play.call_args_list[round][0], (self.board4, PLAYER_4, 11, None))

        round = 3
        self.assertEqual(self.agent1.play.call_args_list[round][0], (self.board4, PLAYER_1, 12, None))
        # self.assertEqual(self.agent2.play.call_args_list[round][0], (self.board4, PLAYER_2, 13, None))
        # self.assertEqual(self.agent3.play.call_args_list[round][0], (self.board4, PLAYER_3, 13, None))
        # self.assertEqual(self.agent4.play.call_args_list[round][0], (self.board4, PLAYER_4, 13, None)) Jamais l'occasion de jouer la partie est terminé

        self.trace4.set_winner.assert_called_with(PLAYER_4, "Opponent's have been expelled.")

    def test_play_should_not_show_all_player_to_ranking_even_if_disconnected(self):
        self.agent3.initialize = MagicMock(side_effect=TimeCreditExpiredError)
        self.board4.is_finished = MagicMock(side_effect=[False, False, False, False, True])
        self.agent1.play = MagicMock(return_value=(WALL_H, 1, 2))
        self.agent2.play = MagicMock(return_value=(WALL_H, 2, 3))
        self.agent4.play = MagicMock(return_value=(WALL_H, 4, 5))
        self.game4.play()
        self.agent1.initialize.assert_called_with(self.board4, [PLAYER_1], None)
        self.agent2.initialize.assert_called_with(self.board4, [PLAYER_2], None)
        self.agent3.initialize.assert_called_with(self.board4, [PLAYER_3], None)
        self.agent4.initialize.assert_called_with(self.board4, [PLAYER_4], None)

        self.trace4.set_ranking.assert_called_with([PLAYER_4, PLAYER_2, PLAYER_1, PLAYER_3])


class TestGameMetaInformation(unittest.TestCase):
    def setUp(self):
        credits = [None, None, None, None]
        self.agent1 = Agent()
        self.agent2 = Agent()
        self.agent3 = Agent()
        self.agent4 = Agent()
        agents = [self.agent1, self.agent2, self.agent3, self.agent4]
        for agent in agents:
            agent.initialize = MagicMock()
            agent.play = MagicMock()
        self.board4 = Board(player_count=4)
        self.trace4 = Trace(self.board4, credits)
        self.trace4.set_winner = MagicMock()
        self.trace4.set_ranking = MagicMock()
        self.trace4.set_reasons = MagicMock()
        self.viewer = HeadlessViewer()
        self.viewer.finished = MagicMock()
        self.game4 = Game(agents, self.board4, self.viewer, credits, self.trace4)

    def test_should_add_information_about_disconnection(self):
        self.board4.is_finished = MagicMock(return_value=False)
        self.agent1.play = MagicMock(side_effect=[(WALL_H, 1, 1), (WALL_H, 1, 3), (WALL_H, 1, 5), socket.timeout])
        self.agent2.play = MagicMock(side_effect=[(WALL_H, 2, 1), socket.timeout])
        self.agent3.play = MagicMock(side_effect=[(WALL_H, 3, 1), (WALL_H, 3, 3), socket.timeout])
        self.agent4.play = MagicMock(side_effect=[(WALL_H, 4, 1), (WALL_H, 4, 3), (WALL_H, 4, 5), (WALL_H, 5, 1)])
        self.game4.play()

        self.trace4.set_reasons.assert_called_with([(12, "Timeout "), (6, "Timeout "), (10, "Timeout "), (None, "")])


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)
