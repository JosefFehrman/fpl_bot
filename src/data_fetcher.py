import requests
import pandas as pd
import time
import os

BASE_API = "https://fantasy.premierleague.com/api"

def get_fpl_data():
    url = f"{BASE_API}/bootstrap-static/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        players = pd.DataFrame(data['elements'])
        teams = pd.DataFrame(data['teams'])
        return players, teams
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def get_player_history(player_id):
    url = f"{BASE_API}/element-summary/{player_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "history" not in data:
            raise ValueError("Missing 'history' key in response")

        return pd.DataFrame(data["history"])

    except Exception as e:
        print(f"❌ Failed to fetch history for player {player_id}: {e}")
        return None

def get_all_players():
    try:
        response = requests.get(f"{BASE_API}/bootstrap-static/")
        response.raise_for_status()
        bootstrap = response.json()
        return pd.DataFrame(bootstrap["elements"])
    except Exception as e:
        print(f"❌ Failed to get all players: {e}")
        return pd.DataFrame()


def fetch_weekly_data(save_path="data/processed/player_gameweeks.csv", limit=10):
    """
    Download weekly-level player performance data for active players.
    Args:
        save_path (str): Path to save output CSV
        limit (int): Number of active players to fetch (default: 10)
    Returns:
        pd.DataFrame: Merged gameweek history
    """
    all_players = get_all_players()
    if all_players.empty:
        raise ValueError("No players found from API.")

    # Filter only 'active' players (status == 'a')
    active_players = all_players[all_players["status"] == "a"].copy()
    if active_players.empty:
        raise ValueError("No active players found.")

    print(f"🔍 Found {len(active_players)} active players. Limiting to {limit} for this run...")

    all_data = []

    for i, (_, player) in enumerate(active_players.iterrows()):
        if i >= limit:
            break

        pid = player["id"]
        name = f"{player['first_name']} {player['second_name']}"
        print(f"⬇️ Fetching history for {name} (id={pid})")

        history = get_player_history(pid)
        if history is not None and not history.empty:
            history["player_id"] = pid
            history["name"] = name
            all_data.append(history)

        time.sleep(0.8)  # be kind to FPL API

    if not all_data:
        raise ValueError("No player history was fetched.")

    df = pd.concat(all_data, ignore_index=True)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    df.to_csv(save_path, index=False)
    print(f"✅ Data saved to {save_path}")
    return df