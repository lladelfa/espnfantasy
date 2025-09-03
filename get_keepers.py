
import json
import os
import requests
from espn_api.football import League

# --- Configuration ---
# The year of the fantasy league you want to query.
LEAGUE_YEAR = 2025

def process_keeper_data():
    try:
        # Load credentials from environment variables set by your .bat file
        league_id = os.getenv('LEAGUE_ID')
        espn_s2 = os.getenv('ESPN_S2')
        swid = os.getenv('SWID')

        if not all([league_id, espn_s2, swid]):
            print("Error: Make sure LEAGUE_ID, ESPN_S2, and SWID environment variables are set.")
            print("You can set them by running your .bat file before executing this script.")
            return

        # Initialize the league object using the authenticated API
        try:
            league = League(league_id=int(league_id), year=LEAGUE_YEAR, espn_s2=espn_s2, swid=swid)
        except Exception as e:
            print(f"Error initializing ESPN API. Check your credentials and league ID. Details: {e}")
            return

        # Construct the dynamic URL to fetch keeper data using the provided endpoint.
        # This endpoint gives us the keeper selections before the draft is finalized.
        keeper_url = (
            f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{LEAGUE_YEAR}"
            f"/segments/0/leagues/{league_id}?view=mKeeperRosters"
        )

        # Use the same credentials (as cookies) to make an authenticated request
        cookies = {"espn_s2": espn_s2, "SWID": swid}

        try:
            print("Fetching live keeper data from ESPN API...")
            response = requests.get(keeper_url, cookies=cookies)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to fetch keeper data from the API. Details: {e}")
            return

        teams = data.get('teams', [])

        print("Keepers for each team:")
        for team in teams:
            team_name = team.get('name')
            keeper_ids = team.get('draftStrategy', {}).get('keeperPlayerIds', [])

            if team_name and keeper_ids:
                print(f"\nTeam: {team_name}")
                for player_id in keeper_ids:
                    # Use the espn_api League object to get player info by ID
                    player = league.player_info(playerId=player_id)
                    if player:
                        print(f"  - {player.name} ({player.position}, {player.proTeam})")
                    else:
                        print(f"  - Unknown Player (ID: {player_id})")

    except json.JSONDecodeError:
        print("Error: Could not decode the JSON response from the API. The data might be malformed.")

if __name__ == "__main__":
    process_keeper_data()
