from typing import TYPE_CHECKING

if TYPE_CHECKING:  # prevents circular references induced by annotations
    from game.board import Action


class InvalidActionError(Exception):
    """Raised when an invalid action is played."""

    def __init__(self,  action: 'Action' = None, player: int = -1):
        self.action = action
        self.player = player


class NoPathError(Exception):
    """Raised when a player puts a wall such that no path exists
    between a player and its goal row.
    """

    def __repr__(self) -> str:
        return 'Exception: no path to reach the goal'
