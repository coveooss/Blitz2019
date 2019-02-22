import argparse

from flask import (
    Flask
)

# Create the application instance
app = Flask(__name__)

flip = True


# Create a URL route in our application for '/'
@app.route('/microchallenge')
def ping():
    global flip  # sue me
    flip = not flip
    if flip:
        print('Returning pong')
    else:
        print('Not pong')
    return 'pong' if flip else 'wrong'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='I can\'t decide pong.')
    parser.add_argument('port', metavar='port', type=int)

    args = parser.parse_args()
    app.run(port=args.port)
