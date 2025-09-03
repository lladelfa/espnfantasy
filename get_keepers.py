
import json
import os
from espn_api.football import League

# --- Configuration ---
# The year of the fantasy league you want to query.
LEAGUE_YEAR = 2024

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

        # Load the keeper data from the local JSON file
        with open(r'c:\Users\llade\Documents\GitHub\espnfantasy\keeper_response.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

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

    except FileNotFoundError:
        print("Error: keeper_response.json not found. Please make sure the file exists in the correct directory.")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from the file. The file might be corrupted or not in valid JSON format.")

if __name__ == "__main__":
    process_keeper_data()
