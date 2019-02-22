"""Quoridor board logic."""

from __future__ import annotations

from functools import partial
from typing import List, Tuple, Optional, Iterator

from game.constants import ACTION_TYPES, MOVE, WALL_H, WALL_V
from game.exceptions import InvalidActionError, NoPathError

ActionType = str
Action = Tuple[ActionType, int, int]

Position = Tuple[int, int]
Pawns = List[Position]
Walls = List[Position]

Goal = Tuple[Optional[int], Optional[int]]
Goals = List[Goal]


class InvalidPlayerCountError(Exception):
    """Raised when a player count is invalid (i.e. not 2 or 4)."""


class InvalidStartingWallsCountError(Exception):
    """Raised when the player count the amount of items in starting
    walls are not equal.
    """


class Board:
    size = 9 # 9x9 board; change this if you want to break anything (or do a PR...)
    rows = size
    cols = size
    outside_board_pos = (-rows - 1, -cols - 1)
    last_index = size - 1
    middle_index = int(size/2)

    """Representation of a Quoridor Board."""
    pawns: Pawns
    goals: Goals

    def __init__(self,
                 percepts: Board = None,
                 player_count: int = 2,
                 starting_walls: List[int] = None) -> None:
        """Initialize a representation for a quoridor game of size 9.

        The representation can also be initialized by a percepts.
        If percepts is None:
            Player 0 is position (Board.middle_index,0) and its goal is
            to reach row Board.last_index.
            Player 1 is position (Board.middle_index,Board.last_index)
            and its goal is to reach row 0.
            Each player owns 10 walls and there is initially no wall on
            the board.
        """
        if player_count not in (2, 4) or percepts and player_count != len(percepts.pawns):
            raise InvalidPlayerCountError()

        if starting_walls and len(starting_walls) != player_count:
            raise InvalidStartingWallsCountError

        self.player_count: int = player_count
        self.pawns, self.goals = self.default_pawns_and_goals(player_count)
        self.starting_wall_count = int(20 / player_count)  # 20 walls split evenly between players
        self.player_walls: List[int] = starting_walls or [self.starting_wall_count] * player_count
        self.horiz_walls: Walls = []
        self.verti_walls: Walls = []

        if percepts:
            for i in range(percepts.player_count):
                self.pawns[i] = percepts.pawns[i]
                self.goals[i] = percepts.goals[i]
                self.player_walls[i] = percepts.player_walls[i]

            for pos in percepts.horiz_walls:
                self.horiz_walls.append(pos)
            for pos in percepts.verti_walls:
                self.verti_walls.append(pos)

    def __str__(self) -> str:
        """Visual representation of the board in string format."""
        string_buffer: List[str] = []
        for i in range(self.size):
            for j in range(self.size):
                if self.pawns[0][0] == i and self.pawns[0][1] == j:
                    string_buffer += 'P0'
                elif self.pawns[1][0] == i and self.pawns[1][1] == j:
                    string_buffer += 'P1'
                elif len(self.pawns) > 2 and self.pawns[2][0] == i and self.pawns[2][1] == j:
                    string_buffer += 'P2'
                elif len(self.pawns) > 2 and self.pawns[3][0] == i and self.pawns[3][1] == j:
                    string_buffer += 'P3'
                else:
                    string_buffer += 'OO'
                if (i, j) in self.verti_walls:
                    string_buffer += '|'
                elif (i - 1, j) in self.verti_walls:
                    string_buffer += '|'
                else:
                    string_buffer += ' '
            string_buffer += '\n'
            for j in range(self.size):
                if (i, j) in self.horiz_walls:
                    string_buffer += '---'
                elif (i, j - 1) in self.horiz_walls:
                    string_buffer += '-- '
                elif (i, j) in self.verti_walls:
                    string_buffer += '  |'
                elif (i, j - 1) in self.horiz_walls and (i, j) in self.verti_walls:
                    string_buffer += '--|'
                else:
                    string_buffer += '   '
            string_buffer += '\n'

        return ''.join(string_buffer)

    def add_wall(self, pos: Position, is_horiz: bool, player: int) -> None:
        """Add a wall at specified Position.

        The wall is horizontal if is_horiz and is vertical otherwise.
        If it is not possible to add such a wall, nothing happens.
        """
        if self.player_walls[player] > 0 and self.is_wall_possible_here(pos, is_horiz):
            (self.horiz_walls if is_horiz else self.verti_walls).append(pos)
            self.player_walls[player] -= 1

    def can_move_here(self, i: int, j: int, player: int) -> bool:
        """Return True if the player can move to (i, j); False
        otherwise.
        """
        return self.is_pawn_move_ok(
            self.pawns[player], (i, j), self.get_other_player_positions(player))

    def clone(self) -> Board:
        """Return a clone of this object."""
        clone_board = Board(player_count=len(self.pawns))
        clone_board.pawns = self.pawns.copy()
        clone_board.goals = self.goals.copy()
        clone_board.player_walls = self.player_walls.copy()
        clone_board.horiz_walls = self.horiz_walls.copy()
        clone_board.verti_walls = self.verti_walls.copy()
        return clone_board

    def get_actions(self, player: int) -> List[Action]:
        """Return all the possible actions for the player's pawn."""
        return self.get_legal_pawn_moves(player) + self.get_legal_wall_moves(player)

    def get_min_steps_before_victory(self, player: int) -> int:
        """Return the minimum number of pawn moves necessary for the
        player to reach its goal row.
        """
        return len(self.get_shortest_path(player))

    def get_legal_pawn_moves(self, player: int) -> List[Action]:
        """Return the legal moves for the player's pawn."""
        x, y = self.pawns[player]
        positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
                     (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1),
                     (x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
        moves = []
        for new_pos in positions:
            if self.is_legal_pawn_move(player, (x, y), new_pos):
                moves.append((MOVE, new_pos[0], new_pos[1]))
        return moves

    def get_legal_wall_moves(self, player: int) -> List[Action]:
        """Return the legal wall placements (adding a wall somewhere)
        for the player's pawn.
        """
        positions: List[Position] = []
        moves: List[Action] = []
        if self.player_walls[player] <= 0:
            return moves
        for i in range(self.size - 1):
            for j in range(self.size - 1):
                positions.append((i, j))
        for pos in positions:
            if self.is_wall_possible_here(pos, True):
                moves.append((WALL_H, pos[0], pos[1]))
            if self.is_wall_possible_here(pos, False):
                moves.append((WALL_V, pos[0], pos[1]))
        return moves

    def get_other_player_positions(self, player: int) -> List[Position]:
        return [self.pawns[player_number] for player_number in range(self.player_count) if
                player_number != player]

    def get_score(self, player: int = 1) -> int:
        """Return a score for this board for the given player.

        The score is the difference between the theoretical max length
        of the shortest path of the player minus the current distance.
        """
        maximum_distance = 50
        return max(0, maximum_distance - self.get_min_steps_before_victory(player))

    def get_scores(self) -> List[Tuple[int, int]]:
        """Return the list of players with their scores in order."""
        player_scores: List[Tuple[int, int]] = list(
            map(lambda p: (p, self.get_score(p)), range(self.player_count)))
        return list(sorted(player_scores, key=lambda p: (p[1], self.player_walls[p[0]], p[0]),
                           reverse=True))

    def get_shortest_path(self, player: int) -> List:
        """Return a shortest path for player to reach its goal.

        If player is on its goal, the shortest path is an empty list.
        If no path exists, NoPathError is raised.
        """

        def get_pawn_moves(pos: Position) -> List[Position]:
            x, y = pos
            positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
                         (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1),
                         (x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
            moves: List[Position] = []
            for new_pos in positions:
                if self.is_legal_pawn_move(player, pos, new_pos):
                    moves.append(new_pos)
            return moves

        if self.is_on_goal(self.pawns[player], self.goals[player]):
            return []
        visited = [[False for _ in range(self.size)] for _ in range(self.size)]
        # Predecessor matrix in the BFS
        prede: List[List[Optional[Position]]] = [[None for _ in range(self.size)] for _ in
                                                 range(self.size)]
        neighbors = [self.pawns[player]]

        while neighbors:
            neighbor = neighbors.pop(0)
            x, y = neighbor
            visited[x][y] = True
            if self.is_on_goal(neighbor, self.goals[player]):
                succ = [neighbor]
                curr = prede[x][y]
                while curr is not None and curr != self.pawns[player]:
                    succ.append(curr)
                    x_, y_ = curr
                    curr = prede[x_][y_]
                succ.reverse()
                return succ
            unvisited_succ = [(x_, y_) for (x_, y_) in
                              get_pawn_moves(neighbor) if not visited[x_][y_]]
            for n_ in unvisited_succ:
                x_, y_ = n_
                if n_ not in neighbors:
                    neighbors.append(n_)
                    prede[x_][y_] = neighbor
        raise NoPathError()

    def is_action_valid(self, action: Action, player: int) -> bool:
        """Return True if the action played is valid; False
        otherwise.
        """
        if len(action) != 3:
            raise InvalidActionError(action, player)

        kind, i, j = action

        if kind not in ACTION_TYPES:
            return False

        if kind == MOVE:
            return self.is_pawn_move_ok(self.pawns[player], (i, j),
                                        self.get_other_player_positions(player))

        return self.player_walls[player] > 0 and (
            self.is_wall_possible_here((i, j), is_horiz=kind == WALL_H))

    def is_diagonal_move_legal(
            self, former_pos: Position, new_pos: Position, opponent_pos: Position) -> bool:
        """Return True if moving one pawn from former_pos to new_pos is
        valid.
        """
        x_form, y_form = former_pos
        x_new, y_new = new_pos
        x_op, y_op = opponent_pos

        # Move of 2 (above the opponent pawn) or diagonal
        def manhattan(pos1: Position, pos2: Position) -> int:
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

        if manhattan(former_pos, opponent_pos) + manhattan(opponent_pos, new_pos) == 2:
            ok = self.is_pawn_move_ok(opponent_pos, new_pos, [self.outside_board_pos]) and (
                 self.is_pawn_move_ok(former_pos, opponent_pos, [self.outside_board_pos])
            )
            if not ok:
                return False
            # Check if the move is in straight angle that there were no
            # possibility of moving straight ahead
            if abs(x_form - x_new) ** 2 + abs(y_form - y_new) ** 2 == 2:
                # There is a possibility of moving straight ahead leading the
                # move to be illegal
                return not self.is_pawn_move_ok(opponent_pos,
                                                (x_op + (x_op - x_form), y_op + (y_op - y_form)),
                                                [self.outside_board_pos])
            return True
        return False

    def is_finished(self) -> bool:
        """Return whether no more moves can be made (i.e., game finished)."""
        finished_count = sum([self.is_on_goal(self.pawns[pawn], self.goals[pawn])
                              for pawn in range(0, len(self.pawns))])
        return len(self.pawns) == finished_count + 1

    def is_legal_pawn_move(self,
                           player: int,
                           player_pos: Position,
                           new_position: Position) -> bool:
        opponent_positions = self.get_other_player_positions(player)
        return self.is_pawn_move_ok(player_pos, new_position, opponent_positions)

    def is_pawn_move_ok(self,
                        former_pos: Position,
                        new_pos: Position,
                        opponent_pos: List[Position]) -> bool:
        """Return True if moving one pawn from former_pos to new_pos is
        valid.
        """
        x_form, y_form = former_pos
        x_new, y_new = new_pos

        for (x_op, y_op) in opponent_pos:
            if (x_op == x_new and y_op == y_new) or (x_form == x_new and y_form == y_new):
                return False

        diagonal_moves = list(
            map(partial(self.is_diagonal_move_legal, former_pos, new_pos), opponent_pos)
        )
        return self.is_simplified_pawn_move_ok(former_pos, new_pos) or any(diagonal_moves)

    def is_player_on_goal(self, player: int) -> bool:
        return self.is_on_goal(self.pawns[player], self.goals[player])

    def is_simplified_pawn_move_ok(self, former_pos: Position, new_pos: Position) -> bool:
        """Return True if moving one pawn from former_pos to new_pos is
        valid (without the heap move above the opponent).
        """
        row_form, col_form = former_pos
        row_new, col_new = new_pos

        if (row_form == row_new and col_form == col_new) or (
                row_new >= self.size) or (
                row_new < 0) or (
                col_new >= self.size) or (
                col_new < 0):
            return False

        wall_right = any((r, col_form) in self.verti_walls for r in [row_form, row_form - 1])
        wall_left = any((r, col_form - 1) in self.verti_walls for r in [row_form - 1, row_form])
        wall_up = any((row_form - 1, c) in self.horiz_walls for c in [col_form - 1, col_form])
        wall_down = any((row_form, c) in self.horiz_walls for c in [col_form, col_form - 1])

        # check that the pawn doesn't move through a wall
        if row_new == row_form + 1 and col_new == col_form:
            return not wall_down
        if row_new == row_form - 1 and col_new == col_form:
            return not wall_up
        if row_new == row_form and col_new == col_form + 1:
            return not wall_right
        if row_new == row_form and col_new == col_form - 1:
            return not wall_left

        return False

    def is_wall_possible_here(self, pos: Position, is_horiz: bool) -> bool:
        """Return True if it is possible to put a wall at specified
        Position.

        Direction is specified by is_horiz.
        """
        x, y = pos
        if x >= self.size - 1 or x < 0 or y >= self.size - 1 or y < 0:
            return False

        if not (tuple(pos) in self.horiz_walls or tuple(pos) in self.verti_walls):
            wall_horiz_right = (x, y + 1) in self.horiz_walls
            wall_horiz_left = (x, y - 1) in self.horiz_walls
            wall_vert_up = (x - 1, y) in self.verti_walls
            wall_vert_down = (x + 1, y) in self.verti_walls

            if is_horiz:
                if wall_horiz_right or wall_horiz_left:
                    return False
                self.horiz_walls.append(pos)
                if not self.paths_exist:
                    self.horiz_walls.pop()
                    return False
                self.horiz_walls.pop()
                return True

            if wall_vert_up or wall_vert_down:
                return False
            self.verti_walls.append(pos)
            if not self.paths_exist:
                self.verti_walls.pop()
                return False
            self.verti_walls.pop()
            return True

        return False

    def move_pawn(self, new_pos: Position, player: int) -> None:
        """Modifify the state of the board to take into account the new
        position of the player's pawn.
        """
        self.pawns[player] = new_pos

    def play_action(self, action: Action, player: int) -> Board:
        """Play an Action if it is valid, or raise an
        InvalidActionError.
        """
        if not self.is_action_valid(action, player):
            raise InvalidActionError(action, player)

        try:
            kind, x, y = action
            if kind == WALL_H:
                self.add_wall((x, y), is_horiz=True, player=player)
            elif kind == WALL_V:
                self.add_wall((x, y), is_horiz=False, player=player)
            else:
                assert kind == MOVE
                self.move_pawn((x, y), player)

        except Exception as exception:
            raise InvalidActionError(action, player) from exception

        return self

    def players_on_goal(self) -> Iterator[bool]:
        return map(self.is_player_on_goal, range(self.player_count))

    def pretty_print(self) -> None:
        """Debug print the current state of players and walls."""
        for player_number in range(len(self.pawns)):
            print(f'Player {player_number} => pawn: {self.pawns[player_number]} '
                  f'goal: {self.goals[player_number]} '
                  f'nb walls: {self.player_walls[player_number]}')
        print('Horizontal walls:', self.horiz_walls)
        print('Vertical walls:', self.verti_walls)

    @property
    def paths_exist(self) -> bool:
        """Return True if there exists a path from all players to at
        least one of their respective goals; False otherwise.
        """
        try:
            for player in range(self.player_count):
                self.get_min_steps_before_victory(player)
        except NoPathError:
            return False
        return True

    @staticmethod
    def default_pawns_and_goals(player_count: int) -> Tuple[Pawns, Goals]:
        """Return the starting pawns and goals, given a player count."""
        assert player_count in (2, 4)

        last = Board.last_index
        middle = Board.middle_index
        if player_count == 2:
            pawns: Pawns = [(0, middle), (last, middle)]
            goals: Goals = [(last, None), (0, None)]
        else:
            pawns = [(0, middle), (middle, last), (last, middle), (middle, 0)]
            goals = [(last, None), (None, 0), (0, None), (None, last)]

        assert len(pawns) == player_count
        assert len(goals) == player_count

        return pawns, goals

    @staticmethod
    def is_on_goal(position: Position, goal: Goal) -> bool:
        return goal[0] in (None, position[0]) and (goal[1] in (None, position[1]))
