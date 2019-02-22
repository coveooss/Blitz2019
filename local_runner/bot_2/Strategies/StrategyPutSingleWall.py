from Strategies import Strategy
from Position import *


class StrategyPutSingleWall(Strategy.Strategy):
    def __init__(self):
        self.moves = [GameMoveWallHorizontal(Position(0, 3))]

    def get(self, bot):
        for m in self.moves:
            yield m
