import json
import logging
import os
import signal
import subprocess
import time

from challenges.pingpong import pingpong
from challenges.pathfinder import pathfinder
from challenges.subsetsum import subsetsum
from challenges.water import water
from .score_calculator import calculate_score, serialize


# TODO: Split that baby <3
def main(challenge_name: str,
         replay_file: str,
         results_json_file: str,
         service_url: str,
         team_name: str,
         max_timeout: int,
         connect_timeout: int,
         duration: int,
         rate: int = 5):

    pinput = []
    expected_output = {}
    # Générer des problèmes & Solution
    if challenge_name == 'pingpong':
        pinput, expected_output = pingpong.generate_problem(rate * duration)
    if challenge_name == 'pathfinder':
        pinput, expected_output = pathfinder.generate_problem(rate * duration)
    if challenge_name == 'subsetsum':
        pinput, expected_output = subsetsum.generate_problem(rate * duration)
    if challenge_name == 'water':
        pinput, expected_output = water.generate_problem(rate * duration)

    # Attendre 30 secondes pour l'initiation du programme étudiant
    # TODO: Attente active
    logging.info('Waiting for student app to connect')
    time.sleep(connect_timeout)

    # TODO: Test de connectivité
    # ??? (PROFIT)

    # Attaque végéta
    # TODO: Valider la présence de végéta
    input_list = list(
        map(lambda input_tuple: input_tuple[0] + ' ' + service_url + input_tuple[1], pinput))
    # for line in input_list:
    #     if len(line) > 8192:
    #         logging.warning('Line too long for some webservers:/ ')

    formatted_input = '\n'.join(input_list)

    # Can't use StringIO because it doesn't fully respect the interface of BaseIO and doesn't
    # support fileno -_-'
    input_file_name = 'input1'
    with open(input_file_name, mode='w') as finput:
        finput.writelines(formatted_input)

    logging.info('====== WARMUP =======')
    with open(input_file_name, mode='r') as finput:
        warmup = subprocess.Popen(
            ['vegeta attack -duration 5s -connections 1 -rate 1/1s | vegeta encode -to json'],
            shell=True,
            stdout=subprocess.PIPE,
            stdin=finput)
        warmup.send_signal(signal.SIGINT)
        warmup.terminate()
        warmup.kill()
        time.sleep(6)
    logging.info('====== END WARMUP =======')
    logging.info('====== STARTING EVALUATION =======')

    with open(input_file_name, mode='r') as finput:
        process = subprocess.Popen(
            [f'vegeta attack -duration {duration}s -connections 1 '
             f'-rate {rate}/1s | vegeta encode -to json'],
            shell=True,
            stdout=subprocess.PIPE,
            stdin=finput)

    os.remove(input_file_name)

    start_time = time.time()
    while (process.poll() is None) and ((time.time() - start_time) < max_timeout):
        logging.info('Waiting for the end')
        time.sleep(min(duration, 5))

    logging.info('Waited: %ss', str(time.time() - start_time))

    process.send_signal(signal.SIGINT)
    process.terminate()

    logging.info('After kill after %ss', str(time.time() - start_time))

    # TODO: Arrêter de lire si on attend trop longtemps
    results = []
    if process.stdout is not None:
        results = list(map(json.loads, iter(process.stdout.readline, b'')))

    if process.stderr is not None:
        for line in iter(process.stderr.readline, b''):
            logging.info(line.rstrip())

    process.kill()

    result = calculate_score(results, 1, expected_output)

    with open(replay_file, 'w') as output:
        output.writelines(str(json.dumps(result, default=serialize)))

    with open(results_json_file, 'w') as results_file:
        results = [{'teamName': team_name, 'score': result.total, 'rank': 1}]
        json.dump(results, results_file)

    return result.total
