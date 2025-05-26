from models.power_rating import calculate_power_rating_interactive
from models.monte_carlo import simulate_match
from utils.team_stats import calculate_team_stats
from utils.data_loader import load_data

def analyze():
    print("🔍 Starting match analysis...")

    league = "premier_league"
    _, df_detailed, _ = load_data(league)


    # Dane od użytkownika
    home_team = input("Enter HOME team name: ").strip()
    away_team = input("Enter AWAY team name: ").strip()
    round_number = int(input("Enter match round number (e.g. 15): "))

    # Statystyki gospodarza
    print(f"\n📈 Calculating stats for {home_team} (Home)...")
    stats_home = calculate_team_stats(df_detailed, home_team, "Home", round_number)

    # Statystyki gościa
    print(f"\n📉 Calculating stats for {away_team} (Away)...")
    stats_away = calculate_team_stats(df_detailed, away_team, "Away", round_number)

    if not stats_home or not stats_away:
        print("❌ Could not calculate stats for one or both teams.")
        return

    # Power Rating – wybór składników (dla obu drużyn)
    print(f"\n💡 Choose components to calculate Power Rating for {home_team}:")
    pr_home = calculate_power_rating_interactive(stats_home)

    print(f"\n💡 Choose components to calculate Power Rating for {away_team}:")
    pr_away = calculate_power_rating_interactive(stats_away)

    print(f"\n⚡ Power Rating {home_team}: {pr_home}")
    print(f"⚡ Power Rating {away_team}: {pr_away}")

    # xG = uproszczona wersja: wykorzystaj np. xG_avg z recent data
    xg_home = stats_home["xG_diff"] + 1.5  # lub coś bardziej realistycznego
    xg_away = stats_away["xG_diff"] + 1.2

    print(f"\nEstimated xG → {home_team}: {xg_home:.2f}, {away_team}: {xg_away:.2f}")

    result = simulate_match(xg_home, xg_away)
    print(f"\n🎲 Simulation Result (10,000 runs):")
    print(f"🏠 {home_team} Win Probability : {result['home_win_prob'] * 100:.1f}%")
    print(f"🤝 Draw Probability           : {result['draw_prob'] * 100:.1f}%")
    print(f"🛫 {away_team} Win Probability : {result['away_win_prob'] * 100:.1f}%")
