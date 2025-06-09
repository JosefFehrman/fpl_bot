import streamlit as st
import pandas as pd
from src.data_fetcher import get_fpl_data
from src.optimizer import select_optimal_team
from src.model import predict_expected_points


TOTAL_BUDGET = 1000  # in tenths of millions, i.e. £100.0M

POSITION_MAP = {
    1: "Goalkeeper",
    2: "Defender",
    3: "Midfielder",
    4: "Forward"
}

def render():
    st.header("Select Your Team - Budget Tracker (mock data)")

    players, _ = get_fpl_data()
    players["full_name"] = players["first_name"] + " " + players["second_name"]
    players["position"] = players["element_type"].map(POSITION_MAP)
    players["value_per_point"] = players["now_cost"] / players["total_points"].replace(0, 1)  # Avoid division by zero


    players = players.sort_values(by="total_points", ascending=False)

    players = predict_expected_points(players)

    # Select players
    selected_players = st.multiselect(
        "Pick your players",
        options=players["full_name"],
        help="Choose up to 15 players",
    )

    # Filter selected
    selected_df = players[players["full_name"].isin(selected_players)]
    total_cost = selected_df["now_cost"].sum()
    budget_left = TOTAL_BUDGET - total_cost

    # Show budget
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 Total Cost", f"£{total_cost / 10:.1f}M")
    with col2:
        st.metric("📉 Budget Left", f"£{budget_left / 10:.1f}M")

    # Show selected players
    if not selected_df.empty:
        st.subheader("Selected Players")
        st.dataframe(selected_df[["full_name", "now_cost", "total_points", "minutes", "value_per_point", "position", "expected_points"]])
    else:
        st.info("No players selected yet.")


    # -- optional: Show player value --
    st.divider()
    st.subheader("Player Value Analysis")

    min_points = st.slider("Minimum Points", min_value=0, max_value=int(players["total_points"].max()), value=50)
    select_position = st.selectbox("Select Position", options=["All"] + list(POSITION_MAP.values()))

    filtered = players[players["total_points"] >= min_points]
    if select_position != "All":
        filtered = filtered[filtered["position"] == select_position]

    top_value = filtered.sort_values(by="value_per_point", ascending=False).head(10)
    top_value["value_per_point"] = top_value["value_per_point"].round(2)

    st.dataframe(top_value[["full_name", "position", "now_cost", "total_points", "value_per_point", "expected_points"]])
    st.info("Player value is calculated as cost per point. Lower value indicates better value for money.")

    # -- optional: Show optimal team --
    st.divider()
    st.subheader("Auto-Pick: Optimal 15-man Team (Value-Based)")

    optimal_team = select_optimal_team(players)
    team_cost = optimal_team["now_cost"].sum()
    team_points = optimal_team["total_points"].sum()

    st.markdown(f"**Total Cost**: £{team_cost / 10:.1f}M")
    st.markdown(f"**Total Points**: {team_points} pts")

    st.dataframe(optimal_team[["full_name", "position", "now_cost", "total_points", "value_per_point"]])

    # ---- Auto-Pick Optimal Team via PuLP ----
    # ---- optional: Show optimal team baset on excpeted points ----
    st.divider()
    st.subheader("🤖 Auto-Pick Optimal 15-man Team (LP Solver)")

    optimal_team = select_optimal_team(players)
    cost = optimal_team["now_cost"].sum()
    points = optimal_team["total_points"].sum()

    st.markdown(f"**Total Cost**: £{cost / 10:.1f}M")
    st.markdown(f"**Total Points**: {points} pts")

    st.dataframe(
        optimal_team[[
            "full_name", "position", "now_cost", "total_points"
        ]].assign(
            value_per_point=lambda df: (df["total_points"] / df["now_cost"]).round(2)
        )
    )






