
import json
import os
from typing import Dict, Tuple, Optional, Any
import requests
from espn_api.football import League

# --- Configuration ---
# The year of the fantasy league you want to query.
LEAGUE_YEAR = 2025 # The upcoming season for which keepers are being selected
HISTORY_YEAR = 2024 # The most recently completed season to get draft data from

# The draft round cost for a player who was not drafted by the team (e.g., waiver pickup).
UNDRAFTED_ROUND_COST = 16

def get_credentials() -> Optional[Tuple[str, str, str]]:
    """Loads and validates required credentials from environment variables."""
    league_id = os.getenv('LEAGUE_ID')
    espn_s2 = os.getenv('ESPN_S2')
    swid = os.getenv('SWID')

    if not all([league_id, espn_s2, swid]):
        print("Error: Make sure LEAGUE_ID, ESPN_S2, and SWID environment variables are set.")
        print("You can set them by running your .bat file before executing this script.")
        return None
    return league_id, espn_s2, swid

def initialize_league(league_id: int, year: int, espn_s2: str, swid: str) -> Optional[League]:
    """Initializes and returns a League object for a given year."""
    try:
        print(f"Connecting to league for {year}...")
        return League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)
    except Exception as e:
        print(f"Error initializing ESPN API for {year}. Check credentials and league ID. Details: {e}")
        return None

def build_draft_history(league_history: League) -> Dict[Tuple[int, int], int]:
    """Creates a lookup map of (player_id, team_id) to draft round number."""
    print("Building historical draft map...")
    return {
        (pick.playerId, pick.team.team_id): pick.round_num
        for pick in league_history.draft
    }

def fetch_keeper_json(league_id: str, year: int, cookies: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Fetches the raw keeper data from the private ESPN API endpoint."""
    keeper_url = (
        f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{year}"
        f"/segments/0/leagues/{league_id}?view=mKeeperRosters"
    )
    try:
        print("Fetching live keeper data from ESPN API...")
        response = requests.get(keeper_url, cookies=cookies)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch keeper data from the API. Details: {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Could not decode the JSON response from the API. The data might be malformed.")
        return None

def main():
    """Main function to orchestrate fetching and processing keeper data."""
    creds = get_credentials()
    if not creds:
        return
    league_id_str, espn_s2, swid = creds
    league_id_int = int(league_id_str)

    # 1. Initialize league connections
    league = initialize_league(league_id_int, LEAGUE_YEAR, espn_s2, swid)
    league_history = initialize_league(league_id_int, HISTORY_YEAR, espn_s2, swid)

    if not league or not league_history:
        print("Failed to initialize one or more league sessions. Aborting.")
        return

    # 2. Build the historical draft map
    draft_history = build_draft_history(league_history)

    # 3. Fetch the live keeper data
    cookies = {"espn_s2": espn_s2, "SWID": swid}
    keeper_data = fetch_keeper_json(league_id_str, LEAGUE_YEAR, cookies)

    if not keeper_data:
        print("Failed to fetch keeper data. Aborting.")
        return

    # 4. Process and display the results
    teams = keeper_data.get('teams', [])
    print("\n--- Keepers for each team ---")
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

if __name__ == "__main__":
    main()
