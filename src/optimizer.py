# src/optimizer.py
import pandas as pd
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpBinary

TOTAL_BUDGET = 1000  # £100M in tenths

def select_optimal_team(players: pd.DataFrame) -> pd.DataFrame:
    # Ensure positions and cleanup
    players = players.copy()
    players = players[players["now_cost"] > 0].reset_index(drop=True)

    # Build LP
    prob = LpProblem("FPL_Team_Selection", LpMaximize)
    n = len(players)
    vars_ = [LpVariable(f"x_{i}", cat=LpBinary) for i in range(n)]

    # Objective: max total points
    prob += lpSum(vars_[i] * players.at[i, "total_points"] for i in range(n))

    # Budget constraint
    prob += lpSum(vars_[i] * players.at[i, "now_cost"] for i in range(n)) <= TOTAL_BUDGET
    # Squad size
    prob += lpSum(vars_) == 15

    # Position quotas
    quotas = {"Goalkeeper":2, "Defender":5, "Midfielder":5, "Forward":3}
    for pos, q in quotas.items():
        prob += lpSum(vars_[i] for i in range(n) if players.at[i, "position"] == pos) == q

    # Max 3 per club
    for team in players["team"].unique():
        prob += lpSum(vars_[i] for i in range(n) if players.at[i, "team"] == team) <= 3

    # Solve and extract
    prob.solve()
    mask = [v.varValue == 1 for v in vars_]
    return players[mask]
