import * as xmlrpc from 'xmlrpc';
import * as yargs from 'yargs';
import {RandomBot} from './RandomBot';

var argv = yargs
  .number('p')
  .number('port')
  .argv
const PORT = argv.port || argv.p || 4000;
const server = xmlrpc.createServer( { host: '0.0.0.0', port: PORT }, () => {
    console.log(`Server listening on port ${PORT}`);
});

const agent = new RandomBot();

server.on('NotFound', function(method, params) {
    console.log('Method ' + method + ' does not exist');
});

// Handle method calls by listening for events with the method call name
server.on('initialize', (err, [board, players, timeLeft], callback) => {
    agent.initialize(board, players, timeLeft);
    callback(null, undefined);
});

server.on('play', (err, [percepts, player, step, timeLeft], callback) => {
    const action = agent.play(percepts, player, step, timeLeft);
    callback(null, action.asMove());
});
