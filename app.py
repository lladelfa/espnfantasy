from flask import Flask, render_template, request, jsonify
from common import get_league
from get_draft_data import fetch_draft_data
from get_rosters import fetch_rosters
from get_keeper_analysis import fetch_keeper_analysis

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    try:
        data = request.json
        league_id = data.get('league_id')
        year = data.get('year')
        espn_s2 = data.get('espn_s2')
        swid = data.get('swid')
        action = data.get('action')

        if not league_id:
            return jsonify({'error': 'League ID is required.'}), 400

        import datetime
        league_id = int(league_id)
        year = int(year) if year else datetime.datetime.now().year - 1

        if action in ['draft', 'rosters']:
            league = get_league(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid, exit_on_error=False)
            if action == 'draft':
                result = fetch_draft_data(league)
                columns = ['Round', 'Pick', 'Player Name', 'Position', 'Team']
            elif action == 'rosters':
                result = fetch_rosters(league)
                columns = ['Team', 'Position', 'Player Name', 'Pro Team', 'Total Points', 'Draft Year', 'Draft Round', 'Draft Pick', 'Keeper']
        elif action == 'keepers':
            # Keeper analysis handles multiple years internally
            result = fetch_keeper_analysis(league_id=league_id, espn_s2=espn_s2, swid=swid)
            columns = ['name', 'team', 'streak']
        else:
            return jsonify({'error': 'Invalid action specified.'}), 400

        return jsonify({'data': result, 'columns': columns})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
