import Position


class GameMove:
    MOVE_WALL = 'W'
    MOVE_PAWN = 'P'

    def __init__(self, type, line: int, column: int):
        self.type = type
        self.line = line
        self.column = column

    def __str__(self):
        return "({}, {}, {})".format(self.type, self.line, self.column)

    def is_pawn_move(self):
        return self.type == GameMove.MOVE_PAWN

    def to_game_format(self):
        return (self.type, self.line, self.column)


class GameMoveEnd(GameMove):
    def __init__(self):
        super().__init__('E', 0, 0)


class GameMovePawn(GameMove):
    def __init__(self, p: Position):
        super().__init__(self.MOVE_PAWN, p.line, p.column)


class GameMoveWallVertical(GameMove):
    def __init__(self, p: Position):
        super().__init__('WV', p.line, p.column)


class GameMoveWallHorizontal(GameMove):
    def __init__(self, p: Position):
        super().__init__('WH', p.line, p.column)
