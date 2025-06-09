# src/model.py

import pandas as pd
import joblib

MODEL_PATH = "models/fpl_ai_model.pkl"  # adjust if your path is different

# Define only the features the model was trained on
FEATURE_COLUMNS = [
    "now_cost", "minutes", "form", "transfers_in", "goals_scored",
    "assists", "yellow_cards", "threat", "influence"
    # Add/remove based on model
]

def predict_expected_points(players_df: pd.DataFrame) -> pd.DataFrame:
    model = joblib.load(MODEL_PATH)

    # Ensure missing features are handled
    for col in FEATURE_COLUMNS:
        if col not in players_df:
            players_df[col] = 0

    X = players_df[FEATURE_COLUMNS].fillna(0)
    players_df["expected_points"] = model.predict(X)

    return players_df
