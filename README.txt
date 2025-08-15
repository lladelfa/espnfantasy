================================
 ESPN Fantasy Football Data Tool
================================

This project provides a set of scripts to fetch and display data from your private or public ESPN Fantasy Football league.


Features
--------
*   Display a full draft recap, including round, overall pick number, and drafting team.
*   Display a consolidated table of all team rosters, including player position, pro team, total points, draft round, overall pick, and keeper status.
*   Flexible command-line options to specify the season year and save output to a file.
*   Analyze and display players who have been kept by the same team for consecutive years.


Requirements
------------
*   Python 3.x
*   The `espn-api` Python library. You can install it by running:
    pip install espn-api


Configuration
-------------
Before you can use the tool, you must configure your league details in the `run_fantasy_data.bat` file.
This file contains sensitive information and is ignored by Git.

1.  Make a copy of the template file: `run_fantasy_data.bat.template`.
2.  Rename the copy to `run_fantasy_data.bat`.
3.  Open your new `run_fantasy_data.bat` in a text editor.

4.  Update the following placeholder variables in the "Configuration" section:

    -   `YOUR_LEAGUE_ID`: Your fantasy league's unique ID number.
    -   `YOUR_ESPN_S2_COOKIE`: Your `espn_s2` cookie value (for private leagues).
    -   `YOUR_SWID_COOKIE`: Your `SWID` cookie value (for private leagues).

    NOTE: For public leagues, you can leave `ESPN_S2` and `SWID` with their placeholder values.

How to get your cookies (for private leagues):
---------------------------------------------
1.  Log in to your ESPN fantasy account in a web browser (e.g., Chrome, Firefox).
2.  Open the browser's Developer Tools (usually by pressing F12).
3.  Go to the "Application" (Chrome) or "Storage" (Firefox) tab.
4.  Find the "Cookies" section for `espn.com` or `fantasy.espn.com`.
5.  Locate the `espn_s2` and `swid` cookies and copy their values into the `run_fantasy_data.bat` file.


Usage
-----
All tasks are run from the command line using the `run_fantasy_data.bat` script.

Syntax:
    run_fantasy_data.bat <script_name.py> [year] [output_file]

Arguments:
    <script_name.py>: Required. The script to run (`get_draft_data.py`, `get_rosters.py`, or `get_keeper_analysis.py`).
    [year]: Optional. The season year to fetch data for. If omitted, it defaults to the previous year.
    [output_file]: Optional. The name of a file to save the output to. If omitted, output is displayed in the console.

Examples:

    # Get the draft recap for the most recently completed season
    run_fantasy_data.bat get_draft_data.py

    # Get all team rosters for the 2022 season
    run_fantasy_data.bat get_rosters.py 2022

    # Get the 2021 draft recap and save it to a file named "draft_2021.txt"
    run_fantasy_data.bat get_draft_data.py 2021 draft_2021.txt

    # Run the keeper analysis for the last 3 seasons
    run_fantasy_data.bat get_keeper_analysis.py

    # Get rosters for the 2023 season and export to a CSV file
    run_fantasy_data.bat get_rosters.py 2023 rosters_2023.csv
