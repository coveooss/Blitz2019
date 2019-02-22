import json
import random

import numpy


def generate_inputs(problem_data):
    inputs = []
    for problem in problem_data:
        problem = json.dumps(problem, separators=(',', ':'))
        inputs.append(('GET', f'/microchallenge?problem={problem}', None))
    return inputs


def generate_problem_data(number_of_problems=50):
    problem_data = []
    for _ in range(number_of_problems):
        sampler = numpy.random.uniform(10.0, 1000.0, numpy.random.randint(10, 100))
        problem_data.append([int(i) for i in sampler.tolist()])

    return problem_data


def compute_answer_for_array(data, test_candidate):
    # Time complexity of the above solution is O(testCandidate*len(data)).

    # Cleanup big values
    data = [d for d in data if d <= test_candidate]

    # The value of subset[i][j] will be
    # true if there is a
    # subset of set[0..j-1] with sum equal to i
    subset = ([[False for _ in range(test_candidate + 1)] for _ in range(len(data)+1)])

    # If sum is 0, then answer is true
    for i in range(len(data)+1):
        subset[i][0] = True

        # If sum is not 0 and set is empty,
        # then answer is false
        for j in range(1, test_candidate + 1):
            subset[0][j] = False

        # Fill the subset table in botton up manner
        for j in range(1, len(data)+1):
            for k in range(1, test_candidate + 1):
                if k < data[j-1]:
                    subset[j][k] = subset[j-1][k]
                if k >= data[j-1]:
                    subset[j][k] = (subset[j-1][k] or
                                    subset[j - 1][k-data[j-1]])

    return subset[len(data)][test_candidate]


def generate_outputs(problem_data):
    outputs = {}
    for problem in problem_data:
        sum_ = 0

        for data in problem['data']:
            if compute_answer_for_array(data, problem['test']):
                sum_ = sum_+1

            outputs['/microchallenge?problem=' + json.dumps(problem, separators=(',', ':'))] = sum_
    return outputs


def generate_problem(nb_of_problems=15):
    list_of_problem_data = []
    for i in range(nb_of_problems):
        list_of_problem_data.append(
            {'test': numpy.random.randint(10, 500),
             'data': generate_problem_data(2 * (i % 5) + 5)
             })

    nb_item_to_duplicate = int(len(list_of_problem_data) / 5)
    for i in range(nb_item_to_duplicate):
        list_of_problem_data.pop()

    for i in range(nb_item_to_duplicate):
        list_of_problem_data.append(random.choice(list_of_problem_data))

    return generate_inputs(list_of_problem_data), generate_outputs(list_of_problem_data)
