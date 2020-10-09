from .classes.data_sources import DataSources
from .classes.draft import Draft
from .classes.msf_connector import MSFConnector
from .classes.season import Season
from .classes.team_owner import TeamOwner
import argparse
from datetime import date
from dotenv import load_dotenv
import json
import os


def create_draft_file(draft_season, pick_file, draft_file, player_file):
    owner_count = int(os.getenv('MSF_FANTASY_OWNERS'))
    round_count = int(os.getenv('MSF_FANTASY_DRAFT_ROUNDS'))
    snake_style_draft = True if os.getenv('MSF_FANTASY_DRAFT_SNAKE') == 'true' else False
    owner_file = 'data/team_owners.json'
    all_owners = []
    ordered_owners = []
    draft_order_owner_ids = os.getenv('MSF_FANTASY_DRAFT_ORDER').split(',')

    with open(owner_file, 'r') as f1:
        owner_data = json.load(f1)
    for owner in owner_data:
        all_owners.append(TeamOwner(**owner))
    for pick_owner in draft_order_owner_ids:
        ordered_owners.append([x for x in all_owners if x.owner_id == int(pick_owner)][0])

    draft_obj = Draft(draft_season, owner_count, round_count, snake_style_draft)
    draft_obj.set_owners(ordered_owners)
    draft_obj.load_picks_from_file(pick_file)
    draft_obj.reconcile_players_with_data_provider(player_file)
    draft_obj.finalize_draft()

    with open(draft_file, 'w') as f3:
        json.dump(json.loads(str(draft_obj)), f3)


def start_season_from_draft_data(draft_file, season_file, season_type):
    season_obj = Season().from_draft_file(draft_file, season_type)
    season_obj.start_season()
    season_obj.save_data(season_file)


def update_season_data(season_file, stat_file_name):
    season_obj = Season().from_json_file(season_file)
    season_obj.update_player_stats(stat_file_name)
    season_obj.save_data(season_file)


