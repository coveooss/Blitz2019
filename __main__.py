import csv
import json
import logging
import xmlrpc.client
from functools import partial
from operator import is_not
from typing import Union, Iterable, List

import jsonpickle

from game import gui
from game.game import ConsoleViewer, Game
from game.quoridor import Board
from game.trace import load_trace


def connect_agent(uri: str) -> xmlrpc.client.ServerProxy:
    """Connect to a remote player and return a proxy for the Player object."""
    return xmlrpc.client.ServerProxy(uri, allow_none=True)


def load_percepts(csvfile: Union[str, Iterable[str]]) -> List[List[int]]:
    """Load percepts from a CSV file.

    Cells are hexadecimal numbers.
    """
    if isinstance(csvfile, str):
        with open(csvfile, "r") as f:
            return load_percepts(f)

    percepts = []
    for hex_row in csv.reader(csvfile):
        if not hex_row:
            continue
        row: List[int] = [int(c.strip(), 16) for c in hex_row]
        percepts.append(row)
        assert len(row) == len(percepts[0]), "rows must have the same length"
    return percepts


class Result:
    def __init__(self, team_name, rank):
        self.team_name = team_name
        self.rank = rank


def result_serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, Result):
        return obj.__dict__

    return obj.__dict__


if __name__ == "__main__":
    import argparse

    def posfloatarg(string):
        value = float(string)
        if value <= 0:
            raise argparse.ArgumentTypeError("%s is not strictly positive" %
                                             string)
        return value

    parser = argparse.ArgumentParser(
        usage="%(prog)s [options] AGENT1 AGENT2 [AGENT3 AGENT4]\n" +
              "       %(prog)s [options] -r FILE")
    parser.add_argument("agent1", nargs='?', default='human',
                        help="URI of the first agent (blue player) or" +
                             " keyword 'human' (default: human)",
                        metavar="AGENT1")
    parser.add_argument("agent2", nargs='?', default='human',
                        help="URI of the second agent (red player) or" +
                             " keyword 'human' (default: human)",
                        metavar="AGENT2")
    parser.add_argument("agent3", nargs='?', default=None,
                        help="URI of the third agent (teal player) or" +
                             " keyword 'human' (default: None)",
                        metavar="AGENT3")
    parser.add_argument("agent4", nargs='?', default=None,
                        help="URI of the fourth agent (yellow player) or" +
                             " keyword 'human' (default: None)",
                        metavar="AGENT4")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="be verbose")
    parser.add_argument("-n", "--names", nargs='*', default=[],
                        help="names of the bots",
                        metavar="NAMES")
    parser.add_argument("-a", "--wall", nargs='*', default=[], type=int,
                        help="walls bots will starts with",
                        metavar="WALL")
    parser.add_argument("--no-gui",
                        action="store_false", dest="gui", default=True,
                        help="do not try to load the graphical user interface")
    parser.add_argument("-o", "--output", type=argparse.FileType('w'),
                        help="write the results to FILE",
                        metavar="OUTPUT")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--headless", action="store_true", default=False,
                   help="run without user interface (players cannot be" +
                        " human)")
    g.add_argument("-r", "--replay", type=argparse.FileType('r'),
                   help="replay the trace written in FILE",
                   metavar="FILE")
    parser.add_argument("-w", "--write", type=argparse.FileType('w'),
                        help="write the trace to FILE for replay with -r" +
                             " (no effect on replay)",
                        metavar="FILE")
    g = parser.add_argument_group("Rule options (no effect on replay)")
    g.add_argument("-t", "--time", type=posfloatarg,
                   help="set the time credit per player (default: untimed" +
                        " game)",
                   metavar="SECONDS")
    g.add_argument("--board", type=argparse.FileType('r'),
                   help="load initial board from FILE", metavar="FILE")
    g = parser.add_argument_group("Replay options")
    g.add_argument("-s", "--speed", type=posfloatarg,
                   help="set the duration of each step in seconds or scale" +
                        " if realtime (default: %(default)s)",
                   metavar="SECONDS", default=2.0)
    g.add_argument("--realtime", action="store_true", default=False,
                   help="replay with the real durations")
    args = parser.parse_args()
    if args.replay is None and args.headless and \
            (args.agent1 == "human" or args.agent2 == "human" or args.agent3 == "human" or args.agent4 == "human"):
        parser.error("human players are not allowed in headless mode")

    if args.realtime:
        args.speed = -args.speed

    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    logging.basicConfig(format="%(asctime)s -- %(levelname)s: %(message)s",
                        level=level)

    # Create initial board
    if args.replay is not None:
        # replay mode
        logging.info("Loading trace '%s'", args.replay.name)
        try:
            trace = load_trace(args.replay)
            args.replay.close()
        except (IOError, jsonpickle.UnpicklingError) as e:
            logging.error("Unable to load trace. Reason: %s", e)
            exit(1)
        board = trace.get_initial_board()
    elif args.board is not None:
        # load board
        logging.debug("Loading board from '%s'", args.board.name)
        try:
            percepts = load_percepts(args.board)
            args.board.close()
        except Exception as e:
            logging.warning("Unable to load board. Reason: %s", e)
            parser.error("argument --board: invalid board")
        board = Board(percepts, len(percepts.pawns))
    else:
        # default board
        board = Board(player_count= 2 if args.agent4 is None else 4, starting_walls=args.wall)

    # Create viewer
    if args.headless:
        args.gui = False
        viewer = None
    else:
        if args.gui:
            try:
                viewer = gui.TkViewer()
            except Exception as e:
                logging.warning("Unable to load GUI, falling back to" +
                        " console. Reason: %s", e)
                args.gui = False
        if not args.gui:
            viewer = ConsoleViewer()

    if args.replay is None:
        # Normal play mode
        print(args.agent1)
        agents = list(filter(partial(is_not, None),[args.agent1, args.agent2, args.agent3, args.agent4]))
        credits = [None, None, None, None][0:len(agents)]
        for i in range(len(agents)):
            if agents[i] == 'human':
                agents[i] = viewer
            else:
                logging.info("Connecting to agent %s", i)
                agents[i] = connect_agent(agents[i])
                credits[i] = args.time
        if len(args.names) > 0 and len(args.names) > len(agents):
            logging.error("Wrong player names count")
            exit(1)
        game = Game(agents, board, viewer, credits, None, args.names)

        def play():
            try:
                game.play()
            except KeyboardInterrupt:
                exit()
            if args.write is not None:
                logging.info("Writing trace to '%s'", args.write.name)
                try:
                    game.trace.write(args.write)
                    args.write.close()
                except IOError as e:
                    logging.error("Unable to write trace. Reason: %s", e)
            if args.gui:
                logging.debug("Replaying trace.")
                viewer.replay(game.trace, args.speed, show_end=True)
            if args.output is not None:
                logging.debug("Writting results")
                try:
                    if len(game.trace.player_names) > 0:
                        ranking = []
                        for rankIndex in range(0,len(game.trace.players_ranking)):
                            list.append(ranking, Result(game.trace.player_names[game.trace.players_ranking[rankIndex]], rankIndex))
                        for index in filter(lambda x: x not in game.trace.players_ranking, range(0, len(game.trace.player_names))):
                            list.append(ranking, Result(game.trace.player_names[index], 100))
                    else:
                        ranking = [Result(str(game.trace.winner), game.trace.winner)]
                    json.dump(ranking, args.output, default=result_serialize)
                    args.output.close()
                except IOError as e:
                    logging.error("Unable to write output, reason: %s", e)

        if args.gui:
            import threading
            threading.Thread(target=play).start()
            viewer.run()
        else:
            play()
    else:
        # Replay mode
        logging.debug("Replaying trace.")
        viewer.replay(trace, args.speed)
