from ..classes.season import Season
from . import app
from flask import render_template, request


def get_season_object(req):
    season = req.args['season'] if 'season' in req.args else 2000
    season_type = req.args['season_type'] if 'season_type' in req.args else 'regular'
    return Season().from_json_file(f'data/seasons/{season}-{season_type}.json')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/leaderboard')
def owner_leaderboard():
    season_obj = get_season_object(request)

    return render_template('leaderboard.html', owners=season_obj.owner_leaderboard)


@app.route('/stats/<player_type>')
def stats(player_type):
    season_obj = get_season_object(request)

    if player_type == 'all':
        return render_template('stats_all.html', owners=season_obj.rosters_by_owner)
    else:
        return render_template('not_implemented.html')


@app.route('/top10')
def top_10():
    return render_template('not_implemented.html')


@app.route('/unreconciled')
def unreconciled_players():
    season_obj = get_season_object(request)

    return render_template('unreconciled_players.html', owners=season_obj.unreconciled_players_by_owner)
