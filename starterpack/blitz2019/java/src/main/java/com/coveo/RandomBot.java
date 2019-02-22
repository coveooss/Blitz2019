package com.coveo;

import com.coveo.rpc.Action;
import com.coveo.rpc.Agent;
import com.coveo.rpc.Board;
import java.util.Hashtable;
import java.util.List;
import java.util.Random;
import java.util.Vector;

public class RandomBot implements Agent {

  public RandomBot() {
    System.out.println("constructeur");
  }

  @Override
  public Boolean initialize(Hashtable percepts, Vector players, Double time_left) {
    System.out.println("INIT");
    return true;
  }

  @Override
  public Object[] play(Hashtable percepts, int player, int step, Double time_left) {
    System.out.println("PLAY");
    Board board = Board.fromPercepts(percepts);
    List<Action> actions = board.getActions(player);

    Random rand = new Random();
    Action action = actions.get(rand.nextInt(actions.size()));
    return new Object[]{action.actionType, action.coord.i, action.coord.j};
  }
}
