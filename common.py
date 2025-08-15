import os
import sys
from espn_api.football import League


def get_league(year: int = None) -> League:
    """
    Connects to the ESPN Fantasy Football league using configuration
    from environment variables.

    :param year: Optional. The season year to connect to. If None, uses
                 the SEASON_ID from environment variables.
    """
    # Load configuration from environment variables
    try:
        league_id = int(os.environ["LEAGUE_ID"])
        if year is None:
            season_id = int(os.environ["SEASON_ID"])
        else:
            season_id = year
    except (KeyError, ValueError):
        print("Error: LEAGUE_ID and SEASON_ID environment variables must be set as integers.")
        print("This is typically handled by the run_fantasy_data.bat file.")
        sys.exit(1)

    # For private leagues, ESPN_S2 and SWID cookies are required.
    espn_s2 = os.environ.get("ESPN_S2")
    swid = os.environ.get("SWID")

    try:
        if espn_s2 and swid:
            print(f"Attempting to connect to private league {league_id} for the {season_id} season...")
            league = League(league_id=league_id, year=season_id, espn_s2=espn_s2, swid=swid)
        else:
            print(f"Attempting to connect to public league {league_id} for the {season_id} season...")
            league = League(league_id=league_id, year=season_id)
        
        print("Successfully connected to the league.")
        return league
    except Exception as e:
        print(f"Error connecting to the league: {e}")
        print("Please ensure your league credentials and IDs are correct and up-to-date in the .bat file.")
        sys.exit(1)