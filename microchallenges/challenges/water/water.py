import json
import random

import numpy


def generate_inputs(list_of_problem_data):
    inputs = []
    for problem_data in list_of_problem_data:
        problem = json.dumps(problem_data['problem'], separators=(',', ':'))
        inputs.append(('GET', f'/microchallenge?problem={problem}', None))
    return inputs


def generate_outputs(list_of_problem_data):
    outputs = {}

    for problem_data in list_of_problem_data:
        problem = json.dumps(problem_data['problem'], separators=(',', ':'))
        outputs[f'/microchallenge?problem={problem}'] = problem_data['solution']

    return outputs


def solve_water(data):
    right_maximums = [data[-1]]  # list to hold all right maximums by index
    for value in data[-2::-1]:
        right_maximums.append(max(value, right_maximums[-1]))
    right_maximums = right_maximums[-1::-1]  # done computing right maximums

    left_maximum = data[0]  # current left maximum while iterating
    water = 0

    for i, value in enumerate(data[1:], 1):
        if value >= left_maximum:
            left_maximum = value
            continue  # if value is the new left_maximum or equals it, then there is no water here
        if value < right_maximums[i]:  # value has to be lower than right and left to hold water
            water += min(left_maximum, right_maximums[i]) - value

    return water


def generate_problem(nb_of_problems=15):
    list_of_problem_data = []

    nb_of_problems = nb_of_problems + 2
    for _ in range(int(nb_of_problems / 10)):
        data: list = numpy.random.randint(0, 10, 5).tolist()
        list_of_problem_data.append({'solution': solve_water(data), 'problem': data})

    for _ in range(int((nb_of_problems / 10) * 9)):
        data: list = numpy.random.randint(0, 10, 4000).tolist()
        list_of_problem_data.append({'solution': solve_water(data), 'problem': data})

    nb_item_to_duplicate = int(len(list_of_problem_data) / 5)
    for _ in range(nb_item_to_duplicate):
        list_of_problem_data.pop()

    for _ in range(nb_item_to_duplicate):
        list_of_problem_data.append(random.choice(list_of_problem_data))

    return generate_inputs(list_of_problem_data), generate_outputs(list_of_problem_data)
