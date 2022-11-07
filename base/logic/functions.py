def randomize(credits, upper_bound, lower_bound) -> list:
    import random
    score_and_credits = []
    for j in credits:
        i = round(random.uniform(lower_bound, upper_bound), 2)
        j = int(j)
        score_and_credits.append((i, j))
    return score_and_credits