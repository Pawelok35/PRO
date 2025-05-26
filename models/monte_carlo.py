import numpy as np
from scipy.stats import poisson

def simulate_match(xg_home: float, xg_away: float, simulations: int = 10000):
    """
    Simulate match outcome using Poisson distribution for expected goals.
    Returns win/draw/loss probabilities for home team.
    """
    home_wins = 0
    draws = 0
    away_wins = 0

    for _ in range(simulations):
        goals_home = poisson.rvs(mu=xg_home)
        goals_away = poisson.rvs(mu=xg_away)

        if goals_home > goals_away:
            home_wins += 1
        elif goals_home < goals_away:
            away_wins += 1
        else:
            draws += 1

    return {
        "home_win_prob": round(home_wins / simulations, 3),
        "draw_prob": round(draws / simulations, 3),
        "away_win_prob": round(away_wins / simulations, 3),
    }
