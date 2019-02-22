from Strategies import Strategy


class StrategyAggregate(Strategy.Strategy):
    def __init__(self, strategies: []):
        self.strategies = strategies

    def get(self, bot):
        for s in self.strategies:
            for m in s.get(bot):
                yield m


if __name__ == "__main__":
    from .StrategyBoxPlayer import *
    from .StrategyBeeLine import *
    strats = StrategyAggregate([StrategyBoxPlayer(), StrategyBeeLine()])
    for m in strats.get():
        print(m)

