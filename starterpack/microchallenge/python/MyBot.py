import argparse

from flask import (
    Flask,
    request
)

app = Flask(__name__)

@app.route('/microchallenge')
def microchallenge():
    print("\n\n\n-------------------------- REQUEST LOGS STARTING HERE --------------------------")
    print("You can log stuff and download the logs from the UI in the replay section.")
    print("Here is the current problem:")
    print(request.args.get('problem')); # problem is in json format
    print("---------------------------------------------------------------------------------")
    
    return str(18)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Microchallenge Starter Pack')
    parser.add_argument('-p', metavar='p', type=int)

    args = parser.parse_args()
    app.run(port=args.p, host="0.0.0.0")