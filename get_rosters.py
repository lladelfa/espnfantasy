import sys
import csv
from espn_api.football import League
from common import get_league


def display_rosters(league: League, output_file: str = None):
    """
    Fetches a consolidated list of all players on all rosters.
    Can export the data to a CSV file.
    """
    print(f"\nFetching rosters and draft data for the {league.year} season...")

    # Fetch draft data and create a mapping from player ID to draft info
    draft_map = {}
    try:
        # The .draft property fetches draft data, ordered by overall pick
        draft_picks = league.draft
        if draft_picks:
            draft_map = {
                pick.playerId: {
                    "round": pick.round_num,
                    "overall": i + 1,
                    "is_keeper": pick.keeper_status,
                }
                for i, pick in enumerate(draft_picks)
            }
    except Exception as e:
        # This might fail if the draft hasn't happened yet for the season
        print(f"Warning: Could not fetch draft data. Draft rounds may not be displayed. Error: {e}")

    all_players_data = []
    # Iterate through each team and player to populate the table
    for team in league.teams:
        team_name = getattr(team, 'team_name', 'Unknown Team')
        for player in team.roster:
            # Using getattr for safety, though these attributes should exist for rostered players
            pos = getattr(player, 'position', 'N/A')
            name = getattr(player, 'name', 'Unknown Player')
            pro_team = getattr(player, 'proTeam', 'N/A')
            points = getattr(player, 'total_points', 0)
            draft_info = draft_map.get(player.playerId)
            if draft_info:
                draft_round = draft_info['round']
                draft_pick = draft_info['overall']
                keeper_status = "Yes" if draft_info.get("is_keeper") else "No"
            else:
                draft_round, draft_pick, keeper_status = "N/A", "N/A", "N/A"

            all_players_data.append({
                'Team': team_name,
                'Position': pos,
                'Player Name': name,
                'Pro Team': pro_team,
                'Total Points': points,
                'Draft Year': league.year,
                'Draft Round': draft_round,
                'Draft Pick': draft_pick,
                'Keeper': keeper_status
            })

    if output_file and output_file.lower().endswith('.csv'):
        print(f"Exporting roster data to {output_file}...")
        if not all_players_data:
            print("No roster data to export.")
            return
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            # Format points to 2 decimal places for CSV
            for player in all_players_data:
                player['Total Points'] = f"{player['Total Points']:.2f}"
            writer = csv.DictWriter(f, fieldnames=all_players_data[0].keys())
            writer.writeheader()
            writer.writerows(all_players_data)
    else:
        table_width = 104
        print("\n" + "=" * table_width)
        print(f"{'TEAM':<20} {'POS':<5} {'PLAYER NAME':<25} {'PRO TEAM':<10} {'TOTAL PTS':>12} {'RND':>8} {'PICK':>8} {'KEEPER':>8}")
        print("-" * table_width)
        for player_data in all_players_data:
            print(f"{player_data['Team']:<20} {player_data['Position']:<5} {player_data['Player Name']:<25} {player_data['Pro Team']:<10} {player_data['Total Points']:>12.2f} {str(player_data['Draft Round']):>8} {str(player_data['Draft Pick']):>8} {player_data['Keeper']:>8}")
        print("=" * table_width)


def main():
    """
    Main function to get league data and display team rosters.
    """
    output_file = sys.argv[1] if len(sys.argv) > 1 else None
    league = get_league()
    display_rosters(league, output_file)


if __name__ == "__main__":
    main()