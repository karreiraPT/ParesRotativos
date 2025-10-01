import pandas as pd

def generate_doubles_matrix(doubles, players):
    matrix = pd.DataFrame(0, index=players, columns=players)

    for (j1, j2), count in doubles.items():
        matrix.loc[j1, j2] = count
        matrix.loc[j2, j1] = count

    return matrix


def generate_opponents_matrix(opponents, players):
    matrix = pd.DataFrame(0, index=players, columns=players)

    for (j1, j2), count in opponents.items():
        matrix.loc[j1, j2] = count
        matrix.loc[j2, j1] = count

    return matrix
