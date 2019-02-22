import * as express from 'express';
import {Request, Response} from 'express';
import * as yargs from 'yargs';

const app = express();
var argv = yargs
    .number('p')
    .number('port')
    .argv
const PORT = argv.port || argv.p || 8010;

app.get('/microchallenge', (req:Request, res:Response) => {
    console.log("\n\n\n-------------------------- REQUEST LOGS STARTING HERE --------------------------");
    console.log("You can log stuff and download the logs from the UI in the replay section.");
    console.log("Here is the current problem:");
    console.log(req.query.problem); // problem is in json format
    console.log("---------------------------------------------------------------------------------");

    res.send((18).toString());
});

app.listen(PORT, () => {
    console.log(`Example app listening on port ${PORT}!`)
});
