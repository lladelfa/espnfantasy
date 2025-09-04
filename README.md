# ESPN Fantasy Football Utilities

A collection of Python scripts designed to pull and analyze data from a private ESPN fantasy football league using the unofficial ESPN API.

## Features

The primary script, `get_keepers.py`, provides a comprehensive pre-draft overview by:

- Fetching the live keeper selections for the upcoming season.
- Looking up the original draft round cost for each keeper from the previous season's draft.
- Assigning a default round cost for players acquired via waivers or free agency.
- Displaying a consolidated view of each team's keepers, including their name, position, pro team, and draft round cost.

## Setup

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

- Python 3.8+
- Git

### 2. Clone the Repository

```sh
git clone <your-repository-url>
cd espnfantasy
```

### 3. Install Dependencies

It's recommended to use a virtual environment.

```sh
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the required Python packages
pip install -r requirements.txt
```

### 4. Configure Credentials

To access data from a private league, you need to provide your credentials. Create a file named `run_fantasy_data.bat` in the root of the project directory.

**Note:** This file is listed in `.gitignore` and will **not** be committed to the repository to protect your sensitive information.

Add the following content to `run_fantasy_data.bat`, replacing the placeholder values with your actual league ID and ESPN credentials:

```bat
@echo off
set "LEAGUE_ID=YOUR_LEAGUE_ID"
set "ESPN_S2=YOUR_ESPN_S2_COOKIE"
set "SWID={YOUR_SWID_COOKIE}"

echo Environment variables set for the fantasy league.
```

## Usage

1.  Open a command prompt or terminal in the project's root directory.
2.  Run the batch script to set your environment variables for the current session:
    ```sh
    run_fantasy_data.bat
    ```
3.  Execute the main script:
    ```sh
    python get_keepers.py
    ```

The script will then connect to the ESPN API and print the keeper information for each team directly to your console.