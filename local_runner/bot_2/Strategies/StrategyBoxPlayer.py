from Strategies import Strategy
from Position import *
import random

class StrategyBoxPlayer(Strategy.Strategy):
    def __init__(self, d: Direction):
        diff_horiz_wall = random.choice([0, 3])
        diff_vert_wall = 0 if diff_horiz_wall == 0 else 1
        if d.SOUTH:
            self.moves = [GameMoveWallVertical(Position(7, 4 - diff_vert_wall)),
                          GameMoveWallHorizontal(Position(6, 3 + diff_horiz_wall)),
                          GameMoveWallHorizontal(Position(6, 1 + diff_horiz_wall))]
        else:
            self.moves = [GameMoveWallVertical(Position(1, 4 - diff_vert_wall)),
                          GameMoveWallHorizontal(Position(2, 3 + diff_horiz_wall)),
                          GameMoveWallHorizontal(Position(2, 1 + diff_horiz_wall))]
        print('StrategyBoxPlayer moves: {}'.format([m.__str__() for m in self.moves]))

    def get(self, bot):
        for m in self.moves:
            print('StrategyBoxPlayer.get move: {}'.format(m.to_game_format()))
            yield m
