using System;
using System.Collections.Generic;
using System.Linq;

namespace Blitz2019
{
    public static class Bot { 
        /*
         * Creates a new PlayerMove. Use it to move your pawn arround.
         */
        public static Move PlayerMove(Position position)
        {
            return new Move() { type = "P", position = position };
        }

        /*
         * Creates a new PlaceVerticalWall move. Use it to place a vertical wall.
         */
        public static Move PlaceVerticalWall(Position position)
        {
            return new Move() { type = "WV", position = position };
        }
        
        /*
         * Creates a new PlaceHorizontalWall move. Use it to place a horizontal wall.
         */
        public static Move PlaceHorizontalWall(Position position)
        {
            return new Move() { type = "WH", position = position };
        }
    }

    /*
     * Represent a location on the board.
     * Keep in mind that x and y can be null to indicate a direction instead!
     */
    public struct Position
    {
        public int? x;
        public int? y;
    }

    /*
     * Represent the game board and the current status of the game.
     */
    public class Board
    {
        public int size;
        public int rows;
        public int cols;
        public int starting_walls;
        public Position[] pawns;
        public Position[] goals;
        public int[] nb_walls;
        public Position[] horiz_walls;
        public Position[] verti_walls;

        /*
         * Dictates if you can move to the specified location.
         */
        public bool canMoveHere(Move action)
        {
            bool isInBound = action.position.x >= 0 && action.position.y >= 0 && 
                             action.position.x < size && action.position.y < size;

            bool isOnAnotherPlayer = (from pawm in pawns
                                      where action.position.x == pawm.x && action.position.y == pawm.y
                                      select true).FirstOrDefault();

            return isInBound && !isOnAnotherPlayer;
        }

        /*
         * Returns all the possible player moves that you can do.
         */
        public List<Move> getMoves(int player)
        {
            Position position = pawns[player];
            List<Move> possibleMoves = new List<Move>()
            {
                Bot.PlayerMove(new Position() {x = position.x + 1, y= position.y }),
                Bot.PlayerMove(new Position() {x = position.x - 1, y= position.y }),
                Bot.PlayerMove(new Position() {x = position.x, y= position.y + 1 }),
                Bot.PlayerMove(new Position() {x = position.x, y= position.y - 1}),
            };

            return possibleMoves.Where(move => canMoveHere(move)).ToList();
        }
    }

    /*
     * Represent a "Move" action
     */
    public struct Move
    {
        public string type;
        public Position position;
    }

    public interface IBot
    {
        /*
         * Called first when a new game starts.
         * Return true when you are ready.
         */
        Boolean initialize(Board board, int[] players, double? time_left);

        /*
         * Called for each "turn", you have to anser with a Move.
         * Moves can be a "Bot.PlaverMove()", "Bot.PlaceVerticalWall" or "Bot.PlaceHorizontalWall".
         */
        Move play(Board board, int player, int step, double? time_left);
    }
}
