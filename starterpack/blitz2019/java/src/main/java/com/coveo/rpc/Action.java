package com.coveo.rpc;
public class Action {
  public String actionType;
  public Coords coord;

  public Action(String actionType, Coords coord) {
    this.actionType = actionType;
    this.coord = coord;
  }
}
