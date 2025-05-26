import pandas as pd

def load_excel_file(filepath):
    try:
        return pd.read_excel(filepath)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None
