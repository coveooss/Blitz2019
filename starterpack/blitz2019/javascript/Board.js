const _ = require('lodash');
const {Coords} = require('./Coords');
const {Action} = require('./Action');

const Board = (function () {
    function Board(pawns, goals, nbWalls, horizontalWalls, verticalWalls, rows, cols, size) {
        this.pawns = pawns;
        this.goals = goals;
        this.nbWalls = nbWalls;
        this.horizontalWalls = horizontalWalls;
        this.verticalWalls = verticalWalls;
        this.rows = rows;
        this.cols = cols;
        this.size = size;
    }

    Board.prototype.canMoveHere = function (action) {
        const isInBound = 0 <= action.coord.i
            && action.coord.i < this.size
            && 0 <= action.coord.j && action.coord.j < this.size;
        const isOnAnotherPlayer = _.some(this.pawns, (coords) => _.isEqual(action.coord, coords));

        return isInBound && !isOnAnotherPlayer;
    };

    Board.prototype.getActions = function(player) {
        const coord = this.pawns[player];
        const actions = [
            new Action("P", new Coords(coord.i + 1, coord.j)),
            new Action("P", new Coords(coord.i - 1, coord.j)),
            new Action("P", new Coords(coord.i, coord.j + 1)),
            new Action("P", new Coords(coord.i, coord.j - 1)),
        ];

        return actions.filter((action) => this.canMoveHere(action));
    };

    Board._convertRawCoords = function([i, j]) {
        return new Coords(i, j);
    };

    Board.fromPercepts = function(percepts) {
        const pawns = percepts.pawns.map(Board._convertRawCoords);
        const goals = percepts.goals.map(Board._convertRawCoords);
        const horizontalWalls = percepts.horiz_walls.map(Board._convertRawCoords);
        const verticalWalls = percepts.verti_walls.map(Board._convertRawCoords);
        const {nbWalls, rows, cols, size} = percepts;

        return new Board(pawns, goals, nbWalls, horizontalWalls, verticalWalls, rows, cols, size);
    };

    return Board;
}());

module.exports = {Board};
