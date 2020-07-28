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

    b = season_obj.batters
    b.sort(key=lambda x: (x.owner.display_name, -x.player.player.points))
    p = season_obj.pitchers
    p.sort(key=lambda x: (x.owner.display_name, -x.player.player.points))

    if player_type == 'batters':
        return render_template('not_implemented.html')
    elif player_type == 'pitchers':
        return render_template('not_implemented.html')
    elif player_type == 'all':
        return render_template('stats_all.html', owners=season_obj.rosters_by_owner)


@app.route('/top10')
def top_10():
    season_obj = get_season_object(request)

    b = season_obj.top_x_batters
    b.sort(key=lambda x: (x.owner.display_name, -x.player.player.points))
    p = season_obj.top_x_pitchers
    p.sort(key=lambda x: (x.owner.display_name, -x.player.player.points))

    return render_template('not_implemented.html')
