#!/usr/bin/env python3
from MoveFinder import *
from Strategies.StrategyPutSingleWall import StrategyPutSingleWall
from utils import *
from Strategies.StrategyAggregate import *
from Strategies.StrategyBoxPlayer import *
from Strategies.StrategyBeeLine import *
from Position import *


class RandomAgent(Agent):
    def __init__(self):
        print("Agent init.")
        self.player_move = 0
        self.player = -1
        self.board = None
        self.actions = list()
        self.pos_starting = None
        self.pos_current = None
        self.pos_goal = None
        self.pawn_moves_previous = list()
        self.goal_direction = Direction.NORTH
        self.strategies = None
        self.move_generator = None
        self.possible_pawn_actions = list()
        print("Agent init done.")

    def init_strategies(self):
        self.strategies = StrategyAggregate([StrategyBeeLine()])
        self.move_generator = self.strategies.get(self)

    def get_current_position(self) -> Position:
        l_c = self.board.pawns[self.player]
        return Position(l_c[0], l_c[1])

    def get_possible_pawn_positions(self):
        vw_expanded = []
        # expand vertical walls
        for w in self.board.verti_walls:
            vw_expanded.append(Position(w[0], w[1]))
            vw_expanded.append(Position(w[0] + 1, w[1]))
        # print('verti_walls expanded: {}'.format([m.__str__() for m in vw_expanded]))
        vertical_moves = MoveFinder.get_moves_vertical_axis(self.pos_current, vw_expanded)

        hw_expanded = []
        # expand horizontal walls
        for w in self.board.horiz_walls:
            hw_expanded.append(Position(w[0], w[1]))
            hw_expanded.append(Position(w[0], w[1] + 1))
        # print('horiz_walls expanded: {}'.format([m.__str__() for m in hw_expanded]))
        horizontal_moves = MoveFinder.get_moves_horizontal_axis(self.pos_current, hw_expanded)

        actions = list(set(vertical_moves).union(horizontal_moves))
        print('all possible actions: {}'.format([m.__str__() for m in actions]))
        return actions

    def get_position_goal(self) -> Position:
        return self.pos_goal

    def get_position_current(self):
        return self.pos_current

    def get_previous_pawn_moves(self) -> []:
        return self.pawn_moves_previous

    def get_goal_direction(self) -> Direction:
        direction = Direction.NORTH
        pos_goal = self.pos_goal
        if pos_goal.line == 8:
            direction = Direction.SOUTH
        elif pos_goal.line == 0:
            direction = Direction.NORTH
        elif pos_goal.column == 8:
            direction = Direction.WEST
        elif pos_goal.column == 0:
            direction = Direction.EAST
        else:
            print('No idea where to go...')
        print('Goal direction {}'.format(direction))
        return direction

    def find_goal(self):
        board_goal = self.board.goals[self.player][0]
        # player 0 and 1 are NORTH and SOUTH
        if self.player < 2:
            return Position(board_goal, self.pos_current.column)
        print('Unknown player index... Cannot resolve goal')
        return None

    def play(self, percepts, player, step, time_left):
        self.player = player
        self.board = dict_to_board(percepts)
        self.actions = list(self.board.get_actions(player))
        # is our first move
        self.pos_current = self.get_current_position()
        self.pos_goal = self.find_goal()
        if step <= len(self.board.pawns):
            self.pos_starting = self.pos_current
            self.goal_direction = self.get_goal_direction()
            self.init_strategies()
        self.possible_pawn_actions = self.get_possible_pawn_positions()
        print('--------------------------------')
        print('Step: {}, player: {}, player move: {}\nat: {}, goal: {}, goal direction: {}'.format(step, self.player, self.player_move, self.pos_current, self.pos_goal, self.goal_direction))
        # print('horiz_walls on board: {}'.format(self.board.horiz_walls))
        # print('verti_walls on board: {}'.format(self.board.verti_walls))
        # print('possible pawn moves: {}'.format([m.__str__() for m in self.get_possible_pawn_positions()]))
        print('Pawn moves to date: {}'.format([m.__str__() for m in self.pawn_moves_previous]))

        if step == 101:
            return GameMoveEnd().to_game_format()

        for m in self.move_generator:
            if m.is_pawn_move():
                self.pawn_moves_previous.append(Position(m.line, m.column))
            print('Next move: {}'.format(m))
            self.player_move += 1
            return m.to_game_format()

        print('No more move to do. END GAME.')
        return GameMoveEnd().to_game_format()

if __name__ == "__main__":
    agent = RandomAgent()
    agent_main(agent)
