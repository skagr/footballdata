"""Helper functions for footballdata"""


def odds_to_probability(odds):
    return 1 / odds


def probability_to_odds(prob):
    return 1 / prob
