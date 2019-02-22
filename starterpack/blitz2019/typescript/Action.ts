import {Coords} from './Coords';

export class Action {
    readonly actionType: string;
    readonly coord: Coords;

    constructor(actionType: string, coord: Coords) {
        this.actionType = actionType;
        this.coord = coord;
    }

    asMove() {
        return [this.actionType, this.coord.i, this.coord.j];
    }
}
