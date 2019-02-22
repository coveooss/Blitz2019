import argparse

from flask import (
    Flask
)

# Create the application instance
app = Flask(__name__)


# Create a URL route in our application for '/'
@app.route('/microchallenge')
def ping():
    return 'wrong'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='THE worst pong.')
    parser.add_argument('port', metavar='port', type=int)

    args = parser.parse_args()
    app.run(port=args.port)
