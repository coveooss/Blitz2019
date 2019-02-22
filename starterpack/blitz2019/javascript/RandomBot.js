const _ = require('lodash');
const {Board} = require('./Board');

const RandomBot = (function () {
    function RandomBot() {}

    RandomBot.prototype.initialize = function(board, players, timeLeft) {
        console.log('INIT');
    };

    RandomBot.prototype.play = function(percepts, player, step, timeLeft) {
        console.log('PLAY');

        const board = Board.fromPercepts(percepts);
        const actions = board.getActions(player);

        return actions[Math.floor(Math.random() * actions.length)];
    };

    return RandomBot;
}());

module.exports = {RandomBot};
