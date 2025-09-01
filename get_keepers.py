import os
from espn_api.football import League # Or .basketball, .baseball, etc.

def get_keeper_draft_details():
    """
    Pulls each team's full roster from the 2024 season and lists the
    original draft round for each player by their current team.
    """
    # --- Configuration ---
    # This script reads credentials from environment variables.
    # It expects them to be set by the calling process (e.g., your .bat file).
    #
    # To find your cookies, log into your ESPN fantasy account on your web browser,
    # open the developer tools (usually F12), go to the 'Application' or 'Storage' tab,
    # and find the cookies for the espn.com domain. Copy the values for 'espn_s2' and 'swid'.
    #
    # Try the standard 'ESPN_LEAGUE_ID' first, then fall back to 'LEAGUE_ID' for compatibility with your .bat file.
    LEAGUE_ID = os.environ.get('ESPN_LEAGUE_ID') or os.environ.get('LEAGUE_ID')
    YEAR = 2024  # The most recently completed season to get data from
    ESPN_S2 = os.environ.get('ESPN_S2') # Set environment variable, or replace None
    SWID = os.environ.get('SWID') # Set environment variable, or replace None

    # --- Default values ---
    # The draft round cost for a player who was not drafted by the team.
    UNDRAFTED_ROUND_COST = 16

    if not all([LEAGUE_ID, ESPN_S2, SWID]):
        print("Configuration Error: Please ensure LEAGUE_ID (or ESPN_LEAGUE_ID), ESPN_S2, and SWID environment variables are set.")
        return
    
    # --- Connect to the historical season for draft data ---
    print(f"Attempting to connect to ESPN Fantasy League for {YEAR} season...")
    try:
        league_history = League(league_id=int(LEAGUE_ID), year=YEAR, espn_s2=ESPN_S2, swid=SWID)
        print(f"Successfully connected to league: {league_history.settings.name}")
        print("-" * 40)
    except Exception as e:
        print(f"Error connecting to the league for {YEAR}. Please check your credentials and league ID.")
        print(f"Details: {e}")
        return

    # Create a quick lookup for the draft results of the specified YEAR.
    # We map (player_id, team_id) to the round they were drafted in.
    draft_history = {
        (pick.playerId, pick.team.team_id): pick.round_num
        for pick in league_history.draft
    }

    print(f"Full Roster Details from {YEAR} Season:\n")

    # Iterate through each team in the historical league to maintain order and access team info.
    for team in league_history.teams:
        # The error "AttributeError: 'Team' object has no attribute 'owner'" indicates this convenience
        # property isn't available. The hint "Did you mean: 'owners'?" points to the correct attribute, which is a list.
        owner_display = ", ".join([f"{o.get('firstName', '')} {o.get('lastName', '')}".strip() for o in team.owners])
        print(f"Team: {team.team_name} ({owner_display})")

        # Get the full roster for the team from the specified season.
        roster_players = team.roster

        if not roster_players:
            print("  Roster is empty.")
            print("-" * 40)
            continue

        for player in roster_players:
            # Check if the player was drafted by this team in the initial draft
            draft_key = (player.playerId, team.team_id)
            draft_round = draft_history.get(draft_key, UNDRAFTED_ROUND_COST)

            print(f"  - {player.name}: Round {draft_round}")

        print("-" * 40)


if __name__ == '__main__':
    get_keeper_draft_details()