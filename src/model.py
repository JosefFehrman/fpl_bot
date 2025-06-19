# import pandas as pd
# from sklearn.linear_model import Ridge
# from sklearn.model_selection import train_test_split
# import joblib
#
# def train_model(input_csv="data/processed/player_gameweeks.csv", model_path="models/week_model.pkl"):
#     df = pd.read_csv(input_csv)
#
#     features = ["minutes", "opponent_team", "was_home", "transfers_in", "goals_scored", "assists"]
#     X = df[features].fillna(0)
#     y = df["total_points"]
#
#     x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
#
#     model = Ridge()
#     model.fit(x_train, y_train)
#
#     joblib.dump(model, model_path)
#     return model


import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

def train_model():
    df = pd.read_csv("data/processed/player_gameweeks.csv")
    features = ["minutes", "opponent_team", "was_home", "transfers_in", "goals_scored", "assists"]
    target = "total_points"
    x = df[features]
    y = df[target]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
    }

    results = []

    for name, model in models.items():
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        mae = mean_absolute_error(y_test, preds)
        mse = mean_squared_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        results.append({
            "Model": name,
            "MAE": round(mae, 3),
            "MSE": round(mse, 3),
            "R²": round(r2, 3)
        })

        # Save the best model (example: Random Forest)

        if name == "Random Forest":
            joblib.dump((model, features), "models/week_model.pkl")

    return pd.DataFrame(results)
