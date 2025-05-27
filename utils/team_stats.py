import pandas as pd

def get_last_n_matches(df, team_name, side, current_round, n=5):
    """
    Zwraca ostatnie n meczów drużyny (Home lub Away) przed daną kolejką.
    """
    if side == "Home":
        df_filtered = df[
            (df["TEAM"] == team_name) &
            (df["Type"] == "Home") &
            (df["Round"] < current_round)
        ]
    else:
        df_filtered = df[
            (df["TEAM"] == team_name) &
            (df["Type"] == "Away") &
            (df["Round"] < current_round)
        ]

    return df_filtered.sort_values(by="Round", ascending=False).head(n)


def calculate_team_stats(df, team_name, side, current_round):
    """
    Oblicza wszystkie składniki Power Ratingu na podstawie detailed match data.
    """
    recent_matches = get_last_n_matches(df, team_name, side, current_round)

    if recent_matches.empty or len(recent_matches) < 3:
        print(f"⚠️ Warning: Not enough matches for {team_name} ({side}) before round {current_round}")
        return None

    # xPTS_avg – jeśli nie ma xPTS, użyj średniej punktów
    if "xPTS" in recent_matches.columns:
        xpts_avg = recent_matches["xPTS"].mean()
    else:
        xpts_avg = recent_matches["Points"].mean()

    # xG_diff = średnia różnica xG - xG_Opponent
    xg_diff = (recent_matches["xG"] - recent_matches["xG_Opponent"]).mean()

    # form_score = suma punktów
    form_score = recent_matches["Points"].sum()

    # dominance_ratio = % meczów z dominacją (True)
    if "Domination" in recent_matches.columns:
        dominance_ratio = (recent_matches["Domination"] == True).sum() / len(recent_matches)
    else:
        dominance_ratio = 0.0

    # SoS_factor – średnia pozycja przeciwników (jeśli dostępna)
    if "Opponent_Position" in recent_matches.columns:
        SoS_factor = recent_matches["Opponent_Position"].mean()
    else:
        SoS_factor = 10.0  # wartość neutralna

    # momentum – czy xPTS rośnie (względna forma ostatnich 2 vs 3 meczów)
    if "xPTS" in recent_matches.columns and len(recent_matches) >= 5:
        first_half = recent_matches.head(3)["xPTS"].mean()
        second_half = recent_matches.tail(2)["xPTS"].mean()
        momentum = 1 if second_half > first_half else -1 if second_half < first_half else 0
    else:
        momentum = 0

    # efficiency_vs_opponent_tier – stosunek xG do xG_Opponent
    efficiency = (recent_matches["xG"] / recent_matches["xG_Opponent"]).mean()

    return {
    "xpts_avg": round(xpts_avg, 3),
    "xg_diff": round(xg_diff, 3),
    "form_score": round(form_score, 3),
    "dominance_ratio": round(dominance_ratio, 3),
    "sos_factor": round(SoS_factor, 3),
    "momentum": momentum,
    "efficiency_vs_opponent_tier": round(efficiency, 3)
}

# Dostępne składniki Power Score
available_power_score_components = {
    'xpts_avg': 'Średnia xPTS z 5 meczów',
    'xg_diff': 'Różnica xG - xGA',
    'form_score': 'Punkty z ostatnich 5 meczów',
    'dominance_ratio': 'Procent zwycięstw 3+ bramkami',
    'sos_factor': 'Średnia siła przeciwników',
    'momentum': 'Momentum (czy xPTS rośnie)',
    'efficiency_vs_opponent_tier': 'Efektywność vs siła przeciwnika'
}

# Funkcja licząca Power Score na podstawie konfiguracji użytkownika
def calculate_power_score(team_data: dict, selected_components: dict) -> float:
    total_weight = sum(selected_components.values())
    if total_weight == 0:
        return 0.0

    score = 0.0
    for component, weight in selected_components.items():
        normalized_weight = weight / total_weight
        value = team_data.get(component) or 0  # <- zabezpieczenie
        score += value * normalized_weight
    return round(score, 2)

