package com.coveo.rpc;

import java.util.Hashtable;
import java.util.Vector;

public interface Agent {
  Boolean initialize(Hashtable percepts, Vector players, Double time_left);
  Object[] play(Hashtable percepts, int player, int step, Double time_left);
}
