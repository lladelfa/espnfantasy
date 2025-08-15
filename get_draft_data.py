import sys
import csv
from espn_api.football import League
from common import get_league


def display_draft_recap(league: League, output_file: str = None):
    """
    Fetches and displays the draft recap for a completed draft.
    Can export the data to a CSV file.
    """
    try:
        print(f"\nFetching draft data for the {league.year} season...")
        draft_picks = league.draft

        if not draft_picks:
            print(f"Could not find any draft data for the {league.year} season.")
            return

        draft_data = []
        for i, pick in enumerate(draft_picks):
            team = pick.team.team_name
            round_num = pick.round_num
            pick_num = i + 1

            # Robustly get player info to avoid errors with older seasons
            player_info = league.player_info(playerId=pick.playerId)
            if player_info:
                player_name, position = player_info.name, player_info.position
            else:
                player_name, position = f"Unknown (ID: {pick.playerId})", "N/A"

            draft_data.append({
                'Round': round_num,
                'Pick': pick_num,
                'Player Name': player_name,
                'Position': position,
                'Team': team
            })

        if output_file and output_file.lower().endswith('.csv'):
            print(f"Exporting draft data to {output_file}...")
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=draft_data[0].keys())
                writer.writeheader()
                writer.writerows(draft_data)
        else:
            print(f"Draft Recap for {league.year}:")
            print("-" * 80)
            print(f"{'ROUND':>5} {'PICK':>5} {'PLAYER NAME':<25} {'POSITION':<10} {'TEAM':<25}")
            print("-" * 80)
            for pick_data in draft_data:
                print(f"{pick_data['Round']:>5} {pick_data['Pick']:>5} {pick_data['Player Name']:<25} {pick_data['Position']:<10} {pick_data['Team']:<25}")
            print("-" * 80)
    except Exception as e:
        print(f"An unexpected error occurred while fetching draft data: {e}")
        sys.exit(1)


def main():
    """
    Main function to get league data and display the draft recap.
    """
    output_file = sys.argv[1] if len(sys.argv) > 1 else None
    league = get_league()
    display_draft_recap(league, output_file)


if __name__ == "__main__":
    main()