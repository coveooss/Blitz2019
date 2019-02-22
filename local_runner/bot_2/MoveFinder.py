from Position import *


class MoveFinder():
    @staticmethod
    def is_position_valid(p: Position):
        return p.column >= 0 and p.column <= 8 and p.line >= 0 and p.line <= 8

    @staticmethod
    def get_moves_sanitized(positions: []) -> []:
        return [m for m in positions if MoveFinder.is_position_valid(m)]

    @staticmethod
    def get_positions_str(positions: []) -> []:
        return [p.__str__() for p in positions]

    @staticmethod
    def get_moves_vertical_axis(position_from: Position, walls: []) -> []:
        """
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves_vertical_axis(Position(1,4), []))
        ['(1,3)', '(1,5)']
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves_vertical_axis(Position(1,4), [Position(1, 4)]))
        ['(1,3)']
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves_vertical_axis(Position(1,4), [Position(1, 3)]))
        ['(1,5)']
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves_vertical_axis(Position(1,4), [Position(1, 3), Position(1, 4)]))
        []
        """
        move_right = Position(position_from.line, position_from.column + 1)
        move_left = Position(position_from.line, position_from.column - 1)
        possible_moves = MoveFinder.get_moves_sanitized([move_left, move_right])
        if len(walls) == 0:
            return possible_moves

        moves = []
        # can go right?
        # (1,4) can move to (1,5)
        #  is there a wall at (1,4)
        if MoveFinder.is_position_valid(move_right) and position_from not in walls:
            moves.append(move_right)
        # can go left?
        # (1,4) can move to (1,3)
        #  is there a wall at (1,3)
        if MoveFinder.is_position_valid(move_left) and move_left not in walls:
            moves.append(move_left)
        return moves

    @staticmethod
    def get_moves_horizontal_axis(position_from: Position, walls: []) -> []:
        """
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves_horizontal_axis(Position(1,4), []))
        ['(0,4)', '(2,4)']
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves_horizontal_axis(Position(1,4), [Position(0, 4)]))
        ['(2,4)']
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves_horizontal_axis(Position(1,4), [Position(1, 4)]))
        ['(0,4)']
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves_horizontal_axis(Position(1,4), [Position(0, 4), Position(1, 4)]))
        []
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves_horizontal_axis(Position(0,4), [Position(0, 3), Position(0, 4)]))
        []
        """
        move_up = Position(position_from.line - 1, position_from.column)
        move_down = Position(position_from.line + 1, position_from.column)
        possible_moves = MoveFinder.get_moves_sanitized([move_up, move_down])
        if len(walls) == 0:
            return possible_moves

        moves = []
        # can go up?
        # (1,4) can move to (0,4)
        # is there a wall on (0,4)
        if MoveFinder.is_position_valid(move_up) and move_up not in walls:
            moves.append(move_up)
        # can go down?
        # (0,4) can move to (1,4)
        # is there a wall at (0,4)
        if MoveFinder.is_position_valid(move_down) and position_from not in walls:
            moves.append(move_down)
        return moves

    @staticmethod
    def get_moves(position_from: Position, walls:[]) -> set:
        """
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves(Position(1, 4), []))
        ['(1,3)', '(2,4)', '(0,4)', '(1,5)']
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves(Position(1, 4), [Position(0, 3)]))
        ['(1,3)', '(2,4)', '(0,4)', '(1,5)']
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves(Position(1, 4), [Position(0, 4)]))
        ['(1,3)', '(2,4)', '(1,5)']
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves(Position(1, 4), [Position(0, 4), Position(1, 4)]))
        ['(1,3)', '(2,4)']
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves(Position(1, 4), [Position(0, 4), Position(1, 4), Position(1, 4)]))
        ['(1,3)']
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves(Position(1, 4), [Position(0, 4), Position(1, 4), Position(1, 4), Position(1, 3)]))
        []
        >>> MoveFinder.get_positions_str(MoveFinder.get_moves(Position(0, 4), []))
        ['(0,3)', '(1,4)', '(0,5)']
        """
        moves = set(MoveFinder.get_moves_horizontal_axis(position_from, walls))
        return moves.union(MoveFinder.get_moves_vertical_axis(position_from, walls))
