"""
Common definitions for the Arlecchino players.
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
from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Callable, List, Optional

from xmlrpc.server import SimpleXMLRPCServer

from game.board import Board, Action


class Agent:
    """Interface for an Arlecchino agent."""

    def initialize(self, percepts: Board, players: List[int], time_left: float) -> None:
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

    @abstractmethod
    def play(self, percepts: Board, player: int, step: int, time_left: float) -> Optional[Action]:
        """Play and return an action.

        Arguments:
        percepts -- the current board in a form that can be fed to the Board
            constructor.
        player -- the player to control in this step
        step -- the current step number, starting from 1
        time_left -- a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.

        """


def serve_agent(agent: Agent, address: str, port: int) -> None:
    """Serve agent on specified bind address and port number."""
    server = SimpleXMLRPCServer((address, port), allow_none=True)
    server.register_instance(agent)
    print('Listening on ', address, ':', port, sep="")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def agent_main(agent: Agent,
               args_cb: Callable[[Agent, ArgumentParser], None] = None,
               setup_cb: Callable[[Agent, ArgumentParser, Namespace], None] = None) -> None:
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

    def portarg(string: str) -> int:
        value = int(string)
        if value < 1 or value > 65535:
            raise argparse.ArgumentTypeError(f'{string} is not a valid port number')
        return value

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bind', dest='address', default="",
                        help='bind to address ADDRESS (default: *)')
    parser.add_argument('-p', '--port', type=portarg, default=8000,
                        help='set port number (default: %(default)s)')
    if args_cb is not None:
        args_cb(agent, parser)
    args = parser.parse_args()
    if setup_cb is not None:
        setup_cb(agent, parser, args)

    serve_agent(agent, args.address, args.port)
