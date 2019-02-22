package com.coveo.rpc;

import java.util.Arrays;
import java.util.Hashtable;
import java.util.List;
import java.util.stream.Collectors;

public class Board {
  private List<Coords> pawns;
  private List<Coords> goals;
  private List<Integer> nbWalls;
  private List<Coords> horizontalWalls;
  private List<Coords> verticalWalls;
  private int rows;
  private int cols;
  private int size;

  public Board(List<Coords> pawns, List<Coords> goals, List<Integer> nbWalls,
      List<Coords> horizontalWalls, List<Coords> verticalWalls, int rows, int cols, int size) {
    this.pawns = pawns;
    this.goals = goals;
    this.nbWalls = nbWalls;
    this.horizontalWalls = horizontalWalls;
    this.verticalWalls = verticalWalls;
    this.rows = rows;
    this.cols = cols;
    this.size = size;
  }

  private static Coords convertRawCoords(Object[] rawCoords) {
    return new Coords((Integer) rawCoords[0], (Integer) rawCoords[1]);
  }

  public static Board fromPercepts(Hashtable percepts) {
    List<Coords> pawns = Arrays.stream((Object[]) percepts.get("pawns"))
        .map(rawCoords -> Board.convertRawCoords((Object[]) rawCoords))
        .collect(Collectors.toList());
    List<Coords> goals = Arrays.stream((Object[])percepts.get("goals"))
        .map(rawCoords -> Board.convertRawCoords((Object[]) rawCoords))
        .collect(Collectors.toList());
    List<Integer> nbWalls = Arrays.stream((Object[]) percepts.get("nb_walls"))
        .map(nbWall -> (Integer) nbWall)
        .collect(Collectors.toList());
    List<Coords> horizontalWalls = Arrays.stream((Object[])percepts.get("horiz_walls"))
        .map(rawCoords -> Board.convertRawCoords((Object[]) rawCoords))
        .collect(Collectors.toList());
    List<Coords> verticalWalls = Arrays.stream((Object[])percepts.get("verti_walls"))
        .map(rawCoords -> Board.convertRawCoords((Object[]) rawCoords))
        .collect(Collectors.toList());
    int rows = (int)percepts.get("rows");
    int cols = (int)percepts.get("cols");
    int size =  (int)percepts.get("size");
    return new Board(pawns, goals, nbWalls, horizontalWalls, verticalWalls, rows, cols, size);
  }

  public boolean canMoveHere(Action action) {
    boolean isInBound = 0 <= action.coord.i && action.coord.i < this.size &&
                        0 <= action.coord.j && action.coord.j < this.size;
    boolean isOnAnotherPlayer = pawns.stream().anyMatch(coords -> action.coord.equals(coords));

    return isInBound && !isOnAnotherPlayer;
  }

  public List<Action> getActions(int player) {
    Coords coord = pawns.get(player);
    List<Action> actions = Arrays.asList(
        new Action("P", new Coords(coord.i + 1, coord.j)),
        new Action("P", new Coords(coord.i-1, coord.j)),
        new Action("P", new Coords(coord.i, coord.j + 1)),
        new Action("P", new Coords(coord.i, coord.j - 1))
      );

    return actions.stream().filter(this::canMoveHere).collect(Collectors.toList());
  }

  public List<Coords> getPawns() {
    return pawns;
  }

  public void setPawns(List<Coords> pawns) {
    this.pawns = pawns;
  }

  public List<Coords> getGoals() {
    return goals;
  }

  public void setGoals(List<Coords> goals) {
    this.goals = goals;
  }

  public List<Integer> getNbWalls() {
    return nbWalls;
  }

  public void setNbWalls(List<Integer> nbWalls) {
    this.nbWalls = nbWalls;
  }

  public List<Coords> getHorizontalWalls() {
    return horizontalWalls;
  }

  public void setHorizontalWalls(List<Coords> horizontalWalls) {
    this.horizontalWalls = horizontalWalls;
  }

  public List<Coords> getVerticalWalls() {
    return verticalWalls;
  }

  public void setVerticalWalls(List<Coords> verticalWalls) {
    this.verticalWalls = verticalWalls;
  }

  public int getRows() {
    return rows;
  }

  public void setRows(int rows) {
    this.rows = rows;
  }

  public int getCols() {
    return cols;
  }

  public void setCols(int cols) {
    this.cols = cols;
  }
}
