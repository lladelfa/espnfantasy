import sys
import csv
import datetime
from collections import defaultdict
from common import get_league


def analyze_keepers(output_file: str = None):
    """
    Fetches draft data for the last 3 years and analyzes consecutive
    keeper streaks for players kept by the same team.
    """
    try:
        current_year = datetime.datetime.now().year
        # Analyze the last 3 completed seasons
        years_to_check = range(current_year - 1, current_year - 4, -1)
        
        print(f"Analyzing keeper data for seasons: {list(years_to_check)}...")

        player_keeper_history = defaultdict(list)

        for year in years_to_check:
            print(f"\nFetching data for {year} season...")
            # The get_league function is now flexible enough to be called with a specific year
            league = get_league(year=year)
            
            if not league.draft:
                print(f"Warning: No draft data found for {year}. Skipping.")
                continue

            keeper_count = 0
            for pick in league.draft:
                if pick.keeper_status:
                    keeper_count += 1

                    # --- ROBUST PLAYER NAME FETCH ---
                    # Instead of pick.player_name, which can fail on older data,
                    # we look up the player by their ID for reliability.
                    player_info = league.player_info(playerId=pick.playerId)
                    player_name = player_info.name if player_info else f"Unknown (ID: {pick.playerId})"

                    player_keeper_history[pick.playerId].append({
                        "year": year,
                        "team_id": pick.team.team_id,
                        "team_name": pick.team.team_name,
                        "player_name": player_name
                    })
            print(f"Found {keeper_count} keepers in {year}.")

        print("\n--- Keeper Streak Analysis ---")
        consecutive_keepers = []

        # The most recent season we are analyzing is the first in the list
        most_recent_analyzed_year = years_to_check[0]

        for player_id, history in player_keeper_history.items():
            if len(history) < 2:
                continue

            # Sort by year descending to find the most recent streak
            history.sort(key=lambda x: x['year'], reverse=True)

            # A keeper streak is only relevant if it includes the most recent season.
            if history[0]['year'] != most_recent_analyzed_year:
                continue

            streak = 1
            last_team_id = history[0]['team_id']
            
            for i in range(1, len(history)):
                # Check if the current pick is from the previous year and by the same team
                if history[i]['year'] == history[i-1]['year'] - 1 and history[i]['team_id'] == last_team_id:
                    streak += 1
                else:
                    break  # The streak is broken
            
            if streak > 1:
                consecutive_keepers.append({
                    "name": history[0]['player_name'],
                    "team": history[0]['team_name'],
                    "streak": streak
                })

        if not consecutive_keepers:
            print("No players found with a keeper streak of 2 or more consecutive years.")
            return

        consecutive_keepers.sort(key=lambda x: (-x['streak'], x['name']))

        if output_file and output_file.lower().endswith('.csv'):
            print(f"Exporting keeper analysis to {output_file}...")
            csv_data = [{
                'Player Name': k['name'],
                'Team': k['team'],
                'Consecutive Years Kept': k['streak']
            } for k in consecutive_keepers]
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                writer.writeheader()
                writer.writerows(csv_data)
        else:
            table_width = 70
            print("=" * table_width)
            print(f"{'PLAYER NAME':<25} {'TEAM':<25} {'CONSECUTIVE YEARS KEPT':>20}")
            print("-" * table_width)
            for keeper in consecutive_keepers:
                print(f"{keeper['name']:<25} {keeper['team']:<25} {str(keeper['streak']) + ' years':>20}")
            print("=" * table_width)


    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please ensure your credentials in 'run_fantasy_data.bat' are correct.")
        sys.exit(1)


def main():
    """Main function to run the keeper analysis."""
    output_file = sys.argv[1] if len(sys.argv) > 1 else None
    analyze_keepers(output_file)


if __name__ == "__main__":
    main()