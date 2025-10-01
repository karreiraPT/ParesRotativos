from collections import defaultdict

def count_duels_by_player(schedule):
    duels = defaultdict(int)

    for game in schedule:
        if game['Dupla 1'] == "—":
            continue

        dupla1 = [j.strip() for j in game['Dupla 1'].split(" & ")]
        dupla2 = [j.strip() for j in game['Dupla 2'].split(" & ")]

        for j1 in dupla1:
            for j2 in dupla2:
                par = tuple(sorted([j1, j2]))
                duels[par] += 1

    return duels

def count_doubles_by_player(schedule):
    pares = defaultdict(int)

    for game in schedule:
        if game['Dupla 1'] == "—":
            continue

        for dupla_str in [game['Dupla 1'], game['Dupla 2']]:
            j1, j2 = dupla_str.split(" & ")
            par = tuple(sorted([j1.strip(), j2.strip()]))
            pares[par] += 1

    return pares
