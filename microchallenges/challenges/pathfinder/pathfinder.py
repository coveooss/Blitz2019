import copy
import json
import random

import networkx
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


def generate_board(width=50, height=50, with_weight=False):
    if with_weight:
        board = [[int(numpy.random.choice([1, 10, 100, 1000]))] * width] * height
    else:
        board = [[1] * width] * height

    board[0][numpy.random.randint(0, height)] = 0
    board[width - 1][numpy.random.randint(0, height)] = 0

    return board


def find_solution(board_original):
    board = copy.deepcopy(board_original)

    start = (0, board[0].index(0))
    end = (len(board) - 1, board[len(board) - 1].index(0))

    g = networkx.grid_2d_graph(len(board), len(board[0]), create_using=networkx.DiGraph())

    for n in g.nodes:
        for e in g.out_edges(n):
            g[n][e[1]]['weight'] = board[e[1][0]][e[1][1]]

    return networkx.dijkstra_path_length(g, start, end)


def generate_problem(nb_of_problems=80):
    list_of_problem_data = []

    nb_of_problems = nb_of_problems + 2

    # Easy
    for _ in range(int(nb_of_problems / 10)):
        board = generate_board(5, 5, False)
        list_of_problem_data.append({'solution': find_solution(board), 'problem': board})

    # Pas facile
    for _ in range(int((nb_of_problems / 10) * 9)):
        board = generate_board(40, 40, True)
        list_of_problem_data.append({'solution': find_solution(board), 'problem': board})

    nb_item_to_duplicate = int(len(list_of_problem_data)/5)
    for _ in range(nb_item_to_duplicate):
        list_of_problem_data.pop()

    for _ in range(nb_item_to_duplicate):
        list_of_problem_data.append(random.choice(list_of_problem_data))

    return generate_inputs(list_of_problem_data), generate_outputs(list_of_problem_data)
