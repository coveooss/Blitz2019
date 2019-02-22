from Strategies import Strategy
from Position import *


class StrategyBeeLine(Strategy.Strategy):
    def get_fn_cost(self, bot):
        # (0,4) -> (8,4) => MAX x (SOUTH)
        # (8,4) -> (0,4) => MIN x (NORTH)
        # (4,0) -> (4,8) => MAX Y (WEST)
        # (4,8) -> (4,0) => MIN Y (EAST)
        fn = int.__gt__
        direction = bot.goal_direction
        if direction == Direction.NORTH or direction == Direction.EAST:
            fn = int.__lt__
        print('Cost function: {}'.format(fn))
        return fn

    def get_fn_position_property(self, bot):
        def get_line(p: Position) -> int:
            return p.line

        def get_column(p: Position) -> int:
            return p.column

        fn = get_line
        direction = bot.goal_direction
        if direction == Direction.EAST or direction == Direction.WEST:
            fn = get_column
        print('Properties function: {}'.format(fn))
        return fn

    def get(self, bot):
        while len(bot.possible_pawn_actions) > 0:
            possible_pawn_positions = bot.possible_pawn_actions

            # ignore previous moves
            if len(possible_pawn_positions) > 1:
                previous_moves = bot.pawn_moves_previous
                possible_pawn_positions = [m for m in possible_pawn_positions if m not in previous_moves]

            pos_next = Position(possible_pawn_positions[0].line, possible_pawn_positions[0].column)
            fn_cost = self.get_fn_cost(bot)
            fn_property = self.get_fn_position_property(bot)
            goal = bot.pos_goal
            cost_to_beat = fn_property(pos_next) - fn_property(goal)
            for move in possible_pawn_positions:
                potential_new_cost = fn_property(move) - fn_property(goal)
                print('Cost to beat is {}, potential new cost {} ({})'.format(cost_to_beat, potential_new_cost, move))
                if fn_cost(potential_new_cost, cost_to_beat):
                    cost_to_beat = potential_new_cost
                    pos_next = move
                    print('New cost to beat {}, pos_next is {}'.format(potential_new_cost, pos_next))
            yield GameMovePawn(pos_next)
