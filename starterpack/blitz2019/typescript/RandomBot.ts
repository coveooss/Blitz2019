import {Action} from './Action';
import {Board} from './Board';

export class RandomBot {
    initialize(board: any, players: number[], timeLeft: number | null) {
        console.log('INIT');
    }

    play(percepts: any, player: number, step: number, timeLeft: number | null) {
        console.log('PLAY');

        const board: Board = Board.fromPercepts(percepts);
        const actions: Action[] = board.getActions(player);

        return actions[Math.floor(Math.random() * actions.length)];
    };
}
