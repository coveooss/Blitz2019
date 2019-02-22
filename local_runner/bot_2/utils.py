# """
# Common definitions for the Arlecchino players.
# Author: Cyrille Dejemeppe <cyrille.dejemeppe@uclouvain.be>
# Copyright (C) 2013, Université catholique de Louvain
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# """

import random
import itertools
import operator
from functools import partial


class InvalidAction(Exception):
    """Raised when an invalid action is played."""

    def __init__(self, action=None, player=-1):
        self.action = action
        self.player = player


class NoPath(Exception):
    """Raised when a player puts a wall such that no path exists
    between a player and its goal row"""
    def __repr__(self):
        return "Exception: no path to reach the goal"


class Board:

    """
    Representation of a Quoridor Board.

    """

    def __init__(self):
        self.size = 9
        self.rows = self.size
        self.cols = self.size
        self.pawns = [] # whatever, will be filled with what we receive from the network
        self.goals = [] # whatever, will be filled with what we receive from the network
        self.nb_walls = [] # whatever, will be filled with what we receive from the network
        self.horiz_walls = []
        self.verti_walls = []

    def clone(self):
        """Return a clone of this object."""
        clone_board = Board()
        for i in range(0, len(self.pawns)):
            clone_board.pawns[i] = self.pawns[i]
            clone_board.goals[i] = self.goals[i]
            clone_board.nb_walls[i] = self.nb_walls[i]

        for (x, y) in self.horiz_walls:
            clone_board.horiz_walls.append((x, y))
        for (x, y) in self.verti_walls:
            clone_board.verti_walls.append((x, y))
        return clone_board

    def can_move_here(self, action):
        action_type, i, j = action
        is_in_bound = 0 <= i < self.size and 0 <= j < self.size
        is_on_another_player = (i, j) in self.pawns

        return is_in_bound and not is_on_another_player

    def get_actions(self, player):
        """Returns legal moves for the pawn of player."""
        (x, y) = self.pawns[player]
        return list(filter(self.can_move_here, [('P', x + 1, y), ('P', x - 1, y), ('P', x, y + 1), ('P', x, y - 1)]))


def dict_to_board(dictio):
    """Return a clone of the board object encoded as a dictionary."""
    clone_board = Board()
    for i in range(len(dictio['pawns'])):
        clone_board.pawns = dictio['pawns'].copy()
        clone_board.goals = dictio['goals'].copy()
        clone_board.nb_walls = dictio['nb_walls'].copy()
    for (x, y) in dictio['horiz_walls']:
        clone_board.horiz_walls.append((x, y))
    for (x, y) in dictio['verti_walls']:
        clone_board.verti_walls.append((x, y))

    return clone_board


class Agent:

    """Interface for an Arlecchino agent"""

    def initialize(self, percepts, players, time_left):
        """Begin a new game.

        The computation done here also counts in the time credit.

        Arguments:
        percepts -- the initial board in a form that can be fed to the Board
            constructor.
        players -- sequence of players this agent controls
        time_left -- a float giving the number of seconds left from the time
            credit for this agent (all players taken together). If the game is
            not time-limited, time_left is None.

        """
        pass

    def play(self, percepts, player, step, time_left):
        """Play and return an action.

        Arguments:
        percepts -- the current board in a form that can be fed to the Board
            constructor.
        player -- the player to control in this step
        step -- the current step number, starting from 1
        time_left -- a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.

        """
        pass


def serve_agent(agent, address, port):
    """Serve agent on specified bind address and port number."""
    from xmlrpc.server import SimpleXMLRPCServer
    server = SimpleXMLRPCServer((address, port), allow_none=True)
    server.register_instance(agent)
    print("Listening on ", address, ":", port, sep="")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def agent_main(agent, args_cb=None, setup_cb=None):
    """Launch agent server depending on arguments.

    Arguments:
    agent -- an Agent instance
    args_cb -- function taking two arguments: the agent and an
        ArgumentParser. It can add custom options to the parser.
        (None to disable)
    setup_cb -- function taking three arguments: the agent, the
        ArgumentParser and the options dictionary. It can be used to
        configure the agent based on the custom options. (None to
        disable)

    """
    import argparse

    def portarg(string):
        value = int(string)
        if value < 1 or value > 65535:
            raise argparse.ArgumentTypeError("%s is not a valid port number" %
                                             string)
        return value

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind", dest="address", default="",
                        help="bind to address ADDRESS (default: *)")
    parser.add_argument("-p", "--port", type=portarg, default=8010,
                        help="set port number (default: %(default)s)")
    if args_cb is not None:
        args_cb(agent, parser)
    args = parser.parse_args()
    if setup_cb is not None:
        setup_cb(agent, parser, args)

    serve_agent(agent, args.address, args.port)
