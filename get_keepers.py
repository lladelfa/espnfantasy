
import json
import os
import requests
from espn_api.football import League

# --- Configuration ---
# The year of the fantasy league you want to query.
LEAGUE_YEAR = 2025 # The upcoming season for which keepers are being selected
HISTORY_YEAR = 2024 # The most recently completed season to get draft data from

# The draft round cost for a player who was not drafted by the team (e.g., waiver pickup).
UNDRAFTED_ROUND_COST = 16

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

        # 1. Initialize the league object for the UPCOMING season to get player details
        try:
            print(f"Connecting to league for {LEAGUE_YEAR} to get player metadata...")
            league = League(league_id=int(league_id), year=LEAGUE_YEAR, espn_s2=espn_s2, swid=swid)
        except Exception as e:
            print(f"Error initializing ESPN API for {LEAGUE_YEAR}. Check credentials and league ID. Details: {e}")
            return

        # 2. Initialize a league object for the HISTORICAL season to get draft data
        try:
            print(f"Connecting to league for {HISTORY_YEAR} to get draft history...")
            league_history = League(league_id=int(league_id), year=HISTORY_YEAR, espn_s2=espn_s2, swid=swid)
        except Exception as e:
            print(f"Error initializing ESPN API for {HISTORY_YEAR}. Check credentials and league ID. Details: {e}")
            return

        # 3. Create a lookup map of historical draft results.
        # We map (player_id, drafting_team_id) to the round they were drafted in.
        print("Building historical draft map...")
        draft_history = {
            (pick.playerId, pick.team.team_id): pick.round_num
            for pick in league_history.draft
        }

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
            team_id = team.get('id')
            team_name = team.get('name')
            keeper_ids = team.get('draftStrategy', {}).get('keeperPlayerIds', [])

            if team_name and keeper_ids:
                print(f"\nTeam: {team_name}")
                for player_id in keeper_ids:
                    # Get player's name and position from the current league object
                    player = league.player_info(playerId=player_id)

                    # Look up the player's original draft round from the historical map
                    draft_key = (player_id, team_id)
                    draft_round = draft_history.get(draft_key, UNDRAFTED_ROUND_COST)

                    if player:
                        print(f"  - {player.name} ({player.position}, {player.proTeam}) - Keeper Cost: Round {draft_round}")
                    else:
                        # Still provide draft cost even if player name is unknown
                        print(f"  - Unknown Player (ID: {player_id}) - Keeper Cost: Round {draft_round}")

    except json.JSONDecodeError:
        print("Error: Could not decode the JSON response from the API. The data might be malformed.")

if __name__ == "__main__":
    process_keeper_data()
