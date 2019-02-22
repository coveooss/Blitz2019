import * as _ from 'lodash';
import {Coords} from './Coords';
import {Action} from './Action';

export class Board {
    constructor(
        public pawns: Coords[],
        public goals: Coords[],
        public nbWalls: number[],
        public horizontalWalls: Coords[],
        public verticalWalls: Coords[],
        public rows: number,
        public cols: number,
        public size: number
    ) {}

    canMoveHere(action: Action): boolean {
        const isInBound = 0 <= action.coord.i
                          && action.coord.i < this.size
                          && 0 <= action.coord.j && action.coord.j < this.size;
        const isOnAnotherPlayer = _.some(this.pawns, (coords) => _.isEqual(action.coord, coords));

        return isInBound && !isOnAnotherPlayer;
    }

    getActions(player: number): Action[] {
        const coord = this.pawns[player];
        const actions = [
            new Action("P", new Coords(coord.i + 1, coord.j)),
            new Action("P", new Coords(coord.i - 1, coord.j)),
            new Action("P", new Coords(coord.i, coord.j + 1)),
            new Action("P", new Coords(coord.i, coord.j - 1)),
        ];

        return actions.filter((action: Action) => this.canMoveHere(action));
    };

    private static convertRawCoords([i, j]: number[]): Coords {
        return new Coords(i, j);
    }

    static fromPercepts(percepts): Board {
        const pawns = percepts.pawns.map(Board.convertRawCoords);
        const goals = percepts.goals.map(Board.convertRawCoords);
        const horizontalWalls = percepts.horiz_walls.map(Board.convertRawCoords);
        const verticalWalls = percepts.verti_walls.map(Board.convertRawCoords);
        const {nbWalls, rows, cols, size} = percepts;

        return new Board(pawns, goals, nbWalls, horizontalWalls, verticalWalls, rows, cols, size);
    }
}
