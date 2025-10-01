def schedule_games(matches, slots):
    from collections import defaultdict

    schedule = []
    occupation_by_hour = defaultdict(set)
    games_by_player = defaultdict(int)
    partners = defaultdict(int)
    duels = defaultdict(int)

    missing_matches = matches.copy()

    for court, time in slots:
        best_score = float('inf')
        best_match = None

        for pair1, pair2 in missing_matches:
            players = set(pair1 + pair2)

            if not players.isdisjoint(occupation_by_hour[time]):
                continue  # conflict

            # individual score
            individual_score = sum(games_by_player[j] for j in players)

            # repeat partner score
            partner_score = partners[tuple(sorted(pair1))] + partners[tuple(sorted(pair2))]

            # duels score
            duel_score = sum(
                duels[tuple(sorted([j1, j2]))]
                for j1 in pair1 for j2 in pair2
            )

            total_score = individual_score + partner_score * 2 + duel_score * 2

            if total_score < best_score:
                best_score = total_score
                best_match = (pair1, pair2)

        if best_match:
            pair1, pair2 = best_match
            players = set(pair1 + pair2)

            schedule.append({
                "Campo": f"Campo {court}",
                "Hora": time,
                "Dupla 1": f"{pair1[0]} & {pair1[1]}",
                "Dupla 2": f"{pair2[0]} & {pair2[1]}"
            })

            occupation_by_hour[time].update(players)
            for j in players:
                games_by_player[j] += 1
            partners[tuple(sorted(pair1))] += 1
            partners[tuple(sorted(pair2))] += 1
            for j1 in pair1:
                for j2 in pair2:
                    duels[tuple(sorted([j1, j2]))] += 1

            missing_matches.remove(best_match)
        else:
            schedule.append({
                "Campo": f"Campo {court}",
                "Hora": time,
                "Dupla 1": "—",
                "Dupla 2": "—"
            })

    return schedule, games_by_player
