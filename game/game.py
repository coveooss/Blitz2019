#!/usr/bin/env python3
"""
Main program for the Quoridor game.
Author: Cyrille Dejemeppe <cyrille.dejemeppe@uclouvain.be>
Copyright (C) 2013, Université catholique de Louvain

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
import logging
import time
import socket
from abc import abstractmethod
from itertools import filterfalse, tee, chain
from typing import Callable, Tuple, Iterable, Optional, List, cast, Any

import xmlrpc.client

from game.board import Board, Action
from game.exceptions import InvalidActionError
from game.quoridor import Agent
from game.trace import Trace


Score = Tuple[int, int]

MAX_STEPS_GAME_OVER: int = 1000


class TimeCreditExpiredError(Exception):
    """An agent has expired its time credit."""


class BoardNotInitializedError(Exception):
    """Occurs when trying to board functions before it was initialized."""


class Viewer(Agent):
    """Interface for an Quoridor viewer and human agent."""

    def __init__(self) -> None:
        """Blank console viewer without a board."""
        self._board: Optional[Board] = None

    # I'm under the impression this is only for the gui, probably broken right now
    @abstractmethod
    def finished(self, steps: int, winner: int, reason: str = "") -> None:
        """The game is finished.

        Arguments:
        steps -- the number of steps played
        winner -- the winner (>0: even players, <0: odd players, 0: draw)
        reason -- a specific reason for the victory or "" if standard
        """

    @abstractmethod
    def playing(self, step: int, player: int) -> None:
        """Player player is currently playing step step."""

    @abstractmethod
    def update(self, step: int, action: Action, player: int) -> None:
        """Update the viewer after an action has been played.

        Arguments:
        step -- current step number
        action -- action played
        player -- player that has played

        """

    def init_viewer(self, board: Board) -> None:
        """Initialize the viewer with an initial board."""
        self._board = board

    def replay(self, trace: Trace, speed: float = 1.0, show_end: bool = False) -> None:
        """Replay a game given its saved trace."""
        step = 0
        self.init_viewer(trace.get_initial_board())

        for player, action, t in trace.actions:
            step += 1
            self.playing(step, player)
            if speed < 0:
                time.sleep(-t / speed)
            else:
                time.sleep(speed)
            self.update(step, action, player)

        self.finished(step, trace.winner, trace.reason)

    @property
    def board(self) -> Board:
        if not self._board:
            raise BoardNotInitializedError
        return self._board


class HeadlessViewer(Agent):
    """Dummy viewer implementation for headless mode."""
    def init_viewer(self, board: Board) -> None: ...

    def playing(self, step: int, player: int) -> None: ...

    def update(self, step: int, action: Action, player: int) -> None: ...

    def finished(self, steps: int, winner: int, reason: str = "") -> None: ...

    def play(self, percepts: Board, player: int, step: int, time_left: float) -> Action: ...


class ConsoleViewer(Viewer):
    """Simple console viewer."""

    def init_viewer(self, board: Board) -> None:
        super().init_viewer(board)
        print(self.board)

    def playing(self, step: int, player: int) -> None:
        print('Step', step, '- player', player, 'is playing')

    def update(self, step: int, action: Action, player: int) -> None:
        print('Step', step, '- player', player, 'has played', action)
        self.board.play_action(action, player)
        print(self.board)

    def play(self, percepts: Board, player: int, step: int, time_left: float) -> Action:
        line = str()
        while True:
            try:
                line = input(f'Player {player} plays (kind, i, j): ')
            except EOFError:
                exit(1)

            try:
                kind, i, j = [x.strip() for x in line.split(',')]
                return kind, int(i), int(j)
            except (ValueError, AssertionError):
                pass

    def finished(self, steps: int, winner: int, reason: str = "") -> None:
        print(f'Winner: P{winner}')
        if reason:
            print('Reason:', reason)


class Game:
    """Main Quoridor game class."""

    def __init__(self,
                 agents: List[Viewer],
                 board: Board,
                 viewer: Viewer = None,
                 time_credits: List[Optional[float]] = None,
                 trace: Trace = None,
                 player_names: List[str] = None):
        """New Quoridor game.

        Arguments:
        agents -- a sequence of 2 elements containing the agents (instances
            of Agent)
        board -- the board on which to play
        viewer -- the viewer or None if none should be used
        time_credits -- a sequence of 2 elements containing the time credit in
            seconds for each agent, or None for a time-unlimited agent.

        """
        self.agents = agents
        self.board = board
        self.viewer = viewer or HeadlessViewer()
        self.credits = time_credits or [None, None]
        self.starting_credits = self.credits.copy()
        self.step = 0
        self.player = 0
        self.trace = trace if trace is not None else Trace(board, self.credits, player_names or [])

    def play(self) -> None:
        """Play the game."""
        logging.info('Starting new game')
        self.viewer.init_viewer(self.board.clone())
        is_connected: List[bool] = [True] * self.board.player_count
        reasons: List[Tuple[Optional[int], str]] = [(None, "")] * self.board.player_count
        winning_order: List[int] = []

        for agent in range(self.board.player_count):
            try:
                logging.debug('Initializing agent %d', agent)
                self.timed_exec('initialize', self.board, [agent], agent=agent)
            except Exception:
                logging.info('Player %s is flagged as disconnected during initialisation', agent)
                is_connected[agent] = False
                reasons[agent] = (self.step, 'disconnected during Initialisation')
            self.player = (self.player + 1) % len(self.agents)

        disconnected_msg_template = 'Player %s is flagged as disconnected during play, reason:%s'

        while not self.board.is_finished() and (
                sum(is_connected) - sum(self.board.players_on_goal())) > 1 and (
                self.step < MAX_STEPS_GAME_OVER):
            if is_connected[self.player] and not self.board.is_player_on_goal(self.player):
                try:
                    self.step += 1
                    logging.debug('Asking player %d to play step %d', self.player, self.step)
                    self.viewer.playing(self.step, self.player)
                    self.credits[self.player] = self.starting_credits[self.player]
                    action, t = self.timed_exec('play', self.board, self.player, self.step)
                    self.board.play_action(action, self.player)
                    self.viewer.update(self.step, action, self.player)
                    self.trace.add_action(self.player, action, t)

                    if self.board.is_player_on_goal(self.player):
                        winning_order.append(self.player)

                except InvalidActionError as e:
                    logging.info(disconnected_msg_template, self.player, e)
                    is_connected[self.player] = False
                    reasons[self.player] = (self.step, f'Invalid action {e}')

                except TimeCreditExpiredError as e:
                    logging.info(disconnected_msg_template, self.player, e)
                    is_connected[self.player] = False
                    reasons[self.player] = (self.step, f'Timeout {e}')

                except Exception as e:
                    logging.info(disconnected_msg_template, self.player, e)
                    is_connected[self.player] = False
                    reasons[self.player] = (self.step, 'Unknown error')

            self.player = (self.player + 1) % len(self.agents)

        if sum(is_connected) == 0:
            reason = 'No one could connect.'
        elif sum(is_connected) == 1:
            reason = 'Opponent\'s have been expelled.'
        else:
            reason = ""

        if not winning_order:
            scores: Tuple[List[Score], List[Score]] = cast(
                Tuple[List[Score], List[Score]],
                self.partition(lambda x: cast(bool, is_connected[x[0]]), self.board.get_scores()))
            disconnected_scores, connected_scores = scores

            if not connected_scores:
                # whatever, last player wins! ¯\_(ツ)_/¯
                winner = self.board.player_count - 1
                self.trace.set_ranking([player for player, _ in disconnected_scores])
            else:
                winner_points = connected_scores[0]
                winner = winner_points[0]
                logging.info('Score: %d', winner_points[1])
                self.trace.set_ranking([player for player, _
                                        in chain(connected_scores, disconnected_scores)])

        else:
            winner = winning_order[0]
            # Append the last connected player not in the winning_order list
            connected_pawn = [player for player, _ in self.board.get_scores()
                              if is_connected[player]]
            winning_order.extend(player for player in connected_pawn
                                 if player not in winning_order)

            # Append disconnected players
            disconnected_scores, _ = self.partition(
                lambda x: cast(bool, is_connected[x[0]]), self.board.get_scores())
            winning_order.extend(player for player, _ in disconnected_scores)

            self.trace.set_ranking(winning_order)

        self.trace.set_reasons(reasons)

        logging.info('Winner: %d', winner)
        self.trace.set_winner(winner, reason)

        # I'm under the impression this is only for the gui, probably broken right now
        self.viewer.finished(self.step, winner, reason)

    def timed_exec(self, fn_name: str, *args: Any, agent: int = None) -> Tuple[Any, float]:
        """Execute a function with the time limit for the current
        player.

        This returns a tuple (result, t) with the function result and the time taken
        in seconds. If agent is None, the agent will be computed from
        self.player.
        """
        if agent is None:
            agent = self.player % len(self.agents)

        remaining_credits = self.credits[agent]
        if remaining_credits is not None:  # None == unlimited.
            logging.debug('Time left for agent %d: %f', agent, remaining_credits)
            if remaining_credits < 0:
                raise TimeCreditExpiredError
            socket.setdefaulttimeout(remaining_credits + 1)
        start = time.time()

        try:
            result = getattr(self.agents[agent], fn_name)(*args, self.credits[agent])
        except socket.timeout:
            self.credits[agent] = -1.0  # ensure it is counted as expired
            raise TimeCreditExpiredError
        except (socket.error, xmlrpc.client.Fault) as e:
            logging.error('Agent %d was unable to play step %d. Reason: %s', agent, self.step, e)
            raise InvalidActionError

        elapsed = time.time() - start
        logging.info('Step %d: received result %s in %fs', self.step, result, elapsed)

        if remaining_credits is not None:
            remaining_credits -= elapsed
            self.credits[agent] = remaining_credits
            logging.debug('New time credit for agent %d: %f', agent, remaining_credits)
            if remaining_credits < -0.5:  # small epsilon to be sure
                raise TimeCreditExpiredError

        return result, elapsed

    @staticmethod
    def partition(pred: Callable[..., bool], iterable: Iterable) -> Tuple[List, List]:
        """Use a predicate to partition entries into false entries and
        true entries.
        """
        # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
        t1, t2 = tee(iterable)
        return list(filterfalse(pred, t1)), list(filter(pred, t2))
