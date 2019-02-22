using System;
using System.Collections.Generic;

namespace Blitz2019
{
    /*
     * Sample bot - Random
     * 
     * This is a random bot to help you start in your journey.
     * Please do better than this.
     **/
    public class MyBot : IBot
    {
        /*
         * Called first when a new game starts.
         * Return true when you are ready.
         */
        public bool initialize(Board board, int[] players, double? time_left)
        {
            return true;
        }

        /*
         * Called for each "turn", you have to anser with a Move.
         * Moves can be a "Bot.PlaverMove()", "Bot.PlaceVerticalWall" or "Bot.PlaceHorizontalWall".
         */
        public Move play(Board board, int player, int step, double? time_left)
        {
            List<Move> possibleMoves = board.getMoves(player);
            return possibleMoves[new Random().Next(possibleMoves.Count)];
        }
    }
}