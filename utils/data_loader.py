import pandas as pd
import os

def load_data(league: str):
    """
    Load raw, detailed, and team table data for the selected league.
    """
    base_path = "data"
    filenames = {
        "raw": f"{league}_raw_match_data.xlsx",
        "detailed": f"{league}_match_data_detailed.xlsx",
        "tables": f"{league}_team_tables_home_away.xlsx"
    }

    try:
        df_raw = pd.read_excel(os.path.join(base_path, filenames["raw"]))
        df_detailed = pd.read_excel(os.path.join(base_path, filenames["detailed"]))
        df_tables = pd.read_excel(os.path.join(base_path, filenames["tables"]))

        print(f"✅ Loaded data for league: {league}")
        return df_raw, df_detailed, df_tables

    except FileNotFoundError as e:
        print(f"❌ File not found: {e.filename}")
    except Exception as e:
        print(f"❌ Error loading data for league '{league}': {e}")

    return None, None, None
