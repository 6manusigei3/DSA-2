def recommend_friends(graph, user):
    if user not in graph:
        return []

    scores = {}

    for friend in graph.get(user, []):
        for fof in graph.get(friend, []):
            if fof != user and fof not in graph[user]:
                scores[fof] = scores.get(fof, 0) + 1

    # Sort by strongest recommendation
    return sorted(scores, key=scores.get, reverse=True)