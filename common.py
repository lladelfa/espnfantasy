import os
import sys
from espn_api.football import League


def get_league(league_id: int = None, year: int = None, espn_s2: str = None, swid: str = None, exit_on_error: bool = True) -> League:
    """
    Connects to the ESPN Fantasy Football league using configuration
    from parameters or environment variables.

    :param league_id: Optional. The league ID.
    :param year: Optional. The season year to connect to.
    :param espn_s2: Optional. The ESPN_S2 cookie for private leagues.
    :param swid: Optional. The SWID cookie for private leagues.
    """
    # Load configuration from environment variables if not provided
    try:
        if league_id is None:
            league_id = int(os.environ["LEAGUE_ID"])
        else:
            league_id = int(league_id)

        if year is None:
            season_id = int(os.environ["SEASON_ID"])
        else:
            season_id = int(year)
    except (KeyError, ValueError) as e:
        err_msg = "Error: LEAGUE_ID and SEASON_ID must be provided or set as environment variables."
        print(err_msg)
        print("This is typically handled by the run_fantasy_data.bat file or the web app form.")
        if exit_on_error:
            sys.exit(1)
        else:
            raise ValueError(err_msg) from e

    # For private leagues, ESPN_S2 and SWID cookies are required.
    espn_s2 = espn_s2 or os.environ.get("ESPN_S2")
    swid = swid or os.environ.get("SWID")

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
        if exit_on_error:
            sys.exit(1)
        else:
            raise Exception(f"Failed to connect to the league: {e}") from e