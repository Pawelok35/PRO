from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Pozwól Reactowi łączyć się z backendem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # możesz tu wstawić "http://localhost:3000" dla bezpieczeństwa
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PowerScoreInput(BaseModel):
    team_data: dict
    user_weights: dict

@app.post("/calculate_power_score")
def calculate_power_score(input_data: PowerScoreInput):
    team_data = input_data.team_data
    user_weights = input_data.user_weights

    total = sum(user_weights.values())
    if total == 0:
        raise HTTPException(status_code=400, detail="No weights provided.")

    normalized = {k: v / total for k, v in user_weights.items()}
    score = sum(team_data.get(k, 0) * w for k, w in normalized.items())
    readable = {k: round(w * 100, 1) for k, w in normalized.items()}

    return {
        "score": round(score, 3),
        "components": readable
    }
import pandas as pd
import os

@app.get("/team_stats/{league}/{team}/{side}/{matchday}")
def get_team_stats(league: str, team: str, side: str, matchday: int):
    file_path = f"data/{league}_match_data_detailed.xlsx"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Nie znaleziono pliku z danymi")

    df = pd.read_excel(file_path)

    if side not in ["Home", "Away"]:
        raise HTTPException(status_code=400, detail="Side musi być 'Home' lub 'Away'")

    # Normalizacja danych
    df["TEAM"] = df["TEAM"].astype(str).str.strip()
    df["Type"] = df["Type"].astype(str).str.capitalize()
    df["Round"] = df["Round"].astype(int)

    # Diagnostyka krok po kroku
    df_1 = df[df["TEAM"] == team.strip()]
    print("✅ Po TEAM:", len(df_1))

    df_2 = df_1[df_1["Type"] == side.capitalize()]
    print("✅ Po Type:", len(df_2))

    df_team = df_2[df_2["Round"] < matchday]
    print("✅ Po Round <", matchday, ":", len(df_team))

    # Dodatkowy podgląd danych
    print("🔍 Wszystkie rundy dla tej drużyny i typu:")
    print(df_2[["Round", "Points", "xG", "xG_Opponent"]].sort_values("Round", ascending=False).head(10))

    df_team = df_team.sort_values("Round", ascending=False).head(5)
    print("🔍 FILTR:", team, side, matchday)
    print("✅ ZNALEZIONE MECZE:")
    print(df_team[["TEAM", "Round", "Type", "xG", "xG_Opponent", "Points"]])

    print("➡️ LICZBA:", len(df_team))


    print("👉 DF_TEAM:\n", df_team)
    print("➡️ Liczba meczów:", len(df_team))

    if df_team.empty:
        raise HTTPException(status_code=404, detail="Brak danych meczowych dla tej drużyny")


    xpts_avg = df_team["Points"].mean()
    xg_diff = (df_team["xG"] - df_team["xG_Opponent"]).mean()
    form_score = df_team["Points"].sum()
    dominance_ratio = (df_team["Domination"] == True).sum() / len(df_team)
    sos_factor = 10.0  # wartość neutralna, bo brak danych

    momentum = (
    1 if df_team.tail(2)["Points"].mean() > df_team.head(3)["Points"].mean() else
    -1 if df_team.tail(2)["Points"].mean() < df_team.head(3)["Points"].mean()
    else 0
)
    efficiency = (df_team["xG"] / df_team["xG_Opponent"]).mean()

    return {
        "Points_avg": float(round(xpts_avg, 3)),
        "xG_diff": float(round(xg_diff, 3)),
        "form_score": float(round(form_score, 3)),
        "dominance_ratio": float(round(dominance_ratio, 3)),
        "SoS_factor": float(round(sos_factor, 3)),
        "momentum": int(momentum),
        "efficiency_vs_opponent_tier": float(round(efficiency, 3))
    }

