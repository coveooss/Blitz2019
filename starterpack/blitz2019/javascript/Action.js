const Action = (function () {
    function Action(actionType, coord) {
        this.actionType = actionType;
        this.coord = coord;
    }

    Action.prototype.asMove = function() {
        return [this.actionType, this.coord.i, this.coord.j];
    };

    return Action;
}());

module.exports = {Action};
