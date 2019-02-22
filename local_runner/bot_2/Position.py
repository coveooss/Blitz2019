from Direction import *
from GameMove import *


class Position:
    def __init__(self, line, column):
        self.line = line
        self.column = column
        self.directions = {Direction.NORTH: self.go_north,
                           Direction.SOUTH: self.go_south,
                           Direction.EAST: self.go_east,
                           Direction.WEST: self.go_west}

    def go_south(self):
        return Position(self.line + 1, self.column)

    def go_north(self):
        return Position(self.line - 1, self.column)

    def go_east(self):
        return Position(self.line, self.column + 1)

    def go_west(self):
        return Position(self.line, self.column - 1)

    def go(self, d:Direction):
        return self.directions[d]()

    def __str__(self):
        return '({},{})'.format(self.line, self.column)

    def __sub__(self, other):
        return Position(self.line - other.line, self.column - other.column)

    def to_game_format(self) -> tuple:
        return (GameMove.MOVE_PAWN, self.line, self.column)

    def __eq__(self, other: Position) -> bool:
        return self.line == other.line and self.column == other.column

    def __hash__(self) -> int:
        return self.line * 7 + self.column * 11

    def is_left_of(self, p: Position) -> bool:
        """
        >>> Position(1, 4).is_left_of(Position(1, 5))
        False
        >>> Position(1, 4).is_left_of(Position(1, 4))
        True
        >>> Position(1, 4).is_left_of(Position(1, 3))
        False
        >>> Position(1, 4).is_left_of(Position(1, 2))
        False
        >>> Position(1, 4).is_left_of(Position(0, 4))
        False
        >>> Position(1, 4).is_left_of(Position(0, 5))
        False
        """
        return self.line == p.line and self.column == p.column

    def is_right_of(self, p: Position) -> bool:
        """
        >>> Position(1, 4).is_right_of(Position(1, 5))
        False
        >>> Position(1, 4).is_right_of(Position(1, 4))
        False
        >>> Position(1, 4).is_right_of(Position(1, 3))
        True
        >>> Position(1, 4).is_right_of(Position(1, 2))
        False
        >>> Position(1, 4).is_right_of(Position(0, 4))
        False
        >>> Position(1, 4).is_right_of(Position(0, 5))
        False
        """
        return self.line == p.line and self.column - 1 == p.column