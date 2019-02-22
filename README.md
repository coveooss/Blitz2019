# Coveo Blitz 2019

This is the source for the Coveo Blitz 2019

## Installation 

Install the dependancies in a virtual environment using tools like _virtualenv_, _pyenv_ or _conda_

`python -m pip install -r requirements.txt`

## Usage

To run the tests
`python -m unittest discover .`

To play a game 
`python __main__.py`

To save a game
`python __main__.py -w <filename>`

To visualize a replay
`python __main__py -r <filename>`

_* Please be aware that the python GUI only partially support 4 player games, for better support use the web UI_

The starterpack contains working clients for the main challenges and the microchallenges

The local_runner allows you to run the game as a "server" and connect your client from the starterpack agains pre-included adversary.

The ui folder contains a web interface to visualize the game.

## Microchallenges
Every microchallenge comes with an associated docker image.

To test the microchallenges

`cd microchallenges`

`python __main__.py` Use --help to view to available arguments.

ex. `python __main__.py water` to test the "water" problem

## Contributing
Pull requests are welcome. For major changes we recommand a fork, bug fixes are welcome. Please update tests as appropriate.



