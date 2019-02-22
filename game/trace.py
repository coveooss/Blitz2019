from typing import List, Optional, Tuple, IO

import jsonpickle

from game.board import Board, Action


class Trace:

    """Keep track of a played game.

    Attributes:
    time_limits -- a sequence of 2 elements containing the time limits in
        seconds for each agent, or None for a time-unlimitted agent
    initial_board -- the initial board
    actions -- list of tuples (player, action, time) of the played action.
        Respectively, the player number, the action and the time taken in
        seconds.
    winner -- winner of the game
    reason -- specific reason for victory or "" if standard
    """

    def __init__(self,
                 board: Board,
                 time_limits: List[Optional[float]],
                 player_names: List[str] = None) -> None:
        """Initialize the trace.

        Arguments:
        board -- the initial board
        time_limits -- a sequence of 2 elements containing the time limits in
            seconds for each agent, or None for a time-unlimited agent
        player_names -- names of the players on the board, in corresponding order
        """
        self.time_limits = time_limits
        self.initial_board = board.clone()
        self.actions: List[Tuple[int, Action, float]] = []
        self.winner = 0
        self.reason = ""
        self.player_names = player_names or []
        self.players_ranking: List[int] = []
        self.reasons: List[Tuple[Optional[int], str]] = []

    def add_action(self, player: int, action: Action, t: float) -> None:
        """Add an action to the trace.

        Arguments:
        player -- the player
        action -- the played action, a tuple as specified by
            avalam.Board.play_action
        t -- a float representing the number of seconds the player has taken
            to generate the action
        """
        self.actions.append((player, action, t))

    def set_winner(self, winner: int, reason: str) -> None:
        """Set the winner.

        Arguments:
        winner -- the winner
        reason -- the specific reason of victory
        """
        self.winner = winner
        self.reason = reason

    def set_ranking(self, players_ranking: List[int]) -> None:
        self.players_ranking = players_ranking

    def set_reasons(self, reasons: List[Tuple[Optional[int], str]]) -> None:
        self.reasons = reasons

    def get_initial_board(self) -> Board:
        """Return a Board instance representing the initial board."""
        return Board(self.initial_board, len(self.initial_board.pawns))

    def write(self, f: IO) -> None:
        """Write the trace to a file."""
        f.write(jsonpickle.encode(self))


class CannotLoadTrace(Exception):
    """Occurs when the trace cannot be un-pickled."""


def load_trace(f: IO) -> Trace:
    """Load a trace from a file."""
    trace = jsonpickle.decode(f.read())
    if isinstance(trace, Trace):
        return trace
    raise CannotLoadTrace