def update_provider_data():
    def flatten_provider_data(data_type):
        players = []
        data_level_one = ''
        data_level_two = ''

        in_file = f'msf_{data_type}'
        out_file = f'flat_{data_type}'

        if data_type == 'players':
            data_level_one = 'activeplayers'
            data_level_two = 'playerentry'
        elif data_type == 'stats':
            data_level_one = 'cumulativeplayerstats'
            data_level_two = 'playerstatsentry'

        with open(file_names['msf_season'], 'r') as f:
            curr_seas = json.load(f)
        with open(file_names[in_file], 'r') as f:
            curr_stats = json.load(f)

        eligible_stats = curr_seas['currentseason']['season'][0]['supportedPlayerStats']

        for player in curr_stats[data_level_one][data_level_two]:
            this_player = {}
            this_player['player_id'] = player["player"]["ID"]
            this_player['first_name'] = player["player"]["FirstName"]
            this_player['last_name'] = player["player"]["LastName"]
            this_player['player_position'] = player["player"]["Position"]
            this_player['player_type'] = 'P' if player['player']['Position'] == 'P' else 'B'

            try:
                this_player['team_id'] = player['team']['ID']
                this_player['team_city'] = player['team']['City']
                this_player['team_name'] = player['team']['Name']
            except Exception as e:
                this_player['team_id'] = 0
                this_player['team_city'] = ''
                this_player['team_name'] = ''

            if data_type == 'stats':
                for stat in eligible_stats['playerStat']:
                    if stat['name'] == 'Homeruns':
                        stat_name = 'home_runs'
                    elif stat['name'] == 'Runs Batted In':
                        stat_name = 'rbi'
                    elif stat['name'] == 'Strikeouts':
                        stat_name = f'{stat["category"].lower()}_strikeouts'
                    elif stat['name'] == 'Walks':
                        stat_name = f'{stat["category"].lower()}_walks'
                    else:
                        stat_name = (stat['name'].replace('(', '')
                                     .replace(')', '')
                                     .replace('-', '')
                                     .replace(' ', '_').lower())

                    player_stat = next((x for x in player['stats'].values() if '@category' in x and
                                        x['@category'] == stat['category'] and
                                        x['@abbreviation'] == stat['abbreviation']), None)
                    if player_stat is not None:
                        this_player[stat_name] = player_stat["#text"]
                    else:
                        this_player[stat_name] = 0

            players.append(this_player)

        with open(file_names[out_file], 'w') as f:
            json.dump(players, f)

    call_file = 'data/potential_api_calls.json'
    data_source = DataSources.API
    league = os.getenv('MSF_FANTASY_LEAGUE')
    file_names = {}
    msf = MSFConnector(os.getenv('MSF_VERSION'), os.getenv('MSF_API_KEY'), os.getenv('MSF_PASSWORD'), call_file)

    current_msf_season = msf.get_current_season(league, os.getenv('MSF_RESPONSE_FORMAT'))

    local_season = int(os.getenv('MSF_SEASON')) or 1776
    local_season = args.season if args.season != 1776 else local_season
    local_season_type = os.getenv('MSF_SEASON_TYPE') or 'regular'
    local_season_type = args.season_type if args.season_type != 'none' else local_season_type

    if local_season == 1776:
        season = current_msf_season[0]
        season_type = current_msf_season[1]
    else:
        season = local_season
        season_type = local_season_type

    season_type_for_filename = 'regular' if season_type == 'playoff' and not has_postseason_draft else season_type

    file_names['msf_players'] = f'results/active_players-{league}-{season}-{season_type}.json'
    file_names['msf_season'] = f'results/current_season-{league}--{date.today().strftime("%Y%m%d")}.json'
    file_names['msf_stats'] = f'results/cumulative_player_stats-{league}-{season}-{season_type}.json'
    file_names['pick_data'] = f'data/drafts/{season}-{season_type_for_filename}-picks.txt'
    file_names['draft_data'] = f'data/drafts/{season}-{season_type_for_filename}.json'
    file_names['season_data'] = f'data/seasons/{season}-{season_type}.json'
    file_names['flat_players'] = f'data/players/{season}-{season_type}.json'
    file_names['flat_stats'] = f'data/stats/{season}-{season_type}.json'

    endpoint = 'active_players'
    msf.set_call_signature(league, season_type, endpoint, season)
    msf.make_api_call(data_source)
    file_names[endpoint] = msf.file_name

    endpoint = 'cumulative_player_stats'
    msf.set_call_signature(league, season_type, endpoint, season)
    msf.make_api_call(data_source)
    file_names[endpoint] = msf.file_name

    flatten_provider_data('players')
    flatten_provider_data('stats')

    return season, season_type, file_names


def main():
    current_season, current_season_type, file_names = update_provider_data()

    if args.run_type == 'draft':
        create_draft_file(current_season, file_names['pick_data'], file_names['draft_data'], file_names['flat_players'])
    elif args.run_type == 'season':
        start_season_from_draft_data(file_names['draft_data'], file_names['season_data'], current_season_type)
    elif args.run_type == 'update':
        update_season_data(file_names['season_data'], file_names['flat_stats'])
    elif args.run_type == 'all':
        create_draft_file(current_season, file_names['pick_data'], file_names['draft_data'],
                          file_names['flat_players'])
        start_season_from_draft_data(file_names['draft_data'], file_names['season_data'], current_season_type)
        update_season_data(file_names['season_data'], file_names['flat_stats'])


if __name__ == '__main__':
    load_dotenv()

    has_postseason_draft = True if os.getenv('MSF_HAS_POSTSEASON_DRAFT') == 'true' else False

    parser = argparse.ArgumentParser()
    parser.add_argument('--run-type', '-r', help='What type of run to do', choices=['all', 'draft', 'season', 'update'])
    parser.add_argument('--season', '-s', type=int, default=1776, help='MLB season as 4-digit year')
    parser.add_argument('--season-type', '-t', help='MLB season type', choices=['pre', 'regular', 'playoff'],
                        default='none')
    args = parser.parse_args()

    main()
