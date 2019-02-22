#!/usr/bin/env python3
"""
Random agent for Blitz
Author: Cyrille Dejemeppe <cyrille.dejemeppe@uclouvain.be>
Author: Coveo blitz.coveo.com
Copyright (C) 2013, Undisclosed for Blitz

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""

import logging
import random


from utils import *


class RandomAgent(Agent):

    """A dumb random agent."""
    def play(self, percepts, player, step, time_left):
        board = dict_to_board(percepts)
        actions = list(board.get_actions(player))
        logging.info('step %s player %s actions %s',step, player, len(actions))
        return random.choice(actions)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        handlers=[
                            logging.FileHandler("bot_random.log"),
                            logging.StreamHandler()
                        ],
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logging.info("Starting the random_bot")

    agent_main(RandomAgent())
