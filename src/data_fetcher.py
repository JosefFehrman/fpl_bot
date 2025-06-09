import requests
import pandas as pd

fpl_api_url = "https://fantasy.premierleague.com/api/bootstrap-static/"

def get_fpl_data():
    """
    Fetches the Fantasy Premier League data from the official API.

    Returns:
        pd.DataFrame: A DataFrame containing the player data.
    """
    response = requests.get(fpl_api_url)
    if response.status_code == 200:
        data = response.json()
        players = pd.DataFrame(data['elements'])
        teams = pd.DataFrame(data['teams'])
        return players, teams
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")