from utils.data_loader import load_data
from scripts.analyze_match import analyze

if __name__ == "__main__":
    print("=== IN STATS WE TRUST ===")
    print("Supported leagues: premier_league, la_liga, serie_a, bundesliga, ligue1")

    league = input("Enter league code: ").strip().lower()
    df_raw, df_detailed, df_tables = load_data(league)

    if df_raw is not None:
        analyze()
    else:
        print("⚠️ Could not load data. Please check file names and try again.")
