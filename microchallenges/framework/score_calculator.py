import datetime
import logging
import re
from base64 import b64decode
from urllib.parse import urlparse


class Score:
    def __init__(self,
                 timestamp,
                 score,
                 request_number,
                 request_timestamp,
                 http_code,
                 problem,
                 expected,
                 answer):
        self.timestamp = timestamp
        self.score = score
        self.request_number = request_number
        self.request_timestamp = request_timestamp
        self.http_code = http_code
        self.problem = problem
        self.expected = expected
        self.answer = answer


class Results:
    def __init__(self):
        self.scores = []
        self.total = 0.0


def serialize(obj):
    """Serialize objects not JSON-serializable by default."""

    if isinstance(obj, Score):
        return obj.__dict__

    if isinstance(obj, datetime.timedelta):
        return obj.microseconds/1000

    return obj.__dict__


# https://stackoverflow.com/a/25878651
def parse_timestamp(timestamp: str):

    # This regex removes all colons and all
    # dashes EXCEPT for the dash indicating + or - utc offset for the timezone
    # also remove extra precision in the ns
    conformed_timestamp = re.sub(
        r'[:]|([-](?!((\d{2}[:]\d{2})|(\d{4}))$))|(?<=\.\d{6})\d*|[Z]', '', timestamp)

    # Split on the offset to remove it. Use a capture group to keep the delimiter
    split_timestamp = re.split(r'[+|-]', conformed_timestamp)
    main_timestamp = split_timestamp[0]
    if len(split_timestamp) == 3:
        sign = split_timestamp[1]
        offset = split_timestamp[2]
    else:
        sign = None
        offset = None

    # Generate the datetime object without the offset at UTC time
    output_datetime = datetime.datetime.strptime(main_timestamp + 'Z', '%Y%m%dT%H%M%S.%fZ')
    if offset:
        # Create timedelta based on offset
        offset_delta = datetime.timedelta(
            hours=int(sign + offset[:-2]),
            minutes=int(sign + offset[-2:]))

        # Offset datetime with timedelta
        output_datetime = output_datetime + offset_delta
    return output_datetime


def calculate_score(results: list, query_timeout: int, expected_responses: dict):
    game_result = Results()
    points: float = 0.0

    if results:
        start_time = parse_timestamp(results[0]['timestamp'])

        for result in results:
            request_url = urlparse(result['target']['url'])
            request_key = request_url.path + '?' + request_url.query
            expected = expected_responses[request_key]
            request_start_time = (
                parse_timestamp(result['timestamp']) - start_time).total_seconds()
            if result['error'] == "" and result['code'] == 200:
                response_time = result['latency']/1000000000.0
                point = 0.0
                answer = b64decode(result['body']).decode()
                if answer == str(expected):
                    point = max(0.0, query_timeout - response_time)
                    points += point

                    if point > 0.0:
                        logging.info(
                            ('Result accepted: %s  --- Expected %s (%s points in %ss) | '
                             'Received Http Code: %s | Request %s'),
                            answer,
                            expected,
                            point,
                            response_time,
                            result['code'],
                            result['target']['url'])
                    else:
                        logging.info(
                            ('Result rejected: %s  --- Expected %s | '
                             'Timed out after %ss | Received Http Code: %s | Request %s'),
                            answer,
                            expected,
                            response_time,
                            result['code'],
                            result['target']['url'])
                else:
                    logging.info(
                        ('Result rejected: %s  --- Expected %s (0.0 points in %ss) | '
                         'Received Http Code: %s | Request %s'),
                        answer, expected, response_time, result['code'], result['target']['url'])

                game_result.scores.append(
                    Score(request_start_time + response_time,
                          point, result['seq'],
                          request_start_time,
                          result['code'],
                          result['target']['url'].split('problem=', 1)[-1],
                          str(expected),
                          answer))
            else:
                logging.info('No result received  --- Expected %s | Request %s',
                             expected, result['target']['url'])
                game_result.scores.append(
                    Score(request_start_time + query_timeout,
                          0.0, result['seq'],
                          request_start_time, 0,
                          result['target']['url'].split('problem=', 1)[-1],
                          str(expected), ""))

    game_result.total = points
    return game_result
