package com.coveo.rpc;

import java.util.Objects;

public class Coords {

  public Integer i;
  public Integer j;

  public Coords(Integer i, Integer j) {
    this.i = i;
    this.j = j;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    Coords coords = (Coords) o;
    return Objects.equals(i, coords.i) &&
        Objects.equals(j, coords.j);
  }

  @Override
  public int hashCode() {
    return Objects.hash(i, j);
  }
}
