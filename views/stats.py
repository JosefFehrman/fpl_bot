import streamlit as st
from src.data_fetcher import get_fpl_data

def render():
    st.header("player stats")
    # Fetch the data
    players, teams = get_fpl_data()
    select_team = st.selectbox("Select Team", teams['name'])

    team_id = teams[teams["name"] == select_team]['id'].values[0]
    team_players = players[players['team'] == team_id]
    st.dataframe(team_players[["first_name", "second_name", "total_points", "minutes", "now_cost"]])