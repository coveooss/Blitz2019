# génère des pings, demande des pongs
def generate_inputs(nb_of_problems):
    inputs = []
    for i in range(nb_of_problems):
        inputs.append(('GET', f'/microchallenge?whatev={i}', None))
    return inputs


def generate_outputs(nb_of_problems):
    outputs = {}
    for i in range(nb_of_problems):
        # TODO Add body
        outputs[f'/microchallenge?whatev={i}'] = 'pong'
    return outputs


def generate_problem(nb_of_problems=15):
    return generate_inputs(nb_of_problems), generate_outputs(nb_of_problems)
